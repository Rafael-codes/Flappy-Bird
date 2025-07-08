import pygame
import random

# Initialize Pygame
pygame.init()

# Display dimensions
WIDTH, HEIGHT = 600, 400
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Background image
image=pygame.image.load("background.jpg")
image=pygame.transform.scale(image,(WIDTH, HEIGHT))

# Flappy bird properties
radius=20
spawnx=100
spawny=200

# Flappy bird image
fimage=pygame.image.load("angry_bird.jpg")
fimage=pygame.transform.scale(fimage,(2*radius,2*radius))

# Pillar properties
Width= 60
gap = 120
speed = 3
pipe_color = (34, 139, 34)
interval=2000

# Clock
clock = pygame.time.Clock()
FPS = 60

# Previous pipe's spawn time
last_spawn_time = pygame.time.get_ticks()

# List of pipes
pipes=[]
font = pygame.font.SysFont(None, 36)
game=True

# Game loop
running = True
score=0

while running:
    display.blit(image,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type ==pygame.MOUSEBUTTONDOWN:
            spawny-=35

    # Spawn new pipe at intervals
    current_time = pygame.time.get_ticks()
    if current_time - last_spawn_time > interval:
        gap_y = random.randint(80, 330)
        top_pipe = pygame.Rect(WIDTH, 0, Width, gap_y - gap// 2)
        bottom_pipe = pygame.Rect(WIDTH, gap_y + gap//2, Width, HEIGHT - (gap_y + gap // 2))
        scored=False
        pipes.append([top_pipe, bottom_pipe,scored])
        last_spawn_time = current_time
    h=pygame.Rect(spawnx,spawny,radius,radius)
    if game==True:
        # Move and draw pipes
        for pipe_pair in pipes[:]:
            top, bottom,scored1 = pipe_pair
            top.x -= speed
            bottom.x -= speed
            #Collision check
            if h.colliderect(top) or h.colliderect(bottom):
                game=False
                break
            pygame.draw.rect(display, pipe_color, top)    
            pygame.draw.rect(display, pipe_color, bottom)
            
            # Remove if off display
            if top.right < 0:
                pipes.remove(pipe_pair)
            #Calculation of score
            if (not scored1) and (top.right<spawnx):
                score+=1
                pipe_pair[2]=True
        display.blit(fimage,(spawnx,spawny))
        spawny+=1.6
        # Collision check
        if spawny+radius>=HEIGHT or spawny-radius<=0:
            game=False
    else:
        #Game restart with Game over window
        font = pygame.font.SysFont(None, 48)
        over = font.render("Game Over", True, (255, 0, 0))
        display.blit(over, (WIDTH // 2 - 100, (HEIGHT // 4)*1.5))
        score2=font.render("Score: "+str(score), True, (255, 0, 0))
        display.blit(score2, (WIDTH // 2 - 100, (HEIGHT // 4)*2))
        pygame.display.flip()
        pygame.time.delay(1500)
        # Reset values
        pipes = []
        score = 0
        spawny = 200
        game = True
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    display.blit(score_text, (10, 10))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
