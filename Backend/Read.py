from xml.dom import minidom
from Builders import *
import re

class Read:
    def __init__(self,profiles : list,users : list,discarded : list):
        self.profiles = profiles
        self.users = users
        self.discarded = discarded
        self.dates = []
        self.msgTest = {}

    def readProfiles(self,content):
        file = minidom.parseString(content)
        Profiles = file.getElementsByTagName('perfiles')[0]
        profiles = Profiles.getElementsByTagName('perfil')
        newProfiles = 0
        updatedProfiles = 0

        for profile in profiles:
            name = profile.getElementsByTagName('nombre')[0].firstChild.data
            keywords = profile.getElementsByTagName('palabra')

            pr = self.searchProfile(name)
            if pr:
                self.addWord(pr,keywords)
                updatedProfiles += 1
            else:
                pr = Profile(name)
                self.addWord(pr,keywords)
                self.profiles.append(pr)
                newProfiles += 1

        discarded = file.getElementsByTagName('descartadas')[0]
        discard = discarded.getElementsByTagName('palabra')
        discardedW = 0
        for word in discard:
            word = word.firstChild.data
            if word not in self.discarded:
                self.discarded.append(word)
                discardedW += 1

        return self.generateXMLProfiles(newProfiles, updatedProfiles, discardedW)

    def addWord(self,pr,keywords):
        for keyword in keywords:
            word = keyword.firstChild.data
            if word not in pr.words:
                pr.words.append(word)

    def generateXMLProfiles(self, new_profiles_count, updated_profiles_count, discarded_words_count):
        doc = minidom.Document()
        
        response_elem = doc.createElement('respuesta')
        doc.appendChild(response_elem)

        new_profiles_elem = doc.createElement('perfilesNuevos')
        new_profiles_elem.appendChild(doc.createTextNode(f"Se han creado {new_profiles_count} perfiles nuevos"))
        response_elem.appendChild(new_profiles_elem)

        updated_profiles_elem = doc.createElement('perfilesExistentes')
        updated_profiles_elem.appendChild(doc.createTextNode(f"Se han actualizado {updated_profiles_count} perfiles existentes"))
        response_elem.appendChild(updated_profiles_elem)

        discarded_words_elem = doc.createElement('descartadas')
        discarded_words_elem.appendChild(doc.createTextNode(f"Se han creado {discarded_words_count} nuevas palabras a descartar"))
        response_elem.appendChild(discarded_words_elem)

        return doc.toprettyxml(indent='\t')

    # LECTURA DE MENSAJES
    def readMessage(self,content,test):
        file = minidom.parseString(content)
        messages = file.getElementsByTagName('mensaje')
        userCount = 0
        messagesCount = 0

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
                messagesCount += 1
                if test:
                    self.msgTest['user'] = us.user
                    self.msgTest['message'] = us.messages[len(us.messages) - 1]
            else:
                us = User(user)
                self.users.append(us)
                us.messages.append(Message(place,date,time,message))
                userCount += 1
                messagesCount += 1
                if test:
                    self.msgTest['user'] = us.user
                    self.msgTest['message'] = us.messages[len(us.messages) - 1]

        return self.generateXMLMessages(userCount,messagesCount)

    def generateXMLMessages(self, userCount, messagesCount):
        doc = minidom.Document()
        
        response_elem = doc.createElement('respuesta')
        doc.appendChild(response_elem)

        new_profiles_elem = doc.createElement('usuarios')
        new_profiles_elem.appendChild(doc.createTextNode(f'Se procesaron mensajes para {userCount} usuarios distintos'))
        response_elem.appendChild(new_profiles_elem)

        updated_profiles_elem = doc.createElement('mensajes')
        updated_profiles_elem.appendChild(doc.createTextNode(f'Se procesaron {messagesCount} mensajes en total'))
        response_elem.appendChild(updated_profiles_elem)

        return doc.toprettyxml(indent='\t')

    def searchProfile(self,profile_) -> Profile:
        for profile in self.profiles:
            if profile.name == profile_:
                return profile
        return None

    def searchUser(self,user_) -> User:
        for user in self.users:
            if user.user == user_:
                return user
        return None