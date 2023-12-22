#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pygame
import random
import os
pygame.mixer.init()


pygame.init()


# In[3]:


# Colors
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
green = (0, 255, 0)


# In[4]:


# Creating window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))


# In[5]:


#background image
bgimg = pygame.image.load("back.png")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()


# In[6]:


# Game Title
pygame.display.set_caption("Snake Game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


# In[7]:


# making text to display on window
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x,y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


# In[8]:


# Game Loop

def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
   
 # error handling of deleted hiscore file
    if (not os.path.exists("hiscore.txt")):
        with open ("hiscore.txt","w") as f:
            f.write("0")
    with open("hiscore.txt","r")as f:
        hiscore=f.read()

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    init_velocity = 4
    snake_size = 30
    fps = 60
    while not exit_game:
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.fill(white)
            
            imp = pygame.image.load("Snake.jpg").convert()
            gameWindow.blit(imp,(200,300))
            text_screen("Game Over! Press Enter To Continue", red, 100, 250)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pygame.mixer.music.load("bg.mp3")
                        pygame.mixer.music.play()
                        gameloop()

        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y


            if abs(snake_x - food_x)<15 and abs(snake_y - food_y)<15:
                score +=1
                
                sound= pygame.mixer.Sound("eat.mp3")
                pygame.mixer.Sound.play(sound)

                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length +=5
                if score>=40:
                    init_velocity+=1
                    if score>=100:
                        init_velocity+=2
                        if score>=150:
                            init_velocity+=3
                        if score>=200:
                            init_velocity+=4
                    
                if score>int(hiscore):
                    hiscore=score

            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0, 0))
            text_screen("Score: " + str(score )+ "  High Score"+(" ")+str(hiscore), black, 5, 5)
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])


            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
        
            
            if len(snk_list)>snk_length:
                del snk_list[0]
                
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("out.mp3")
                pygame.mixer.music.play()

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over = True
                pygame.mixer.music.load("out.mp3")
                pygame.mixer.music.play()
            plot_snake(gameWindow, green, snk_list, snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()
pygame.mixer.music.load("bg.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)
gameloop()

