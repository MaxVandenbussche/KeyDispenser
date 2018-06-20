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
img_logo = pygame.image.load('Logo.png')


class c_language:
    def __init__(self, name):
        self.name = name
        self.flag = pygame.image.load(name + '.png')

def button(x, y, img, action_arg, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    gameDisplay.blit(img, (x,y))
    if x+img.get_size()[0] > mouse[0] > x and y+img.get_size()[1] > mouse[1] > y:
        if click[0] == 1 and action != None:
            action(action_arg)



def chooseLanguage(lang):
    print(lang.name)

def showLanguageOptions():
    x = display_width
    for language in availableLanguages:
        flagimg = language.flag
        y = display_height - flagimg.get_size()[1]
        x = x - flagimg.get_size()[0]
        button(x, y, flagimg, language, chooseLanguage)

def screen_welcome():
    x = (display_width / 2)- img_logo.get_size()[0]/2
    y = (display_height /2)- img_logo.get_size()[1]/2
    gameDisplay.blit(img_logo, (x,y))
    showLanguageOptions()



availableLanguages = [c_language('nl'), c_language('fr'), c_language('gb')]

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    gameDisplay.fill(black)
    screen_welcome()
    pygame.display.update()
    clock.tick(15)

pygame.quit()
quit()