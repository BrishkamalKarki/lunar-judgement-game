import pygame
import os
import sprites, states 
 
window_width = 1200  
window_height = 600 
frame_width = 240 
frame_height = 128 
collective_sprites = pygame.sprite.Group() # a grounp of every sprites Eldermoon_sprites_grp = pygame.sprite.Group()
Eldermoon_sprites_grp = pygame.sprite.Group()
Eldermoon_attack_sprites_grp = pygame.sprite.Group()
axe_demon_sprites_grp = pygame.sprite.Group()
evil_wizard_sprites_grp = pygame.sprite.Group()
slime_demon_sprites_grp = pygame.sprite.Group()

class Backgroud:    
    def mainMenu(self): 
        game_bg_path = os.path.join("assets", "images", "background", "moony_day.png")
        play_button_path = os.path.join("assets", "images", "background", "play_button.png")
        exit_button_path = os.path.join("assets", "images", "background", "exit_button.png")
        victory_path = os.path.join("assets", "images", "background", "victory.png")
        paused_path = os.path.join("assets", "images", "background", "paused.png")
        lost_path = os.path.join("assets", "images", "background", "lost.png")
        main_menu_bg_path = os.path.join("assets", "images", "background", "main_menu.png")
        self.hp_bar_frame_path = os.path.join("assets", "images", "background", "id.png")
        self.hp_bar_path = os.path.join("assets", "images", "background", "hp_bars", "hp_bar_")
        self.arena_bg_image = pygame.transform.scale(pygame.image.load(game_bg_path), (window_width + 300, window_height + 12))
        self.bg_image = pygame.transform.scale(pygame.image.load(main_menu_bg_path), (window_width, window_height))
        self.play_image = pygame.transform.scale(pygame.image.load(play_button_path), (200, 50))
        self.exit_image = pygame.transform.scale(pygame.image.load(exit_button_path), (200, 50))
        states.victory = pygame.transform.scale(pygame.image.load(victory_path), (200, 50))
        states.paused = pygame.transform.scale(pygame.image.load(paused_path), (200, 50))
        states.lost = pygame.transform.scale(pygame.image.load(lost_path), (200, 50))
        self.hp_bar_img =[pygame.transform.scale(pygame.image.load(f"{self.hp_bar_path}{i}.png"), (4, 23)) for i in range(1, 51)]
        self.bg_surface = pygame.Surface((window_width, window_height))
        play_img_rect = self.play_image.get_rect(center = (450, 565))
        exit_img_rect = self.exit_image.get_rect(center = (750, 565))
        self.bg_surface.blit(self.bg_image, (0, 0), (0, 0, window_width, window_height))
        self.bg_surface.blit( self.play_image, play_img_rect)
        self.bg_surface.blit( self.exit_image, exit_img_rect)
        self.arena_bg_surface = pygame.Surface((window_width, window_height))
        self.hp_bar_frame_img = pygame.transform.scale(pygame.image.load(self.hp_bar_frame_path), (400, 100))
        self.buttons = ["pause_button.png", "resume_button.png", "home_button.png", "quit_button.png"]
        states.buttons_path = [pygame.transform.scale(pygame.image.load(f"{os.path.join("assets", "images", "background", path)}"), (40, 40)) for path in self.buttons]
        states.buttons_rect.append(states.buttons_path[0].get_rect(topleft=(1151, 9)))
        states.buttons_rect.append(states.buttons_path[1].get_rect(topleft=(440, 400)))
        states.buttons_rect.append(states.buttons_path[2].get_rect(topleft=(580, 400)))
        states.buttons_rect.append(states.buttons_path[3].get_rect(topleft=(720, 400)))        
        return self.bg_surface, play_img_rect, exit_img_rect

    def _BackGround(self):
        self.hp_bar_frame_img = pygame.transform.scale(pygame.image.load(self.hp_bar_frame_path), (336, 104))
        self.arena_bg_surface.blit(self.arena_bg_image, (0, 0), (0, 10, 1200, 600))

        for i in range(1, (int)(states.Eldermoon_HP / 2)):
            self.hp_bar_frame_img.blit(self.hp_bar_img[i-1], (126 + (i-1) * 4 , 39)) # 237
        self.arena_bg_surface.blit(self.hp_bar_frame_img, (9 , 9)) 
        self.arena_bg_surface.blit(states.buttons_path[0], (1151, 9)) 
        return self.arena_bg_surface
    
    def dialouge(self, game_screen):
        if states.Eldermoon_comming:
            bg_path = os.path.join("assets", "images", "background", "background.jpg") 
            bg_image = pygame.transform.scale(pygame.image.load(bg_path).convert_alpha(), (window_width, window_height)) 
            Eldermoon_diag_path = os.path.join("assets", "images", "dialouge", "Eldermoon_comming.png") 
            Eldermoon_diag_img = pygame.transform.scale(pygame.image.load(Eldermoon_diag_path).convert_alpha(), (700, 500)) 
            opac_bg = 255 
            opac_diag = 0 
            diag_st_time = pygame.time.get_ticks()  
            while(1):
                for event in pygame.event.get():
                        if event.type == pygame.QUIT: 
                            pygame.quit()
                            return False
                game_screen.fill((0,0,0))
                Eldermoon_diag_img.set_alpha(opac_diag)
                bg_image.set_alpha(opac_bg)
                bg_image.blit(Eldermoon_diag_img, (250, 250))
                game_screen.blit(bg_image, (0, 0))
                if pygame.time.get_ticks() - diag_st_time < 5000:
                    opac_diag += 0.1
                else:
                    opac_diag -= 0.1
                    opac_bg -= 0.1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return False
                if pygame.time.get_ticks() - diag_st_time > 10000:
                    break
                pygame.display.update()
        
class Eldermoon():
    def __init__(self):
        self.run_frame_path = os.path.join("assets", "images", "eldermoon", "run_state", "frame")
        self.idle_frame_path = os.path.join("assets", "images", "eldermoon","idle_state", "frame")
        self.walking_frame_path = os.path.join("assets", "images", "eldermoon","walk_state", "frame")
        self.jumping_start_frame_path = os.path.join("assets", "images", "eldermoon","jump_state_starting_phase", "frame")
        self.jumping_loop_frame_path = os.path.join("assets", "images", "eldermoon","jump_state_loop_phase", "frame")
        self.landing_frame_path = os.path.join("assets", "images", "eldermoon","jump_state_landing_phase", "frame")
        self.attack_1_frame_path = os.path.join("assets", "images", "eldermoon","attack_1_state", "frame")
        self.attack_2_frame_path = os.path.join("assets", "images", "eldermoon","attack_2_state", "frame")
        self.dash_frame_path = os.path.join("assets", "images", "eldermoon","dash_state", "frame")
        self.hit_frame_path = os.path.join("assets", "images", "eldermoon","hit_state", "frame")
        self.death_frame_path = os.path.join("assets", "images", "eldermoon","death_state", "frame")
        self.Eldermoon_frames_dict = {"idle": [pygame.transform.scale(pygame.image.load(f"{self.idle_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (17)],
                                    "walking": [pygame.transform.scale(pygame.image.load(f"{self.walking_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (12)],
                                    "jump_st": [pygame.transform.scale(pygame.image.load(f"{self.jumping_start_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (5)],
                                    "jump_lp": [pygame.transform.scale(pygame.image.load(f"{self.jumping_loop_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (3)],
                                    "landing": [pygame.transform.scale(pygame.image.load(f"{self.landing_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (5)],
                                    "running": [pygame.transform.scale(pygame.image.load(f"{self.run_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (6)],
                                    "attack_1": [pygame.transform.scale(pygame.image.load(f"{self.attack_1_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (11)],
                                    "attack_2": [pygame.transform.scale(pygame.image.load(f"{self.attack_2_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (10)],
                                    "dash": [pygame.transform.scale(pygame.image.load(f"{self.dash_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (15)],
                                    "hit": [pygame.transform.scale(pygame.image.load(f"{self.hit_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (3)],
                                    "death": [pygame.transform.scale(pygame.image.load(f"{self.death_frame_path}{i}.png").convert_alpha(), (frame_width, frame_height * 1.5)) for i in range (19)]}
        self.Eldermoon_frames_no = {"idle": 16, "walking": 11, "running": 5, "jump_st": 4, "jump_lp": 2, "landing": 4, "attack_1": 10, "attack_2": 9, "dash": 14, "hit":2, "death": 18}
        self.Eldermoon = sprites.Eldermoon(self.Eldermoon_frames_dict, self.Eldermoon_frames_no, collective_sprites, Eldermoon_sprites_grp)

    def load_Eldermoon_sprites(self):
        self.Eldermoon.set_state()

class AxeDemon():
    def __init__(self, game_screen):
        images_folder = ["attack1", "attack2", "dead", "fall_back", "hit", "run", "stand_up", "walk"]
        frames_no = [6, 6, 4, 4, 3, 6, 5, 6]
        frame = 0
        frames = []
        for folder in images_folder:
            frames.append([pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "enemies", "axe_demon-lev-C", folder, f"{folder}_{i+1}.png")), (frame_width / 1.4, frame_height / 1.2 )) for i in range(0, frames_no[frame])])
            frame += 1
        frames_dict = {"attack1": frames[0], "attack2": frames[1], "dead": frames[2], "fall_back": frames[3], "hit": frames[4], "run": frames[5], "stand_up": frames[6], "walk": frames[7]}
        frames_no = {"attack1": 6, "attack2": 6, "dead": 4, "fall_back": 4, "hit": 3, "run": 6, "stand_up": 5, "walk": 6}
        sprites.AxeDemon(frames_dict, frames_no, collective_sprites, axe_demon_sprites_grp, game_screen)

class EvilWizard():
    def __init__(self, game_screen):
        frame_width = 250
        frame_height = 250
        spritesheets_name = ["attack1", "attack2", "death","hit", "idle", "run"]
        spritesheets_path = [os.path.join("assets", "images", "enemies", "evil_wizard-lev-B", f"{ssp}.png") for ssp in spritesheets_name]
        spritesheets = [pygame.image.load(sp).convert_alpha() for sp in spritesheets_path]
        frames_no_list = [8, 8, 7, 3, 8, 8]
        frames_images = [] # for all the spritesheets
        sub_frames_images = [] # for individual spritesheets
        fn = 0
        for sprite in spritesheets_name:
            for i in range(frames_no_list[fn]):
                surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
                surface.blit(spritesheets[fn], (0, 0), (frame_width * i, 0, frame_width, frame_height))
                sub_frames_images.append(pygame.transform.scale(surface, (240 * 1.8, 128 * 2.8)))
            fn += 1
            frames_images.append(sub_frames_images) 
            sub_frames_images = []
        frames_no = {"attack1": 8, "attack2": 8, "death": 7, "hit": 3, "idle": 8, "run": 8}
        frames_dict = {"attack1": frames_images[0], "attack2": frames_images[1], "death": frames_images[2], "hit": frames_images[3], "idle": frames_images[4], "run": frames_images[5]}
        sprites.EvilWizard(frames_dict, frames_no, collective_sprites, evil_wizard_sprites_grp, game_screen)

class SlimeDemon():
    def __init__(self, game_screen):
        images_folder = ["idle", "walk", "cleave", "death", "hit"]
        frames_no_list = [6, 12, 15, 22, 5]
        frame = 0
        frames = []
        
        for folder in images_folder:
            frames.append([pygame.transform.scale(pygame.image.load(os.path.join("assets", "images", "enemies", "slime_demon-lev-A", folder, f"{folder}_{i}.png")), (frame_width * 3, frame_height * 2.5)) for i in range(1, frames_no_list[frame] + 1)])
            frame += 1
        frames_dict = {"idle": frames[0], "walk": frames[1], "cleave": frames[2], "death": frames[3], "hit": frames[4]}
        frames_no = {"idle": 6, "walk": 12, "cleave": 15, "death": 22, "hit": 5}
        sprites.SlimeDemon(frames_dict, frames_no, collective_sprites, slime_demon_sprites_grp, game_screen)