import pygame as pg
import sys
import random
import os
from pygame.transform import scale

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
   game_over = True
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

main_dir = os.path.dirname(os.path.abspath(__file__))

DIR_UP = 1
DIR_DOWN = 2
DIR_LEFT = 3
DIR_RIGHT = 4

zoom_factor = 8


def draw_arrow(surf, color, posn, direction):
    x, y = posn
    if direction == DIR_UP:
        pointlist = ((x - 29, y + 30), (x + 30, y + 30), (x + 1, y - 29), (x, y - 29))
    elif direction == DIR_DOWN:
        pointlist = ((x - 29, y - 29), (x + 30, y - 29), (x + 1, y + 30), (x, y + 30))
    elif direction == DIR_LEFT:
        pointlist = ((x + 30, y - 29), (x + 30, y + 30), (x - 29, y + 1), (x - 29, y))
    else:
        pointlist = ((x - 29, y - 29), (x - 29, y + 30), (x + 30, y + 1), (x + 30, y))
    pg.draw.polygon(surf, color, pointlist)


def add_arrow_button(screen, regions, posn, direction):
    draw_arrow(screen, pg.Color("black"), posn, direction)
    draw_arrow(regions, (direction, 0, 0), posn, direction)


def scroll_view(screen, image, direction, view_rect):
    src_rect = None
    zoom_view_rect = screen.get_clip()
    image_w, image_h = image.get_size()
    if direction == DIR_UP:
        if view_rect.top > 0:
            screen.scroll(dy=zoom_factor)
            view_rect.move_ip(0, -1)
            src_rect = view_rect.copy()
            src_rect.h = 1
            dst_rect = zoom_view_rect.copy()
            dst_rect.h = zoom_factor
    elif direction == DIR_DOWN:
        if view_rect.bottom < image_h:
            screen.scroll(dy=-zoom_factor)
            view_rect.move_ip(0, 1)
            src_rect = view_rect.copy()
            src_rect.h = 1
            src_rect.bottom = view_rect.bottom
            dst_rect = zoom_view_rect.copy()
            dst_rect.h = zoom_factor
            dst_rect.bottom = zoom_view_rect.bottom
    elif direction == DIR_LEFT:
        if view_rect.left > 0:
            screen.scroll(dx=zoom_factor)
            view_rect.move_ip(-1, 0)
            src_rect = view_rect.copy()
            src_rect.w = 1
            dst_rect = zoom_view_rect.copy()
            dst_rect.w = zoom_factor
    elif direction == DIR_RIGHT:
        if view_rect.right < image_w:
            screen.scroll(dx=-zoom_factor)
            view_rect.move_ip(1, 0)
            src_rect = view_rect.copy()
            src_rect.w = 1
            src_rect.right = view_rect.right
            dst_rect = zoom_view_rect.copy()
            dst_rect.w = zoom_factor
            dst_rect.right = zoom_view_rect.right
    if src_rect is not None:
        scale(image.subsurface(src_rect), dst_rect.size, screen.subsurface(dst_rect))
        pg.display.update(zoom_view_rect)


def main(image_file=None):
    if image_file is None:
        image_file = os.path.join(main_dir, "data", "desert.jpg")
    margin = 80
    view_size = (30, 20)
    zoom_view_size = (view_size[0] * zoom_factor, view_size[1] * zoom_factor)
    win_size = (zoom_view_size[0] + 2 * margin, zoom_view_size[1] + 2 * margin)
    background_color = pg.Color("beige")

    pg.init()

    # set up key repeating so we can hold down the key to scroll.
    old_k_delay, old_k_interval = pg.key.get_repeat()
    pg.key.set_repeat(500, 30)

    try:
        screen = pg.display.set_mode(win_size)
        screen.fill(background_color)
        pg.display.flip()

        image = pg.image.load(image_file).convert()
        image_w, image_h = image.get_size()

        if image_w < view_size[0] or image_h < view_size[1]:
            print("The source image is too small for this example.")
            print("A %i by %i or larger image is required." % zoom_view_size)
            return

        regions = pg.Surface(win_size, 0, 24)
        add_arrow_button(screen, regions, (40, win_size[1] // 2), DIR_LEFT)
        add_arrow_button(
            screen, regions, (win_size[0] - 40, win_size[1] // 2), DIR_RIGHT
        )
        add_arrow_button(screen, regions, (win_size[0] // 2, 40), DIR_UP)
        add_arrow_button(
            screen, regions, (win_size[0] // 2, win_size[1] - 40), DIR_DOWN
        )
        pg.display.flip()

        screen.set_clip((margin, margin, zoom_view_size[0], zoom_view_size[1]))

        view_rect = pg.Rect(0, 0, view_size[0], view_size[1])

        scale(
            image.subsurface(view_rect),
            zoom_view_size,
            screen.subsurface(screen.get_clip()),
        )
        pg.display.flip()

        # the direction we will scroll in.
        direction = None

        clock = pg.time.Clock()
        clock.tick()

        going = True
        while going:
            # wait for events before doing anything.
            # events = [pg.event.wait()] + pg.event.get()
            events = pg.event.get()

            for e in events:
                if e.type == pg.KEYDOWN:
                    if e.key == pg.K_ESCAPE:
                        going = False
                    elif e.key == pg.K_DOWN:
                        scroll_view(screen, image, DIR_DOWN, view_rect)
                    elif e.key == pg.K_UP:
                        scroll_view(screen, image, DIR_UP, view_rect)
                    elif e.key == pg.K_LEFT:
                        scroll_view(screen, image, DIR_LEFT, view_rect)
                    elif e.key == pg.K_RIGHT:
                        scroll_view(screen, image, DIR_RIGHT, view_rect)
                elif e.type == pg.QUIT:
                    going = False
                elif e.type == pg.MOUSEBUTTONDOWN:
                    direction = regions.get_at(e.pos)[0]
                elif e.type == pg.MOUSEBUTTONUP:
                    direction = None

            if direction:
                scroll_view(screen, image, direction, view_rect)
            clock.tick(30)

    finally:
        pg.key.set_repeat(old_k_delay, old_k_interval)
        pg.quit()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        image_file = sys.argv[1]
    else:
        image_file = None
    main(image_file)
