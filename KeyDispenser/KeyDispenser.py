import pygame


pygame.init()


display_width = 1024
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Key Check-in')

black = (0,0,0)
white = (255,255,255)

clock = pygame.time.Clock()
done = False
# Images used in the program
img_logo = pygame.image.load('logo.png')
img_settings =pygame.image.load('Settings.png')
img_back = pygame.image.load('back.png')
img_key = pygame.image.load('key.png')




class c_language:
    def __init__(self, name):
        self.name = name
        self.flag = pygame.image.load(name + '.png')

class c_screen_main:
   def __init__(self):
       self.done = False
       
   def putStuffOnScreen(self):
        x = (display_width / 2)- img_logo.get_size()[0]/2
        #y = (display_height /2)- img_logo.get_size()[1]/2
        y = 10
        gameDisplay.blit(img_logo, (x,y))
        gameDisplay.blit(img_key, (((display_width/2)-img_key.get_size()[0]/2),(display_height /2)- img_key.get_size()[1]/2))
        showLanguageOptions()
        imagebutton(0, display_height - img_settings.get_size()[0], img_settings, None, settingsScreen.show)

   def show(self):
       while not self.done:
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   self.done = True
               gameDisplay.fill(black)
               self.putStuffOnScreen()
               pygame.display.update()
               clock.tick(20)

class c_screen_settings:
    def __init__(self):
        self.done = False

    def putStuffOnScreen(self):
        showLanguageOptions()
        largeText = pygame.font.SysFont("Arial",30)
        TextSurf, TextRect = text_objects("Settings", largeText)
        TextRect.midleft = (30,20);
        gameDisplay.blit(TextSurf, TextRect)
        imagebutton(0, display_height - img_back.get_size()[0], img_back, None, self.goBack)
    
    def goBack(self):
        self.done = True

    def show(self):
        self.done = False
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                    mainScreen.done = True
                gameDisplay.fill(black)
                self.putStuffOnScreen()
                pygame.display.update()
                clock.tick(20)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def imagebutton(x, y, img, action_arg= None, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    gameDisplay.blit(img, (x,y))
    if x+img.get_size()[0] > mouse[0] > x and y+img.get_size()[1] > mouse[1] > y:
        if click[0] == 1 and action != None:
            if action_arg != None:
                action(action_arg)
            else:
                action()

def chooseLanguage(lang):
    print(lang.name)
    currentLanguage = lang

def showLanguageOptions():
    x = display_width
    for language in availableLanguages:
        flagimg = language.flag
        y = display_height - flagimg.get_size()[1]
        x = x - flagimg.get_size()[0]
        imagebutton(x, y, flagimg, language, chooseLanguage)




availableLanguages = [c_language('nl'), c_language('fr'), c_language('gb')]
currentLanguage = availableLanguages[0]

mainScreen = c_screen_main()
settingsScreen = c_screen_settings()

mainScreen.show()
pygame.quit()
quit()