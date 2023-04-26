from xml.dom import minidom
from Builders import *
import re

class Read:
    def __init__(self,profiles : list,users : list,discarded : list):
        self.profiles = profiles
        self.users = users
        self.discarded = discarded

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

    def readMessage(self,content):
        file = minidom.parseString(content)
        messages = file.getElementsByTagName('listaMensajes')[0]
        message = messages.getElementsByTagName('mensaje')

        for text in message:
            text = text.firstChild.data

            placeDate = re.search(r'Lugar y Fecha:\s*(.*?),\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})', text)
            user = re.search(r'Usuario: ([^\n\t\s]+)', text)
            socialN = re.search(r'Red social: (\w+)', text)
            message = re.search(r'Red social: \w+\n(.+\n)+', text)
            message = message.group().split("\n",1)[1].strip().replace('\t', ' ')

            place = placeDate.group(1)
            date = placeDate.group(2)
            hour = placeDate.group(3)
            user = user.group(1)
            socialN = socialN.group(1)

            message = ' '.join(message.splitlines())
            message = re.sub(r'\s+', ' ', message)

            us = self.searchUser(user)
            if not us:
                self.users.append(User(user))
            else:
                us.messages.append(Message(place,date,hour,message))

    def searchUser(self,user_) -> User:
        for user in self.users:
            if user == user_:
                return user
        return None


# Read().readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
# read = Read()
# read.readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
# read.readMessage(open('./Mensajes.xml',encoding='utf-8').read())