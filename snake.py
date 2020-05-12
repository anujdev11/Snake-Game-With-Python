import pygame 
import random
import os


pygame.mixer.init()
pygame.init()
# color 
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)

#Window
gameWindow=pygame.display.set_mode((900,500))
pygame.display.set_caption("Snakes By Anuj")
pygame.display.update()

bgimg = pygame.image.load("bg2.jpg")
bgimg = pygame.transform.scale(bgimg, (900, 500)).convert_alpha()

welcomeimg = pygame.image.load("Intro.jpeg")
welcomeimg = pygame.transform.scale(welcomeimg, (900, 500)).convert_alpha()

gameover = pygame.image.load("outro.png")
gameover = pygame.transform.scale(gameover, (900, 500)).convert_alpha()




clock=pygame.time.Clock()
font=pygame.font.Font(None, 55)

def text_display(text,color,x,y):
    sceen_text=font.render(text, True, color)
    gameWindow.blit(sceen_text,[x,y])

def plot_snake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color,[x,y,snake_size,snake_size])

def welcome():
    
    exit_game = False
    while not exit_game:
        gameWindow.fill((233,210,229))
        gameWindow.blit(welcomeimg, (0, 0))
        text_display("Welcome to Snakes", black, 260, 220)
        text_display("Press Space Bar To Play", black, 232, 260)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load('back.mp3')
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)

# Game Loop 
def gameloop():
    # Variables
    game_exit=False
    game_over=False
    snake_x=100
    snake_y=200
    snake_size=15
    fps=60
    velocity_x=0
    velocity_y=0
    init_velocity=5
    score=0
    food_x=random.randint(0,900-100)
    food_y=random.randint(0,500-100)
    snk_list=[]
    snk_length=1

    if(not os.path.exists("hiscore.txt")):
        with open("hiscore.txt", "w") as f:
            f.write("0")

    with open("hiscore.txt","r") as f:
        hiscore=f.read()

    while not game_exit:
        if game_over:
            with open("hiscore.txt","w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            gameWindow.blit(gameover, (0, 0))
            # text_display("Game Over! Press Enter To continue",red,110,210)
            text_display("Score:"+str(score),red,350,320)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_exit=True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x=init_velocity
                        velocity_y=0
                    if event.key == pygame.K_LEFT:
                        velocity_x=-init_velocity
                        velocity_y=0
                    if event.key == pygame.K_UP:
                        velocity_y=-init_velocity
                        velocity_x=0
                    if event.key == pygame.K_DOWN:
                        velocity_y=init_velocity
                        velocity_x=0
            snake_x+=velocity_x
            snake_y+=velocity_y

            if abs(snake_x-food_x)<8 and abs(snake_y-food_y)<8:
                score+=10
                food_x=random.randint(0,900-100)
                food_y=random.randint(0,500-100)
                snk_length+=5

                if score>int(hiscore):
                    hiscore = score

            gameWindow.fill(white)
            gameWindow.blit(bgimg, (0, 0))
            text_display("Score:"+str(score) + "  Hi-Score:"+str(hiscore),red,5,5)
            pygame.draw.rect(gameWindow, red,[food_x,food_y,snake_size,snake_size])

            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list)>snk_length:
                del snk_list[0]
            
            if head in snk_list[:-1]:
                pygame.mixer.music.load('Game_over.mp3')
                pygame.mixer.music.play()
                game_over=True
            
            if snake_x<0 or snake_x>900 or snake_y<0 or snake_y>500:
                pygame.mixer.music.load('Game_over.mp3')
                pygame.mixer.music.play() 
                game_over=True

            plot_snake(gameWindow, black,snk_list,snake_size)

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()
welcome()