class Profile:
    def __init__(self,name):
        self.name = name
        self.words = []

class Message:
    def __init__(self,place,date,time,content):
        self.place = place
        self.date = date
        self.time = time
        self.content = content

class User:
    def __init__(self,user):
        self.user = user
        self.messages: list[Message] = []