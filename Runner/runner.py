import pygame
from sys import exit
from random import randint, choice


class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Runner/graphics/player/player_walk_1.png').convert_alpha()
        player_walk2 = pygame.image.load('Runner/graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_jump = pygame.image.load('Runner/graphics/player/jump.png').convert_alpha()
        self.player_index = 0
        
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        self.jumping = False

        self.jump_sound = pygame.mixer.Sound('Runner/audio/jump.mp3')
        self.jump_sound.set_volume(0.03)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()

        if type == 'fly':
            fly_frame1 = pygame.image.load('Runner/graphics/fly/fly1.png').convert_alpha()
            fly_frame2 = pygame.image.load('Runner/graphics/fly/fly2.png').convert_alpha()
            self.frames = [fly_frame1, fly_frame2]
            y_pos = 210
        else: 
            snail_frame1 = pygame.image.load('Runner/graphics/snail/snail1.png').convert_alpha()
            snail_frame2 = pygame.image.load('Runner/graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_frame1, snail_frame2]
            y_pos = 300

        self.passed = False
        self.animation_index = 0     
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()
        if self.rect.right < 0:
            self.kill()
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    global score_surf, score_rect, time_rect, hs_surf, hs_rect

    curr_time = (pygame.time.get_ticks() / 1000) - start_time
    time_surf = test_font.render(str(round(curr_time, 2)), True, 'White')
    time_rect = time_surf.get_rect(center=(750, 370))
    screen.blit(time_surf, time_rect)

    score_surf = test_font.render(str(score), False, 'Green')
    score_rect = score_surf.get_rect(center=(200, 100))
    hs_surf = test_font.render('High Score:' + str(high_score), False, 'Light Blue')
    hs_rect = hs_surf.get_rect(center=(600, 100))
    return

def reset_game():
    global obs_group, test_font, obs_list, game_active, score, start_time, high_score, curr_time, score_rect, hs_rect
    game_active = True
    if score > high_score:
        high_score =  score
        
    score = 0
    score_surf = test_font.render(str(score), False, 'Green')
    score_rect = score_surf.get_rect(center=(200, 100))
    hs_surf = test_font.render('High Score: ' + str(high_score), False, 'Light Blue')
    hs_rect = hs_surf.get_rect(center=(600, 100))
    start_time = pygame.time.get_ticks() / 1000
    obs_group.empty() 
    obs_list.clear()
    obs_group.empty()

    return

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obs_group, False):
        obs_group.empty()
        return False
    else:
        return True
        
pygame.init()

# basic
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption('Runner')
clock = pygame.time.Clock()
test_font = pygame.font.Font('Runner/font/Pixeltype.ttf', 50)

# constants
game_active = True
pass_snail = False
start_game = False
score = 0
high_score = 0
curr_time = 0
start_time = 0
obs_list = []

# groups
player = pygame.sprite.GroupSingle()
player.add(Player())
obs_group = pygame.sprite.Group()

# timer
obs_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obs_timer, 1500)

# sound
music = pygame.mixer.Sound('Runner/audio/music.wav')
music.set_volume(0.01)
music.play(loops=-1)


# surfaces
sky_surf = pygame.image.load('Runner/graphics/Sky.png').convert()
ground_surf = pygame.image.load('Runner/graphics/ground.png').convert()

text_surf = test_font.render('  Runner ', False, 'Dark Green')
text_rect = text_surf.get_rect(center=(400, 50))

end_surf = test_font.render(' Game Over ! ', False, 'Dark Green')
end_rect = end_surf.get_rect(center=(400, 100))

again_surf = test_font.render(' try again ?', False, 'White')
again_rect = again_surf.get_rect(center=(400,270))


# intro/outro player
player_stand_surf = pygame.image.load('Runner/graphics/player/player_stand.png').convert_alpha()
player_stand_rect = player_stand_surf.get_rect(center = (400, 200))
player_stand_scaled = pygame.transform.scale2x(player_stand_surf)
player_stand_scaled_rect = player_stand_scaled.get_rect(center=(400,200))



# start
start_surf = test_font.render('Runner', False, 'White')
start_rect = start_surf.get_rect(center=(400, 325))

while not start_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.type ==  pygame.MOUSEBUTTONDOWN:
                start_game = True
                
    screen.fill((94,129,162))
    screen.blit(player_stand_scaled, player_stand_scaled_rect)
    screen.blit(start_surf, start_rect)

    pygame.display.update()
    clock.tick(60)


# game
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == obs_timer:
                obs_group.add(Obstacle(choice(['fly', 'snail', 'snail','snail'])))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    obs_group.add(Obstacle(choice(['fly', 'snail', 'snail','snail'])))
    if game_active:
        screen.blit(ground_surf,(0,300))
        screen.blit(sky_surf,(0,0))
        display_score()

        pygame.draw.rect(screen, '#c0e8ec', text_rect)
        screen.blit(text_surf, text_rect)
        screen.blit(score_surf, score_rect)
        screen.blit(hs_surf, hs_rect)

        player.draw(screen)
        player.update()

        obs_group.draw(screen)
        obs_group.update()

       # collision handler  
        collisions = pygame.sprite.spritecollide(player.sprite, obs_group, False)
        if collisions:
            game_active = False
        for obstacle in obs_group:
            if player.sprite.rect.right > obstacle.rect.right and not obstacle.passed:
                obstacle.passed = True
                score += 1
        
        obs_group.remove(*collisions)
            
        score_surf = test_font.render(str(score), False, 'Green')
        score_rect = score_surf.get_rect(center=(200, 100))
        screen.blit(score_surf, score_rect)

            

    else:
        screen.fill((94,129,162))
        screen.blit(end_surf, end_surf.get_rect(center = (400, 75)))
        if score > high_score:
            high_score = score
            hs_surf = test_font.render('High Score: ' + str(high_score), False, 'Light Blue')
        screen.blit(player_stand_surf, player_stand_surf.get_rect(center = (400, 175)))
        screen.blit(hs_surf, hs_surf.get_rect(center=(400, 315)))
        screen.blit(again_surf, again_rect)

        screen.blit(again_surf, again_rect)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()


    # update
    pygame.display.update()
    clock.tick(60)