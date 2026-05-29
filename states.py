from pygame import Vector2

# Eldermoon states in here  
Eldermoon_comming = 1
Eldermoon_state = "jump_lp" # default 
Eldermoon_facing = "right" # default 
Eldermoon_state_just_changed = False
Eldermoon_sprite_called = 0
Eldermoon_prev_state = "jump_lp" 
Eldermoon_dash_time = 0 # storing the time just after the dash key is pressed thus limiting the dash 
Eldermoon_catagory = "jumping"
Eldermoon_subcatagory = "jumping_down"
Eldermoon_st_pos_x = -20 # intial coordinates position
Eldermoon_st_pos_y = 100
Eldermoon_pos_x = 200 # dynamic position for the eldermoon
Eldermoon_pos_y = 500
Eldermoon_dx = 0 
gravity = 1600 # per 1/60th part of a second
Eldermoon_initial_velocity = 900 # for jumping
Eldermoon_final_velocity = 000 
Eldermoon_HP = 100
air_time = 0 # time in the air
check_collision_Axe_demon = False # default
check_collision_Evil_wizard = False # default
check_collision_Slime_demon = False # default
Eldermoon_hit = False
Eldermoon_hit_taken = False
Eldermoon_entry_done = False
Eldermoon_attack1 = None
Eldermoon_attack2 = None
Eldermoon_jump = None

Eldermoon_speed = 100 # normal walking speed
Eldermoon_direction = Vector2() # direction

# game states over here
game_started = False
game_paused = False
buttons_path = []
buttons_rect = []
paused = None
victory = None
lost = None
dead = False
game_won = False

# AXE DEMON STATS AND PROPERTIES OVER HERE
Axe_demon_st_pos_x = 0
Axe_demon_st_pos_y = 500
Axe_demon_facing = 0
Axe_demon_speed = 80
Axe_demon_animation_speed = 0.08
Axe_demon_state_changeable = False

Axe_demons = {}
Axe_demons_spawned = 0
Axe_demon_done = 0
Axe_demon = "onplay"

# SLIME DEMON STATS AND PROPERTIES OVER HERE 
Slime_demon_st_pos_x = 0
Slime_demon_st_pos_y = 386
Slime_demon_facing = 0
Slime_demon_speed = 140
Slime_demon_state_changeable = False
slime_demons = {}
slime_demons_spawned = 0
Slime_demon_HP = 200
Slime_demon_cleave = None
Slime_demon_laughter = None
Slime_demon = "onplay"

# WIZARD STATS STATS AND PROPERTIES OVER HERE 
Evil_wizard_st_pos_x = 0
Evil_wizard_st_pos_y = 485
Evil_wizard_facing = 0
Evil_wizard_speed = 80
Evil_wizard_animation_speed = 0.1 
Evil_wizard_state_changeable = False
Evil_wizzard_attack = False
Evil_wizard = "onplay"

Evil_wizards = {}
Evil_wizards_spawned = 0
Evil_wizard_done = 0


