class Profile:
    def __init__(self,name):
        self.name = name
        self.words = []

class User:
    def __init__(self,user):
        self.user = user
        self.messages = []

class Message:
    def __init__(self,place,date,time,content):
        self.place = place
        self.date = date
        self.time = time
        self.content = content