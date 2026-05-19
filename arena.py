import pygame
import surfaces
import states
import os, importlib

# This class contains the main game arena

class Arena:
    def __init__(self, screen_width, screen_height):
        self.game_screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("LUNAR JUDGEMENT: REAPING OF SINS")
        pygame.display.set_icon(pygame.image.load(os.path.join("assets", "images", "eldermoon", "portrait", "Facing_Up.png")))
        self.screen_width = screen_width 
        self.screen_height = screen_height 
        self.running = True 
        self.game_clock = pygame.time.Clock()
        self.screen_cpy = None
        self.music_loader()
        self.mainMenu()
        if self.running:
            self.load_Eldermoon()
            self.arena()

    def reload(self):
        self.running = True
        self.game_clock = pygame.time.Clock()
        self.music_loader()
        self.mainMenu()
        self.load_Eldermoon()
        self.arena()
    
    def music_loader(self):
        sound_path = os.path.join('assets','music','track.mp3')
        self.music_track = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join('assets','music','attack1_eldermoon.mp3')
        states.Eldermoon_attack1 = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join('assets','music','attack2_eldermoon.mp3')
        states.Eldermoon_attack2 = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join('assets','music','slime_demon_laughter.mp3')
        states.Slime_demon_laughter = pygame.mixer.Sound(sound_path)
        sound_path = os.path.join('assets','music','eldermoon_jump.mp3')
        states.Eldermoon_jump = pygame.mixer.Sound(sound_path)

    def load_Eldermoon(self):
        # getting 
        self.Eldermoon = surfaces.Eldermoon()
        self.Eldermoon.load_Eldermoon_sprites()
        states.Eldermoon_sprite_called = 1 
        states.Eldermoon_state_just_changed = True

    def mainMenu(self):
        self.background = surfaces.Backgroud()
        main_menu_surf, play_rect, exit_rect = self.background.mainMenu()
        self.game_screen.blit(main_menu_surf, (0, 0))
        pygame.display.update()
        while(not states.game_started):
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT:
                    pygame.quit() 
                    self.running = False
                    return
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    mouse_coord = event.pos  
                else: 
                    mouse_coord = (0, 0) 
                if play_rect.collidepoint( mouse_coord): 
                    state = self.background.dialouge(self.game_screen) 
                    if not state:
                        self.running = False 
                        return
                    self.game_clock.tick()
                    states.game_started = True 
                if exit_rect.collidepoint( mouse_coord):
                    self.running = False
                    pygame.quit()
                    return 

    def Eldermoon_status(self):
        if not states.dead and not states.game_won and not states.game_paused:
            if states.Eldermoon_entry_done:
                if states.Eldermoon_state != "death":
                    keys = pygame.key.get_pressed()
                    states.Eldermoon_direction.x = (keys[pygame.K_d] or keys[ pygame.K_RIGHT]) - (keys[pygame.K_a] or keys[ pygame.K_LEFT])

                    if states.Eldermoon_hit and states.Eldermoon_catagory != "jumping":
                        states.Eldermoon_state = "hit"
                        states.Eldermoon_catagory = "taking_hit"

                    elif states.Eldermoon_catagory != "jumping":
                        if keys[pygame.K_w] or keys[pygame.K_UP]:
                            pygame.mixer.Channel(5).play(states.Eldermoon_jump, loops = 0)
                            states.Eldermoon_state = "jump_st"
                            states.Eldermoon_catagory = "jumping"
                            states.Eldermoon_subcatagory = "jumping_up"
            
                    if states.Eldermoon_catagory is None:
                        if states.Eldermoon_direction.x: 
                            states.Eldermoon_state = "walking" 
                            if keys[pygame.K_LALT] or keys[pygame.K_LALT]:
                                states.Eldermoon_state = "running" 
                        else:
                            states.Eldermoon_state = "idle"
                        
                        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and states.Eldermoon_dash_time == 0:
                            states.Eldermoon_state = "dash"
                            states.Eldermoon_catagory = "dashing" 

                        if keys[pygame.K_j]:
                            states.Eldermoon_state = "attack_1" 
                            states.Eldermoon_catagory = "attacking"
                            pygame.mixer.Channel(1).play(states.Eldermoon_attack1, loops = 0)
                        if keys[pygame.K_k]:
                            states.Eldermoon_state = "attack_2"
                            states.Eldermoon_catagory = "attacking" 
                            pygame.mixer.Channel(1).play(states.Eldermoon_attack2, loops = 0)
                        
                    if states.Eldermoon_direction.x == -1: 
                        states.Eldermoon_facing = "left"
                    elif states.Eldermoon_direction.x == 1: 
                        states.Eldermoon_facing = "right"

        if states.Eldermoon_prev_state != states.Eldermoon_state: 
            self.Eldermoon.load_Eldermoon_sprites()
            states.Eldermoon_prev_state = states.Eldermoon_state 

    def arena(self): 
        self.axe_demon_time = pygame.time.get_ticks()  
        channel0 = pygame.mixer.Channel(0)
        channel0.play(self.music_track, loops = -1) 
        while (self.running):  
            self.dt = self.game_clock.tick(60) 
            # checking the Eldermoon facings and states
            self.Eldermoon_status()

            self.background_surface = self.background._BackGround() 
            self.game_screen.blit(self.background_surface, (0, 0))
            surfaces.Eldermoon_sprites_grp.draw(self.game_screen)
            surfaces.axe_demon_sprites_grp.draw(self.game_screen)
            surfaces.slime_demon_sprites_grp.draw(self.game_screen) 
            surfaces.evil_wizard_sprites_grp.draw(self.game_screen)
            surfaces.collective_sprites.update(self.dt/1000) 

            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    self.running = False  
                    break
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    mouse_coord = event.pos 
                    if states.buttons_rect[0].collidepoint(mouse_coord): 
                        self.screen_cpy = self.game_screen.copy() 
                        states.game_paused = True 
                        channel0.pause() 
                        self.game_screen.fill((0,0,0)) 
                        self.screen_cpy.set_alpha(130)
                        self.game_screen.blit(self.screen_cpy)
                        self.game_screen.blit(states.buttons_path[1], (440, 400))
                        self.game_screen.blit(states.buttons_path[2], (580, 400))
                        self.game_screen.blit(states.buttons_path[3], (720, 400))
                        self.game_screen.blit(states.paused, (500, 200))
                        pygame.display.update()  
                        while(states.game_paused):
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit() 
                                    return
                                if event.type == pygame.MOUSEBUTTONDOWN: 
                                    mouse_coord = event.pos   
                                    if states.buttons_rect[1].collidepoint(mouse_coord):
                                        states.game_paused = False
                                        channel0.unpause()
                                        self.game_clock = pygame.time.Clock()
                                    if states.buttons_rect[2].collidepoint(mouse_coord):
                                        importlib.reload(states)
                                        surfaces.axe_demon_sprites_grp.empty()
                                        surfaces.slime_demon_sprites_grp.empty()
                                        surfaces.evil_wizard_sprites_grp.empty()
                                        surfaces.Eldermoon_sprites_grp.empty()
                                        surfaces.Eldermoon_attack_sprites_grp.empty()
                                        surfaces.collective_sprites.empty()
                                        self.reload()
                                    if states.buttons_rect[3].collidepoint(mouse_coord):
                                        pygame.event.clear()
                                        return
            
            if states.dead:
                self.screen_cpy = self.game_screen.copy() 
                channel0.pause()
                self.game_screen.fill((0,0,0))
                self.screen_cpy.set_alpha(130)
                self.game_screen.blit(self.screen_cpy)
                self.game_screen.blit(states.lost, (500, 200))
                states.buttons_rect[2] = states.buttons_path[2].get_rect(topleft=(500, 400))
                states.buttons_rect[3] = states.buttons_path[3].get_rect(topleft=(640, 400))         
                self.game_screen.blit(states.buttons_path[2], (500, 400))
                self.game_screen.blit(states.buttons_path[3], (640, 400))
                pygame.display.update()
                while(states.dead):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: 
                            pygame.quit()
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN: 
                            mouse_coord = event.pos   
                            if states.buttons_rect[2].collidepoint(mouse_coord):
                                importlib.reload(states)
                                surfaces.axe_demon_sprites_grp.empty()
                                surfaces.slime_demon_sprites_grp.empty()
                                surfaces.evil_wizard_sprites_grp.empty()
                                surfaces.Eldermoon_sprites_grp.empty()
                                surfaces.Eldermoon_attack_sprites_grp.empty()
                                surfaces.collective_sprites.empty()
                                self.reload()
                            if states.buttons_rect[3].collidepoint(mouse_coord):
                                pygame.quit() 
                                return
                
            if states.game_won: 
                self.screen_cpy = self.game_screen.copy() 
                channel0.pause() 
                self.game_screen.fill((0,0,0)) 
                self.screen_cpy.set_alpha(130) 
                self.game_screen.blit(self.screen_cpy) 
                self.game_screen.blit(states.victory, (500, 200)) 
                states.buttons_rect[2] = states.buttons_path[2].get_rect(topleft=(500, 400))
                states.buttons_rect[3] = states.buttons_path[3].get_rect(topleft=(640, 400))  
                self.game_screen.blit(states.buttons_path[2], (500, 400))  
                self.game_screen.blit(states.buttons_path[3], (640, 400))
                pygame.display.update()
                while(states.game_won):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT: 
                            pygame.quit()
                            return
                        if event.type == pygame.MOUSEBUTTONDOWN: 
                            mouse_coord = event.pos   
                            if states.buttons_rect[2].collidepoint(mouse_coord):
                                importlib.reload(states)
                                surfaces.axe_demon_sprites_grp.empty()
                                surfaces.slime_demon_sprites_grp.empty()
                                surfaces.evil_wizard_sprites_grp.empty()
                                surfaces.Eldermoon_sprites_grp.empty()
                                surfaces.Eldermoon_attack_sprites_grp.empty()
                                surfaces.collective_sprites.empty()
                                self.reload()
                            if states.buttons_rect[3].collidepoint(mouse_coord):
                                pygame.quit()
                                return

            pygame.display.update()      
            # collision checking condition for Axe demon getting hit
            if states.check_collision_Axe_demon:
                states.check_collision_Axe_demon = False

            if states.Eldermoon_entry_done:
                if states.slime_demons_spawned == 0 and states.Evil_wizard_done == 1:
                    surfaces.SlimeDemon(self.game_screen) 
                    states.slime_demons_spawned = 1
                    pygame.mixer.Channel(6).play(states.Slime_demon_laughter, loops = 10)

                if states.Evil_wizards_spawned == 0 and states.Axe_demons_spawned >= 10:
                    surfaces.EvilWizard(self.game_screen)
                    states.Evil_wizards_spawned = 1

                # spawning the axe demon every 10 seconds
                if (pygame.time.get_ticks() - self.axe_demon_time > 7000 and states.Axe_demons_spawned < 10):
                    states.Axe_demons_spawned += 1
                    surfaces.AxeDemon(self.game_screen)
                    self.axe_demon_time = pygame.time.get_ticks()

        pygame.quit()
