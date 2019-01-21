import pygame
import datetime
from time import sleep
import os

pygame.init()


display_width = 1024
display_height = 600

numberOfRooms = 12

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Key Check-in')

black = (0,0,0)
white = (255,255,255)
blue = (0,0,255)

clock = pygame.time.Clock()
done = False
# Images used in the program
img_logo = pygame.image.load('logo.png')
img_settings =pygame.image.load('Settings.png')
img_back = pygame.image.load('back.png')
img_key = pygame.image.load('key.png')


smallText = pygame.font.SysFont("Arial",20)
largeText = pygame.font.SysFont("Arial",30)

currentLanguage = None

validKeys={
    "jan": 1,
    "piet": 2,
    "joris": 4,
    "korneel": 7
}

translations={
    'mainMessage':{
        'gb':'Touch screen to begin',
        'fr': "Tappez l'ecran pour commencer",
        'nl': "Raak het scherm aan om te beginnen"
    },
    'endGreeting':{
        'gb': "Enjoy your stay at the hotel",
        'fr': "Fromage!",
        'nl': "Geniet van uw verblijf in het hotel!"
    },
    'enterPass':{
        'gb': "Enter the passcode to retrieve your key",
        'fr': "Du vin et du pain",
        'nl': "Toets de code in om uw sleutel te ontvangen"
    },
    'tooManyWrongPass':{
        'gb': "Too many wrong attempts!",
        'fr': "Trop de mauvais codes esseyez",
        'nl': "Teveel verkeerde codes ingegeven"
    },
    'invalidKey':{
        'gb': "Invalid key",
        'fr': "Mauvais code",
        'nl': "Verkeerde code"
    },
    'waitFor':{
        'gb': "Wait for: ",
        'fr': "Attendez ",
        'nl': "Wacht gedurende "
    },
    'retrieveKey':{
        'gb': "Retrieve key",
        'fr': "Aquiyez cles",
        'nl': "Ontvang sleutel"
    }
}

ActiveReservations = {
    1 : None,
    2 : None,
    3 : 'Jos',
    4 : None,
    5 : None,
    6 : None,
    7 : None,
    8 : None,
    9 : None,
    10 : None,
    11 : None,
    12 : None
}


class c_language:
    def __init__(self, name, keyLayout):
        self.name = name
        self.flag = pygame.image.load(name + '.png')
        self.layout = keyLayout

class c_imageButton:
    def __init__(self, x, y, img, action = None, action_arg= None):
        self.x = x
        self.y = y
        self.img = img
        self.action = action
        self.action_arg = action_arg
        return
        
    def show(self):
        gameDisplay.blit(self.img, (self.x,self.y))

    def checkClick(self, mouse):
        if self.x + self.img.get_size()[0] > mouse[0] > self.x and self.y + self.img.get_size()[1] > mouse[1] > self.y:
            if(self.action_arg != None):
                self.action(self.action_arg)
            else:
                self.action()
    
class c_textButton:
    def __init__(self, msg, x, y, w, h, color, action = None, action_arg = None):
        self.msg = msg
        self.x = x
        self.y= y
        self.w = w
        self.h = h
        self.color = color
        self.action = action
        self.action_arg = action_arg

    def show(self):
        pygame.draw.rect(gameDisplay, self.color,(self.x,self.y,self.w,self.h))    
        textSurf, textRect = text_objects(self.msg, smallText)
        textRect.center = ((self.x+(self.w/2)), (self.y+(self.h/2)) )
        gameDisplay.blit(textSurf, textRect)
        textSurf, textRect = text_objects(self.msg, smallText)
        textRect.center = ( (self.x+(self.w/2)), (self.y+(self.h/2)) )
        gameDisplay.blit(textSurf, textRect)

    def checkClick(self, mouse):
        if self.action is None: return
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            if(self.action_arg != None):
                self.action(self.action_arg)
            else:
                self.action()

class c_screen:
    def __init__(self):
        self.authenticated = False
        self.done = False
        self.screenButtons = []
        self.langBtns = []
        self.lastInput = datetime.datetime.now()
        x = display_width
        for language in availableLanguages:
            flagimg = language.flag
            y = display_height - flagimg.get_size()[1]
            x = x - flagimg.get_size()[0]
            self.langBtns.append(c_imageButton(x, y, flagimg, chooseLanguage, language))
        self.screenButtons.append(self.langBtns)
        

    def putStuffOnScreen(self):
        gameDisplay.fill(black)

    def goBack(self):
        self.done = True

    def putText(self,x, y, text, markup):
        TextSurf, TextRect = text_objects(text, markup)
        TextRect.midtop = (x, y)
        gameDisplay.blit(TextSurf, TextRect)

    def showLanguageOptions(self):
        for btn in self.langBtns:
            btn.show()

    def showBtns(self):
        for button in self.screenButtons:
            #print(type(button))
            if(type(button) is type([])):
                for subButton in button :
                    if(hasattr(subButton, 'show')):
                        subButton.show()
            elif(hasattr(button, 'show')):
                button.show()

    def checkbuttons(self):
        mouse = pygame.mouse.get_pos()
        for button in self.screenButtons:
            #print(type(button))
            if(type(button) is type([])):
                for subButton in button :
                    if(hasattr(subButton, 'checkClick')):
                        subButton.checkClick(mouse)
            elif(hasattr(button, 'checkClick')):
                button.checkClick(mouse)

    def show(self):
        self.done = False
        self.authenticated = False
        self.lastInput = datetime.datetime.now()
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.lastInput = datetime.datetime.now()
                    self.checkbuttons()
            timediff = datetime.datetime.now() - self.lastInput
            if(timediff.total_seconds() > 30):
                print(timediff.total_seconds())
                self.lastInput = datetime.datetime.now()
                self.done = True
            gameDisplay.fill(black)
            self.putStuffOnScreen()
            pygame.display.update()
            clock.tick(20)

class c_screen_main(c_screen):
    def __init__(self):
        super().__init__()
        self.settingsScreen = c_screen_settings()
        self.cRetrievekey = c_retrieveKey()
        self.btn_settings = c_imageButton(0, display_height - img_settings.get_size()[0], img_settings, self.settingsScreen.show)
        

    def putStuffOnScreen(self):
        #self.done = False
        self.showLanguageOptions()
        x = (display_width / 2)- img_logo.get_size()[0]/2
        #y = (display_height /2)- img_logo.get_size()[1]/2
        y = 10
        gameDisplay.blit(img_logo, (x,y))
        gameDisplay.blit(img_key, (((display_width/2)-img_key.get_size()[0]/2),(display_height /2)- img_key.get_size()[1]/2))
        self.btn_settings.show()
        mainMessage = translations['mainMessage'][currentLanguage.name]
        showText(mainMessage, largeText, display_width/2, 450)

    def checkbuttons(self):
        super().checkbuttons()
        mouse = pygame.mouse.get_pos()
        self.btn_settings.checkClick(mouse)
        if(mouse[1] < 500):
            self.cRetrievekey.show()

class c_screen_settings(c_screen):
    def __init__(self):
        super().__init__()
        self.authenticated = False
        self.btn_back = c_imageButton(0, display_height - img_back.get_size()[0], img_back, self.goBack)
        self.btn_changePass = c_textButton('Change settings password',100, 100, 300, 60, blue)
        self.screenButtons.append(self.btn_back)
        self.screenButtons.append(self.btn_changePass)
        self.loginScreen = c_login("admin")
        self.loginScreen.CustomMessage = "Geef code"

    def putStuffOnScreen(self):
        if self.authenticated is False:
            self.loginScreen.show()
            if self.loginScreen.authenticated:
                self.authenticated = True
            else:
                self.done = True
        else:
            TextSurf, TextRect = text_objects("Settings", largeText)
            TextRect.midleft = (30,20)
            gameDisplay.blit(TextSurf, TextRect)
            self.btn_back.show()
            self.btn_changePass.show()
    
class c_retrieveKey(c_screen):
    def __init__(self):
        super().__init__()
        self.authenticated = False
        self.btn_back = c_imageButton(0, display_height - img_back.get_size()[0], img_back, self.goBack)
        self.screenButtons.append(self.btn_back)
        self.loginScreen = c_login()

    def putStuffOnScreen(self):
        if self.authenticated is False:
            self.loginScreen.show()
            if self.loginScreen.room is None:
                self.done = True
            else:
                self.authenticated = True
        else:
            message = translations['endGreeting'][currentLanguage.name]        
            showText(message, smallText, display_width/2, 300)
            showText("Room: " + str(self.loginScreen.room), largeText, display_width/2, 350)
        self.btn_back.show()

class c_keyboard():
    def __init__(self, layout):
        self.keyboardLayout = {
        "azerty" : ['a','z','e','r','t','y','u','i','o','p','q','s','d','f','g','h','j','k','l','m','w','x','c','v','b','n'],
        "qwerty" : ['q','w','e','r','t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m']
    }
        self.currentText = ''
        self.keyboardKeys = []
        self.keysize = 85
        self.keyspacing = 10
        self.keyboard_y = 100
        self.keyboard_x = 25
        #First row:
        keys = self.keyboardLayout[layout][0:10]
        #keys = ['a', 'z', 'e','r','t','y','u','i','o','p']
        for x_key in range(len(keys)):
            self.keyboardKeys.append(c_textButton(keys[x_key], self.keyboard_x+x_key*(self.keysize+self.keyspacing), self.keyboard_y, self.keysize, self.keysize, blue, self.tap, keys[x_key]))
        #Second row:
        if layout is 'azerty':
            keys = self.keyboardLayout[layout][10:20]
        elif layout is 'qwerty':
            keys = self.keyboardLayout[layout][10:19]
        for x_key in range(len(keys)):
            self.keyboardKeys.append(c_textButton(keys[x_key], self.keyboard_x+self.keysize/3+x_key*(self.keysize+self.keyspacing), self.keyboard_y+self.keysize+self.keyspacing, self.keysize, self.keysize, blue, self.tap, keys[x_key]))
        #Last row:
        if layout is 'azerty':
            keys = self.keyboardLayout[layout][20:]
        elif layout is 'qwerty':
            keys = self.keyboardLayout[layout][19:]
        for x_key in range(len(keys)):
            self.keyboardKeys.append(c_textButton(keys[x_key], self.keyboard_x+self.keysize*2/3+x_key*(self.keysize+self.keyspacing), self.keyboard_y+2*(self.keysize+self.keyspacing), self.keysize, self.keysize, blue, self.tap, keys[x_key]))

        self.keyboardKeys.append(c_textButton('Back', self.keyboard_x+self.keysize*2/3+7*(self.keysize+self.keyspacing), self.keyboard_y+2*(self.keysize+self.keyspacing), 2*self.keysize, self.keysize, blue, self.tap, 'BKSP'))

    def show(self):
        for key in self.keyboardKeys:
            key.show()

    def checkClick(self,mouse):
        for key in self.keyboardKeys:
            key.checkClick(mouse)

    def tap(self,key_value):
        if(key_value is 'BKSP' and len(self.currentText) is not 0):
            self.currentText = self.currentText[0:-1]
        elif(key_value is not 'BKSP'):
            self.currentText += str(key_value)
        #print(self.currentText)

class c_login(c_screen):
    def __init__(self, code = None):
        super().__init__()
        self.room = None
        self.codeToCheck = code
        self.authenticated = False
        self.done = False
        self.CustomMessage = None
        self.btn_back = c_imageButton(0, display_height - img_back.get_size()[0], img_back, self.goBack)
        self.btn_go = c_textButton("Retrieve Key", 800, 400, 150,50, blue, self.checkKey)
        self.keyboard = c_keyboard("qwerty")
        self.screenButtons.append(self.btn_back)
        self.screenButtons.append(self.btn_go)
        self.screenButtons.append(self.keyboard)

    def putStuffOnScreen(self):
        global languageHasChanged
        if languageHasChanged:
            self.screenButtons.remove(self.keyboard)
            self.keyboard = c_keyboard(currentLanguage.layout)
            self.screenButtons.append(self.keyboard)
            languageHasChanged = False
        if(self.CustomMessage is None):
            self.btn_go.msg = translations['retrieveKey'][currentLanguage.name]
        else:
            self.btn_go.msg = "OK"
        self.showLanguageOptions()        
        self.keyboard.show()
        if self.CustomMessage is None:
            message = translations['enterPass'][currentLanguage.name]
        else:
            message = self.CustomMessage
        showText(message, smallText, display_width/2, 25)
        self.btn_back.show()
        if len(self.keyboard.currentText) > 0:
            self.btn_go.show()
        showText(self.keyboard.currentText, smallText, display_width/2, 400)
    

    def checkKey(self):
        if self.codeToCheck is None:
            if self.keyboard.currentText in validKeys:
                self.room = validKeys[self.keyboard.currentText]
                print("Passcode given for room: " + str(self.room))
                self.done = True
            else:
                self.keyboard.currentText = ""
                showText(translations['invalidKey'][currentLanguage.name],smallText, display_width/2, 500)
                pygame.display.update()
                sleep(2)
                print("invalid key!")
        else:
            if self.keyboard.currentText == self.codeToCheck:
                self.authenticated = True
                self.done = True
            else:
                self.keyboard.currentText = ""
                showText("verkeerde code",smallText, display_width/2, 500)
                pygame.display.update()
                sleep(2)
                print("invalid key!")
        self.keyboard.currentText = ""

class c_textInput(c_screen):
    def __init__(self,code = None):
        super().__init__()
        self.room = None
        self.codeToCheck = code
        self.authenticated = False
        self.done = False
        self.CustomMessage = None
        self.btn_back = c_imageButton(0, display_height - img_back.get_size()[0], img_back, self.goBack)
        self.btn_go = c_textButton("Change", 800, 400, 150,50, blue, self.checkInput)
        self.keyboard = c_keyboard("qwerty")
        self.screenButtons.append(self.btn_back)
        self.screenButtons.append(self.btn_go)
        self.screenButtons.append(self.keyboard)

    def putStuffOnScreen(self):
        global languageHasChanged
        if languageHasChanged:
            self.screenButtons.remove(self.keyboard)
            self.keyboard = c_keyboard(currentLanguage.layout)
            self.screenButtons.append(self.keyboard)
            languageHasChanged = False
        if(self.CustomMessage is None):
            self.btn_go.msg = translations['retrieveKey'][currentLanguage.name]
        else:
            self.btn_go.msg = self.CustomMessage
        self.showLanguageOptions()        
        self.keyboard.show()
        if self.CustomMessage is None:
            message = translations['enterPass'][currentLanguage.name]
        else:
            message = self.CustomMessage
        showText(message, smallText, display_width/2, 25)
        self.btn_back.show()
        if len(self.keyboard.currentText) > 0:
            self.btn_go.show()
        showText(self.keyboard.currentText, smallText, display_width/2, 400)
    

    def checkInput(self):
        if self.codeToCheck is type([]):
            if self.keyboard.currentText in self.codeToCheck:
                self.room = self.codeToCheck[self.keyboard.currentText]
                print("Passcode given for room: " + str(self.room))
                self.done = True
            else:
                showText(translations['invalidKey'][currentLanguage.name],smallText, display_width/2, 500)
                pygame.display.update()
                sleep(2)
                print("invalid key!")
            self.keyboard.currentText = ""
        elif self.codeToCheck is type(""):
            if self.keyboard.currentText == self.codeToCheck:
                self.authenticated = True
                self.done = True
            else:
                self.keyboard.currentText = ""
                showText("verkeerde code",smallText, display_width/2, 500)
                pygame.display.update()
                sleep(2)
                print("invalid key!")
        #self.keyboard.currentText = ""
        self.done = True
        
class c_screen_reservations(c_screen):
    def __init__(self):
        self.x_BtnOffset = 300  # This is the offset from the text to the button. In other words: the maximun txt length
        self.x_textOffset = 25
        self.y_offset = 25
        self.spacing = 75
        self.x_spacing = 100
        self.textInput = c_textInput()
        self.textInput.CustomMessage = "Change"
        super().__init__()
        self.btn_back = c_imageButton(0, display_height - img_back.get_size()[0], img_back, self.goBack)
        self.screenButtons.append(self.btn_back)
        for room in range(0, numberOfRooms):
            #First column
            if(room < numberOfRooms/2):
                x = self.x_textOffset + self.x_BtnOffset
                y = self.y_offset + self.spacing * room
            else:
                x = (display_width/2) + self.x_textOffset + self.x_BtnOffset
                y = self.y_offset + self.spacing*(room-(numberOfRooms/2))
            self.screenButtons.append(c_textButton("change", x, y, 120, 20, blue, self.changeRoom, room))

    def putStuffOnScreen(self):
        self.showBtns()
        self.showRooms()

    def showRooms(self):
        global ActiveReservations
        for room in range(0,numberOfRooms):
            textToShow = 'Kamer '+ str(room + 1)
            textToShow += ':    '
            if ActiveReservations[room+1] is None:
                textToShow +=  '-'
            else:
                textToShow += str(ActiveReservations[room+1])
            if(room < numberOfRooms/2):
                x = self.x_textOffset
                y = self.y_offset + self.spacing * room
            else:
                x = (display_width/2) + self.x_textOffset
                y = self.y_offset + self.spacing*(room-(numberOfRooms/2))
            #showText(textToShow, smallText, 100, 25+room * self.spacing, 0)
            showText(textToShow, smallText,x, y, 0)

    def changeRoom(self, roomNr):
        global ActiveReservations
        self.textInput.show()
        ActiveReservations[roomNr+1] = str(self.textInput.keyboard.currentText)


def showText(text,font, x, y, allignment = 1):
    TextSurf, TextRect = text_objects(text, font)
    if allignment is 0:
        TextRect.midleft  = (x,y)
    elif allignment is 1:
        TextRect.midtop = (x, y)
    gameDisplay.blit(TextSurf, TextRect)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def chooseLanguage(lang):
    print(lang.name)
    global currentLanguage
    currentLanguage= lang
    global languageHasChanged
    languageHasChanged = True

#def saveSettings():


availableLanguages = [c_language('nl', 'azerty'), c_language('fr', 'azerty'), c_language('gb', 'qwerty')]
currentLanguage = availableLanguages[0]
languageHasChanged = False

mainScreen = c_screen_main()
settingsScreen = c_screen_settings()
mainScreen.show()
langPointer = 0
while True:
    print("STARTING")
    langPointer += 1
    if langPointer >= len(availableLanguages):
        langPointer = 0
    currentLanguage = availableLanguages[langPointer]
    test = c_screen_main()
    test.show()
pygame.quit()
quit()