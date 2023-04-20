from xml.dom import minidom

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
        for msg in message:
            msg = msg.firstChild.data
            print(msg)


# Read().readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
read = Read()
read.readProfiles(open('./Perfiles.xml',encoding='utf-8').read())
read.readMessage(open('./Mensajes.xml',encoding='utf-8').read())