import pygame
import os
import random
from boosters import load_booster
pygame.font.init() #initilize font library
pygame.mixer.init() #initialize sound library

#################################################################################################################################

#SETTINGS
FPS = 60
YELLOW_HEALTH = 5
RED_HEALTH = 20
VELOCITY = 6 #SHIP SPEED
BULLET_LENGTH = 20
BULLET_WIDTH = 7
BULLET_DAMAGE = 1
BULLET_VEL = 12 #BULLET SPEED
MAX_BULLETS = 3 #MAX BULLETS ON SCREEN PER SHIP
RESTART_PAUSE = 1000 #Time between GameOver to Restart in ms

#BOOSTERS GLOBAL SETTINGS
BOOSTER_SIZE = 70
BOOSTER_DURATION = 8000 #How long buff lasts for
BOOSTER_INITIAL = 3000 #First booster appearance
BOOSTER_DELAY = 1000 #Delay between subsequent boosters
BOOSTER_TYPES = ["heart", "rocket", "sniper", "cannon", "sonic"] #["heart", "rocket", "sniper", "cannon", "sonic"]

#Specific Boosters settings
BOOSTER_HEALTH = 3 #Specifies amount of health boost
BOOSTER_ROCKET_DAMAGE, ROCKET_WIDTH, ROCKET_LENGTH = 2, 11, 40
BOOSTER_SNIPER_VEL, SNIPER_MAX_BULLETS = 24, 1
BOOSTER_CANNON_SIZE, CANNON_MAX_BULLETS = 50, 3
BOOSTER_SONIC_VEL = 12

#################################################################################################################################

#GLOBAL VAR
SPACESHIP_X_LENGTH, SPACESHIP_Y_LENGTH = 65, 90 #note that this is based on the global coordinates
WIDTH, HEIGHT = 1200, 640 #GAME BOARD SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (173, 216, 230)
NAVY = (0, 0, 100)
YELLOW = (255, 255, 0)
TIMER_FONT = pygame.font.SysFont("comicsans", 40)
HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

#BOOSTERS
HEART_IMAGE, ROCKET_IMAGE, SNIPER_IMAGE, CANNON_IMAGE, SONIC_IMAGE = load_booster(BOOSTER_SIZE)
BOOSTER_LIST = {
    "heart": HEART_IMAGE,
    "rocket": ROCKET_IMAGE,
    "sniper": SNIPER_IMAGE,
    "cannon": CANNON_IMAGE,
    "sonic": SONIC_IMAGE
}

#INITIALIZE WINDOW
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Spaceship Game!")
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT )

#EVENTS
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
Y_BOOSTER_HEART = pygame.USEREVENT + 10
Y_BOOSTER_ROCKET = pygame.USEREVENT + 11
Y_BOOSTER_SNIPER = pygame.USEREVENT + 12
Y_BOOSTER_CANNON = pygame.USEREVENT + 13
Y_BOOSTER_SONIC = pygame.USEREVENT + 14
R_BOOSTER_HEART = pygame.USEREVENT + 20
R_BOOSTER_ROCKET = pygame.USEREVENT + 21
R_BOOSTER_SNIPER = pygame.USEREVENT + 22
R_BOOSTER_CANNON = pygame.USEREVENT + 23
R_BOOSTER_SONIC = pygame.USEREVENT + 24

#LOAD IMAGES AND SCALE
YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.scale(
    pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, 90), (SPACESHIP_X_LENGTH, SPACESHIP_Y_LENGTH))

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.scale(
    pygame.transform.rotate(RED_SPACESHIP_IMAGE, 270), (SPACESHIP_X_LENGTH, SPACESHIP_Y_LENGTH))

SPACE_IMAGE = pygame.transform.scale(pygame.image.load(
    os.path.join("Assets", "space.png")).convert(), (WIDTH, HEIGHT))

CANNON_SCALE_FACTOR = 1
CANNON_BALL_IMAGE = pygame.image.load(
    os.path.join("Assets", "cannon_ball.png"))
CANNON_BALL = pygame.transform.scale(
    CANNON_BALL_IMAGE, (BOOSTER_CANNON_SIZE*CANNON_SCALE_FACTOR, BOOSTER_CANNON_SIZE*CANNON_SCALE_FACTOR))

#LOAD SOUNDS
BG_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "arcade_theme.mp3"))
BULLET_HIT_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Grenade+1.mp3"))
SNIPER_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "Gun+Silencer.mp3"))
CANNON_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "cannon.mp3"))
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    os.path.join("Assets", "laser.mp3"))
UPGRADE = pygame.mixer.Sound(
    os.path.join("Assets", "coins.mp3"))


#################################################################################################################################
#CODE

# to keep track game time in current game, including when game is restart
class CurrentClock: 
    def __init__(self):
        self.timer_start = pygame.time.get_ticks()

    def reset(self):
        self.timer_start = pygame.time.get_ticks()
    
    def current_game_ticks(self):
        return (pygame.time.get_ticks() - self.timer_start)


class Booster:
    def __init__(self, booster_type, x, y, delay, duration):
        self.type = booster_type
        self.rect = pygame.Rect(x, y, BOOSTER_SIZE, BOOSTER_SIZE)
        self.delay = delay
        self.duration = duration
        self.created_time_delay = pygame.time.get_ticks()
        self.created_time_duration = float("inf")
        self.active = True
    
    def collide(self):
        self.active = False
        self.created_time_delay = pygame.time.get_ticks()
        self.created_time_duration = pygame.time.get_ticks()
    
    def check_delay(self): #returns true if there is no delay left
        if pygame.time.get_ticks() > self.created_time_delay + self.delay:
            return True
        return False
        
    def check_booster_duration(self): #returns true if buff ends
        if pygame.time.get_ticks() > self.created_time_duration + self.duration:
            return True
        return False
    

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, timer, booster_image, booster, y_bullet_colour, r_bullet_colour, y_cannon_active, r_cannon_active):
    WIN.blit(SPACE_IMAGE, (0,0))
    pygame.draw.rect(WIN, NAVY, BORDER) #Draw onto window, colour, what im drawing

    #text
    timer_text = TIMER_FONT.render(timer, 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(f"Health: {yellow_health}", 1, WHITE)
    red_health_text = HEALTH_FONT.render(f"Health: {red_health}", 1, WHITE)
    WIN.blit(timer_text, (WIDTH//2 - timer_text.get_width()//2, 5))
    WIN.blit(yellow_health_text, (10, 10))
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    if booster is not None and booster.active:
        WIN.blit(booster_image, (booster.rect.x, booster.rect.y))
    
    for bullet in yellow_bullets:
            if y_cannon_active:
                WIN.blit(CANNON_BALL, (bullet.x, bullet.y))
            else:
                pygame.draw.rect(WIN, y_bullet_colour, bullet)

    for bullet in red_bullets:
        if r_cannon_active:
            WIN.blit(CANNON_BALL, (bullet.x, bullet.y))
        else:
            pygame.draw.rect(WIN, r_bullet_colour, bullet)
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow, y_velocity):
    if keys_pressed[pygame.K_a] and yellow.x - y_velocity > 0: #LEFT
        yellow.x -= y_velocity
    if keys_pressed[pygame.K_d] and yellow.x + y_velocity + yellow.width < BORDER.x: #RIGHT
        yellow.x += y_velocity
    if keys_pressed[pygame.K_w] and yellow.y - y_velocity > 0: #UP
        yellow.y -= y_velocity
    if keys_pressed[pygame.K_s] and yellow.y + y_velocity + yellow.height < HEIGHT: #DOWN
        yellow.y += y_velocity


def red_handle_movement(keys_pressed, red, r_velocity):
    if keys_pressed[pygame.K_LEFT] and red.x - r_velocity > BORDER.x + 10: #LEFT
        red.x -= r_velocity
    if keys_pressed[pygame.K_RIGHT] and red.x + r_velocity + red.width < WIDTH: #RIGHT
        red.x += r_velocity
    if keys_pressed[pygame.K_UP] and red.y - r_velocity > 0: #UP
        red.y -= r_velocity
    if keys_pressed[pygame.K_DOWN] and red.y + r_velocity + red.height < HEIGHT: #DOWN
        red.y += r_velocity


def handle_bullets(yellow_bullets, red_bullets, yellow, red, y_bullet_velocity, r_bullet_velocity, y_bullet_boost, r_bullet_boost):
    for bullet in yellow_bullets:
        bullet.x += y_bullet_velocity
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
            del y_bullet_boost[:1]
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)
            del y_bullet_boost[:1]

    for bullet in red_bullets:
        bullet.x -= r_bullet_velocity
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(RESTART_PAUSE)


def main():
    # Initilize yellow hitbox and other props
    yellow = pygame.Rect(100, HEIGHT//2, SPACESHIP_X_LENGTH, SPACESHIP_Y_LENGTH) #Initialize Postion (coordinates, size)
    yellow_bullets = []
    y_bullet_boost = []
    yellow_health = YELLOW_HEALTH
    # Initilize red hitbox and other props
    red = pygame.Rect(WIDTH-100, HEIGHT//2, SPACESHIP_X_LENGTH, SPACESHIP_Y_LENGTH) #Initialize Postion
    red_bullets = []
    r_bullet_boost = []
    red_health = RED_HEALTH

    BG_SOUND.play(-1)
    clock = pygame.time.Clock()
    game = CurrentClock()
    
    #initialize empty variables to for default values before boost
    booster = None #before booster object is initialized
    booster_image = None
    y_active_boosters, r_active_boosters = [], [] 
    y_fire_sound, r_fire_sound = BULLET_FIRE_SOUND, BULLET_FIRE_SOUND
    y_max_bullets, r_max_bullets = MAX_BULLETS, MAX_BULLETS
    y_bullet_length, y_bullet_width, r_bullet_length, r_bullet_width = BULLET_LENGTH, BULLET_WIDTH, BULLET_LENGTH, BULLET_WIDTH
    y_bullet_damage, r_bullet_damage = BULLET_DAMAGE, BULLET_DAMAGE
    y_bullet_velocity, r_bullet_velocity = BULLET_VEL, BULLET_VEL
    y_bullet_colour, r_bullet_colour = "YELLOW", "RED"
    y_velocity, r_velocity = VELOCITY, VELOCITY


    run = True
    while run:
        clock.tick(FPS)
        timer = str(round(game.current_game_ticks()/1000, 1))

        # Create a booster object @ booster_delay intervals
        if booster is None or (not booster.active and booster.check_delay()): 
            if game.current_game_ticks() < BOOSTER_INITIAL:
                pass
            else:
                booster_y = random.choice(range(HEIGHT - BOOSTER_SIZE))
                booster_type = random.choice(BOOSTER_TYPES)
                # initialize object, with .active to be true
                booster = Booster(booster_type, WIDTH//2 - BOOSTER_SIZE//2, booster_y, BOOSTER_DELAY, BOOSTER_DURATION)
                booster_image = BOOSTER_LIST[booster.type]

        # YELLOW booster implementation, create event on collision
        if booster is not None:
            if booster.active and yellow.colliderect(booster.rect):
                y_active_boosters.append(booster)
                UPGRADE.play()
                if booster.type == "heart":
                    pygame.event.post(pygame.event.Event(Y_BOOSTER_HEART))
                if booster.type == "rocket":
                    pygame.event.post(pygame.event.Event(Y_BOOSTER_ROCKET))
                if booster.type == "sniper":
                    pygame.event.post(pygame.event.Event(Y_BOOSTER_SNIPER))
                if booster.type == "cannon":
                    pygame.event.post(pygame.event.Event(Y_BOOSTER_CANNON))
                if booster.type == "sonic":
                    pygame.event.post(pygame.event.Event(Y_BOOSTER_SONIC))
                booster.collide()
        
            
        # YELLOW BOOSTER DURATION CHECKER, FOR EACH BOOSTER
        for buff in y_active_boosters:
            if buff.check_booster_duration():
                y_active_boosters.remove(buff)
                #list comprehension, first boost is output, second one is iterating y_active_boosters, boost.type is refering to index of y_active_boosters
                if len([boost for boost in y_active_boosters if boost.type == buff.type]) == 0:
                    only_buff = True
                else:
                    only_buff = False
                
                if buff.type == "rocket":
                    y_bullet_damage = BULLET_DAMAGE
                    y_bullet_colour = "YELLOW"
                    cannon_active = any(boost.type == "cannon" for boost in y_active_boosters)
                    if cannon_active:
                        pass
                    else:
                        y_bullet_width, y_bullet_length = BULLET_WIDTH, BULLET_LENGTH                     
                
                elif buff.type == "sniper" and only_buff:
                    cannon_active = any(boost.type == "cannon" for boost in y_active_boosters)
                    if cannon_active:
                        y_fire_sound = CANNON_SOUND
                    else:
                        y_fire_sound = BULLET_FIRE_SOUND
                    y_bullet_velocity = BULLET_VEL
                    y_fire_sound = BULLET_FIRE_SOUND
                    y_max_bullets = MAX_BULLETS
                
                elif buff.type == "cannon" and only_buff:
                    sniper_active = any(boost.type == "sniper" for boost in y_active_boosters)
                    if sniper_active:
                        y_fire_sound = SNIPER_SOUND
                    else:
                        y_fire_sound = BULLET_FIRE_SOUND

                    rocket_active = any(boost.type == "rocket" for boost in y_active_boosters)
                    if rocket_active:
                        y_bullet_width, y_bullet_length = ROCKET_WIDTH, ROCKET_LENGTH
                    else:
                        y_bullet_width, y_bullet_length = BULLET_WIDTH, BULLET_LENGTH
                
                elif buff.type == "sonic" and only_buff:
                    y_velocity = VELOCITY
        
        # RED booster implementation, create event on collision
        if booster is not None:
            if booster.active and red.colliderect(booster.rect):
                r_active_boosters.append(booster)
                UPGRADE.play()
                if booster.type == "heart":
                    pygame.event.post(pygame.event.Event(R_BOOSTER_HEART))
                if booster.type == "rocket":
                    pygame.event.post(pygame.event.Event(R_BOOSTER_ROCKET))
                if booster.type == "sniper":
                    pygame.event.post(pygame.event.Event(R_BOOSTER_SNIPER))
                if booster.type == "cannon":
                    pygame.event.post(pygame.event.Event(R_BOOSTER_CANNON))
                if booster.type == "sonic":
                    pygame.event.post(pygame.event.Event(R_BOOSTER_SONIC))
                booster.collide()

        # YELLOW BOOSTER DURATION CHECKER, FOR EACH BOOSTER
        for buff in r_active_boosters:
            if buff.check_booster_duration():
                r_active_boosters.remove(buff)
                #list comprehension, first boost is output, second one is iterating r_active_boosters, boost.type is refering to index of r_active_boosters
                if len([boost for boost in r_active_boosters if boost.type == buff.type]) == 0:
                    only_buff = True
                else:
                    only_buff = False
                
                if buff.type == "rocket" and only_buff:
                    r_bullet_damage = BULLET_DAMAGE
                    r_bullet_colour = "YELLOW"
                    cannon_active = any(boost.type == "cannon" for boost in r_active_boosters)
                    if cannon_active:
                        pass
                    else:
                        r_bullet_width, r_bullet_length = BULLET_WIDTH, BULLET_LENGTH                     
                
                elif buff.type == "sniper" and only_buff:
                    cannon_active = any(boost.type == "cannon" for boost in r_active_boosters)
                    if cannon_active:
                        r_fire_sound = CANNON_SOUND
                    else:
                        r_fire_sound = BULLET_FIRE_SOUND
                    r_bullet_velocity = BULLET_VEL
                    r_fire_sound = BULLET_FIRE_SOUND
                    r_max_bullets = MAX_BULLETS
                
                elif buff.type == "cannon" and only_buff:
                    sniper_active = any(boost.type == "sniper" for boost in r_active_boosters)
                    if sniper_active:
                        r_fire_sound = SNIPER_SOUND
                    else:
                        r_fire_sound = BULLET_FIRE_SOUND

                    rocket_active = any(boost.type == "rocket" for boost in r_active_boosters)
                    if rocket_active:
                        r_bullet_width, r_bullet_length = ROCKET_WIDTH, ROCKET_LENGTH
                    else:
                        r_bullet_width, r_bullet_length = BULLET_WIDTH, BULLET_LENGTH
                
                elif buff.type == "sonic" and only_buff:
                    r_velocity = VELOCITY
        
        
        # Event Loop
        for event in pygame.event.get():
            # Exit when clicking x
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            # Create bullet on shift key stroke, limit max bullet on screen
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(yellow_bullets) < y_max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - y_bullet_width//2, y_bullet_length, y_bullet_width)
                    yellow_bullets.append(bullet)
                    y_fire_sound.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < r_max_bullets:
                    bullet = pygame.Rect(red.x, red.y + red.height//2 - r_bullet_width//2, r_bullet_length, r_bullet_width)
                    red_bullets.append(bullet)
                    r_fire_sound.play()
            
            
            # yellow booster event handler
            if event.type == Y_BOOSTER_HEART:
                yellow_health += BOOSTER_HEALTH
            elif event.type == Y_BOOSTER_ROCKET:
                y_bullet_damage = BOOSTER_ROCKET_DAMAGE
                y_bullet_colour = LIGHT_BLUE
                if y_cannon_active:
                    pass
                else:
                    y_bullet_width, y_bullet_length = ROCKET_WIDTH, ROCKET_LENGTH
            elif event.type == Y_BOOSTER_SNIPER:
                y_bullet_velocity = BOOSTER_SNIPER_VEL
                y_fire_sound = SNIPER_SOUND
                y_max_bullets = SNIPER_MAX_BULLETS
            elif event.type == Y_BOOSTER_CANNON:
                y_bullet_width, y_bullet_length = BOOSTER_CANNON_SIZE, BOOSTER_CANNON_SIZE
                y_fire_sound = CANNON_SOUND
            elif event.type == Y_BOOSTER_SONIC:
                y_velocity = BOOSTER_SONIC_VEL


            # red booster event handler
            if event.type == R_BOOSTER_HEART:
                red_health += BOOSTER_HEALTH
            elif event.type == R_BOOSTER_ROCKET:
                r_bullet_damage = BOOSTER_ROCKET_DAMAGE
                r_bullet_colour = LIGHT_BLUE
                if r_cannon_active:
                    pass
                else:
                    r_bullet_width, r_bullet_length = ROCKET_WIDTH, ROCKET_LENGTH
            elif event.type == R_BOOSTER_SNIPER:
                r_bullet_velocity = BOOSTER_SNIPER_VEL
                r_fire_sound = SNIPER_SOUND
                r_max_bullets = SNIPER_MAX_BULLETS
            elif event.type == R_BOOSTER_CANNON:
                r_bullet_width, r_bullet_length = BOOSTER_CANNON_SIZE, BOOSTER_CANNON_SIZE
                r_fire_sound = CANNON_SOUND
            elif event.type == R_BOOSTER_SONIC:
                r_velocity = BOOSTER_SONIC_VEL

            #Hit Event
            if event.type == YELLOW_HIT:
                yellow_health -= r_bullet_damage
                BULLET_HIT_SOUND.play()

            if event.type == RED_HIT:
                red_health -= y_bullet_damage
                BULLET_HIT_SOUND.play()

            # Winner Text and checker
            winner_text = ""
            if yellow_health <= 0:
                winner_text = "RED WINS!"
            
            if red_health <= 0:
                winner_text = "YELLOW WINS!"

            if winner_text != "":
                draw_winner(winner_text)
                BG_SOUND.stop()
                run = False

        y_cannon_active = any(boost.type == "cannon" for boost in y_active_boosters)
        r_cannon_active = any(boost.type == "cannon" for boost in r_active_boosters)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow, y_velocity)
        red_handle_movement(keys_pressed, red, r_velocity)
        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health, timer, booster_image, booster, y_bullet_colour, r_bullet_colour, y_cannon_active, r_cannon_active)
        handle_bullets(yellow_bullets, red_bullets, yellow, red, y_bullet_velocity, r_bullet_velocity, y_bullet_boost, r_bullet_boost)
            
    main()

if __name__ == "__main__":
    main()