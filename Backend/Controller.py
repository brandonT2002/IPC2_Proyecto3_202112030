from datetime import datetime
import datetime as dtime
import json
from Read import Read
from Builders import User
import re

class Controller:
    def __init__(self):
        self.profiles = []
        self.users: list[User] = []
        self.discarded = []
        self.rd = Read(self.profiles,self.users,self.discarded)

    def readProfiles(self,path):
        self.rd.readProfiles(open(path,encoding='utf-8').read())
        return 'Perfiles cargados exitosamente',200

    def sortByDateTime(self,messages):
        def getDatetime(message):
            date_string = message.date + ' ' + message.time
            return dtime.datetime.strptime(date_string, '%d/%m/%Y %H:%M')
        return sorted(messages,key = getDatetime)

    def sortDatesMessages(self):
        for user in self.users:
            user.messages = self.sortByDateTime(user.messages)

    def readUsers(self,path,test = False):
        self.rd.readMessage(open(path,encoding='utf-8').read(),test)
        self.rd.dates.sort(key = lambda date : dtime.datetime.strptime(date,'%d/%m/%Y'))
        self.sortDatesMessages()
        return 'Mensajes cargados exitosamente',200

    def viewProfiles(self):
        print('----- PERFILES -----')
        for profile in self.profiles:
            print(f'---{profile.name}---')
            for word in profile.words:
                print(word)
            print()

    def viewDiscarded(self):
        print('----- DESCARTADOS -----')
        for word in self.discarded:
            print(word)

    def viewUsers(self):
        print('----- USUARIOS -----')
        for user in self.users:
            print(user.user)
            for msg in user.messages:
                print('----------')
                print(msg.date,msg.time)
                print(msg.content)
            print()

    def countWords(self,text) -> list:
        text = re.sub(r'(?<!\w)\d+(?!\w)','',text)
        text = re.sub(r'[^\w\s]',' ',text)
        words = text.split()

        leakedWords = []
        for word in words:
            if word.lower() not in self.discarded:
                leakedWords.append(word.lower().replace(' ',''))
        return {'words':leakedWords,'length':len(leakedWords)}

    def searchWord(self,globalWords,wordKey):
        for k in globalWords:
            if k == wordKey:
                return globalWords[k]
        return 0

    def profilesProbability1(self,text):
        words = self.countWords(text)
        text = ' '.join(words.get('words'))
        data = {}
        global_words = {}
        for profile in self.profiles:
            profile.words = sorted(profile.words,key = len,reverse = True)
            words_match = []
            for word in profile.words:
                aux = re.findall(word,text)
                global_words[word] = self.searchWord(global_words,word) + len(aux)
                if len(aux) > 0:
                    words_match.extend(aux)
                    text = re.sub(word,'',text)
                else:
                    for i in range(self.searchWord(global_words,word)):
                        words_match.append(word)
            words_match = ' '.join(words_match).split(' ') if len(words_match) > 0 else words_match
            data[profile.name] = round((len(words_match) / words.get('length')) * 100,2)
        return data

    def profilesProbability(self,date,time,content):
        return {'date':date,'time':time,'probabilities':self.profilesProbability1(content)}

    def profilesWeights(self,data):
        for user in data:
            msgs = user[list(user.keys())[0]]
            probabilities = None
            weights = {}
            for msg in msgs:
                probabilities = msg['probabilities']
                for profile,probability in probabilities.items():
                    try:
                        weights[profile]['sum'] += probability
                    except:
                        weights[profile] = {'sum':probability,'n':0}
                    if probability > 0:
                        weights[profile]['n'] += 1
            weightsAux = {}
            for profile,sum_n in weights.items():
                weightsAux[profile] = round(sum_n['sum'] / sum_n['n'],2) if sum_n['n'] > 0 else 0
            user['weights'] = weightsAux
        return data

    def __msgByUser(self,user: User,date):
        messages = []
        if date:
            for m in user.messages:
                if m.date == date:
                    messages.append(self.profilesProbability(m.date,m.time,m.content))
            return messages
        else:
            for m in user.messages:
                messages.append(self.profilesProbability(m.date,m.time,m.content))
        return messages

    def __byUser(self,date = None,user = None):
        users = []
        if user:
            for u in self.users:
                if u.user == user:
                    users.append({user:self.__msgByUser(u,date)})
                    return users
        else:
            for u in self.users:
                users.append({u.user:self.__msgByUser(u,date)})
        return users

    # Resumen de perfiles y porcentajes de probabilidad, uno o más usuarios
    def service1(self,date,user = None):
        # return self.__byUser(date,user)
        return self.getDOTServ1(self.__byUser(date,user))

    def getDOTServ1(self,array):
        dot = 'digraph pasos {\nrankdir = TB;\n'
        dot += f'node0 [shape=none, margin=0, label=\n<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">\n'
        dot += '<tr>\n'
        dot += '<td BGCOLOR="black" width="175" height="30"><font color="white">Mensaje</font></td>\n'
        dot += '<td BGCOLOR="black" width="175" height="30"><font color="white">Usuario</font></td>\n'
        # se agregan los perfiles a la tabla de resumen
        for profile in self.profiles:
            dot += f'<td BGCOLOR="black" width="175" height="30"><font color="white">% Probabilidad perfil<br/>"{profile.name}"</font></td>\n'
        dot += '</tr>\n'
        for user in array:
            for key,value in user.items():
                # dot += f'<tr>\n<td border="0" colspan="4" align="left">Usuario: {key}</td>\n</tr>\n'
                for data in value:
                    dot += '<tr>\n'
                    dot += f'<td BGCOLOR="white" width="100" height="30">{data.get("date")} {data.get("time")}</td>\n'
                    dot += f'<td BGCOLOR="white" width="100" height="30">{key}</td>\n'
                    for profile in self.profiles:
                        dot += f'<td BGCOLOR="white" width="100" height="30">{data.get("probabilities").get(f"{profile.name}")} %</td>\n'
                    # print('\t->',data.get('probabilities').get('Deportista'))
                    dot += '</tr>\n'
        dot += '</TABLE>>\n'
        dot += '];\n'
        dot += '}'
        return json.dumps({'dot':dot}),200

    # Resumen de pesos por usuario, uno o más usuarios
    def service2(self,user = None):
        # return self.profilesWeights(self.__byUser(user = user))
        return self.getDOTServ2(self.profilesWeights(self.__byUser(user = user)))

    def getDOTServ2(self,array):
        dot = 'digraph pasos {\nrankdir = TB;\n'
        last_node = None
        for i,user in enumerate(array):
            dot += f'node{i} [shape=none, margin=0, label=\n<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">\n'
            for user_ in user.keys():
                if user_ != 'weights':
                    # dot += f'-> {user_}\n'
                    dot += f'<tr>\n<td border="0" colspan="4" align="left">Usuario: {user_}</td>\n</tr>\n'
            dot += '<tr>\n'
            dot += '<td BGCOLOR="black" width="175" height="30"><font color="white">Perfiles</font></td>'
            dot += '<td BGCOLOR="black" width="175" height="30"><font color="white">Pesos</font></td>'
            dot += '</tr>\n'
            for profile,weight in user.get('weights').items():
                dot += '<tr>\n'
                dot += f'<td BGCOLOR="white" width="100" height="30">{profile}</td>'
                dot += f'<td BGCOLOR="white" width="100" height="30">{weight}</td>'
                dot += '</tr>\n'
            dot += '</TABLE>>\n'
            dot += '];\n'
            dot += f'{last_node} -> node{i} [color=transparent];\n' if last_node else ''
            last_node = f'node{i}'
        dot += '}'
        return json.dumps({'dot':dot}),200
    
    # Solicitud de mensaje
    def service3(self,path):
        self.readUsers(path,True)
        msgTest = self.rd.msgTest
        #print(msgTest.get('user'))

        m = msgTest.get('message')
        probabilities = self.profilesProbability(m.date,m.time,m.content)
        weights = self.profilesWeights(self.__byUser(user = msgTest.get('user')))
        # print(weights.get('weights'))
        return self.getXML(probabilities,weights)
        # return weights

    def getXML(self,probabilities,weights):
        xml = '<?xml version="1.0"?>\n'
        xml += '<respuesta>\n'

        xml += f'\t<fechaHora> {probabilities.get("date")} {probabilities.get("time")} </fechaHora>\n'
        xml += f'\t<usuario> {list(weights[0].keys())[0]} </usuario>\n'
        xml += f'\t<perfiles>\n'

        for (profile,probability), (weight) in zip(probabilities.get("probabilities").items(), weights[0].get("weights").values()):
            xml += f'\t\t<perfil nombre={profile}>\n'
            xml += f'\t\t\t<porcentajeProbabilidad> {probability} </porcentajeProbabilidad>\n'
            xml += f'\t\t\t<pesoActual> {weight} </pesoActual>\n'
            xml += f'\t\t</perfil>\n'

        xml += f'\t</perfiles>\n'
        xml += '</respuesta>\n'
        return json.dumps({'xml':xml}),200

ctrl = Controller()
ctrl.readProfiles('./Perfiles_V1.xml')
ctrl.viewProfiles()
ctrl.readProfiles('./Perfiles_V2.xml')
ctrl.viewProfiles()
# ctrl.readUsers('./Mensajes.xml')
# print('SERVICE 1')
# weights = ctrl.service1('01/04/2023')
# print(weights)
# print('\nSERVICE 3')
# weights = ctrl.service3('./NuevoMsg.xml')
# print(weights)
#print('\nSERVICE 2')
#weights = ctrl.service2()
#print(weights)
#ctrl.profileWeight('Hola amigos, nos vemos hoy en el gym... recuerden que después vamos a entrenar para la carrera 2K del próximo sábado. No olvieden su Ropa Deportiva y sus bebidas Hidratantes. Recuerden que hoy por la noche juega la selección de fútbol, nos vemos en Taco Bell a las 7 pm.')
#ctrl.viewUsers()