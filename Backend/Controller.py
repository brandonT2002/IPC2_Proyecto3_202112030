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

    def countWords(self,text):
        text = re.sub(r'(?<!\w)\d+(?!\w)','',text)
        text = re.sub(r'[^\w\s]',' ',text)
        words = text.split()

        leakedWords = []
        for word in words:
            if word.lower() not in self.discarded:
                leakedWords.append(word.lower())

        print(leakedWords)
        print(len(leakedWords))

ctrl = Controller()
ctrl.readProfiles()
# ctrl.viewProfiles()
# ctrl.viewDiscarded()
# ctrl.readUsers()
# ctrl.viewUsers()

ctrl.countWords()