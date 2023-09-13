import pygame
import os

successes, failures = pygame.init()
if failures:
  print(f"Something wrong, which are {failures}")
else:
  print(f"Successfully initiated pygame {successes}")

HEALTH_FONT = pygame.font.SysFont("comicsans", 40)
WINNER_FONT = pygame.font.SysFont("comicsans", 100)

WIDTH, HEIGHT = 1000, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zenbort")
WHITE = (255, 255, 255)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50
YELLOW_SPACESHIP_ORIG = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_ORIG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_ORIG = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_ORIG, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

BORDER = pygame.Rect((WIDTH/2) - 20, 0, 10, HEIGHT)
BLACK = (0, 0, 0)

BULLET_WIDTH, BULLET_HEIGHT = 6, 4
BULLET_VEL = 10
BULLET_MAX = 7
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'arcade explosion.mp3'))
BULLET_SHOOT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'm4a1s.mp3'))


RED = (255, 0, 0)
YELLOW = (255, 255, 0)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
  WIN.blit(SPACE, (0, 0))
  yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
  red_health_text = HEALTH_FONT.render("Health " + str(red_health), 1, WHITE)
  WIN.blit(yellow_health_text, (5, 5))
  WIN.blit(red_health_text, (WIDTH - yellow_health_text.get_width() - 5, 5))
  pygame.draw.rect(WIN, BLACK, BORDER)
  for bullet in yellow_bullets:
    pygame.draw.rect(WIN, YELLOW, bullet)
  for bullet in red_bullets:
    pygame.draw.rect(WIN, RED, bullet)
  WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
  WIN.blit(RED_SPACESHIP, (red.x, red.y))
  pygame.display.update()

VEL = 5

def movements(keys_pressed, yellow, red):
  if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:
    yellow.x -= VEL
  if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:
    yellow.y -= VEL
  if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:
    yellow.x += VEL
  if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:
    yellow.y += VEL  
  
  if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
    red.x -= VEL
  if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
    red.y -= VEL
  if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
    red.x += VEL
  if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:
    red.y += VEL

RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
  for bullet in yellow_bullets:
    bullet.x += BULLET_VEL
    if red.colliderect(bullet):
      yellow_bullets.remove(bullet)
      pygame.event.post(pygame.event.Event(RED_HIT))
    elif bullet.x > WIDTH:
      yellow_bullets.remove(bullet)
  
  for bullet in red_bullets:
    bullet.x -= BULLET_VEL
    if yellow.colliderect(bullet):
      red_bullets.remove(bullet)
      pygame.event.post(pygame.event.Event(YELLOW_HIT))
    elif bullet.x < 0:
      red_bullets.remove(bullet)
    
FPS = 60

def draw_winner(winner_text):
  text = WINNER_FONT.render(winner_text, 1, WHITE)
  WIN.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
  pygame.display.update()
  pygame.time.delay(5000)

def main():
  yellow_bullets, red_bullets = [], []  
  yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
  red = pygame.Rect(WIDTH - 100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
  yellow_health, red_health = 10, 10
  run = True
  clock = pygame.time.Clock()
  while run:
    clock.tick(FPS)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LCTRL and len(yellow_bullets) < BULLET_MAX:
          bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height/2 - BULLET_HEIGHT/2, BULLET_WIDTH, BULLET_HEIGHT)
          yellow_bullets.append(bullet)
          BULLET_SHOOT_SOUND.play()
        if event.key == pygame.K_RCTRL and len(red_bullets) < BULLET_MAX:
          bullet = pygame.Rect(red.x - BULLET_WIDTH, red.y + red.height/2 - BULLET_HEIGHT/2, BULLET_WIDTH, BULLET_HEIGHT)
          red_bullets.append(bullet)
          BULLET_SHOOT_SOUND.play()
      winner_text = ""
      if event.type == RED_HIT:
        red_health -= 1
        BULLET_HIT_SOUND.play()
        if red_health <= 0:
          winner_text = "Yellow Wins!"
      if event.type == YELLOW_HIT:
        yellow_health -= 1
        BULLET_HIT_SOUND.play()
        if yellow_health <= 0:
          winner_text = "Red Wins!"

      if winner_text != "":
        draw_winner(winner_text)
        run = False

    keys_pressed = pygame.key.get_pressed()
    handle_bullets(yellow_bullets, red_bullets, yellow, red)
    movements(keys_pressed, yellow, red)
    draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)
  main()

if __name__ == '__main__':
  main()