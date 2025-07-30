import pygame, sys, math, random

pygame.init()

screen = pygame.display.set_mode((1200,900))
clock = pygame.time.Clock()


font = pygame.font.Font(None,200)
score_font = pygame.font.Font(None, 75)
speed_font = pygame.font.Font(None, 50)


play_but = font.render("PLAY", False, 'red')
play_but.set_alpha(50)

shoot = pygame.mixer.Sound('sound/shotgun-firing-3-14483.wav')
gun_empty = pygame.mixer.Sound('sound/gun_empty.wav')
realoaded = pygame.mixer.Sound('sound/reloaded.mp3')
game_over = pygame.mixer.Sound('sound/game_over.wav')
gain_bullet = pygame.mixer.Sound('sound/gain_bullet.wav')
main_music = pygame.mixer.Sound('sound/music.wav')

main_music.set_volume(0.3)
main_music.play(-1)

const = 0

shot_timer = 0



class Camera_Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surf = pygame.display.get_surface()
        self.rumb_1 = pygame.math.Vector2(random.randint(0,40) , random.randint(0,40))
        self.nothing = pygame.math.Vector2(0,0)

    def rumble(self):
        self.rumb_1 = pygame.math.Vector2(random.randint(0,40) , random.randint(0,40))
        self.cancel = self.rumb_1 * - 1

        if shot_timer <= 20 and shot_timer >= 15:
            return self.rumb_1
        elif shot_timer <= 14 and shot_timer >= 9:
            return self.cancel
        else:
            return self.nothing

    def cstm_draw(self):

        global offset 
        offset = self.rumble()

        for sprites in self.sprites():
            if sprites.att == True and sprites.image != gun_sprite.image:
                offset_pos = sprites.rect.topleft + offset
                self.display_surf.blit(sprites.image, offset_pos)

        player_sprite.draw_eyes()
        screen.blit(gun_sprite.image, gun_sprite.rect.topleft + offset)
                

camera_group = Camera_Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.test = pygame.image.load('graphs/character_1.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.test,0,0.4)
        self.mask = pygame.mask.from_surface(self.image)

        self.pos = pygame.math.Vector2(600,200)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.point_list = []

        self.grav = 0
        self.game_active = False
        self.vel = pygame.math.Vector2(0,0)
        self.bull_count = 3
        self.score = 0
        self.att = True

            

    def gravity(self):

        #gravity
        self.grav += 0.0078
        self.vel.y += self.grav

        self.pos.y += self.vel.y

        # air resistence

        if self.vel.x > 0:
            self.vel.x -=0.009
        elif self.vel.x < 0:
            self.vel.x += 0.009

        self.pos.x += self.vel.x

        #linking gun
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))
        self.mask = pygame.mask.from_surface(self.image)
        gun_sprite.rect = gun_sprite.gun_surf.get_rect(center = (self.pos.x, self.pos.y))


    def border(self):

        if self.pos.x < -10:
            self.pos.x = 1250
        elif self.pos.x > 1300:
            self.pos.x = -5
        elif self.pos.y < 0:

            self.point_list = [(self.pos.x, 0), (self.pos.x - 50, 50), (self.pos.x + 50, 50)]
            pygame.draw.polygon(screen, 'lightblue', self.point_list)

    def game_over(self):
        if self.pos.y > 1100:
            self.game_active = False
            game_over.play()
            player_sprite.remove()

    def draw_eyes(self):


        self.eye_right_pos = pygame.math.Vector2((self.pos.x + 3, self.pos.y - 2))
        self.eye_left_pos = pygame.math.Vector2((self.pos.x - 27, self.pos.y - 2))
        mouse_x , mouse_y = pygame.mouse.get_pos() 
 
        y = (mouse_y - self.eye_right_pos.y ) 
        x = (mouse_x - self.eye_right_pos.x) 

        theta = (math.atan2(y , x))
        offset_lcl = pygame.math.Vector2((math.cos(theta)) * 3.5,(math.sin(theta))* 3.5)

        pygame.draw.circle(screen, ('black'), (self.eye_left_pos + offset_lcl + offset), 8)
        pygame.draw.circle(screen, ('black'), (self.eye_right_pos + offset_lcl + offset), 8)

    def update(self):
        self.gravity()
        self.game_over()
        self.border()

        self.mask = pygame.mask.from_surface(self.image)



player_sprite = Player(camera_group)


class Gun(pygame.sprite.Sprite):
    def __init__(self,group):
        super().__init__(group)
        self.gun_surf = pygame.image.load('graphs/shotgun_cropped.png').convert_alpha()
        self.pos = pygame.math.Vector2(player_sprite.pos.x - 10 , player_sprite.pos.y + 40)
        self.rect = self.gun_surf.get_rect(center = (self.pos.x, self.pos.y))
        self.magnitude = pygame.math.Vector2(0,0)
        self.mouse_coords = pygame.math.Vector2(0,0)
        
        self.mouse_x , self.mouse_y = pygame.mouse.get_pos()
        self.y_mag = self.mouse_y - self.pos.y 
        self.x_mag = self.mouse_x - self.pos.x

        self.angle_y = self.pos.y - self.mouse_y
        self.angle_x = self.mouse_x - self.pos.x
        self.theta = math.degrees(math.atan2(self.angle_y , self.angle_x))

        self.att = True

    def get_aim(self):
        # calculating angle
        self.pos = pygame.math.Vector2(player_sprite.pos.x - 10, player_sprite.pos.y + 40)

        self.mouse_x , self.mouse_y = pygame.mouse.get_pos()

        self.angle_y = self.pos.y - self.mouse_y
        self.angle_x = self.mouse_x - self.pos.x
 
        self.theta = math.degrees(math.atan2(self.angle_y , self.angle_x))

        return self.theta

    def aim(self):

        self.get_aim()

        # dynamically reassigning and updating gun_sprite position and rotation
        self.image = pygame.transform.rotozoom(self.gun_surf, self.theta, 0.3)
        self.rect = self.image.get_rect(center=(self.pos.x, self.pos.y))



    def get_mag(self):
        mouse_x , mouse_y = pygame.mouse.get_pos()

        self.y_mag = mouse_y - self.pos.y 
        self.x_mag = mouse_x - self.pos.x

        self.mouse_coords = pygame.math.Vector2(self.x_mag, self.y_mag)
        self.magnitude =  pygame.math.Vector2((self.mouse_coords * -1) * 0.06)

        return self.magnitude

    def shoot(self):

        player_sprite.vel = (0,0)
        player_sprite.grav = 0
        player_sprite.vel += self.magnitude


    def update(self):
        self.aim()
        

gun_sprite = Gun(camera_group)

#actual projectiles
class drawn_bullet(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.theta = gun_sprite.get_aim()
        self.surf_temp = pygame.image.load('graphs/projectile.png').convert_alpha() 
        self.pos = gun_sprite.pos.copy()
        self.rect = self.surf_temp.get_rect(center = (self.pos))
        self.att = False
        self.magnitude = gun_sprite.magnitude * -0.9

    def move(self):
        
        self.pos += gun_sprite.magnitude * -0.9
        self.image = pygame.transform.rotozoom(self.surf_temp, self.theta, 0.7)
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))
                
ejected_sprite = drawn_bullet(camera_group)
        

#actual projectiles

class drawn_bulls(pygame.sprite.Sprite):
    def __init__(self, rot, offset, group):
        super().__init__(group)
        self.rot = math.radians(rot)
        self.deg = gun_sprite.get_aim() + offset
        self.surf_temp = pygame.image.load('graphs/projectile.png').convert_alpha()
        self.i_hat = pygame.math.Vector2(math.cos(self.rot) , math.sin(self.rot))
        self.j_hat = pygame.math.Vector2(-math.sin(self.rot) , math.cos(self.rot))
        self.pos = gun_sprite.pos.copy()
        self.rect = self.surf_temp.get_rect(center = (self.pos))

        self.comp = pygame.math.Vector2(0,0)
        self.comp_2 = pygame.math.Vector2(0,0)

        self.att = False
        self.magnitude = gun_sprite.get_mag()

    def move(self):

        self.comp = self.i_hat * self.magnitude.x
        self.comp_2 = self.j_hat * self.magnitude.y

        self.magnitude_base = (self.comp + self.comp_2) 

        self.pos += self.magnitude_base
        self.image = pygame.transform.rotozoom(self.surf_temp, self.deg, 0.7)
        self.rect = self.image.get_rect(center = (self.pos.x, self.pos.y))

test_sprite = drawn_bulls(160, 20, camera_group)

test_sprite_1 = drawn_bulls(200, -20, camera_group)

# collecting bullets

class Collecting_Bullets(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.pos = pygame.math.Vector2(random.randint(100,1100), random.randint(100, 850))
        self.surf = pygame.image.load('graphs/coll_bull_cropped.png').convert_alpha()
        self.image = pygame.transform.rotozoom(self.surf, 0, 0.15)
        self.rect = self.image.get_rect(center = (self.pos))
        self.mask = pygame.mask.from_surface(self.image)
        self.att = True
        self.flag = True
        self.is_dead = False
    
    def collision(self):

        global player_sprite

        offset = (int(player_sprite.rect.left - self.rect.left), int(player_sprite.rect.top - self.rect.top))
        if self.mask.overlap(player_sprite.mask, offset):

            if self.flag == True:
                player_sprite.score += 1
                player_sprite.bull_count += 1

                self.flag = False
                self.kill()
                gain_bullet.play()
                self.is_dead = True

    def move(self):
        pass

    def update(self):

        self.move()
        self.collision()
        self.rect = self.image.get_rect(center = (self.pos))
        self.mask = pygame.mask.from_surface(self.image)

coll_bulls = Collecting_Bullets(camera_group)

class Coll_Bulls_Child(Collecting_Bullets):
    def __init__(self, groups):
        super().__init__(groups)

coll_bull_1 = Coll_Bulls_Child(camera_group)


# obstacles

class Obstacles(Collecting_Bullets):
    def __init__(self, groups):
        super().__init__(groups)
        self.temp = pygame.image.load('graphs/help.png').convert_alpha()
        self.i = 0

    def collision(self):

        global player_sprite

        offset = (int(player_sprite.rect.left - self.rect.left), int(player_sprite.rect.top - self.rect.top))
        if self.mask.overlap(player_sprite.mask, offset):

            if self.flag == True:

                self.flag = False
                self.kill()
                game_over.play()
                self.is_dead = True
                player_sprite.game_active = False

    def move(self):

        self.i += 1

        if self.pos.y >= 1000:
            self.pos = pygame.math.Vector2(random.randint(50,1100), random.randint(0, 100))

        self.pos.y +=1
        self.image = pygame.transform.rotozoom(self.temp, self.i, 0.4) 



obst_1 = Obstacles(camera_group)
obst_2 = Obstacles(camera_group)

def bull_refill():

    global coll_bulls
    global coll_bull_1

    if coll_bulls.is_dead == True and coll_bull_1.is_dead == True:
        coll_bulls = Collecting_Bullets(camera_group)
        coll_bull_1 = Coll_Bulls_Child(camera_group)

def obst_refill():

    global obst_1
    global obst_2

    if obst_1.is_dead == True:
        obst_1 = Obstacles(camera_group)
    elif obst_2.is_dead == True:
        obst_2 = Obstacles(camera_group)

def high_scores():

    with open("score.txt", "r") as file:
        content = file.read()

    if player_sprite.score > int(content):
        with open ("score.txt", "w") as file:
            file.write(str(player_sprite.score))

    high_score = score_font.render(f"All time high score:{content}", False, 'red')
    high_score.set_alpha(50)
    high_score_rect = high_score.get_rect(center = (600,550))

    current_sc = score_font.render(f"Current score:{player_sprite.score}", False, 'red')
    current_sc.set_alpha(50)
    current_sc_rect = current_sc.get_rect(center = (600, 300))

    screen.blit(high_score, high_score_rect)
    screen.blit(current_sc, current_sc_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()


        if player_sprite.game_active == True:
            if event.type == pygame.MOUSEBUTTONDOWN and player_sprite.bull_count > 0 and shot_timer == 0:
                player_sprite.bull_count -= 1

                gun_sprite.shoot() 
                shoot.play() # sound effect

                shot_timer = 20
                ejected_sprite.att = True
                test_sprite.att = True
                test_sprite_1.att = True

            elif event.type == pygame.MOUSEBUTTONDOWN and player_sprite.bull_count == 0:
                gun_empty.play()

    if player_sprite.game_active == True:

        bull = score_font.render(str(player_sprite.bull_count), False, 'red')
        bull.set_alpha(50)
        bull_rect = bull.get_rect(center = (380,850) )

        bull_count = score_font.render("Ammo count:", False, 'red')
        bull_count.set_alpha(50)
        bull_count_rect = bull_count.get_rect(center = (180, 850))

        current_sc_str = score_font.render("Current Score", False, 'red')
        current_sc_str.set_alpha(50)
        current_sc_str_rect = current_sc_str.get_rect(center = (600, 320))

        current_sc = font.render(f"{player_sprite.score}", False, 'red')
        current_sc.set_alpha(50)
        current_sc_rect = current_sc.get_rect(center = (600,  400))

        screen.fill('grey')

        screen.blit(current_sc, current_sc_rect)
        screen.blit(bull, bull_rect)
        screen.blit(current_sc_str, current_sc_str_rect)
        screen.blit(bull_count, bull_count_rect)

        if shot_timer > 0:
            shot_timer-= 1
            ejected_sprite.move()
            test_sprite.move()#
            test_sprite_1.move()
        else:
            ejected_sprite.kill()
            ejected_sprite = drawn_bullet(camera_group)
            
            test_sprite.kill()
            test_sprite = drawn_bulls(160, 20, camera_group)
            
            test_sprite_1.kill()
            test_sprite_1 = drawn_bulls(200, -20, camera_group)

        player_sprite.update()
        gun_sprite.update()
        coll_bulls.update()
        coll_bull_1.update()

        obst_1.update()
        obst_2.update()
    
        bull_refill()
        obst_refill()

        camera_group.cstm_draw()

        pygame.display.flip()
        clock.tick(60)

    else:

        const += 0.05
        if const >= 12.5:
            const = 0 

        y = math.sin(const) * 10

        screen.fill('grey')
        play_but_rect = play_but.get_rect(center = (600, 430 + y))

        screen.blit(play_but, play_but_rect)
        high_scores()


        if play_but_rect.collidepoint(pygame.mouse.get_pos()) == True and event.type == pygame.MOUSEBUTTONDOWN:

            realoaded.play()
            player_sprite.kill()
            player_sprite = Player(camera_group) # Reset player_sprite instance

            obst_1.pos = pygame.math.Vector2(random.randint(50,1100), random.randint(0, 100))
            obst_2.pos = pygame.math.Vector2(random.randint(50,1100), random.randint(0, 100))


            coll_bulls.kill()
            coll_bull_1.kill()
            coll_bulls = Collecting_Bullets(camera_group)
            coll_bull_1 = Coll_Bulls_Child(camera_group)

            player_sprite.game_active = True 
   
        pygame.display.flip()
        clock.tick(60)
