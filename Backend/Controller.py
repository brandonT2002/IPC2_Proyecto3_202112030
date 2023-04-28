from Read import Read
import re

class Controller:
    def __init__(self):
        self.profiles = []
        self.users = []
        self.discarded = []
        self.rd = Read(self.profiles,self.users,self.discarded)

    def readProfiles(self):
        self.rd.readProfiles(open('./Perfiles.xml',encoding='utf-8').read())

    def readUsers(self):
        self.rd.readMessage(open('./Mensajes.xml',encoding='utf-8').read())

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
        return leakedWords

    def profileWeight(self,text):
        text = ' '.join(self.countWords(text))
        weight = {}
        for profile in self.profiles:
            print(f'---{profile.name}---')
            profile.words = sorted(profile.words,key = len,reverse = True)
            words_match = []
            for word in profile.words:
                aux = re.findall(word,text)
                words_match.extend(aux)
                text = re.sub(word,'',text)
            print(words_match)
            weight[profile.name] = len(words_match)
            print()
        print(weight)

ctrl = Controller()
ctrl.readProfiles()
ctrl.profileWeight('Hola amigos, nos vemos hoy en el gym... recuerden que después vamos a entrenar para la carrera 2K del próximo sábado. No olvieden su Ropa Deportiva y sus bebidas Hidratantes. Recuerden que hoy por la noche juega la selección de fútbol, nos vemos en Taco Bell a las 7 pm. ropa')
