import pygame
import os
import time

# Initialize Pygame
pygame.init()

# Set Screen
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("~~Tennis Game~~")

# Folder
folder = 'Images'

# Load Images
script_route = os.path.dirname(os.path.abspath(__file__))
images_route = os.path.join(script_route, folder)

# Create ball
ball = pygame.image.load(os.path.join(images_route, 'ball_25x25.png'))
ball_rect = ball.get_rect()

# Create paddle
paddle_img = pygame.image.load(os.path.join(images_route, 'paddle_100x83.png'))
paddle_rect = paddle_img.get_rect()

# Create background
background = pygame.transform.scale(pygame.image.load(os.path.join(images_route, 'background3.png')).convert(), (680, 480))

# Second Collision point
paddle_collision_rect = pygame.Rect(0, 0, 90, 15)

# Set position paddle and collision point
paddle_rect.center = (240, 435)
paddle_collision_rect.center = (240, 438)

# Set speed
speed = [4, 4]
speed_increase = 2

# FPS controls
clock = pygame.time.Clock()

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

# Game Over font
game_over_font = pygame.font.Font(None, 72)

# Game Over message
game_over_message = game_over_font.render("Game Over", True, (255, 0, 0))

# Game Over message position
game_over_message_rect = game_over_message.get_rect(center=(320, 240))

# Touches counter
touch_counter = 0

# Main loop
running = True
game_over = False
while running:
    # Events in Screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Check if any key has been pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle_rect.move_ip(-5, 0)
            paddle_collision_rect.move_ip(-5, 0)
            if  paddle_rect.left < 0:
                paddle_rect.left = 0
                paddle_collision_rect.left = 0


        
        if keys[pygame.K_RIGHT]:
            paddle_rect.move_ip(5, 0)
            paddle_collision_rect.move_ip(5, 0)
            if paddle_rect.right > screen.get_width():
                paddle_rect.right = screen.get_width()
                paddle_collision_rect.right = screen.get_width()
            
        # Screen collision
        if paddle_collision_rect.colliderect(ball_rect):
            # Calculate new angle based on where the ball hits the paddle
            ball_angle = (ball_rect.centerx - paddle_rect.centerx) / (paddle_rect.width / 2)
            speed[1] = -speed[1]
            speed[0] = ball_angle * 5

            # Increment score when ball hits paddle
            score += 1

            #Increase ball speed
            if score % 10 == 0:
                speed[0] += speed_increase
                speed[1] += speed_increase

    
        # Move the Ball
        ball_rect = ball_rect.move(speed)

        if ball_rect.left < 0 or ball_rect.right > screen.get_width():
            speed[0] = -speed[0]
        if ball_rect.top < 0:
            speed[1] = -speed[1]
        if ball_rect.bottom > screen.get_height():
            # Increment touches counter when ball hits bottom of the screen
            touch_counter += 1
            
            if touch_counter >= 5:  # Set your desired number of touches for Game Over
                game_over = True
            else:
                # Show  message
                screen.blit(background, (0, 0))
                message = font.render("Ups", True, (255, 0, 0))
                screen.blit(message, (280, 240))
                pygame.display.flip()
                time.sleep(2)
                ball_rect.center = (320, 240)  # Reset ball position
                speed = [4, 4]  # Reset ball speed
                continue

    # Fill
    screen.blit(background, (0, 0))
    
    # Draw ball
    screen.blit(ball, ball_rect)
    
    # Draw paddle
    screen.blit(paddle_img, paddle_rect)

    # Draw score
    text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(text, (10, 10))
    
    # Draw touches counte
    touches_text = font.render("lost balls: " + str(touch_counter), True, (0, 0, 0))
    screen.blit(touches_text, (500, 10))

    if game_over:
        screen.blit(game_over_message, game_over_message_rect)

    pygame.display.flip()

    # FPS
    clock.tick(60)

pygame.quit()
