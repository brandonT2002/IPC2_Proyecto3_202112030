from Read import Read

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

ctrl = Controller()
ctrl.readProfiles()
# ctrl.viewProfiles()
# ctrl.viewDiscarded()
ctrl.readUsers()
ctrl.viewUsers()