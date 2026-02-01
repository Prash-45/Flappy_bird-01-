import pygame
from sys import exit
from random import randint

def reset_game():
    global game_active, player_gravity, start_time, score, obstacle_rect_list

    game_active = True
    player_gravity = 0
    score = 0
    start_time = int(pygame.time.get_ticks() / 1000)

    obstacle_rect_list.clear()
    player_rect.topright = (100, 100)

def display_score():

    current_time = int(pygame.time.get_ticks()/1000) - start_time
    score_surface = text_font.render(f'Score:{current_time}',False,'black')
    score_rect = score_surface.get_rect(center = (300,25))
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    new_list = []

    for surface, rect in obstacle_list:
        rect.x -= 4
        screen.blit(surface, rect)

        if rect.right > -100:
            new_list.append((surface, rect))

    return new_list

def player_animation():
    global player_surface,player_frame_index

    player_frame_index += 0.1
    if player_frame_index >= len(player_frames):
        player_frame_index = 0
    player_surface = player_frames[int(player_frame_index)]

# pygame setup
pygame.init()
pygame.display.set_caption('Flappy Bird')          #Display_Surface
screen = pygame.display.set_mode((600,400))
clock = pygame.time.Clock()
text_font = pygame.font.Font('font/Pixeltype.ttf',45)
game_active = False
player_gravity = 0
score = 0
start_time = 0
pipe_gap = max(140, 200 - score * 2)
# pipe_gap = 150

# BG_Work (Regular_Surface)
ground_surface = pygame.image.load('graphics/floor-sprite.png').convert()
sky_surface = pygame.image.load('graphics/BG.png').convert()
text_surface = text_font.render('score',False,'black')
text_rect = text_surface.get_rect(center=(300,25))

# Obstacles
if randint(0,1):
    pipe_surface = pygame.image.load('graphics/pipe-green.png').convert()
else:
    pipe_surface = pygame.image.load ('graphics/pipe-red.png').convert()
pipe_surface_2 = pygame.transform.flip(pipe_surface, False, True).convert()



obstacle_rect_list=[]

# Player_work
if randint(0,1):
    player_frame_1 = pygame.image.load('graphics/redbird-upflap.png').convert_alpha()
    player_frame_2 = pygame.image.load('graphics/redbird-midflap.png').convert_alpha()
    player_frame_3 = pygame.image.load('graphics/redbird-downflap.png').convert_alpha()
else:
    player_frame_1 = pygame.image.load('graphics/bluebird-upflap.png').convert_alpha()
    player_frame_2 = pygame.image.load('graphics/bluebird-midflap.png').convert_alpha()
    player_frame_3 = pygame.image.load('graphics/bluebird-downflap.png').convert_alpha()

player_frames = [player_frame_1,player_frame_2,player_frame_3]
player_frame_index = 0
player_surface = player_frames[player_frame_index]
player_rect = player_surface.get_rect(topright=(100,100))

# Intro_screen
player_stand = pygame.image.load('graphics/front_face.png').convert_alpha()
player_stand_scaled = pygame.transform.scale(player_stand,(200,180))
player_stand_rect = player_stand_scaled.get_rect(center=(300,200))
game_name = text_font.render('Flappy Bird',False,'black')
game_name_rect = game_name.get_rect(center=(320,50))
game_message = text_font.render('Press space to run the game',False,'black')
game_message_rect = game_message.get_rect(center=(310,350))
game_over = pygame.image.load('graphics/gameover.png').convert_alpha()
game_over_rect = game_over.get_rect(center=(310,50))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)


while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_gravity = -12
                    


        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()


        if game_active:
            if event.type == obstacle_timer:
                pipe_y = randint(200, 280)

                bottom_pipe = pipe_surface.get_rect(topleft=(600, pipe_y))
                top_pipe = pipe_surface_2.get_rect(bottomleft=(600, pipe_y - pipe_gap))

                obstacle_rect_list.append((pipe_surface, bottom_pipe))
                obstacle_rect_list.append((pipe_surface_2, top_pipe))


    # RENDER YOUR GAME HERE
    if game_active:

        screen.blit(sky_surface,(0,-190))
        

        

        # Player
        player_gravity += 0.5
        player_gravity = min(player_gravity, 8)
        player_rect.y += player_gravity
    
        if player_rect.top <= 0:
            player_rect.top = 0
        player_animation()
        screen.blit(player_surface,player_rect)

        # Obstacle_movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)


        screen.blit(ground_surface,(0,300))
        score = display_score()

        # collision

        for surface, rect in obstacle_rect_list:
            if rect.colliderect(player_rect):
                game_active = False
                break

            if player_rect.bottom >= 300:
                game_active = False

    else:
        screen.fill((102,178,225))
        screen.blit(player_stand_scaled,player_stand_rect)

        
        score_message = text_font.render(f'Your Score:{score}',False,('black'))
        score_message_rect = score_message.get_rect(center = (310,350))



        if score == 0:
            screen.blit(game_message,game_message_rect)
            screen.blit(game_name,game_name_rect)
        else:
            screen.blit(game_over,game_over_rect)
            screen.blit(score_message,score_message_rect)

    pygame.display.update()
    clock.tick(50)  # limits FPS to 60