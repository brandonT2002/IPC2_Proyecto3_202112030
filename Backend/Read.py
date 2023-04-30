from xml.dom import minidom
from Builders import *
import re

class Read:
    def __init__(self,profiles : list,users : list,discarded : list):
        self.profiles = profiles
        self.users = users
        self.discarded = discarded
        self.dates: list[str] = []
        self.msgTest = {}

    def readProfiles(self,content):
        file = minidom.parseString(content)
        Profiles = file.getElementsByTagName('perfiles')[0]
        profiles = Profiles.getElementsByTagName('perfil')

        for profile in profiles:
            name = profile.getElementsByTagName('nombre')[0].firstChild.data
            keywords = profile.getElementsByTagName('palabra')

            pr = Profile(name)
            for keyword in keywords:
                word = keyword.firstChild.data
                pr.words.append(word)
            self.profiles.append(pr)

        discarded = file.getElementsByTagName('descartadas')[0]
        discard = discarded.getElementsByTagName('palabra')
        for word in discard:
            word = word.firstChild.data
            self.discarded.append(word)

    def readMessage(self,content,test):
        file = minidom.parseString(content)
        messages = file.getElementsByTagName('mensaje')

        for text in messages:
            text = text.firstChild.data

            placeDate = re.search(r'Lugar y Fecha:\s*(.*?),\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})', text)
            user = re.search(r'Usuario: ([^\n\t\s]+)', text)
            socialN = re.search(r'Red social: (\w+)', text)
            message = re.search(r'Red social: \w+\n(.+\n)+', text)
            message = message.group().split("\n",1)[1].strip().replace('\t', ' ')

            place = placeDate.group(1)
            date = placeDate.group(2)
            time = placeDate.group(3)
            user = user.group(1)
            socialN = socialN.group(1)
            self.dates.append(date) if not date in self.dates else None

            message = ' '.join(message.splitlines())
            message = re.sub(r'\s+', ' ', message)

            us = self.searchUser(user)
            if us:
                us.messages.append(Message(place,date,time,message))
                if test:
                    self.msgTest['user'] = us.user
                    self.msgTest['message'] = us.messages[len(us.messages) - 1]
            else:
                us = User(user)
                self.users.append(us)
                us.messages.append(Message(place,date,time,message))
                if test:
                    self.msgTest['user'] = us.user
                    self.msgTest['message'] = us.messages[len(us.messages) - 1]
                

    def searchUser(self,user_) -> User:
        for user in self.users:
            if user.user == user_:
                return user
        return None


# Read().readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
# read = Read()
# read.readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
# read.readMessage(open('./Mensajes.xml',encoding='utf-8').read())