import pygame
import math
import time
from game_important import scale_image, blit_rotate_center, control_of_player1, control_of_player2, blit_text_center

pygame.init()
pygame.font.init()

FINISH = pygame.image.load('imgs/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
RED_CAR = scale_image(pygame.image.load('imgs/red-car.png'), 0.5)
GREEN_CAR = scale_image(pygame.image.load('imgs/green-car.png'), 0.5)
WHITE_CAR = scale_image(pygame.image.load('imgs/white-car.png'), 0.5)
TRACK_BORDER = scale_image(pygame.image.load('imgs/track-border1.png'), 0.9)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)
TRACK = scale_image(pygame.image.load('imgs/track1.png'),0.9)
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
MAIN_FONT = pygame.font.SysFont("comicsans", 30)

def main():
    pygame.display.set_caption("racing game")
    
    images = [ (TRACK, (0, 0)), (FINISH, (224, 785)), (TRACK_BORDER, (0, 0))]
    running = True
    player_car1 = Player_car1(8, 4)
    player_car2 = Player_car2(8, 4)
    computer_car = Computer_car(1, 2, PATH)
    game_info = Game_imfo()
    FPS = 60
    clock = pygame.time.Clock()



    while running:
        clock.tick(FPS)
    
        draw(WIN, images, player_car1, player_car2, computer_car, game_info)    


        while not game_info.started:
            blit_text_center(WIN, MAIN_FONT, f'press any key to start the level {game_info.level}')
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    game_info.start_level()        

        for event in pygame.event.get():
            if event.type== pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                computer_car.path.append(pos)
            if event.type == pygame.QUIT:
                running = False

        control_of_player1(player_car1)
        control_of_player2(player_car2)
        computer_car.move()

        handle_collision(player_car1, player_car2, computer_car, game_info)


class AbstractCar:
    def __init__(self, max_vel, resolution_vel):
        self.vel = 0
        self.max_vel = max_vel
        self.angle = 270
        self.resolution_vel = resolution_vel
        self.img = self.IMG
        self.x , self.y = self.START_POS
        self.accelaration = 0.2

    def rotate(self, left=False, right = False):
        if left:
            self.angle += self.resolution_vel
        elif right:
            self.angle -= self.resolution_vel

    def draw(self, win):
        blit_rotate_center(win, self.img,(self.x,self.y) , self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.accelaration, self.max_vel)
        self.move()

    def move_backword(self):
        self.vel = max(self.vel - self.accelaration, -self.max_vel/2)
        self.move()

    def move(self):
        theta = math.radians(self.angle)
        vertical = math.cos(theta) * self.vel
        horizontal = math.sin(theta) * self.vel
        
        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        self.vel = max(self.vel -self.accelaration /2 , 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        point_of_intersection = mask.overlap(car_mask, offset)
        return point_of_intersection
    
    def reset(self):
        self.vel = 0
        self.angle = 270
        self.x , self.y = self.START_POS

    def bounce(self):
        self.vel = -self.vel/2
        self.move()

class Player_car1(AbstractCar):
    IMG = RED_CAR
    START_POS = (260, 797)

class Player_car2(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (260, 826)


PATH =[(369, 800), (1337, 800), (1420, 763), (1329, 690), (891, 703), (561, 356), (579, 226), (724, 213), (1027, 501), (1369, 517), (1473, 324), (1212, 77), (841, 73), (331, 72), (172, 170), (65, 313), (71, 738), (173, 812), (230, 820)]
class Computer_car(AbstractCar):
    IMG = WHITE_CAR
    START_POS = (300, 809)

    def __init__(self, max_vel, rotation_vel, path=[]):
        super().__init__(max_vel, rotation_vel)
        self.path = path
        self.current_point = 0
        self.vel = max_vel
    
    def draw_point(self, win):
        for point in self.path:
            pygame.draw.circle(win, (0,255,0) , point, 5)

    def draw(self, win):
        super().draw(win)
        self.draw_point(win)

    def move(self):
        if self.current_point >= len(self.path):
            return          

        self.calculate_angle()
        self.update_path_point()
        super().move()

    def calculate_angle(self):
        target_x , target_y = self.path[self.current_point]
        x_deff = target_x - self.x
        y_deff = target_y - self.y

        if y_deff == 0:
            need_angle = math.pi /2
        else:
            need_angle = math.atan(x_deff/y_deff)
        if target_y > self.y:
            need_angle += math.pi


        defference_in_angle = self.angle - math.degrees(need_angle)
        if defference_in_angle >=180:
            defference_in_angle -= 360
        
        if defference_in_angle >0:
            self.angle -= min(self.resolution_vel, abs(defference_in_angle))
        else:
            self.angle += min(self.resolution_vel, abs(defference_in_angle))

    def update_path_point(self):
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        
        if rect.collidepoint(*target):
            self.current_point +=1

    def reset(self):
        self.vel = 0
        self.angle = 270
        self.x , self.y = self.START_POS
        self.current_point = 0
    
    def next_level(self, level):
        self.reset()
        self.vel = self.max_vel + ((level-1)*0.4)
        self.resolution_vel = self.resolution_vel+ 0.4


class Game_imfo:
    LEVELS = 8

    def __init__(self, level =1):
        self.level = level
        self.started = False
        self.level_start_time = 0

    def next_level(self):
        self.level += 1
        started = False

    def reset(self):
        self.level = 1
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        self.level > self.LEVELS

    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def game_level_time(self):
        if not self.started:
            return 0 
        return  time.time() - self.level_start_time
    
def handle_collision(player_car1, player_car2, computer_car, game_info):
    if player_car1.collide(TRACK_BORDER_MASK) != None:
        player_car1.bounce()

    if player_car2.collide(TRACK_BORDER_MASK) != None:
        player_car2.bounce()


    finish_collide_poi0 = player_car1.collide(FINISH_MASK, 224, 785)
    if finish_collide_poi0 != None:
        if finish_collide_poi0[0] == 19:
            player_car1.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, f'player 1 wins')
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.next_level()
            player_car1.reset()
            player_car2.reset()
            computer_car.next_level(game_info.level)
            
    finish_collide_poi1 = player_car2.collide(FINISH_MASK, 224, 785)
    if finish_collide_poi1 != None:
        if finish_collide_poi1[0]==19:
            player_car2.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, f'player 2 wins')
            pygame.display.update()
            pygame.time.wait(5000)
            game_info.next_level()
            player_car1.reset()
            player_car2.reset()
            computer_car.next_level(game_info.level)
            
    finish_collide_poi2 = computer_car.collide(FINISH_MASK, 224, 785)
    if finish_collide_poi2 != None:
        if finish_collide_poi2[0]== 19:
            computer_car.bounce()
        else:
            blit_text_center(WIN, MAIN_FONT, f'You Lost!!')
            pygame.display.update()
            pygame.time.wait(5000)

            player_car1.reset()
            player_car2.reset()
            computer_car.reset()
            


def draw(win, images, player_car1, player_car2, computer_car, game_info):
    for img, pos in images:
        win.blit(img, pos)

    level_text = MAIN_FONT.render(f'level - {game_info.level}', 1, (255, 255, 255))
    win.blit(level_text, (10, win.get_height() - 100))
    time_text = MAIN_FONT.render(f'time - {round(game_info.game_level_time(), 1)}', 1,(255, 255, 255))
    win.blit(time_text, (10, win.get_height() - 70))
    player1_vel_text = MAIN_FONT.render(f'player 1 -vel {round(player_car1.vel,1)}', 1, (255,255,255))
    win.blit(player1_vel_text, (10, win.get_height() - 50))
    player2_vel_text = MAIN_FONT.render(f'player 1 -vel {round(player_car2.vel, 1)}', 1, (255,255,255))
    win.blit(player2_vel_text, (500, win.get_height() - 50))
    
    player_car1.draw(win)
    player_car2.draw(win)
    computer_car.draw(win)
    pygame.display.update()

if __name__=="__main__": 
    main()

pygame.quit()