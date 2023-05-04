class Profile:
    def __init__(self,name):
        self.name = name
        self.words: list = []

    def __str__(self) -> str:
        return f'Name: {self.name}, Words: {self.words}'

class Message:
    def __init__(self,place,date,time,content):
        self.place = place
        self.date = date
        self.time = time
        self.content = content

    def __str__(self) -> str:
        return f'\n{self.date} {self.time}, {self.place}, {self.content}'

class User:
    def __init__(self,user):
        self.user = user
        self.messages: list[Message] = []

    def __str__(self) -> str:
        return f'User: {self.user}, Messages: {self.messages}'