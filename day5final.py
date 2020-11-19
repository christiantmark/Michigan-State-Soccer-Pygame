import sys
import pygame as pg 
import random

def drawText(msg, color, size,font):
    font_names = ["timesnewroman","arial","consolas","comicsansms","eras bold itc"]
    font = pg.font.SysFont(font, size)
    msg_image = font.render(msg, True, color)
    msg_rect = msg_image.get_rect()
    return msg_image, msg_rect

def run_game():
    #Initialize and set up screen.
    pg.init()
    screen = pg.display.set_mode([800, 600])
    pg.display.set_caption("Sparty Soccer")
    
    while True:
        start_game(screen)
        count_down(screen)
        play_game(screen)

def start_game(screen):
    screenR = screen.get_rect()
    while True:
        # Print Title screen
        title = pg.image.load('Title Screen.png')
        rectT = title.get_rect()
        screen.blit(title,rectT)
        space = pg.image.load('Press-Space-to-Play.png')
        rectS = space.get_rect()
        rectS.centerx = screenR.centerx
        rectS.centery = 500
        music = pg.mixer.Sound('2stepsfromhellWAV.wav')
        music.play()
        
        # Press Spcae to play Flashing Sequence
        frames = int(pg.time.get_ticks()/1000)
             
        if frames % 2 == 0:
             screen.blit(space,rectS)
        
        # Start event loop.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return
                
        pg.display.update()

def count_down(screen):
    frames = 0
    while True:
        three = pg.image.load('3.png')
        rectThree = three.get_rect()
        two = pg.image.load('2.png')
        rectTwo = two.get_rect()
        one = pg.image.load('1.png')
        rectOne = one.get_rect()
        
        if frames < 50:
            screen.blit(three,rectThree)
        if frames > 50 and frames < 100:
            screen.blit(two,rectTwo)
        if frames > 100 and frames < 150:
            screen.blit(one,rectOne)
        if frames == 151:
            return
        frames+=1
        pg.display.update()

def end_game(screen, goal1_value, goal2_value):
    while True:
        if goal1_value < goal2_value:
            end_image = pg.image.load("PlayerOne.png")
        elif goal1_value > goal2_value:
            end_image = pg.image.load("PlayerTwo.png")
        else:
            end_image = pg.image.load("Tie.png")
        
        end_rect = end_image.get_rect()
        screen.blit(end_image, end_rect)
        
        # Start event loop.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    run_game()
                
        pg.display.update()

def play_game(screen):
    #Colors
    WHITE = [255, 255, 255]
    BLACK = [0, 0, 0]
    TRANSPARENT = [0, 0, 0]

    #Images
    background_image = pg.image.load("Blank Field Template.png") 
    player1_image = pg.image.load("WolverinePlayer.png")
    player2_image = pg.image.load("SpartanPlayer.png")
    background_rect = background_image.get_rect()
    ball_image = pg.image.load("Soccer Ball.png")
    ball_rect = ball_image.get_rect()
    ball_rect.centerx = 400
    ball_rect.centery = 200
    goal_image = pg.image.load("goalOpposite.png")
    goal_rect = goal_image.get_rect()
    goal_rect.left = -30
    goal_rect.bottom = 425
    goal2_image = pg.image.load("goal2.png")
    goal2_rect = goal_image.get_rect()
    goal2_rect.right = 830
    goal2_rect.bottom = 425

    #Velocities
    player1_x_velocity = 0
    player1_y_velocity = 0
    player2_x_velocity = 0
    player2_y_velocity = 0
    ball_x_velocity = 0
    ball_y_velocity = 0
    player1_gravity = .2
    player2_gravity = .2
    #Shapes
    ground_rect = pg.Rect(0, 425, 800, 150)
    background_rect = background_image.get_rect()
    player1_rect = player1_image.get_rect()
    player2_rect = player2_image.get_rect()
    inv_goal_rect = pg.Rect(0,0,45,200)
    inv_goal2_rect = pg.Rect(755,0,45,200)
    screen_rect = screen.get_rect()
    
    player1_rect.centerx = 200
    player1_rect.centery = 350
    player2_rect.centerx = 600
    player2_rect.centery = 300
    
    #Ball variables
    ball_y_velocity = 1
    ball_x_velocity= 0
    gravity = 0.05
    coef_friction = 0.99
    number_of_bounces = 0
    
    # Goal variables
    goal1_value = 0
    goal2_value = 0
    
    # Special abilities
    power1 = 0
    power2 = 0
    ability1 = False
    hit = False
    
    #Other variables
    player1_jumped = False
    player2_jumped = False
    
    #Frame variables
    frameCounter = 0
    f = 0
    
    #Time Label
    time_image = pg.image.load("TimeLabel.png")
    time_rect = time_image.get_rect()
    time_rect.centerx = screen_rect.centerx
    
    a_pressed = False
    d_pressed = False
    left_pressed = False
    right_pressed = False
    
    #Start main loop.
    while True:
        if hit:
            player2_rect.centerx = 200
            player2_rect.centery = 350
            player1_rect.centerx = 600
            player1_rect.centery = 350
            hit = False
            power2 = 0
         # Player hitboxes
        inv_player1_left = pg.Rect(player1_rect.left, player1_rect.top, player1_rect.centerx - player1_rect.left, player1_rect.bottom - player1_rect.top)
        inv_player1_right = pg.Rect(player1_rect.centerx,player1_rect.top,player1_rect.right - player1_rect.centerx, player1_rect.bottom - player1_rect.top)

        inv_player2_left = pg.Rect(player2_rect.left, player2_rect.top, player2_rect.centerx - player2_rect.left, player2_rect.bottom - player2_rect.top)
        inv_player2_right = pg.Rect(player2_rect.centerx,player2_rect.top,player2_rect.right - player2_rect.centerx, player2_rect.bottom - player2_rect.top)
        
        #Ball physics
        ball_rect.centerx += ball_x_velocity
        if ball_rect.top < screen_rect.top:
            ball_y_velocity = abs(ball_y_velocity*.9)
        if ball_rect.left <= screen_rect.left:
            ball_x_velocity = abs(ball_x_velocity*.9)
        if ball_rect.right >= screen_rect.right:
            ball_x_velocity = -abs(ball_x_velocity*.9)
            
        # Ball gravity
        ball_y_velocity += gravity
        ball_y_velocity *= coef_friction
        ball_rect.centery += ball_y_velocity
        
        #Ball bounce
        is_below_ground = ball_rect.bottom > ground_rect.top
        if is_below_ground or ((ball_rect.bottom > goal_rect.top and ball_rect.colliderect(inv_goal_rect)) or (ball_rect.bottom > goal2_rect.top and ball_rect.colliderect(inv_goal2_rect))):
            ball_y_velocity = -abs(ball_y_velocity)
        
        # Goal
        if (ball_rect.centerx < goal_rect.right and not ball_rect.colliderect(inv_goal_rect)):
            ball_rect.centerx = 400
            ball_rect.centery = 200
            ball_y_velocity = 1
            ball_x_velocity = 0
            goal1_value += 1
        
        if (ball_rect.centerx > goal2_rect.left and not ball_rect.colliderect(inv_goal2_rect)):
            ball_rect.centerx = 400
            ball_rect.centery = 200
            ball_y_velocity = 1
            ball_x_velocity = 0
            goal2_value += 1

        
        # Image display
        screen.blit(background_image,background_rect)
        screen.blit(ball_image,ball_rect)
        screen.blit(goal_image,goal_rect)
        screen.blit(goal2_image,goal2_rect)

        #Draw images
        screen.blit(player1_image, player1_rect)
        screen.blit(player2_image, player2_rect)
        
        
        #Draw Timer
        msgImage, rectTxt = drawText((str(f) + " Secs"), BLACK, 25, "arial")
        frameCounter +=1
        f = int(60-frameCounter//60)
        if f == 0:
            end_game(screen, goal1_value, goal2_value)
        rectTxt.centerx = screen_rect.centerx
        rectTxt.centery = screen_rect.top + 40
        screen.blit(msgImage, rectTxt)
        screen.blit(time_image,time_rect)
        goalImage, goalTxt = drawText((str(goal2_value) + "  -  "+ str(goal1_value)), BLACK, 60, "eras bold itc")
        goalTxt.centerx = screen_rect.centerx
        goalTxt.centery = screen_rect.top + 115
        screen.blit(goalImage, goalTxt)
        power1Image, power1Txt = drawText((str(power1) + "  Power"), BLACK, 25, "arial")
        power1Txt.centerx = screen_rect.left + 50
        power1Txt.centery = screen_rect.top + 40
        screen.blit(power1Image, power1Txt)
        power1Image, power1Txt = drawText((str(power2) + "  Power"), BLACK, 25, "arial")
        power1Txt.centerx = screen_rect.right - 50
        power1Txt.centery = screen_rect.top + 40
        screen.blit(power1Image, power1Txt)
        
        #Movement
        player1_rect.left += player1_x_velocity
        player1_rect.top += player1_y_velocity
        player2_rect.left += player2_x_velocity
        player2_rect.top += player2_y_velocity
        ball_rect.left += ball_x_velocity
        ball_rect.top += ball_y_velocity
        
        player1_y_velocity += player1_gravity
        player2_y_velocity += player2_gravity
        
        #Collision detection
        if inv_player1_right.colliderect(inv_player2_left) and not player1_rect.colliderect(inv_player2_right):
            player1_rect.left -= 1
            player2_rect.left += 1
            player1_x_velocity = 0
            player2_x_velocity = 0
        if inv_player1_left.colliderect(inv_player2_right) and not player1_rect.colliderect(inv_player2_left) :
            player1_rect.left += 1
            player2_rect.left -= 1
            player1_x_velocity = 0
            player2_x_velocity = 0
            
        if player1_rect.colliderect(inv_player2_left) and player1_rect.colliderect(inv_player2_right):
            player1_y_velocity = 0
            player2_y_velocity = 0

        
        if player1_rect.colliderect(ground_rect):
            player1_y_velocity = 0
            player1_jumped = False
        
        if player1_rect.top < screen_rect.top:
            player1_y_velocity = player1_y_velocity*.9
        if player1_rect.left <= screen_rect.left:
            player1_x_velocity = 0
            player1_rect.left += 1
        if player1_rect.right >= screen_rect.right:
            player1_x_velocity = 0
            player1_rect.left -= 1
            
        if player2_rect.colliderect(ground_rect):
            player2_y_velocity = 0
            player2_jumped = False
            
        if player2_rect.top < screen_rect.top:
            player2_y_velocity = player2_y_velocity*.9
        if player2_rect.left <= screen_rect.left:
            player2_x_velocity = 0
            player2_rect.left += 1
        if player2_rect.right >= screen_rect.right:
            player2_x_velocity = 0    
            player2_rect.left -= 1

        
#        if inv_player1_left.colliderect(ball_rect) or inv_player2_left.colliderect(ball_rect):
#            ball_x_velocity -= 1
#            ball_y_velocity = -2
#            
#        if inv_player1_right.colliderect(ball_rect) or inv_player2_right.colliderect(ball_rect):
#            ball_x_velocity += 1
#            ball_y_velocity = -2
            
        if ball_rect.colliderect(inv_player1_left):
            if ability1:
                ball_x_velocity = 20
                ball_y_velocity = 0
                
                ability1 = False
            
            if ball_rect.bottom <= (inv_player1_left.top + 50):
                ball_x_velocity -= 1
                ball_y_velocity -= 2
                power1 += 1
            elif ball_rect.top >= (inv_player1_left.bottom -50):
                if ball_rect.colliderect(ground_rect):
                    ball_y_velocity = 0
                    ball_x_velocity = -2
                else:
                    ball_x_velocity -= 2
                    ball_y_velocity += .5
            else:
                if ball_x_velocity != 0:
                    ball_x_velocity = -abs(ball_x_velocity*.9)
                else:
                    ball_rect.centerx = inv_player1_left.left - 30
                    ball_x_velocity -= 1
        if ball_rect.colliderect(inv_player2_left):                
            if ball_rect.bottom <= (inv_player2_left.top + 50):
                ball_x_velocity -= 1
                ball_y_velocity -= 2
                power2 += 1
                
            elif ball_rect.top >= (inv_player2_left.bottom-50):
                
                if ball_rect.colliderect(ground_rect):
                    ball_x_velocity -= 2
                    
                else:
                    ball_x_velocity -= 2
                    ball_y_velocity += .5
                    
            else:
                if ball_x_velocity != 0:
                    ball_x_velocity = -abs(ball_x_velocity*.9)
                    
                else:
                    ball_rect.centerx == inv_player2_left.left - 30
                    ball_x_velocity -= 1
        if ball_rect.colliderect(inv_player1_right):
            if ability1:
                ball_x_velocity = 20
                ball_y_velocity = 0
                
                ability1 = False
            if ball_rect.bottom <= (inv_player1_right.top + 50):
                ball_x_velocity += 1
                ball_y_velocity -= 2
                power1 += 1
            elif ball_rect.top >= (inv_player1_right.bottom - 50):
                if ball_rect.colliderect(ground_rect):
                    ball_y_velocity = 0
                    ball_x_velocity = 2
                else:
                    ball_x_velocity += 2
                    ball_y_velocity += .5
            else:
                if ball_x_velocity != 0:
                    ball_x_velocity = abs(ball_x_velocity*.9)
                else:
                    ball_rect.centerx = inv_player1_right.right + 30
                    ball_x_velocity += 2
        if ball_rect.colliderect(inv_player2_right):
            if ball_rect.bottom <= (inv_player2_right.top + 50):
                ball_x_velocity += 1
                ball_y_velocity -= 2
                power2 += 1
            elif ball_rect.top >= (inv_player2_right.bottom - 50):
                if ball_rect.colliderect(ground_rect):
                    ball_y_velocity = 0
                    ball_x_velocity = -2
                else:
                    ball_x_velocity += 2
                    ball_y_velocity += .5
            else:
                if ball_x_velocity != 0:
                    ball_x_velocity = abs(ball_x_velocity*.9)
                else:
                    ball_rect.centerx = inv_player2_right.right + 30
                    ball_x_velocity += 2
        
        # Start event loop.            
        for event in pg.event.get():
            #Player controls
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    end_game(screen, goal1_value, goal2_value)
                
                if event.key == pg.K_a:
                    player1_x_velocity = -4
                    a_pressed = True
                if event.key == pg.K_d:
                    player1_x_velocity = 4
                    d_pressed = True
                if event.key == pg.K_w and player1_jumped == False:
                    player1_y_velocity = -9 
                    player1_jumped = True
                if event.key == pg.K_s and player1_jumped == True:
                    player1_y_velocity = 5
                
                if event.key == pg.K_a and event.key == pg.K_d:
                    player1_x_velocity = 0
                
                if event.key == pg.K_LEFT:
                    player2_x_velocity = -4
                    left_pressed = True
                if event.key == pg.K_RIGHT:
                    player2_x_velocity = 4
                    right_pressed = True
                if event.key == pg.K_UP and player2_jumped == False:
                    player2_y_velocity = -9
                    player2_jumped = True
                if event.key == pg.K_DOWN and player2_jumped == True:
                    player2_y_velocity = 5
                    
                if event.key == pg.K_RIGHT and event.key == pg.K_LEFT:
                    player2_x_velocity = 0
                
                if event.key == pg.K_r:
                    ball_rect.centerx = 400
                    ball_rect.centery = 200
                    ball_x_velocity = 0
                    ball_y_velocity = 1
                if event.key == pg.K_RCTRL and power2 >= 20:
                    hit = True
                if event.key == pg.K_g and power1 >= 20:
                    ability1 = True
                    power1 = 0
                
#                if not event.key == pg.K_a and not pg.K_d and player1_x_velocity != 0:
#                    player1_x_velocity = 0
#                
#                if not event.key == pg.K_LEFT and not pg.K_RIGHT and player2_x_velocity != 0:
#                    player2_x_velocity = 0

            if event.type == pg.KEYUP:
                if event.key == pg.K_a:
                    player1_x_velocity += 4
                    a_pressed = False
                if event.key == pg.K_d:
                    player1_x_velocity += -4
                    d_pressed = False
                
                if event.key == pg.K_LEFT:
                    player2_x_velocity += 4
                    left_pressed = False
                if event.key == pg.K_RIGHT:
                    player2_x_velocity += -4
                    right_pressed  = False
                    
                
                
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
                
            if a_pressed == False and d_pressed == False and player1_x_velocity != 0:
                player1_x_velocity = 0    
                
            if right_pressed == False and left_pressed == False and player2_x_velocity != 0:
                player2_x_velocity = 0
                
            if player1_x_velocity > 4:
                player1_x_velocity = 4
            if player1_x_velocity < -4:
                player1_x_velocity = -4
                    
            if player2_x_velocity > 4:
                player2_x_velocity = 4
            if player2_x_velocity < -4:
                player2_x_velocity = -4    
        
        pg.display.update()

try:
    run_game()
finally:
    pg.quit()