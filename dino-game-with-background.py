import pygame as pg
import sys
import random

pg.init()
width = 800
height = 600

jump_goal = 200
jumping = False
speed = 2

player_width = 44
player_height = 47
main_player_pos = [200, 400]
player_pos = [main_player_pos[0], main_player_pos[1]]


cactus_width = 30
cactus_height = 50
cactus_pos = [700, 400]
cactus_list = [cactus_pos]



screen = pg.display.set_mode((width, height))
game_over = False

white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)


on_left_dino_foot = False
left_dino_foot = pg.image.load('left-foot-down-dino.png')
right_dino_foot = pg.image.load('right-foot-down-dino.png')

def gravity(player_position):
    if not jumping and player_position[1] < main_player_pos[1]:
      player_position[1] += speed

def jump(player_position):
    if player_position[1] > jump_goal:
      player_position[1] -= speed

def make_cactuses(list_of_cactuses):
    delay = random.random()
    if len(cactus_list) <= 2 and delay < .09:
      x_pos = cactus_pos[0]
      y_pos = cactus_pos[1]
      
      list_of_cactuses.append([x_pos, y_pos])
      
def draw_cactuses(list_of_cactuses):
    for enemy_pos in list_of_cactuses:
        pg.draw.rect(screen, green, (enemy_pos[0], enemy_pos[1], cactus_width, cactus_height))
    
def update_cactus_positions(list_cactuses):
    for idx, cactus_position in enumerate(cactus_list):
      if cactus_position[0] < 0:
         cactus_position[0] += speed
      
      else:
         list_cactuses.pop(idx)
    


while not game_over:
   keys = pg.key.get_pressed()
   for event in pg.event.get():
      if event.type == pg.QUIT:
         pg.quit()
         sys.exit()
         game_over = True
    
    
   if keys[pg.K_UP] or keys[pg.K_SPACE]:
      if player_pos[1] == main_player_pos[1]:
         jumping = True
         jump(player_pos)
    
   if keys[pg.K_DOWN]:
      pass # Passing for now, I haven't yet put in the feature where you can duck.
   
   if keys[pg.K_RIGHT]:
      player_pos[0] += 2
      
   if jumping and player_pos[1] > jump_goal:
      jump(player_pos)
      
   if player_pos[1] <= jump_goal:
      jumping = False
      
   
   gravity(player_pos)
   screen.fill(white)
   make_cactuses(cactus_list)
   update_cactus_positions(cactus_list)
   pg.draw.rect(screen, red, (player_pos[0], player_pos[1], player_width, player_height))
   draw_cactuses(cactus_list)
   pg.display.update()


