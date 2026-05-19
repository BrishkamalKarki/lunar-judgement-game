import pygame
import random
import states
import surfaces

# here is the sprite handling logic
class Eldermoon(pygame.sprite.Sprite):
    def __init__(self, frame_dict, frame_no, collective_groups, relative_groups):
        super().__init__((collective_groups, relative_groups))
        self.image = frame_dict["idle"][0]
        self.Eldermoon_frame_dict = frame_dict
        self.pos_x, self.pos_y = states.Eldermoon_st_pos_x, states.Eldermoon_st_pos_y 
        self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y))
        self.frame_index = 0
        self.animation_speed = 0.4
        self.frame_no_dict = frame_no
        global Eldermoon_sprite 
        global Eldermoon_frame_index 
        Eldermoon_sprite = self

    def set_state(self):
        self.Eldermoon_frame = self.Eldermoon_frame_dict[states.Eldermoon_state]
        self.Eldermoon_frame_no = self.frame_no_dict[states.Eldermoon_state]
        self.frame_index = 0
        self.image = self.Eldermoon_frame[0]

    def update(self, dt):
        if states.Eldermoon_HP <= 0 and states.Eldermoon_HP >= -5:
            states.Eldermoon_state = "death"
            self.frame_index = 0
            states.Eldermoon_HP = -999
            states.Evil_wizard = "offplay"
            states.Slime_demon = "offplay"
            states.Eldermoon_subcatagory = None
            states.Eldermoon_catagory = None
                  
        self.image = self.Eldermoon_frame[int(self.frame_index)] 
        
        if states.Eldermoon_catagory == "attacking":
            self.animation_speed =  0.3
        else:
            self.animation_speed = 0.4

        if states.Eldermoon_facing == "left":
            self.image = pygame.transform.flip(self.Eldermoon_frame[int(self.frame_index)], True, False) # x and y axis flips as true and false
        else:
            self.image = self.Eldermoon_frame[int(self.frame_index)] 

        if states.Eldermoon_state == "jump_st" or states.Eldermoon_state == "jump_lp":
            if states.Eldermoon_subcatagory == "jumping_up":
                self.Eldermoon_velocity_y = ( states.Eldermoon_initial_velocity - states.gravity * states.air_time )
            else:
                self.Eldermoon_velocity_y = ( states.gravity * states.air_time )
            states.air_time += dt 

        if (self.pos_x > 1160 and states.Eldermoon_facing == "right") or (self.pos_x < 40 and states.Eldermoon_facing == "left"):
            states.Eldermoon_speed = 0 
        else:
            states.Eldermoon_speed = 100 
        self.Eldermoon_velocity_x = states.Eldermoon_direction.x * states.Eldermoon_speed 
 
        if states.Eldermoon_state == "walking": 
            self.pos_x += self.Eldermoon_velocity_x * dt * 2
        elif states.Eldermoon_state == "running": 
            self.pos_x += self.Eldermoon_velocity_x * 4 * dt
        elif states.Eldermoon_state == "dash":
            self.animation_speed = 2
            if states.Eldermoon_facing == "right": 
                self.pos_x += states.Eldermoon_speed * 20 * dt 
            else: 
                self.pos_x -= states.Eldermoon_speed * 20 * dt 
        elif states.Eldermoon_state == "jump_st" or states.Eldermoon_state == "jump_lp": 
            self.pos_x += self.Eldermoon_velocity_x * dt 
            if states.Eldermoon_subcatagory == "jumping_down": 
                if not states.Eldermoon_entry_done:
                    self.pos_y += 10
                    if states.Eldermoon_state == "jump_lp": 
                        self.pos_x += 3
                    if self.pos_y >= 500:
                        self.pos_y = 500
                        states.Eldermoon_state = "landing" 
                        states.air_time = 0
                else:
                    self.pos_y += self.Eldermoon_velocity_y * dt 
                    if int(self.Eldermoon_velocity_y) >= states.Eldermoon_final_velocity and self.pos_y >= states.Eldermoon_st_pos_y + 400:
                        self.pos_y = states.Eldermoon_st_pos_y + 400 
                        states.Eldermoon_state = "landing" 
                        states.Eldermoon_initial_velocity = states.Eldermoon_final_velocity 
                        states.Eldermoon_final_velocity = 000 
                        states.air_time = 0 
            else: 
                self.pos_y -= self.Eldermoon_velocity_y * dt  
                if int(self.Eldermoon_velocity_y) <= 0: 
                    states.air_time = 0   
                    states.Eldermoon_subcatagory = "jumping_down"  
                    states.Eldermoon_final_velocity = states.Eldermoon_initial_velocity 
                    states.Eldermoon_initial_velocity = 0 

        self.mask = pygame.mask.from_surface(self.image) 
        Eldermoon_sprite = self 
        self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y)) 

        if self.frame_index == 0.6 and states.Eldermoon_catagory == "attacking": 
            states.check_collision_Axe_demon = True 
        if self.frame_index == 0.6 and states.Eldermoon_catagory == "attacking": 
            states.check_collision_Slime_demon = True 
        if self.frame_index == 0.6 and states.Eldermoon_catagory == "attacking": 
            states.check_collision_Evil_wizard = True 
 
        self.frame_index += self.animation_speed  
        if not states.Eldermoon_hit_taken and states.Eldermoon_state == "hit": 
            self.frame_index = 0 
            states.Eldermoon_hit_taken = True  
            self.animation_speed = 1  

        if self.frame_index > self.Eldermoon_frame_no: 
            self.frame_index = 0 
            if states.Eldermoon_state == "death":
                states.dead = True
            if states.Eldermoon_catagory == "jumping": 
                if states.Eldermoon_state == "jump_st": 
                    states.Eldermoon_state = "jump_lp" 
                elif states.Eldermoon_state == "landing": 
                    if not states.Eldermoon_entry_done:
                        states.Eldermoon_entry_done = True
                    states.Eldermoon_state = "idle" 
                    states.Eldermoon_catagory = None 
                    states.Eldermoon_subcatagory = None 
            if states.Eldermoon_entry_done:
                if states.Eldermoon_catagory == "attacking" or states.Eldermoon_catagory == "dashing":
                    states.Eldermoon_catagory = None
                    states.Eldermoon_state = "idle"
                if states.Eldermoon_state == "hit":
                    states.Eldermoon_catagory = None
                    states.Eldermoon_state = states.Eldermoon_prev_state
                    states.Eldermoon_hit_taken = False
                    states.Eldermoon_hit = False
                    self.animation_speed = 0.4

        if states.Eldermoon_catagory == "dashing":
            states.Eldermoon_dash_time += dt
        if states.Eldermoon_dash_time != 0:
            states.Eldermoon_dash_time += dt

        if states.Eldermoon_dash_time >= 0.5: # one dash in 1/2 seconds
            states.Eldermoon_dash_time = 0
        states.Eldermoon_pos_y = self.pos_y
        states.Eldermoon_pos_x = self.pos_x

class AxeDemon(pygame.sprite.Sprite):
    def __init__(self, frame_dict, frame_no, collective_groups, relative_groups, game_screen):
        super().__init__((collective_groups, relative_groups))
        self.image = frame_dict["walk"][0]
        self.Axe_demon_frame_dict = frame_dict
        # defaults
        self.Axe_demon_state = "walk"
        self.Axe_demon_st_pos_x = random.choice([-300, 1500])
        self.pos_x, self.pos_y = self.Axe_demon_st_pos_x, states.Axe_demon_st_pos_y
        self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y))
        self.frame_index = 0
        self.animation_speed = 0.08
        self.frame_no_dict = frame_no
        self.Axe_demon_direction = 1
        self.attack = random.choice(["attack1", "attack2"])
        if states.Eldermoon_pos_x > self.pos_x:
            self.Axe_demon_direction = 1
        else:
            self.Axe_demon_direction = -1
        self.prev_dir = self.Axe_demon_direction
        self.prev_state = "walk"
        self.HP = 30
        self.check_collision = False
        self.Axe_demon_dict = {}
        self.game_screen = game_screen
        self.dead_bool = False
        self.hp_pos_y = random.randint(self.pos_y - 25, self.pos_y - 10)
        self.fallback_done = False
        self.Axe_demon = "onplay"

    def update(self, dt):
        if self.Axe_demon == "onplay":
            if self.dead_bool:
                self.frame_index = 0
                self.dead_bool = False
            
            self.frame_index += self.animation_speed
            if self.frame_index >= self.frame_no_dict[self.Axe_demon_state]-1:
                if self.Axe_demon_state == "dead":
                    self.frame_index = self.frame_no_dict[self.Axe_demon_state]-1
                    self.pos_y = 505
                    self.Axe_demon = "offplay"
                elif self.Axe_demon_state == "fall_back":
                    self.frame_index = self.frame_no_dict[self.Axe_demon_state]-1
                    self.pos_y = 505
                    self.Axe_demon = "offplay"
                    self.HP = 15                    
                else:
                    self.frame_index = 0 
                    if abs(states.Eldermoon_pos_x - self.pos_x) < 95:
                        self.Axe_demon_state = self.attack
                        self.animation_speed = 0.2
                    elif abs(states.Eldermoon_pos_x - self.pos_x) < 500:
                        self.Axe_demon_state = "run"
                        self.animation_speed = 0.1
                    else:
                        self.Axe_demon_state = "walk"
                        self.animation_speed = states.Axe_demon_animation_speed
                
            if self.Axe_demon_state == "walk": 
                self.pos_x += self.Axe_demon_direction * states.Axe_demon_speed * dt 
            elif self.Axe_demon_state == "run":
                self.pos_x += self.Axe_demon_direction * states.Axe_demon_speed * 2 * dt 

            if states.Eldermoon_catagory == "jumping":
                self.Axe_demon_direction = self.prev_dir 
            else:
                if states.Eldermoon_pos_x > self.pos_x: 
                    self.Axe_demon_direction = 1 
                else:
                    self.Axe_demon_direction = -1 
            self.image = self.Axe_demon_frame_dict[self.Axe_demon_state][int(self.frame_index)] 
            if self.Axe_demon_direction == -1: 
                self.image = pygame.transform.flip(self.image, True, False)  
            self.prev_dir = self.Axe_demon_direction
            self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y)) 
            self.mask = pygame.mask.from_surface(self.image)

            # checking the collision in here 
            if self.Axe_demon_state == self.attack and round(self.frame_index, 2) == 4:      
                self.check_collision = True 
            else:
                self.check_collision = False   
  
            if self.check_collision:
                # if  pygame.sprite.collide_mask(self, Eldermoon_sprite):
                if abs(self.pos_x - states.Eldermoon_pos_x) < 70 and (self.pos_y - states.Eldermoon_pos_y) < 90:
                    states.Eldermoon_HP -= 0.5
                    states.Eldermoon_hit = True

            if states.check_collision_Axe_demon and self.Axe_demon_state != "dead":
                if abs(self.pos_x - states.Eldermoon_pos_x) < 95:
                    self.HP -= 5 
                    self.Axe_demon_state = "hit" 
                    self.frame_index = 0 
                    self.animation_speed = 0.4 

            if  self.Axe_demon_state != "dead":
                hp_bar_rect = pygame.FRect((self.pos_x - 20, self.hp_pos_y, 60, 6)) 
                pygame.draw.rect(self.game_screen, "white", hp_bar_rect)
                if self.HP > 0: 
                    hp_rect = pygame.FRect((self.pos_x - 20, self.hp_pos_y, 60 / (30 / self.HP), 6)) 
                    pygame.draw.rect(self.game_screen, "red", hp_rect)
                elif self.HP == 0:
                    pygame.draw.rect(self.game_screen, "white", hp_bar_rect) 
                    self.Axe_demon_state = "dead" 
                    self.dead_bool = True 
                    self.HP = -273.15
                    self.frame_index = 0
        else:
            if states.Slime_demon_HP == 100:
                self.Axe_demon = "onplay"

class EvilWizard(pygame.sprite.Sprite):
    def __init__(self, frame_dict, frame_no, collective_groups, relative_groups, game_screen):
        super().__init__((relative_groups, collective_groups))
        self.image = frame_dict["run"][0]
        self.Evil_wizard_frame_dict = frame_dict
        # defaults 
        self.Evil_wizard_state = "run"
        self.Evil_wizard_st_pos_x = random.choice([-300, 1500])
        self.pos_x, self.pos_y = self.Evil_wizard_st_pos_x, states.Evil_wizard_st_pos_y
        self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y))
        self.frame_index = 0
        self.animation_speed = 1
        self.frame_no_dict = frame_no
        self.Evil_wizard_direction = 1
        if states.Eldermoon_pos_x > self.pos_x:
            self.Axe_demon_direction = 1
        else:
            self.Axe_demon_direction = -1
        self.prev_dir = self.Axe_demon_direction
        self.prev_state = "run"
        self.HP = 100
        self.check_collision = False
        self.Axe_demon_dict = {}
        self.game_screen = game_screen
        self.dead_bool = False
        self.attack = random.choices(["attack1", "attack2"])

    def update(self, dt):
        if states.Evil_wizard == "onplay":
            if self.dead_bool:
                self.frame_index = 0
                self.dead_bool = False

            self.frame_index += self.animation_speed
            if self.frame_index >= self.frame_no_dict[self.Evil_wizard_state]:
                self.frame_index = 0
                self.attack = random.choice(["attack1", "attack2"]) 
                if self.Evil_wizard_state == "hit":
                    self.Evil_wizard_state = "idle"
                else:
                    if self.Evil_wizard_state == "death":
                        states.Evil_wizard = "offplay"
                        self.frame_index = self.frame_no_dict[self.Evil_wizard_state] - 1
                    else:
                        if states.Eldermoon_catagory == "jumping" and abs(self.pos_x - states.Eldermoon_pos_x) < 150 and abs(self.pos_y - states.Eldermoon_pos_y) > 90: 
                            self.Evil_wizard_state = "idle"
                        else:
                            self.Evil_wizard_state = "run"
                            self.animation_speed = states.Evil_wizard_animation_speed
            if abs(states.Eldermoon_pos_x - self.pos_x) < 140 and self.Evil_wizard_state != "death" and self.Evil_wizard_state != "hit":
                    self.Evil_wizard_state = self.attack
                    self.animation_speed = 0.2
     
            if self.Evil_wizard_state == "run": 
                self.pos_x += self.Evil_wizard_direction * states.Evil_wizard_speed * 4 * dt

            if states.Eldermoon_pos_x > self.pos_x:
                self.Evil_wizard_direction = 1
            else:
                self.Evil_wizard_direction = -1
            self.image = self.Evil_wizard_frame_dict[self.Evil_wizard_state][int(self.frame_index)]
            if self.Evil_wizard_direction == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.prev_dir = self.Evil_wizard_direction
            self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y))
            self.mask = pygame.mask.from_surface(self.image)

            # checking the collision in here
            if self.Evil_wizard_state == self.attack and round(self.frame_index, 2) == 4: 
                self.check_collision = True 
            else:
                self.check_collision = False 

            if self.check_collision:
                if pygame.sprite.collide_mask(self, Eldermoon_sprite): 
                    states.Eldermoon_HP -= 1
                    states.Eldermoon_hit = True 

            if states.check_collision_Evil_wizard and self.Evil_wizard_state != "death":
                if abs(self.pos_x - states.Eldermoon_pos_x) < 122:
                    self.HP -= 10
                    self.Evil_wizard_state = "hit"
                    self.animation_speed = 0.2
                states.check_collision_Evil_wizard = False
            
            hp_bar_rect = pygame.FRect((self.pos_x - 20, self.pos_y - 50, 100, 7)) 
            pygame.draw.rect(self.game_screen, "white", hp_bar_rect)
            if self.HP > 0: 
                hp_rect = pygame.FRect((self.pos_x - 20, self.pos_y - 50, 100 / (100 / self.HP), 7)) 
                pygame.draw.rect(self.game_screen, "red", hp_rect)
            elif self.HP == 0: 
                pygame.draw.rect(self.game_screen, "white", hp_bar_rect) 
                self.Evil_wizard_state = "death" 
                self.dead_bool = True 
                self.animation_speed = 0.15
                self.check_collision = False
                self.HP = -273.15 
                states.Evil_wizard_done = 1

class SlimeDemon(pygame.sprite.Sprite):
    def __init__(self, frame_dict, frame_no, collective_groups, relative_groups, game_screen):
        super().__init__((relative_groups, collective_groups))
        self.image = frame_dict["walk"][0]
        self.Slime_demon_frame_dict = frame_dict
        # defaults 
        self.Slime_demon_state = "walk"
        self.Slime_demon_st_pos_x = random.choice([-300, 1500])
        self.pos_x, self.pos_y = self.Slime_demon_st_pos_x, states.Slime_demon_st_pos_y
        self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y))
        self.frame_index = 0 
        self.animation_speed = 0.1    
        self.frame_no_dict = frame_no     
        self.Slime_demon_direction = 1  
        if states.Eldermoon_pos_x > self.pos_x:    
            self.Axe_demon_direction = 1  
        else:   
            self.Axe_demon_direction = -1  
        self.prev_dir = self.Axe_demon_direction 
        self.prev_state = "walk"  
        self.HP = 200 
        self.check_collision = False 
        self.Axe_demon_dict = {} 
        self.game_screen = game_screen 
        self.dead_bool = False 

    def update(self, dt):
        if states.Slime_demon == "onplay":
            if self.dead_bool:
                self.frame_index = 0
                self.dead_bool = False

            self.frame_index += self.animation_speed
            if self.frame_index >= self.frame_no_dict[self.Slime_demon_state]:
                self.frame_index = 0
                if self.Slime_demon_state == "hit":
                    self.Slime_demon_state = "idle"
                else:
                    if self.Slime_demon_state == "death":
                        states.Slime_demon = "offplay"
                        states.game_won = True 
                        surfaces.axe_demon_sprites_grp.empty()
                        surfaces.slime_demon_sprites_grp.empty()
                        surfaces.evil_wizard_sprites_grp.empty()
                        surfaces.Eldermoon_sprites_grp.empty()
                        surfaces.Eldermoon_attack_sprites_grp.empty()
                        surfaces.collective_sprites.empty()
                        self.frame_index = self.frame_no_dict[self.Slime_demon_state] - 1
                    else:
                        if states.Eldermoon_catagory == "jumping" and abs(self.pos_x - states.Eldermoon_pos_x) < 140 and abs(self.pos_y - states.Eldermoon_pos_y) > 90: 
                            self.Slime_demon_state = "idle"
                        else:
                            self.Slime_demon_state = "walk"
                            self.animation_speed = 0.3

            if abs(states.Eldermoon_pos_x - self.pos_x) < 200 and self.Slime_demon_state != "hit" and self.Slime_demon_state != "death":
                    self.Slime_demon_state = "cleave"
                    self.animation_speed = 0.4

            if self.Slime_demon_state == "walk": 
                self.pos_x += self.Slime_demon_direction * states.Slime_demon_speed * 3 * dt

            if states.Eldermoon_pos_x > self.pos_x:
                self.Slime_demon_direction = 1
            else:
                self.Slime_demon_direction = -1
            self.image = self.Slime_demon_frame_dict[self.Slime_demon_state][int(self.frame_index)]
            if self.Slime_demon_direction == 1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.prev_dir = self.Slime_demon_direction 
            self.rect = self.image.get_frect(center = (self.pos_x, self.pos_y))
            self.mask = pygame.mask.from_surface(self.image)

            # checking the collision in here
            if self.Slime_demon_state == "cleave" and round(self.frame_index, 2) == 10.0: 
                self.check_collision = True  
            else:  
                self.check_collision = False

            if self.check_collision: 
                if pygame.sprite.collide_mask(self, Eldermoon_sprite): 
                    states.Eldermoon_HP -= 3
                    states.Eldermoon_hit = True 

            if states.check_collision_Slime_demon and self.Slime_demon_state != "death": 
                if abs(self.pos_x - states.Eldermoon_pos_x) < 122: 
                    self.HP -= 10
                    self.Slime_demon_state = "hit" 
                    self.animation_speed = 1 
                    self.frame_index = 0 
                states.check_collision_Slime_demon = False 
 
            hp_bar_rect = pygame.FRect((self.pos_x - 80, self.pos_y - 60, 200, 8)) 
            if self.HP > 0: 
                hp_rect = pygame.FRect((self.pos_x - 80, self.pos_y - 60, 200 / (200 / self.HP), 8)) 
                pygame.draw.rect(self.game_screen, "white", hp_bar_rect) 
                pygame.draw.rect(self.game_screen, "red", hp_rect) 
            elif self.HP == 0:
                self.Slime_demon_state = "death" 
                self.dead_bool = True 
                self.animation_speed = 0.15 
                self.check_collision = False 
                self.HP = -273.15 
            states.Slime_demon_HP = self.HP
        
           
            
