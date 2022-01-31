import os
import pygame

pygame.mixer.init()
pygame.init()


WIDTH, HEIGHT = 1400, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
SPACESHIP_SPEED = 5
BULLETS_SPEED = 10
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 100, 75
MAX_NUM_BULLETS = 8

P1_HIT = pygame.USEREVENT + 1
P2_HIT = pygame.USEREVENT + 2

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)


### LOAD ALL SOUNDS
HIT_SOUND = pygame.mixer.Sound('Assets/explode.wav')
FIRE_SOUND = pygame.mixer.Sound('Assets/shoot.wav')
WINNER_SOUND = pygame.mixer.Sound('Assets/winner.wav')
BACKGROUND_MUSIC = pygame.mixer.Sound('Assets/background.wav')

### LOAD ALL IMAGES
PLAYER1_SPACESHIP = pygame.image.load(os.path.join('Assets', 'player1_spaces.png'))
PLAYER2_SPACESHIP = pygame.image.load(os.path.join('Assets', 'player2_spaces.png'))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background1.png')), (WIDTH, HEIGHT))



SPACESHIP_1 = pygame.transform.rotate(pygame.transform.scale(PLAYER1_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)
SPACESHIP_2 = pygame.transform.rotate(pygame.transform.scale(PLAYER2_SPACESHIP, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)



explosion_group = pygame.sprite.Group()

### CREATE BUTTON AND EXPLOSION CLASS

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 6):
			img = pygame.image.load(f"Assets/exp{num}.png")
			img = pygame.transform.scale(img, (100, 100))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 4
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete then delete explosion 
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

### DEFINE ALL FUNCTIONS

def draw_window(player1, player2, p1_bullets, p2_bullets, p1_health, p2_health):


    WINDOW.blit(BACKGROUND, (0 ,0))
    pygame.draw.rect(WINDOW, (0, 0, 0), BORDER)    


    WINDOW.blit(SPACESHIP_1, (player1.x, player1.y))
    WINDOW.blit(SPACESHIP_2, (player2.x, player2.y))

    explosion_group.draw(WINDOW)
    explosion_group.update()


       

    p1_health_text = get_font(20).render("Player 1 Health: " + str(p1_health), 1, (255, 255, 255))
    p2_health_text = get_font(20).render("Player 2 Health: " + str(p2_health), 1, (255, 255, 255))
    WINDOW.blit(p2_health_text, (WIDTH - p1_health_text.get_width() - 15, 10))
    WINDOW.blit(p1_health_text, (15, 10))

    for bullet in p1_bullets:
        pygame.draw.rect(WINDOW, (255,0,0), bullet)
    
    for bullet in p2_bullets:
        pygame.draw.rect(WINDOW, (255, 255, 0), bullet)

    pygame.display.update()

def get_font(size):
    return pygame.font.Font("Assets/font.ttf", size)

def main_menu():

    pygame.display.set_caption("Menu")
    BACKGROUND_MUSIC.play()

    while True:
        WINDOW.blit(BACKGROUND, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        WINDOW.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WINDOW)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play_game()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()

        pygame.display.update()
 
def player1_movement(keys_pressed, player1):
    if keys_pressed[pygame.K_a] and player1.x - SPACESHIP_SPEED > 0:
        player1.x -= SPACESHIP_SPEED
    if keys_pressed[pygame.K_s] and player1.y + SPACESHIP_SPEED + player1.height + 30 < HEIGHT:
        player1.y += SPACESHIP_SPEED
    if keys_pressed[pygame.K_w] and player1.y - SPACESHIP_SPEED > 0:
        player1.y -= SPACESHIP_SPEED
    if keys_pressed[pygame.K_d] and player1.x + SPACESHIP_SPEED + player1.width < BORDER.x:
        player1.x += SPACESHIP_SPEED

def player2_movement(keys_pressed, player2):
    if keys_pressed[pygame.K_LEFT] and player2.x - SPACESHIP_SPEED > BORDER.x + BORDER.width:
        player2.x -= SPACESHIP_SPEED
    if keys_pressed[pygame.K_DOWN] and player2.y + SPACESHIP_SPEED + player2.height + 30 < HEIGHT:
        player2.y += SPACESHIP_SPEED
    if keys_pressed[pygame.K_UP] and player2.y - SPACESHIP_SPEED > 0:
        player2.y -= SPACESHIP_SPEED
    if keys_pressed[pygame.K_RIGHT] and player2.x + SPACESHIP_SPEED + player2.width < WIDTH:
        player2.x += SPACESHIP_SPEED

def bullets_movement(p1_bullets, p2_bullets, player1, player2):



    for bullet1 in p1_bullets:                                   ###### P1 TO SHOOT BULLETS

        bullet1.x += BULLETS_SPEED

        if player2.colliderect(bullet1):


            pygame.event.post(pygame.event.Event(P2_HIT))
            p1_bullets.remove(bullet1)
            explosion = Explosion(bullet1.x, bullet1.y)
            explosion_group.add(explosion)


        elif bullet1.x > WIDTH:
            p1_bullets.remove(bullet1)

        for bullet2 in p2_bullets:                               ###### IF BULLETS COLLIDE, REMOVE THEM
            if bullet2.colliderect(bullet1):
                p1_bullets.remove(bullet1)
                p2_bullets.remove(bullet2)
                explosion = Explosion(bullet2.x, bullet2.y)
                explosion_group.add(explosion)    



    for bullet2 in p2_bullets:                                   ###### IF BULLETS ARE CREATED, 1ST DECREASE X TO MOVE THEM

        bullet2.x -= BULLETS_SPEED

        if player1.colliderect(bullet2):                         ###### IF BULLEIT RECTANGLE COLLIDE WITH SPACESHIP RECTANGE         
            p2_bullets.remove(bullet2)                           ###### BULLETS TO BE REMOVED FROM LIST    
            pygame.event.post(pygame.event.Event(P1_HIT))         
            explosion = Explosion(bullet2.x, bullet2.y)
            explosion_group.add(explosion)     


        elif bullet2.x < 0:
            p2_bullets.remove(bullet2)

        for bullet1 in p1_bullets:
            if bullet2.colliderect(bullet1):
                p2_bullets.remove(bullet2)
                p1_bullets.remove(bullet1)
                explosion = Explosion(bullet2.x, bullet2.y)
                explosion_group.add(explosion)    

def draw_winner(text):
    draw_text = get_font(75).render(text, 1, (255,255,255))
    WINDOW.blit(draw_text, (WIDTH//2 - draw_text.get_width() / 2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def play_game():

    pygame.display.set_caption("PLAY")

    p1_bullets = []
    p2_bullets = []

    player1 = pygame.Rect(50, 415, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)       ######### DEFINE TWO RECTANGLES TO REPRESENT THE POSITION AND SPACE OF EACH OF SPACESHIPS
    player2 = pygame.Rect(1300, 415, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    p1_health = 10
    p2_health = 10

 
    clock = pygame.time.Clock()
    run = True
    while run:  
        

        clock.tick(FPS)                    ####### HOW MUCH SCREEN REFRESHES
        for event in pygame.event.get():   ####### IF USER CLOSES WINDOWS, QUIT GAME
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()



            if event.type == pygame.KEYDOWN:                               ###### CREATE BULLETS INTO p1_bullets LIST EVERYTIME USER PRESSES FIRE KEY (LEFT ALT OR RIGHT ALT)

                if event.key == pygame.K_LALT and len(p1_bullets) < MAX_NUM_BULLETS:
                    bullet = pygame.Rect(player1.x + player1.width - 30, player1.y + player1.height//2 + 5, 10, 5)       ###### BULLETS TO BE CREATED FROM THE CENTER OF THE SPACESHIP
                    p1_bullets.append(bullet)
                    FIRE_SOUND.play()

                if event.key == pygame.K_RALT and len(p2_bullets) < MAX_NUM_BULLETS:
                    bullet = pygame.Rect(player2.x, player2.y + player2.height//2 + 10, 10, 5)
                    p2_bullets.append(bullet)        
                    FIRE_SOUND.play() 

            if event.type == P1_HIT:
                p1_health -= 1
                HIT_SOUND.play()
            
            if event.type == P2_HIT:
                p2_health -= 1
                HIT_SOUND.play()
                
        win_message = ""

        if p1_health <= 0:
            win_message = "Player 2 Wins!"

        if p2_health <= 0:
            win_message = "Player 1 Wins!"

        if win_message != "":
            BACKGROUND_MUSIC.stop()
            WINNER_SOUND.play()
            draw_winner(win_message)


            break

        keys_pressed = pygame.key.get_pressed()      ####### WE CHECK EVERYTIME WHICH KEYS ARE PRESSED AT 60 TIMES PER SECOND
        player1_movement(keys_pressed, player1)
        player2_movement(keys_pressed, player2)

        bullets_movement(p1_bullets, p2_bullets, player1, player2)

        draw_window(player1, player2, p1_bullets, p2_bullets, p1_health, p2_health)              ######### SEND VARIABLES TO UPDATE POSITION OF THE SPACESHIPS AND OBJECTS MOVING



    main_menu()

### LOAD GAME

main_menu()

