from xml.dom import minidom
import re

class Read:
    def readProfiles(self,content):
        file = minidom.parseString(content)
        Profiles = file.getElementsByTagName('perfiles')[0]
        profiles = Profiles.getElementsByTagName('perfil')

        print('--- Perfiles ---')
        for profile in profiles:
            name = profile.getElementsByTagName('nombre')[0].firstChild.data
            keywords = profile.getElementsByTagName('palabra')

            print(name)
            for keyword in keywords:
                word = keyword.firstChild.data
                print(word)
            print()

        discarded = file.getElementsByTagName('descartadas')[0]
        discard = discarded.getElementsByTagName('palabra')
        print('--- Descartadas ---')
        for word in discard:
            word = word.firstChild.data
            print(word)

    def readMessage(self,content):
        file = minidom.parseString(content)
        messages = file.getElementsByTagName('listaMensajes')[0]
        message = messages.getElementsByTagName('mensaje')

        print('--- Mensajes ---')
        for text in message:
            text = text.firstChild.data

            placeDate = re.search(r'Lugar y Fecha:\s*(.*?),\s*(\d{2}/\d{2}/\d{4})\s+(\d{2}:\d{2})', text)
            user = re.search(r'Usuario: ([^\n\t\s]+)', text)
            socialN = re.search(r'Red social: (\w+)', text)
            message = re.search(r'Red social: \w+\n(.+\n)+', text)
            message = message.group().split("\n",1)[1].strip()

            place = placeDate.group(1)
            date = placeDate.group(2)
            hour = placeDate.group(3)
            user = user.group(1)
            socialN = socialN.group(1)

            print("Lugar:", place)
            print("Fecha:", date)
            print("Hora:", hour)
            print("Usuario:", user)
            print("Red social:", socialN)
            print("Mensaje:", message)
            print()


# Read().readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
read = Read()
# read.readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
read.readMessage(open('./Mensajes.xml',encoding='utf-8').read())