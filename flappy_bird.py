import pygame,sys,random

pygame.mixer.pre_init(frequency=60000,size=-16,channels=1,buffer=512)
pygame.init()

def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(600,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midbottom=(600,random_pipe_pos-150))
    return bottom_pipe,top_pipe
   
def move_pipes(pipes): 
    for pipe in pipes:
        pipe.centerx-=5
    return pipes    

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom>=500:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe) 
            #False for x direction and true for y direction   

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
               
            return False
            
    if bird_rect.top<=-100 or bird_rect.bottom>=500:
        return False

    return True

def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
    return new_bird    
    # rotozoom takes 3 arguments: The surface to be rotated, angle,scale

def bird_flying():
    new_bird=bird_frames[bird_index]  
    new_bird_rect=new_bird.get_rect(center=(50,bird_rect.centery)) 
    return new_bird,new_bird_rect 

def display_score(game_state):
    if game_state=="play_game":
        score_surface=game_font.render(f'Score:{int(score)}',True,(0,0,153))
        score_rect=score_surface.get_rect(center=(250,25))
        screen.blit(score_surface,score_rect)
    if game_state=="Game_over":
        score_surface=game_font.render(f'Score: {int(score)}',True,(255,255,0))
        score_rect=score_surface.get_rect(center=(250,200))
        screen.blit(score_surface,score_rect)

        high_score_surface=game_font.render(f'High Score: {int(high_score)}',True,(255,204,0))
        high_score_rect=high_score_surface.get_rect(center=(250,300))
        screen.blit(high_score_surface,high_score_rect)

        Game_restart_surface=game_font.render('Click to Restart Game',True,(255,153,51))
        Game_restart_rect=Game_restart_surface.get_rect(center=(250,400))
        screen.blit(Game_restart_surface,Game_restart_rect)

def score_update(score,high_score):
    if score>high_score:    
        high_score=score
    return high_score    

def cross_prev_highscore(score,highscore):
    if score>highscore:
        return highscore_sound.play()

screen = pygame.display.set_mode((500,600))
surface = pygame.image.load('assets/flappy.png')
pygame.display.set_icon(surface)
clock=pygame.time.Clock()
game_font=pygame.font.Font('assets/04B_19.ttf',30)
pygame.display.set_caption("Flappy Bird")
fps=90

# Game variables
Gravity= 0.25
bird_movement=0
score=0
high_score=0

game_active=True
bg_surface=pygame.image.load('assets/background-day.png').convert()
bg_surface=pygame.transform.scale(bg_surface,(500,600))

floor_surface=pygame.image.load('assets/base.png').convert()
floor_surface=pygame.transform.scale(floor_surface,(500,150))
floor_x_position=0

bird_dsurface=pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_dsurface=pygame.transform.scale(bird_dsurface,(40,30))
bird_msurface=pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_msurface=pygame.transform.scale(bird_msurface,(40,30))
bird_usurface=pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_usurface=pygame.transform.scale(bird_usurface,(40,30))
bird_downflap=pygame.transform.scale(bird_dsurface,(40,30))
bird_midflap=pygame.transform.scale(bird_msurface,(40,30))
bird_upflap=pygame.transform.scale(bird_usurface,(40,30))
bird_frames=[bird_downflap,bird_midflap,bird_upflap]
bird_index=0
bird_surface=bird_frames[bird_index]
bird_rect=bird_surface.get_rect(center=(50,150))

BIRDFLAP=pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,300)

pipe_surface=pygame.image.load('assets/pipe-green.png').convert()
pipe_surface=pygame.transform.scale(pipe_surface,(75,400))
pipe_surface_y_position=300
pipe_list=[]
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,900)
pipe_height=[400,300,200]

Game_over_surface=pygame.image.load('assets/oover.png').convert()
Game_over_surface=pygame.transform.scale(Game_over_surface,(500,500))
Game_over_rect=Game_over_surface.get_rect(center=(250,250))

birdflap_sound=pygame.mixer.Sound('assets/sound_sfx_wing.wav')
dead_sound=pygame.mixer.Sound('assets/sound_sfx_hit.wav')
highscore_sound=pygame.mixer.Sound('assets/sound_sfx_point.wav')

pygame.mixer.music.load('assets/Fluffing-a-Duck.mp3')
pygame.mixer.music.play()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and game_active==True :
                bird_movement=0
                bird_movement-=7
                birdflap_sound.play()
            if event.button == 1 and game_active==False: 
                game_active==True 
                pipe_list.clear()
                bird_rect.center= (50,150) 
                bird_movement=0 
                score=0
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_SPACE and game_active==True:
                bird_movement=0
                bird_movement-=7
                birdflap_sound.play()
            if event.key == pygame.K_SPACE and game_active==False: 
                game_active==True 
                pipe_list.clear()
                bird_rect.center= (50,150) 
                bird_movement=0
                score=0
      
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type==BIRDFLAP:
            if bird_index<2:
                bird_index+=1 
            else:
                bird_index=0

            bird_surface,bird_rect=bird_flying()       
    
    #background
    screen.blit(bg_surface,(0,0))


    if game_active:

        # Loading and playing background music:
        pygame.mixer.music.load('assets/mixkit-sad-game-over-trombone-471.wav')
        pygame.mixer.music.play()
        #bird
        bird_movement+=Gravity
        rotated_bird=rotate_bird(bird_surface)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird,bird_rect)
        #pipe
        pipe_list=move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score+=0.02
        cross_prev_highscore(score,high_score)
        display_score('play_game')
    else:
        screen.blit(Game_over_surface,Game_over_rect)
        high_score=score_update(score,high_score)
        display_score('Game_over')
        
    #check collision
    game_active=check_collision(pipe_list)

    #floor
    screen.blit(floor_surface,(floor_x_position,500))
    screen.blit(floor_surface,(floor_x_position+500,500))
    
    
   
   #floor
    floor_x_position-=3

    if floor_x_position<=-500:
        floor_x_position=0
    



    pygame.display.update()
    clock.tick(fps)        
