"""Author: Michael
   "A WITCH'S HELL"
   Description: Small Bullet Hell Game - A bullet hell game created in 
   pygame with the game_sprites class.
   Known bugs: Some sound do not play when they are supossed to/Late at playing.
   Please note that the instructions are in full detail in the Readme text 
"""

# I - IMPORT AND INITIALIZE
import pygame, game_sprites, random

#pre_init reduces sound delay
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.init()

def main():
    '''This function defines the 'mainline logic' of the game'''
      
    # DISPLAY - set display resolution and caption.
    screen_size = (640, 480)
    screen = pygame.display.set_mode(screen_size)    
    pygame.display.set_icon(pygame.image.load(
        "images/icon.png").convert_alpha())
    pygame.display.set_caption("A WITCH'S HELL")
    

    #Set up main menu loop 
    while game_intro(screen):
        #If game loop if over via window exit, kill game. instead of loop back.
        if not game_loop(screen):
            break
    
    # Unhide the mouse pointer - before closing window
    pygame.mouse.set_visible(True)    
    #Quit the game with delay to hear music fade
    pygame.mixer.music.fadeout(1000)
    pygame.time.delay(1000)
    pygame.quit()     
    
def pause(screen):
    '''This function pauses the game loop with the darker paused frame as 
    background. This function accepts the screen parameter to capture the 
    paused frame from the game loop when the function is called.
    '''
    
    # E - Entities - background, buttons and sprite group set up
    background = screen
    #dark surface is a special surface that is blited to make background darker.
    dark = pygame.Surface((background.get_width()-200, background.get_height()), 
                          flags=pygame.SRCALPHA)
    dark.fill((50, 50, 50, 0))
    background.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)    
    paused = pygame.image.load("images/paused.png").convert_alpha()
    background.blit(
        paused, ((screen.get_width()-330)/2, screen.get_height()-300))
    screen.blit(background, (0, 0))
    resume_button = game_sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-200), "Resume", (255,255,255))
    menu_button = game_sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-150), "Main Menu", (255,255,255))
    #Buttons in order
    buttons = [resume_button, menu_button]
    #Set up sprite group.
    all_sprites = pygame.sprite.Group(buttons)

    #Sound effects 
    select_sound = pygame.mixer.Sound("sounds/select.ogg")
    ok = pygame.mixer.Sound("sounds/ok.ogg")
    select_sound.set_volume(0.3)
    ok.set_volume(0.3)
    
    # A - Action (broken into ALTER steps)
     
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keep_going = True
    FPS = 30
    #Starting select.
    selected = [buttons[0]]    
     
    # L - Loop
    while keep_going:
     
        # T - Timer to set frame rate
        clock.tick(FPS)
     
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                #Window exit return value from pause to game loop
                return 2
            #Navigate through buttons 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [resume_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [menu_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]
                #Confirming button press on z.
                if event.key == pygame.K_z:
                    keep_going = False
                    ok.play()
                    if selected == [resume_button]:
                        #Retrun resume value
                        return 1
                    elif selected == [menu_button]:
                        #Return menu value
                        return 0                     
                                    
        #Select button highlight
        for select in selected:
            select.set_select()
     
        # R - Refresh display
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()        
        pygame.display.flip()       


def game_over(screen):
    '''This function pauses the game loop with a darker paused frame as 
    background using the screen parameter after the game is over. This 
    function to gives player choices to play again or go back to menu. 
    '''
    
    # E - Entities - background, buttons and sprite group set up
    background = screen
    #dark surface is a special surface that is blited to make background darker.
    dark = pygame.Surface((background.get_width()-200, background.get_height()), 
                          flags=pygame.SRCALPHA)
    dark.fill((50, 50, 50, 0))
    background.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)      
    game_over = pygame.image.load("images/game_over.png").convert_alpha()
    background.blit(
        game_over, ((screen.get_width()-400)/2, screen.get_height()-300))
    screen.blit(background, (0, 0))
    restart_button = game_sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-200), "Restart?", 
        (255,255,255))
    menu_button = game_sprites.Button(
        ((screen.get_width()-200)/2, screen.get_height()-150), "Main Menu", 
        (255,255,255))
    #Buttons in order
    buttons = [restart_button, menu_button]
    all_sprites = pygame.sprite.Group(buttons)

    #Sound effects 
    select_sound = pygame.mixer.Sound("sounds/select.ogg")
    ok = pygame.mixer.Sound("sounds/ok.ogg")
    select_sound.set_volume(0.3)
    ok.set_volume(0.3)
    
    # A - Action (broken into ALTER steps)
     
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keep_going = True
    FPS = 30
    #Starting select.
    selected = [buttons[0]]    
     
    # L - Loop
    while keep_going:
     
        # T - Timer to set frame rate
        clock.tick(FPS)
     
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                #Window exit return value
                return 2
            #Navigate through buttons 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [restart_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [menu_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]
                #Confirming button press on z.
                if event.key == pygame.K_z:
                    keep_going = False
                    ok.play()
                    if selected == [restart_button]:
                        #Return resume value
                        return 1
                    elif selected == [menu_button]:
                        #Return menu value
                        return 0                     
                                    
        #Select button highlight
        for select in selected:
            select.set_select()
     
        # R - Refresh display
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()        
        pygame.display.flip()     
    
def game_intro(screen):
    '''
    This function defines the main menu logic for the game. 
    This function accepts a display parameter to know which surface
    to blit all events.
    '''
    
    # E - Entities - background, buttons and sprite group set up
    background = pygame.image.load("images/title.png").convert()
    screen.blit(background, (0, 0))
    start_button = game_sprites.Button(
        (screen.get_width()-50, screen.get_height()-120), "Start", (166, 166, 166))
    erase_button = game_sprites.Button(
        (screen.get_width()-85, screen.get_height()-80), "Erase Data", (166, 166, 166))
    quit_button = game_sprites.Button(
        (screen.get_width()-40, screen.get_height()-40), "Quit", (166, 166, 166))
    #Buttons in order
    buttons = [start_button, erase_button, quit_button]
    #Set up sprite group.
    all_sprites = pygame.sprite.Group(buttons)
    
    #Sounds
    #Background music
    pygame.mixer.music.load("sounds/Bad Apple Lite.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)
    #Sound effects
    select_sound = pygame.mixer.Sound("sounds/select.ogg")
    ok = pygame.mixer.Sound("sounds/ok.ogg")
    reset = pygame.mixer.Sound("sounds/reset.ogg")
    select_sound.set_volume(0.3)
    ok.set_volume(0.3)
    reset.set_volume(0.3)
    
    # A - Action (broken into ALTER steps)
     
    # A - Assign values to key variables
    clock = pygame.time.Clock()
    keep_going = True
    FPS = 30
    #Starting select.
    selected = [buttons[0]]    
     
        # L - Loop
    while keep_going:
     
        # T - Timer to set frame rate
        clock.tick(FPS)
     
        # E - Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                #Return exit game value.
                return 0
            #Navigate through buttons 
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if selected != [start_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])-1)]]
                if event.key == pygame.K_DOWN:
                    if selected != [quit_button]:
                        select_sound.play()
                        selected = [buttons[(buttons.index(selected[0])+1)]]
                #Confirming button press on z.
                if event.key == pygame.K_z:
                    if selected != [erase_button]:
                        keep_going = False
                        ok.play()
                        if selected == [start_button]:
                            pygame.mixer.music.stop()
                            #Return start game loop value.
                            return 1
                        elif selected == [quit_button]:
                            #Return exit game value. 
                            return 0
                    else:
                        reset.play()
                        #reset highscore
                        save_data = open("data/highscore.txt", 'w')
                        save_data.write(str(0))
                        save_data.close()                        
                                    
        #Select button highlight
        for select in selected:
            select.set_select()
     
        # R - Refresh display
        all_sprites.clear(screen, background)
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()        
        pygame.display.flip()   

def game_loop(screen):
    '''
    This function defines the main game logic for the game. 
    This function accepts a display parameter to know which surface
    to blit all events sprites.
    '''
    
    # ENTITIES - create background and gameover label.
    background = game_sprites.Background()
    
    # Create a list of Joystick objects.
    joysticks = []
    for joystick_no in range(pygame.joystick.get_count()):
        stick = pygame.joystick.Joystick(joystick_no)
        stick.init()
        joysticks.append(stick)  
        
    #Sound - loading and setting volume
    
    #Music
    pygame.mixer.music.load("sounds/Background Music.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    
    #Sound effects.
    paused = pygame.mixer.Sound("sounds/pause.ogg")
    player_death = pygame.mixer.Sound("sounds/player_death.ogg")
    player_shoot = pygame.mixer.Sound("sounds/player_shoot.ogg")
    graze = pygame.mixer.Sound("sounds/graze.ogg")
    point = pygame.mixer.Sound("sounds/point.ogg")
    enemy_death = pygame.mixer.Sound("sounds/enemy_death.ogg")
    life_drop = pygame.mixer.Sound("sounds/get_life.ogg")
    bomb_drop = pygame.mixer.Sound("sounds/get_bomb.ogg")
    bombing = pygame.mixer.Sound("sounds/bomb.ogg")
    bullet_sounds = []
    for sound in range(1,6):
        bullet_sounds.append(pygame.mixer.Sound("sounds/bullet"+
            str(sound)+".ogg"))
    paused.set_volume(0.3)
    player_death.set_volume(0.3)
    player_shoot.set_volume(0.1)
    graze.set_volume(0.3)
    point.set_volume(0.3)
    enemy_death.set_volume(0.4)
    life_drop.set_volume(0.4)
    bomb_drop.set_volume(0.4)
    bombing.set_volume(0.4)
    for bullet_sound in bullet_sounds:
        bullet_sound.set_volume(0.1)
        
    #Player sprite creation, append them in a list.
    player = game_sprites.Player(screen)
    hitbox = game_sprites.Hitbox(screen, player)
    
    # Sprites for: ScoreKeeper label
    score_tab = game_sprites.Score_tab(screen)
    
    #Cloud sprite
    clouds = []
    for cloud in range(4):
        clouds.append(game_sprites.Cloud(screen))
        
    #Enemy spawner sprites
    spawners = []
    for spawner_type in range(2):
        spawners.append(game_sprites.Spawner(screen, spawner_type))
    
    #Initialize sprite groups for better layering
    low_sprites = pygame.sprite.OrderedUpdates(spawners, background, clouds,
        player, hitbox)
    enemy_sprites = pygame.sprite.OrderedUpdates()
    player_bullet_sprites = pygame.sprite.OrderedUpdates()
    enemy_bullet_sprites = pygame.sprite.OrderedUpdates()
    bomb_sprites = pygame.sprite.OrderedUpdates()
    animation_sprites = pygame.sprite.OrderedUpdates()
    drop_sprites = pygame.sprite.OrderedUpdates()
    top_sprites = pygame.sprite.OrderedUpdates(score_tab)
    
    #All sprites groups up, layering with order
    all_sprites = pygame.sprite.OrderedUpdates(low_sprites, enemy_sprites, \
    player_bullet_sprites, enemy_bullet_sprites, animation_sprites, \
    drop_sprites, top_sprites)

    # ASSIGN - assign important variables to start game.
    clock = pygame.time.Clock()
    keep_going = True
    half_mode = False
    difficulty = 0
    limits = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6)]
    boss_limit, common_limit = limits[difficulty] 
    common_enemies = 0
    boss_enemies = 0
    FPS = 30
    frames_passed = 0
    window_exit = 0
    restart = 0
    game_over_frames = 30
     
    # Hide the mouse pointer
    pygame.mouse.set_visible(False)
 
    # LOOP
    while keep_going:
     
        # TIME
        clock.tick(FPS)
     
        # EVENT HANDLING: player use arrow keys
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_going = False
                window_exit = 1

            #Get a list containing boolean values of pressed keys to their
            #position.
            keys_pressed = pygame.key.get_pressed()
            #Exit program on escape
            if keys_pressed[pygame.K_ESCAPE]:
                paused.play()
                pygame.mixer.music.pause()
                option = pause(screen)
                if option == 0 or option == 2:
                    keep_going = False
                if option == 2:
                    window_exit = 1
                pygame.mixer.music.unpause()
            #Movement.
            player.change_direction((0,0))
            if keys_pressed[pygame.K_LEFT]:
                player.change_direction((-1,0))
            if keys_pressed[pygame.K_RIGHT]:
                player.change_direction((1,0))
            if keys_pressed[pygame.K_UP]:
                player.change_direction((0,-1))
            if keys_pressed[pygame.K_DOWN]:
                player.change_direction((0,1))
            #Toggle shoot mode
            if keys_pressed[pygame.K_z] and not player.get_lock():
                player.shoot_mode(1)
            elif not keys_pressed[pygame.K_z]:
                player.shoot_mode(0)
            #Add bomb to sprite if there is no bomb on screen, not locked.
            if keys_pressed[pygame.K_x] and not bomb_sprites and not \
               player.get_lock() and score_tab.get_bombs():
                bombing.play()
                player.set_invincible(2)
                bomb_sprites.add(game_sprites.Bomb(player.get_center()))
                score_tab.bomb_used()
            #Toggle focus mode.
            if keys_pressed[pygame.K_LSHIFT] and not player.get_lock():
                player.focus_mode(1)
                hitbox.set_visible(1)
            elif not keys_pressed[pygame.K_LSHIFT]:
                player.focus_mode(0)
                hitbox.set_visible(0)
                
        #Record frames_passed
        frames_passed += 1
        
        #Difficulty based on frames passed.
        if frames_passed == FPS*30:
            difficulty = 1
        elif frames_passed == FPS*60:
            difficulty = 2
        elif frames_passed == FPS*60*2:
            difficulty = 3
        elif frames_passed == FPS*60*5:
            difficulty = 4

        #Set spawn limits based on difficulty.
        boss_limit, common_limit = limits[difficulty] 
        
        #Set spawn rates of spawner classes based on difficulty.
        for spawner in spawners:
            spawner.set_rate(difficulty)
            
            
        #Player bullet event. Let player shoot.
        if player.get_shoot() and not player.get_cool_rate() and not \
        player.get_lock():
            player_shoot.play()
            player_bullet_sprites.add(player.spawn_bullet())        

        #Enemy bullet/sprites. Hit detection, only if player not invincible
        if not player.get_invincible(): 
            
            #Enemy bullets - player hitbox collision.
            for hit in pygame.sprite.spritecollide(
                hitbox, enemy_bullet_sprites.sprites(), False):
                #Shrink the hitbox rect to detect actual size of hitbox
                if hitbox.rect.inflate(-14,-14).colliderect(hit) and \
                   not player.get_invincible():
                    #Player death events
                    animation_sprites.add(game_sprites.Explosion(
                        player.get_center(), 0))
                    player_death.play()
                    player.reset()
                    score_tab.life_loss()
                    
            #Enemy sprites - hitbox collision
            for enemy in pygame.sprite.spritecollide(
                hitbox, enemy_sprites.sprites(), False):   
                #Shrink the hitbox rect to detect actual size of hitbox
                if hitbox.rect.inflate(-14,-14).colliderect(enemy) and \
                   not player.get_invincible():
                    #Player death events
                    animation_sprites.add(game_sprites.Explosion(
                        player.get_center(), 0))
                    player_death.play()
                    player.reset()
                    score_tab.life_loss()
            
            #Grazing bullets, bullets/player sprite collision - add points.
            for bullet in pygame.sprite.spritecollide(
                player, enemy_bullet_sprites.sprites(), False):  
                if player.rect.inflate(-6,-12).colliderect(bullet) and \
                   not player.get_invincible():
                    #Graze events if bullet can be grazed
                    if not bullet.get_grazed():
                        graze.play()
                        score_tab.add_points(0)
                        bullet.set_grazed(1)
                    
        #Player sprite, drop sprite collision events.
        for drop in  pygame.sprite.spritecollide(
                player, drop_sprites.sprites(), False): 
            drop_type = drop.get_type()
            #Play correct sound
            if drop_type <= 1:
                point.play()  
            elif drop_type == 2:
                life_drop.play()
            elif drop_type == 3:
                bomb_drop.play()
            #Add point, life or bomb count to score tab depedning on type.
            score_tab.add_points((drop_type)+6) #+6 is used for drop points
            drop.kill()
                 
        #Enemy rect and shoot events.
        for enemy in enemy_sprites.sprites():  
            #See if enemy is hit by bullet. Return list of bullet that hit.
            for bullet in pygame.sprite.spritecollide(
                enemy, player_bullet_sprites.sprites(), False):
                #Bullet hits enemy. Animate, damage and kill bullet.
                animation_sprites.add(
                    game_sprites.Explosion(bullet.get_center(), 1))
                # ----> SET DAMAGE (0.5 is very hard, 1 is Medium, 2 is Easy, 3 is Very Easy)
                enemy.damaged(2) # -----> This one
                bullet.kill()
                #Kill enemy if appropriate.
                if enemy.get_hp() <= 0 and not enemy.get_killed():
                    #Play enemy death sound.
                    enemy_death.play()
                    #Set enemy instance killed to true.
                    enemy.set_killed()
                    animation_sprites.add(game_sprites.Explosion(
                        enemy.get_center(), 0))
                    #Drop sprites when enemy killed. Determine #drops.
                    if enemy.get_type() <= 3:
                        drops = 4
                    elif enemy.get_type() > 3:
                        drops = 2
                    #Determine drop type.
                    for drop in range(drops):
                        random_num = random.randrange(15)
                        #3 in 15 chance of droping big points
                        if random_num == 3 or random_num == 7 or \
                           random_num == 12:
                            drop_type = 1
                        #Special drops for only boss types, 1 in 15 chance.
                        elif random_num == 5 and drops == 4:
                            #2 in 3 chance bomb drop, 1 in 3 chance life drop.
                            random_special = random.randrange(3)
                            if random_special == 1:
                                drop_type = 2
                            else:
                                drop_type = 3
                        #Drop type normal if no special drops is called.
                        else:
                            drop_type = 0
                        #Create drop sprite
                        drop_sprites.add(game_sprites.Pick_up(
                            screen, enemy, drop_type))
                    #Add the score of the corresponding enemy killed.
                    score_tab.add_points(enemy.get_type())
           
            #Let enemy shoot if appropriate.
            if not enemy.get_cool_rate() and not enemy.get_down_frames() \
               and not enemy.get_lock():
                #Play bullet sound correpsonding to their bullet type
                bullet_sounds[enemy.get_type()-1].play()
                #Create bullets.
                enemy_bullet_sprites.add(enemy.spawn_bullet(player)) 
        
        #Bomb detection event. See if it hits bullets. Return list of bullets
        for bomb in bomb_sprites.sprites():
            for bullet in pygame.sprite.spritecollide(
                bomb, enemy_bullet_sprites.sprites(), False):
                #See if bomb is too small to detect collision with rim, 
                #use entire area to detect area of bomb.
                #If not to small, use approximate bomb rim area to detect hit 
                #by seeing if it doesn't collide with outside.
                if bomb.get_side() <= 140 or not bomb.rect.inflate(
                    -bomb.get_side()/4,-bomb.get_side()/4).colliderect(bullet):
                    #Animate and kill bullet.
                    animation_sprites.add(
                        game_sprites.Explosion(bullet.get_center(), 0))
                    bullet.kill()    
    
        #Detect enemies, record types on screen.
        common_enemies = 0
        boss_enemies = 0        
        for enemy in enemy_sprites.sprites():
            enemy_type = enemy.get_type()
            if enemy_type <= 3:
                boss_enemies += 1
            else:
                common_enemies += 1
    
        #Enemy spawning event, spawn enemy if appropriate, not pass spawn limit.
        for spawner in spawners:
            if (spawner.get_type() == 1 and boss_enemies < boss_limit) or\
               (spawner.get_type() == 0 and common_enemies < common_limit):    
                spawner.set_lock(0)
                if not spawner.get_spawn_frames():
                    enemy_sprites.add(spawner.spawn_enemy())
            if spawner.get_type() == 1 and boss_enemies == boss_limit:
                spawner.set_lock(1)
            elif spawner.get_type() == 0 and common_enemies == common_limit:
                spawner.set_lock(1)  
                
        #Check to end game when player has no more lives.
        if not score_tab.get_lives():
            #Keep reducing game_over frames for smooth game over transition.
            if game_over_frames > 1:
                game_over_frames -= 1
            #When game over frames are down, call game over menu.
            else:
                pygame.mixer.music.stop()
                restart = game_over(screen)
                keep_going = False
                
        #Update what is in the all_sprites group.
        all_sprites = pygame.sprite.OrderedUpdates(low_sprites, enemy_sprites,
            player_bullet_sprites, enemy_bullet_sprites,
            animation_sprites, bomb_sprites, drop_sprites, top_sprites)
                         
        # REFRESH SCREEN - clear previous sprites, update positions and display
        all_sprites.clear(screen, background.get_surface())
        all_sprites.update()
        all_sprites.draw(screen)       
        pygame.display.flip()  
    
    #Save highscore after game.
    save_data = open("data/highscore.txt", 'w')
    save_data.write(str(score_tab.get_highscore()))
    save_data.close()
    
    #Deciding what to return depending on choice.
    if restart == 1:
        #Start game again, get value returned from next game
        game_value = game_loop(screen)
        #Return whatever is returned in next game loop if it is not 2
        if game_value != 2:
            return game_value
        else:
            #Treat as window exit if next value is 2
            window_exit = 1
    
    #Window exit from game over screen, treat as window exit.
    elif restart == 2:
        window_exit = 1

    #Return to main menu if returning and not window exit.
    if not window_exit:       
        return 1
    #Return quit pygame value if window exit is called.
    else:
        return 0
     
# Call the main function
main()    
