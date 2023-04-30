from datetime import datetime
import datetime as dtime
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

    def sortByDateTime(self,messages):
        def getDatetime(message):
            date_string = message.date + ' ' + message.time
            return dtime.datetime.strptime(date_string, '%d/%m/%Y %H:%M')
        return sorted(messages,key = getDatetime)

    def sortDatesMessages(self):
        for user in self.users:
            user.messages = self.sortByDateTime(user.messages)

    def readUsers(self,path):
        self.rd.readMessage(open(path,encoding='utf-8').read())
        self.rd.dates.sort(key = lambda date : dtime.datetime.strptime(date,'%d/%m/%Y'))
        self.sortDatesMessages()

    def viewProfiles(self):
        print('-----Perfiles-----')
        for profile in self.profiles:
            print(f'---{profile.name}---')
            for word in profile.words:
                print(word)
            print()

    def viewDiscarded(self):
        print('-----Descartados-----')
        for word in self.discarded:
            print(word)

    def viewUsers(self):
        print('-----Usuarios-----')
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

    def profileWeight(self,text):
        words = self.countWords(text)
        text = ' '.join(words.get('words'))
        weight = {}
        global_words = {}

        for profile in self.profiles:
            # print(f'---{profile.name}---')
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
            # print(words_match)
            weight[profile.name] = str(round((len(words_match) / words.get('length')) * 100,2)) + ' %'
        for k in weight:
            print(k,'=',weight[k])

ctrl = Controller()
ctrl.readProfiles('./Perfiles.xml')
ctrl.readUsers('./Mensajes.xml')
ctrl.profileWeight('Hola amigos, nos vemos hoy en el gym... recuerden que después vamos a entrenar para la carrera 2K del próximo sábado. No olvieden su Ropa Deportiva y sus bebidas Hidratantes. Recuerden que hoy por la noche juega la selección de fútbol, nos vemos en Taco Bell a las 7 pm.')
#ctrl.viewUsers()