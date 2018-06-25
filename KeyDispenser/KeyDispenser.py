import pygame
import datetime

pygame.init()


display_width = 1024
display_height = 600

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

class c_language:
    def __init__(self, name):
        self.name = name
        self.flag = pygame.image.load(name + '.png')

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
        if self.x + self.w > mouse[0] > self.x and self.y + self.h > mouse[1] > self.y:
            if(self.action_arg != None):
                self.action(self.action_arg)
            else:
                self.action()

class c_screen:
    def __init__(self):
        self.done = False
        self.authenticated = False
    
    def putStuffOnScreen(self):
        gameDisplay.fill(black)
    def showauthenticate(self):
        gameDisplay.fill(black)
    def goBack(self):
        self.done = True
        self.authenticated = False

    def putText(self,x, y, text, markup):
        TextSurf, TextRect = text_objects(text, markup)
        TextRect.midtop = (x, y)
        gameDisplay.blit(TextSurf, TextRect)

    def show(self):
        self.done = False
        while not self.authenticated and not self.done:
            self.mouseDown = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    mainScreen.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkbuttons()
            gameDisplay.fill(black)
            self.showAuthenticate()
            pygame.display.update()
            clock.tick(20)
        while not self.done:
           for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkbuttons()
                gameDisplay.fill(black)
                self.putStuffOnScreen()
                pygame.display.update()
                clock.tick(20)

class c_screen_main(c_screen):
    def __init__(self):
        self.authenticated = True
        settingsScreen = c_screen_settings()
        self.btn_settings = c_imageButton(0, display_height - img_settings.get_size()[0], img_settings, settingsScreen.show)
        self.langBtns = []
        x = display_width
        for language in availableLanguages:
            flagimg = language.flag
            y = display_height - flagimg.get_size()[1]
            x = x - flagimg.get_size()[0]
            self.langBtns.append(c_imageButton(x, y, flagimg, chooseLanguage, language))

    def putStuffOnScreen(self):
        x = (display_width / 2)- img_logo.get_size()[0]/2
        #y = (display_height /2)- img_logo.get_size()[1]/2
        y = 10
        gameDisplay.blit(img_logo, (x,y))
        gameDisplay.blit(img_key, (((display_width/2)-img_key.get_size()[0]/2),(display_height /2)- img_key.get_size()[1]/2))
        self.btn_settings.show()
        for btn in self.langBtns:
            btn.show()

    def checkbuttons(self):
        mouse = pygame.mouse.get_pos()
        self.btn_settings.checkClick(mouse)
        for btn in self.langBtns:
            btn.checkClick(mouse)

class c_screen_settings(c_screen):
    def __init__(self):
        self.authenticated = False
        self.partialPassCode = ''
        self.wrongCodeAttempts = 0
        self.btn_back = c_imageButton(0, display_height - img_back.get_size()[0], img_back, self.goBack)
        self.btn_changePass = c_textButton('Change settings password',100, 100, 300, 60, blue)
        self.numpad = []
        self.initNumpad(display_width/2, display_height/2, 50, 50, 50)
        
        
    def initNumpad(self, x, y, d, w, h):
        for row in range(1,4):
            for column in range(1,4):
                xc = x + (column - 2) * (d + w * 0.5) - d * 0.5
                yc = y - (row - 2) * (d + h * 0.5) - d * 0.5
                number = (column + 3 * (row - 1))
                btn = c_textButton(str(number), xc, yc, w, h, blue, self.enterNumber, number)
                self.numpad.append(btn)
        self.numpad.append(c_textButton(str(0),x - 1* (d + w * 0.5) - d * 0.5, y  + 2 * (d + h * 0.5) - d * 0.5 , w, h, blue, self.enterNumber, 0))
        self.numpad.append(c_textButton('OK', (x - d * 0.5), (y + 2 * (d + h * 0.5) - d * 0.5), 2*w+d*0.5, h, blue, self.authenticate))

    def enterNumber(self, number):
        self.partialPassCode += str(number)

    def putStuffOnScreen(self):
        #showLanguageOptions()        
        TextSurf, TextRect = text_objects("Settings", largeText)
        TextRect.midleft = (30,20)
        gameDisplay.blit(TextSurf, TextRect)
        self.btn_back.show()
        self.btn_changePass.show()
    
    def showAuthenticate(self):
        if(self.wrongCodeAttempts > 3):
            timediff = self.timeoutEnd - datetime.datetime.now()
            if(timediff.total_seconds() > 0):
                self.putText(display_width/2, 500, 'Too many wrong password attempts!', largeText)
                self.putText(display_width/2, 540, 'Wait for: ' + str(int(timediff.total_seconds())) + ' seconds', largeText)
            else:
                self.wrongCodeAttempts = 0
        else:
            TextSurf, TextRect = text_objects("Enter password:", largeText)
            TextRect.midtop = (display_width/2, 150)
            gameDisplay.blit(TextSurf, TextRect)
            self.btn_back.show()
            for btn in self.numpad:
                btn.show()

            TextSurfCode, TextRectCode = text_objects(self.partialPassCode, largeText)
            TextRectCode.midtop = (display_width/2, 500)
            gameDisplay.blit(TextSurfCode, TextRectCode)

    
    def authenticate(self):
        if(self.partialPassCode == '1236'):
            self.wrongCodeAttempts = 0
            self.authenticated = True
        else:
            self.wrongCodeAttempts += 1
            if(self.wrongCodeAttempts > 3):
                self.timeoutEnd = datetime.datetime.now() + datetime.timedelta(seconds=10)
        self.partialPassCode = ''

    def checkbuttons(self):
        mouse = pygame.mouse.get_pos()
        self.btn_back.checkClick(mouse)
        for btn in self.numpad:
            btn.checkClick(mouse)


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def chooseLanguage(lang):
    print(lang.name)
    currentLanguage = lang

availableLanguages = [c_language('nl'), c_language('fr'), c_language('gb')]
currentLanguage = availableLanguages[0]

mainScreen = c_screen_main()
settingsScreen = c_screen_settings()

mainScreen.show()
pygame.quit()
quit()