from Read import Read

class Controller:
    def __init__(self):
        self.profiles = []
        self.users = []
        self.discarded = []
        self.rd = Read(self.profiles,self.users,self.discarded)

    def readProfiles(self):
        self.rd.readProfiles(open('./Perfiles.xml',encoding='utf-8').read())

    def viewProfiles(self):
        for profile in self.profiles:
            print(f'---{profile.name}---')
            for word in profile.words:
                print(word)
            print()

ctrl = Controller()
ctrl.readProfiles()
ctrl.viewProfiles()