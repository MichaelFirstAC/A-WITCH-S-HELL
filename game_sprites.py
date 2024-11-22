"""Author: Michael
    Description: Creates a module used for the game "A WITCH'S HELL" 
    creating many sprite classes. 
"""

#Import needed module
import pygame, math, random

class Button(pygame.sprite.Sprite):
    '''This is the button class where button sprites are created. The button 
    sprite is used in main to select options given that runs specific 
    functions.'''
    
    def __init__(self, xy_pos, message, colour):
        '''This method initializes the sprite using the xy_pos paramter to 
        set up correct positions in initiation. message parameter used for
        label. Lastly, the colour paramter is used to initiate the starting 
        colour for the label button.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set up instances
        self.__message = message
        self.__font = pygame.font.Font("fonts/Pixeltype.ttf", 40)
        self.__select = 0
        self.__colours = [colour, (255,99,71)]
        self.image = self.__font.render(
            message, 1, (self.__colours[self.__select]))
        self.rect = self.image.get_rect()
        self.rect.center = xy_pos
    
    def set_select(self):
        '''This method sets the select instance to 1 as it is selected in main.
        '''
        
        #Set instance to 1.
        self.__select = 1
    
    def update(self):
        '''This method run automatically called every frame to determine if the 
        button should change colour depending on if it is selected.'''
        
        #Reset colour of label depending on if selected.
        self.image = self.__font.render(
            self.__message, 1, (self.__colours[self.__select]))
        
        #Reset, it will be 1 if it is still selected next frame.
        self.__select = 0
        
class Player(pygame.sprite.Sprite):
    '''The player class sprite. This class sprite is the player model being 
    controlled by the user.'''

    def __init__(self, screen):
        '''This method initializes the sprite using the screen parameter to 
        set boundaries in update.'''

        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set up and load images for animation frames while idle
        self.__station_frames = []
        for index in range(5):
            self.__station_frames.append(pygame.image.load("images/player"
                +str(index)+".png").convert_alpha())
        
        #Load images for animation while turning.
        self.__turn_frames_left = []
        for index in range(5):
            self.__turn_frames_left.append(pygame.image.load(
                "images/player_turn"+str(index)+".png").convert_alpha())   
        
        #Fliped all left turn frames for right turning animation frames.
        self.__turn_frames_right = []
        for frame in self.__turn_frames_left:
            self.__turn_frames_right.append(pygame.transform.flip(frame, 1,0))
            
        #Invisible image, used when invincible
        self.__temp = pygame.image.load("images/temp.png").convert_alpha()

        #Set other instances needed for this class.
        self.__frames = self.__station_frames #Set other instances needed for this class
        self.image = self.__frames[0] #Set other instances needed for this class
        self.rect = self.image.get_rect() #Set other instances needed for this class
        
        #Set player sprite to the center of the bottom of the screen.
        self.rect.center = ((screen.get_width()-200)/2, screen.get_height()- 2*self.rect.height)
        
        self.__index = 0 #For animation image
        self.__frame_refresh = 2 #For animation refresh
        self.__temp_frame_refresh = self.__frame_refresh #for animation refresh
        self.__screen = screen #For boundaries
        self.__dx = 0 #For movement
        self.__dy = 0 #For movement
        self.__diagonal = 1 #For diagonal movement
        self.__focus = 1 #For focus mode
        self.__invincible_frames = 110 #For invincible mode
        self.__lock = 0 #For movement lock
        self.__shoot = 0 #For shooting mode
        self.__cool_rate = 3 #For cool down
        self.__focus_cool_rate = 9 #For cool down
        self.__temp_cool_rate = self.__cool_rate #For cool down
        self.__temp_invincible = 0 #For invincible mode
        
        #Set up spawn
        self.reset()
    
    def change_direction(self, xy_change):
        '''This method takes a xy tuple parameter to change the direction of 
        the player.'''
        
        #Multiply appropriate vectors by a magnitude of 8
        if xy_change[0] != 0: #If the player is moving left or right 
            self.__dx = xy_change[0]*8 #Set the x vector to 8
        elif xy_change[1] != 0: #If the player is moving up or down
            self.__dy = xy_change[1]*8 #Set the y vector to 8
        #No vectors if idle
        else:
            self.__dx = 0
            self.__dy = 0
        
        #Toggle/untoggle diagonal mode when depending on if both value = 1.
        if self.__dx != 0 and self.__dy != 0: #If the player is moving diagonally
            self.diagonal_mode(1) #Set the diagonal mode to 1
        else:
            self.diagonal_mode(0) #Set the diagonal mode to 0
        
    def diagonal_mode(self, mode):
        '''This method toggle/untoggles the diagonal mode depending on the 
        mode parameter (boolean). This is used to ensure consistency
        amongst movement.'''
        
        #change factor used in update to approximately 0.7071.
        #This is used to ensure that the player moves at the same speed
        if mode: #If the player is moving diagonally moving speed is reduced by 30%
            self.__diagonal = ((2.0**0.5)/2.0)
        else: #If the player is moving horizontally or vertically moving speed is normal
            self.__diagonal = 1
            
    def focus_mode(self, mode):
        '''This method toggles/untoggles the focused mode depending on the mode
        parameter (boolean). This is used to toggle between different speeds and
        fire types.'''
        
        #Change focus factor to the correct value depending on mode. 
        if mode: #If the player is focused the player moves slower and shoots a stream of bullets
            self.__focus = 1.75
        else: #If the player is not focused the player moves faster and shoots a single bullet
            self.__focus = 1
    
    def shoot_mode(self, mode):
        '''This method toggles/untoggles the shoot mode depending on the mode
        parameter (boolean). This is used to toggle constant firing and non-
        firing.'''        
        
        #Change boolean value depending 
        self.__shoot = mode

    def spawn_bullet(self):
        '''This method spawns bullets, used in main. This spawns different 
        bullets with different pattern depending on focus type.'''
        
        #If focused, shoot stream of bullet, and reset the cool down with 
        #appropriate cool rate.
        if not self.__focus == 1:
            self.__temp_cool_rate = self.__cool_rate
            return Bullet(self.__screen, self, 0)
        #Unfocused shoots muti-bullets. Resetting with appropriate cool rate.
        else:
            self.__temp_cool_rate = self.__focus_cool_rate
            return [Bullet(self.__screen, self, 1, 60),
                    Bullet(self.__screen, self, 1, 75),
                    Bullet(self.__screen, self, 1, 90),
                    Bullet(self.__screen, self, 1, 105),
                    Bullet(self.__screen, self, 1, 120)]
        
    def reset(self):
        '''This method resets the player to original spawn point. Set up for 
        new spawn.'''
        
        #Reposition player outside of the bottom screen.
        self.rect.center = ((self.__screen.get_width()-200)/2,self.__screen.get_height() + 4*self.rect.height)    
        
        #Set invincible mode for certain frames.
        self.__temp_invincible = self.__invincible_frames
        
        #Disable player shoot mode and focus mode.
        self.__shoot = 0 #Disable player shoot mode
        self.__focus = 1 #Disable player focus mode
        
    def set_invincible(self, frames):
        '''This method sets the player invincible frames to the amount 
        indicated by the frames.'''
        
        #Set invincible frames
        self.__temp_invincible = frames
        
    def get_cool_rate(self):
        '''This method returns the self instance, cool rate. Used in main to 
        see if player can fire.'''
        
        #Return instance value.
        return self.__temp_cool_rate
    
    def get_invincible(self):
        '''This method returns the self instance, invincible. Used to detect 
        if bullet can harm player in main.'''
        
        #Return instance value.
        return self.__temp_invincible
    
    def get_lock(self):
        '''This method returns the self instance, lock. Used to determine if 
        user can control player sprite.'''
        
        #Return instance.
        return self.__lock
        
    def get_shoot(self):
        '''This method returns the self instance, shoot mode. Used in main to 
        see if player can fire.'''        
        
        #Return instance.
        return self.__shoot
    
    def get_center(self):
        '''This method returns the self instance, center. Used in respawn and 
        positioning.'''           
        
        #Return instance.
        return self.rect.center
        
    def update(self):
        '''Update method used to update animation frames, cooldowns, and 
        movement.'''
            
        #Invincible frames tick and image mannipulation to invisible.
        if self.__temp_invincible > 0:
            #Movement lock while invincible for 30 frames. Lock player.
            if self.__temp_invincible >= self.__invincible_frames-50:
                self.__lock = 1 #Lock player
                self.__dx, self.__dy = 0,0 #Stop player movement
                #Move up only 
                self.__dy = -5
            #Unlock player movement after 30 frames.
            else:
                self.__lock = 0
            
            #Stop movement from lock when end position reached.
            if not self.__lock and self.__dy == -5:
                self.__dy = 0
        
        #Switch to appropriate animation frames (stationary or turning).
        if self.__dx < 0: #If the player is moving left
            self.__frames = self.__turn_frames_left
        elif self.__dx > 0: #If the player is moving right
            self.__frames = self.__turn_frames_right
        else: #If the player is not moving
            self.__frames = self.__station_frames
            
        #Update sprite animation frames
        if self.__temp_frame_refresh > 0:
            self.__temp_frame_refresh -= 1
        else: #If the player is not moving
            self.__temp_frame_refresh = self.__frame_refresh #Set the frame refresh to 2
            self.__index += 1 #Increment the index by 1
            self.image = self.__frames[self.__index % len(self.__frames)] #Set the image to the current frame
            
        #Invincible frames tick and image mannipulation to invisible.
        if self.__temp_invincible > 0: #If the player is invincible
            self.__temp_invincible -= 1 #Increment the index by 1
            #Every 15 frames and every 3 frames close by will be invisible.
            if self.__temp_invincible % 15 <= 6 and \
            self.__temp_invincible % 15 > 2:
                self.image = self.__temp #Set the image to the invisible image
                
        #Update sprite position using boundaries.
        #Horizontal position.
        if ((self.rect.left > 0) and (self.__dx < 0)) or\
            ((self.rect.right < self.__screen.get_width()-200) and\
            (self.__dx > 0)): #If the player is within the left and right boundaries
            self.rect.centerx += self.__dx/self.__focus*self.__diagonal #Move the player sprite horizontally
        #Vertical position
        if ((self.rect.top > 0) and (self.__dy < 0)) or\
                    ((self.rect.bottom < self.__screen.get_height()) and\
                    (self.__dy > 0)): #If the player is within the top and bottom boundaries
            self.rect.centery += self.__dy/self.__focus*self.__diagonal #Move the player sprite vertically
            
        #Cool down control.
        if self.__temp_cool_rate > 0 : #If the player is not able to shoot
            self.__temp_cool_rate -= 1 #Decrement the cool down by 1
        
class Hitbox(pygame.sprite.Sprite):
    '''The sprite for the player hit box sprite. Used in bullet detection.'''
    
    def __init__(self, screen, player):
        '''This method initializes the sprite using the player sprite.'''
            
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Image loading
        self.__hitbox = pygame.image.load("images/hitbox.png")\
            .convert_alpha() #Load the hitbox image
        self.__temp = pygame.image.load("images/temp.png").convert_alpha() #Load the temp image
        
        #Instance value setting.
        self.image = self.__hitbox #Load the hitbox image
        self.rect = self.image.get_rect() #Get the rectangle of the hitbox image
        self.__player = player #Set the player sprite
        self.__screen = screen #Set the screen
    
    def position(self, player):
        '''This method uses the player sprite instance to reposition itself.'''
        
        #Mutate self center.
        self.rect.center = player.rect.center
        
    def set_visible(self, visible):
        '''This method uses the visible parameter (boolean), to set image from
        visible to invisible.'''
        
        #Change image depending on if visible
        if visible: #If visible
            self.image = self.__hitbox #Set the image to the hitbox image
        else: #If invisible
            self.image = self.__temp #Set the image to the temp image

    def update(self):
        '''This sprite updates the position of the hitbox sprite. using a
        method.'''
        
        #Position hit box in the center of the player sprite.
        self.position(self.__player)
        
        #Set invisible if outside bottom of screen - player reset property
        if self.rect.top > self.__screen.get_height(): #If invisible
            self.set_visible(0) #Set the visible to 0
        
        
class Bomb(pygame.sprite.Sprite):
    '''This class creates a player bomb sprite. Used to detect and kill bullets
    upon detection.'''
    
    def __init__(self, xy_position):
        '''This method initializes the class using the xy parameter 
        (tuple position) to start bomb at a point.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)        
        
        #Set instance values.
        self.__side = 20 #Set the side to 20
        self.image = pygame.Surface((self.__side,self.__side)) #Set the image to a surface
        self.rect = self.image.get_rect() #Get the rectangle of the image
        self.__start = xy_position #Set the start position to the xy position
        self.rect.center = xy_position #Set the center of the rectangle to the xy position
        self.__finish_raidus = 700 #Set the finish
        self.__expand = 30 #Set the expand factor
        self.__width = 3 #Set the width
        
    def get_side(self):
        '''This method returns the instance side. Used in accurate rect 
        detection in main.'''
        
        #Return instance.
        return self.__side

    def update(self):
        ''''This method updates the bomb by increasing the size, the width of 
        the circle drawn and to seemingly animate the bomb to expand off the 
        screen.'''
        
        #If not finished expanding, continue.
        if self.__side/2 < self.__finish_raidus:
            self.__side += self.__expand
            self.__width += 1
            
            #Create new surface with the new size
            self.image = pygame.Surface((self.__side,self.__side))
            
            #Make background invisible
            self.image.set_colorkey((0,0,0))
            
            #Draw circle in surface.
            pygame.draw.circle(self.image, (255,255,255), (self.__side//2, self.__side//2), self.__side//2, self.__width)
            
            #Reset rect for proper collision.
            self.rect = self.image.get_rect()
            self.rect.center = self.__start
            
        #If done, kill bomb.
        else:
            self.kill()
            
class Enemy(pygame.sprite.Sprite):
    '''The Enemy sprite class that shoots bullets at player with different 
    patterns depending on the enemy type.'''
    
    def __init__(self, screen, enemy_type = 1):
        '''This method initializes the enemy sprite with correct properties 
        according to enemy type parameter. The screen parameter is used in for
        boundaries in update.'''
    
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set up and load animation frames.
        self.__unlock_frames = []
        for index in range(4):
            #Load frames of enemy type sprites.
            self.__unlock_frames.append(pygame.image.load("images/fairy"+str(enemy_type)+"_"+str(index)+".png").convert_alpha())
        
        #Load frames of turning animation for boss type enemies.
        self.__lock_frames_right = []
        self.__lock_frames_left = []   
        if enemy_type < 4:
            #Create right turning frames from image files.
            for index in range(4):
                #Load frames of enemy type sprites.
                self.__lock_frames_right.append(pygame.image.load("images/turn"+str(enemy_type)+"_"+str(index)+".png").convert_alpha())
            
            #Left turning frames created by fliping right turning frames
            for frame in self.__lock_frames_right:
                #Flip frames to create left turning frames.
                self.__lock_frames_left.append(pygame.transform.flip(frame,1, 0))        
            
        #Setting default properites
        self.__frames = self.__unlock_frames #Set default frames
        self.image = self.__frames[0] #Load image file
        self.__down_frames = 0 #Set down frames
        self.__active_frames = 0 #Set active frames
        self.__cool_rate = 0 #Set cool rate
        self.__dx = 0 #Set x vector
        self.__dy = 0 #Set y vector
        self.__hp = 0 #Set hp value
        self.__degs_change = 0 #Set degrees change
        self.rect = self.image.get_rect() #Get the rectangle of the image
        self.rect.center = (400-50*enemy_type, 340-50*enemy_type) #Set the center of the rectangle
        self.__screen = screen #Set the screen
        self.__target_degs = None #Set the target degrees
        self.__target_y = screen.get_height()+self.rect.height #Set the target y
        self.__enemy_type = enemy_type #Set the enemy type
        self.__index = 0 #Set the index of the enemy sprite
        self.__frame_refresh = 2 #Set the frame
        self.__images = 4 #Set the images
        self.__lock = 0 #Set the lock mode
        self.__killed  = 0 #Set the killed mode
        
        #Setting special enemy instance values depending on enemy type.
        #enemy 1-2 are common types.
        #enemy 3-5 are bosses.
        if enemy_type == 1: #If the enemy type is 1
            self.__down_frames = 60
            self.__active_frames = 60
            self.__cool_rate = 5
            self.__hp = 35
        elif enemy_type == 2: #If the enemy type is 2
            self.__down_frames = 30
            self.__active_frames = 40
            self.__cool_rate = 10
            self.__hp = 40  
        elif enemy_type == 3: #If the enemy type is 3
            self.__down_frames = 0
            self.__active_frames = 12
            self.__cool_rate = 4
            self.__hp = 45
            self.__degs_change = 6
        elif enemy_type == 4: #If the enemy type is 4
            self.__down_frames = 60
            self.__active_frames = 15
            self.__cool_rate = 3
            self.__hp = 10 
        elif enemy_type == 5: #If the enemy type is 5
            self.__down_frames = 30
            self.__active_frames = 30
            self.__cool_rate = 15
            self.__hp = 15              
        
        #Set up initial spawn position
        self.setup()
        
        #Set temps used in countdowns.
        self.__temp_down_frames = self.__down_frames #Down frames
        self.__temp_frame_refresh = self.__frame_refresh #Current frame
        self.__temp_active_frames = self.__active_frames #Active frames
        self.__temp_cool_rate = self.__cool_rate #Cool rate
        
    def setup(self):
        '''This method sets up the sprite when it spawns. This method decides 
        where the sprite spawns, and where it goes.'''
        
        #Spawn location setting.
        x_pos = random.randrange(self.rect.width,self.__screen.get_width()-201-self.rect.width) #Set the x position
        y_pos = 0-self.rect.height #Set the y position
        self.rect.center = (x_pos, y_pos) #Set the center of the rectangle
        
        #Static target position for boss type sprites.
        if self.__enemy_type < 4:
            target_x = random.randrange(100, self.__screen.get_width()-201-self.rect.width, 100) #Set the x position
            target_y = random.randrange(100, self.__screen.get_height()-229, 50) #Set the y position
            
            #Get the degrees between the target position and starting position.
            degs = self.calc_degs(target_x,target_y)
            #Get the appropriate vector movement according to degrees.
            self.__dx = math.cos(math.radians(degs)) * 5
            self.__dy = -(math.sin(math.radians(degs)) * 5)   
            
            #Save the target y position.
            self.__target_y = target_y
            
            #Disable shooting at start when moving to target position.
            self.__lock = 1 
            
        #Common type sprites randomly goes down screen.
        elif self.__enemy_type >= 4:
            self.__dx = 1
            self.__dy = 2
            #Change direction when colliding with boundary.
            if x_pos > (self.__screen.get_width()-200)/2:
                self.__dx = -self.__dx
        
    def spawn_bullet(self, target):
        '''This method accepts a target parameter (a sprite) and use it to 
        spawn/return bullets. The pattern will vary depending on the enemy 
        types.'''
        
        #Get degrees using the target and the shooter.
        degs = self.calc_degs(target.rect.centerx, target.rect.centery) 
        
        #Type 1, fire 1 bullet that tracks in the direction of the target 
        #with some variation.
        if self.__enemy_type == 1:
            self.__target_degs = degs #Set the target degrees to the degrees of the target position
            vary = random.randrange(-10, 26, 2) #Set the variation to random values between -10 and 26 with a step of 2
            self.__target_degs += vary #Add the variation to the target degrees 
            self.__temp_cool_rate = self.__cool_rate #Set the cool rate to the normal cool rate
            return Bullet(self.__screen, self, self.__enemy_type+1,self.__target_degs) #Return the bullet
        
        #Type 2, fire three bullets in a triple spread pattern towards target 
        #with little variation.
        elif self.__enemy_type == 2:
            if self.__target_degs == None: #Check if the target degrees is None
                self.__target_degs = degs #Set the target degrees to the degrees of the target position
                vary = random.randrange(-2, 12, 2) #Set the variation to random values between -2 and 12 with a step of 2
                self.__target_degs += vary #Add the variation to the target degrees
            self.__temp_cool_rate = self.__cool_rate #Set the cool rate to the normal cool rate
            
                    #Return the bullets in a spread pattern towards the target position
            return [Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs-50), 
                    Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs-25),
                    Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs),
                    Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs+25),
                    Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs+55)]
        
        #Type 3, Fire four bullets in a 90 degree gap each. The degree of 
        #direction will change and rotate as frames pass by.
        elif self.__enemy_type == 3:
            if self.__target_degs == None: #Check if the target degrees is None
                self.__target_degs = 0
            factor = random.randrange(1,4,2)
            #Check if the target degrees is not 0 and the degrees change is less than 0
            if self.__target_degs < 0 and self.__degs_change < 0: 
                self.__degs_change = 9 * factor
            #Check if the target degrees is greater than 180 and the degrees change is greater than 0
            elif self.__target_degs > 180 and self.__degs_change > 0:
                self.__degs_change = -9 * factor
            self.__target_degs += self.__degs_change #Add the degrees change to the target degrees
            self.__temp_cool_rate = self.__cool_rate #Set the cool rate to the normal cool rate
            # Return the bullets in a 90 degree gap each towards the target position
            return [Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs),
                    Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs+90),
                    Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs+180),
                    Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs+270)]
        
        #Type 4, fire at target will a lot of variation in direction.
        elif self.__enemy_type == 4:
            self.__target_degs = degs #Set the direction of the target
            vary = random.randrange(-16, 30, 1) #Set the direction variation
            self.__target_degs += vary #Set the direction variation
            self.__temp_cool_rate = self.__cool_rate #Set the cool rate to the normal cool rate
            # Return the bullet with a lot of variation in direction
            return Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs)     
        
        #Type 5, spread bullets in all directions, 60 degrees gap.
        elif self.__enemy_type == 5:
            #Set the target degrees to random values between 0 and 360 with a step of 15
            self.__target_degs = random.randrange(0, 360, 15) 
            bullets = [] #Set the bullets to an empty list
            for extra_degs in range(0, 360, 60): #Loop through the range of 0 to 360 with a step of 60
                #Add the extra degrees to the target degrees and append the bullet to the list.
                bullets.append(Bullet(self.__screen, self, self.__enemy_type+1, self.__target_degs+extra_degs))             
            self.__temp_cool_rate = self.__cool_rate #Set the cool rate to the normal cool rate
            return bullets
            
    def calc_degs(self, target_x, target_y):
        '''This method accepts the target's x and y coordinates to get the 
        degrees between self and target. The degree is then returned.'''
        
        #Get the differences in xy values.
        delta_x = float(target_x - self.rect.centerx)
        delta_y = float(target_y - self.rect.centery)
        
        #Get radians from delta values using atan2. 
        rads = math.atan2(-delta_y, delta_x) #-delta y,coordinates are reversed.
        
        #Only rads in range degrees 0 - 360
        rads %= 2 * math.pi
        
        #Convert and Return radians to degrees for easy pattern mannipulation.
        return math.degrees(rads)                
        
    def damaged(self, damage):
        '''This method takes a damage parameter (integer). The damage parameter
        is used to decrease enemy/class health.'''
        
        #Mutate hp instance.
        self.__hp -= damage    
        
    def set_killed(self):
        '''This method mutates the killed instance to 1 to inform that the 
        sprite is already killed. This makes it so that the sprite doesn't 
        die mutiple times.'''
        
        #Set instance.
        self.__killed = 1
        
    def get_killed(self):
        '''This method returns the killed instance to inform main if sprite 
        is already killed.'''
        
        #Return instance.
        return self.__killed    
            
    def get_cool_rate(self):
        '''This method returns the cool rate of the enemy. Used in main to see 
        when enemy can fire.'''
        
        #Return instance.
        return self.__temp_cool_rate
    
    def get_down_frames(self):
        '''This method returns the down frames of the enemy. Used to see when 
        the enemy can fire in main.'''
        
        #Return instance
        return self.__temp_down_frames
    
    def get_lock(self):
        '''This method returns the lock mode value. Used to see if enemy can 
        shoot.'''
        
        #Return instance
        return self.__lock
        
    def get_hp(self):
        '''This method returns the hp of the enemy. Used to see when 
        the enemy can be deleted in main.'''        
        
        #Return instance.
        return self.__hp
    
    def get_center(self):
        '''This method returns the down frames of the enemy. Used to position 
        sprites.'''        
        
        #Return instance.
        return self.rect.center
    
    def get_type(self):
        '''This method returns the enemy type to determine numbers of types on 
        screen in main.'''
        
        #Return instance.
        return self.__enemy_type
    
    def update(self):
        '''This method updates what happens to the enemy class as frames passes 
        by. This method kills, moves, animates, and controls cool down of 
        enemy class.'''
        
        #Decide to kill if enemy dies.
        if self.__killed or self.rect.top > self.__screen.get_height():
            self.kill()
        
        #While turning load appropriate turning frames 
        if self.__lock and int(self.__dx) > 0:
            self.__frames = self.__lock_frames_right
        elif self.__lock and int(self.__dx) < 0:
            self.__frames = self.__lock_frames_left
        else:
            self.__frames = self.__unlock_frames
        
        #Animate frames, refresh counter
        if self.__temp_frame_refresh > 0:
            self.__temp_frame_refresh -= 1
        else:
            self.__temp_frame_refresh = self.__frame_refresh
            self.__index += 1
        self.image = self.__frames[self.__index % self.__images]
        
        #Tick cool rate if appropriate.
        if self.__temp_cool_rate > 0 and self.__lock != 1:
            self.__temp_cool_rate -= 1
        
        #Reset down frames and active frames to original.
        if self.__temp_active_frames == 0 == self.__temp_down_frames:
            self.__temp_down_frames = self.__down_frames
            self.__temp_active_frames = self.__active_frames
            
            #Set target degrees to none as appropriate to type 2 pattern
            if self.__enemy_type == 2:
                self.__target_degs = None
        
        #Tick down frames and active frames if appropriate.
        #Lock enemy movement when active frames are not 0.
        if self.__temp_down_frames > 0 and self.__lock != 1: 
            self.__temp_down_frames -= 1
        if self.__temp_active_frames > 0 and self.__temp_down_frames == 0:
            self.__temp_active_frames -= 1
    
        #Change x vector when colliding with boundary for opposite direction.
        if self.rect.left <= 0 and self.__dx < 0:
            self.__dx = abs(self.__dx)
        elif self.rect.right >= self.__screen.get_width()-200 and self.__dx > 0:
            self.__dx = -self.__dx
            
        #move class/sprite according to vectors.
        self.rect.centerx += self.__dx
        
        #Change y vector when colliding with boundary for opposite direction.
        if not self.rect.centery >= self.__target_y:
            self.rect.centery += self.__dy
        else:
            self.__dx = 0
            self.__dy = 0
            self.__lock = 0
        
class Explosion(pygame.sprite.Sprite):
    '''This class creates a Explosion animation depending on type.'''
    
    def __init__(self, xy_position, explosion_type):
        '''This method initializes the class by using paramters starting 
        position and type. The starting position is used as spawn point and
        explosion type is used to load appropriate image.
        '''
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)    
        
        #Set up and load frames depending on type
        self.__frames = []
        if explosion_type == 0:
            for num in range(4):
                #Load frames of enemy type sprites.
                self.__frames.append(pygame.image.load("images/death"+str(num)+".png").convert_alpha())
        elif explosion_type == 1:
            for num in range(3):
                #Load frames of enemy type sprites.
                self.__frames.append(pygame.image.load("images/burst"+str(num)+".png").convert_alpha())
                
        #Set up instances.
        self.image = self.__frames[0] #Load image
        self.rect = self.image.get_rect() #Get rectangle
        self.rect.center = xy_position #Set center
        self.__frame_refresh = 1 #Set frame refresh
        self.__temp_refresh = self.__frame_refresh #Set temp refresh
        self.__index = 0 #Set index
    
    def update(self):
        '''Update class as frames passes by. Control frame refresh, new frame
        and kill.'''
        
        #Frame tick refresh
        if self.__temp_refresh > 0:
            self.__temp_refresh -= 1
            
        #Kill after animation completes.
        else:
            if self.__index >= len(self.__frames)-1:
                self.kill()
            #Next frame if appropriate frames pass by.
            else:
                self.__index += 1 #Increment the index by 1
                self.image = self.__frames[self.__index] #Set the image to the current frame
            self.__temp_refresh = self.__frame_refresh #Set the temp refresh to the frame refresh
            
class Bullet(pygame.sprite.Sprite):
    '''This is the Bullet class sprite that creates a bullet that is used to 
    hit the player or the enemies. The direction will vary on degrees passed in.
    '''
    
    def __init__(self, screen, shooter, shoot_type, degs = None):
        '''This method initializes the bullet sprite using parameters such 
        as screen, shooter of bullet, shoot type, and degrees.'''
    
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Load appropriate image for bullet depending on shoot type.
        self.image = pygame.image.load("images/bullet"+str(shoot_type)+".png").convert_alpha()
        
        #Set up default values.
        self.rect = self.image.get_rect() #Get the rectangle of the image 
        self.rect.center = shooter.rect.center #Set the center of the rectangle to the shooter's center
        self.__screen = screen #Set the screen
        self.__dx = 0 #Set the x vector
        self.__dy = 0 #Set the y vector
        self.__grazed = 0 #Set the grazed mode
        self.__graze_frames = 10 #Set the graze frames
        self.__shoot_type = shoot_type #Set the shoot type
        self.__temp_graze = self.__graze_frames #Set the temp graze
        
        #Set unique bullet speed and direction depending on shoot type.
        if shoot_type == 0:
            self.__dy = -20
        elif shoot_type ==1:
            self.__dx = math.cos(math.radians(degs)) * 20
            self.__dy = -(math.sin(math.radians(degs)) * 20)
        elif shoot_type == 2:
            self.__dx = math.cos(math.radians(degs)) * 6
            self.__dy = -(math.sin(math.radians(degs)) * 6)
        elif shoot_type ==3:
            self.__dx = math.cos(math.radians(degs)) * 6
            self.__dy = -(math.sin(math.radians(degs)) * 6)    
        elif shoot_type ==4:
            self.__dx = math.cos(math.radians(degs)) * 6
            self.__dy = -(math.sin(math.radians(degs)) * 6)  
        elif shoot_type == 5:
            self.__dx = math.cos(math.radians(degs)) * 4
            self.__dy = -(math.sin(math.radians(degs)) * 4)           
        elif shoot_type == 6:
            self.__dx = math.cos(math.radians(degs)) * 4
            self.__dy = -(math.sin(math.radians(degs)) * 4)
            
    def set_grazed(self, mode):
        '''This method sets it so that the bullet is grazed.'''
        
        #Mutate grazed to true.
        self.__grazed = mode
            
    def get_center(self):
        '''This method returns the center instance. Used in main for sprite
        positioning.'''
        
        #Return instance.
        return self.rect.center
    
    def get_grazed(self):
        '''This method returns the grazed instance (boolean). Used in main 
        for sprite positioning.'''
        
        #Return instance.
        return self.__grazed
        
    def update(self):
        '''This method will be called automatically to reposition the
        bullet sprite on the screen.'''
            
        #Reposition
        self.rect.centery += self.__dy  
        self.rect.centerx += self.__dx
        
        #Graze reset
        if self.__grazed == 1:
            self.__temp_graze -= 1
            if self.__temp_graze == 0:
                self.__grazed = 0
                self.__temp_graze = self.__graze_frames
            
        #Kill bullet if out of screen for effciency.
        if (0 >= self.rect.bottom or self.rect.top >= 
            self.__screen.get_height()) or (0 >= self.rect.right or self.rect.left >= self.__screen.get_width()-200):
            self.kill()
            
class Spawner(pygame.sprite.Sprite):
    '''This class is the spawner class which determines when to spawn a type of
    enemy as frames pass by.'''
    
    def __init__(self, screen, spawner_type):
            '''This method initializes the class with screen parameter (used to 
            spawn enemy) and the type parameter (value). Determines if 
            common enemy or boss enemy can be spawned.'''
            
            # Call the parent __init__() method
            pygame.sprite.Sprite.__init__(self)
        
            self.image = pygame.Surface((0,0)) #Set the image to a surface
            self.rect = self.image.get_rect() #Get the rectangle of the image
            self.__type = spawner_type #Get the type of enemy
            self.__screen = screen #Get the screen
            self.__lock = 0 #Set the lock mode
            self.__spawn_types = [] #Set the spawn types to an empty list
            
            #Set up instance values depending on type.
            #Common type spawner
            if self.__type == 0:
                self.__spawn_frames = 150
                self.__spawn_range = [4, 6]
            #Boss type spawner
            elif self.__type == 1:
                self.__spawn_frames = 300
                self.__spawn_range = [1, 4]
            self.__temp_frames = self.__spawn_frames
    
    def spawn_enemy(self):
        '''Spawn enemy if appropriate.'''
        
        #Reset temp.
        self.__temp_frames = self.__spawn_frames
        
        #Spawn appropriate enemy depending on type
        enemy_type = random.randrange(self.__spawn_range[0], self.__spawn_range[1])
        return Enemy(self.__screen, enemy_type)       

    def set_lock(self, mode):
        '''This method sets the instance lock between boolean values. 
        Determines when to countdown spawn time.'''
        
        #Set instance to boolean.
        self.__lock = mode
        
    def set_rate(self, difficulty):
        '''This method changes the spawn rate depending on its own spawn type 
        and difficulty of the game. This method also changes the range of 
        enemies that a spawner can summon depending on difficulty.'''
        
        #Common spawn type, decrease spawn rate by 15 frames each difficulty.
        if self.__type == 0:
            self.__spawn_frames = 150 - (difficulty*15)
            #Different enemy range in common spawner depending on difficulty.
            if difficulty == 0 or difficulty == 1:
                self.__spawn_range = [4,5]
            elif difficulty == 2:
                self.__spawn_range = [4,6]
        #Boss spawn type, decrease spawn rate by 30 frames each difficulty.
        elif self.__type == 1:
            self.__spawn_frames = 300 - (difficulty*30)    
            #Different enemy range in boss spawner depending on difficulty.
            if difficulty == 0:
                self.__spawn_range = [1,2]
            elif difficulty == 1:
                self.__spawn_range = [1,3]
            elif difficulty == 3:
                self.__spawn_range = [1,4]
    
    def get_spawn_frames(self):
        '''This method returns the instance temp_frames to determine if spawn 
        is possible in main.'''
        
        #Return instance.
        return self.__temp_frames
    
    def get_type(self):
        '''This method returns the instance type to determine if which limit 
        in main should be looked at.'''        
            
        #Return instance.
        return self.__type
    
    def update(self):
        '''Tick down spawn time if the spawner is not locked.'''
        
        if not self.__lock:
            if self.__temp_frames >= 0:
                self.__temp_frames -= 1
                
class Pick_up(pygame.sprite.Sprite):
    '''The pick up class is used to spawn points, live and bomb drops to 
    enhance gameplay in main.'''
    
    def __init__(self, screen, enemy, drop_type):
            '''This method initializes the pick class using the screen parameter 
            as bounaries, sprite to get spawn position and drop_type.'''
            
            # Call the parent __init__() method
            pygame.sprite.Sprite.__init__(self)
            
            #Set screen, drop type, and rate of speed update
            self.__screen = screen
            self.__type = drop_type
            self.__speed_frames = 5
            self.__temp_speed = self.__speed_frames
            
            #Image loading 
            self.image = pygame.image.load("images/drop"+str(self.__type)+".png").convert_alpha()
            self.rect = self.image.get_rect()
            
            #Rect setting.
            self.rect = self.image.get_rect()
            self.rect.center = enemy.rect.center
            
            #Randomized initial speeds of drop
            self.__dx = random.randrange(-3,4)
            self.__dy = random.randrange(-2,3)            
            
    
    def get_type(self):
        '''This method returns the self instance type to be passed in to score 
        tab when colliding with player in main.'''
        
        #Return instance.
        return self.__type
    
    def update(self):
        '''This method is called automatically at the end of every frame to 
        update the sprite.'''

        #Kill bullet if out of bottom for effciency.
        if (self.rect.top >= self.__screen.get_height()):
            self.kill()        
        
        #Update speed if appropriate
        if self.__temp_speed == 0:
            #If x velocity is not 0 yet, get closer to it by 1.
            if self.__dx != 0:
                self.__dx -= (self.__dx / abs(self.__dx))
            
            #If y velocity is not 3 yet, get closer to it by 1.
            if self.__dy < 3:
                self.__dy += 1
            elif self.__dy > 3:
                self.__dy -= 1
            
            self.__temp_speed = self.__speed_frames
            
        else:
            self.__temp_speed -= 1
            
        #Update position using vectors.
        self.rect.centerx += self.__dx
        self.rect.centery += self.__dy
        
        
class Score_tab(pygame.sprite.Sprite):
    '''The score tab class used to keep track of score, highscore, lives, and
    bombs.'''
    
    def __init__(self, screen):
        '''This method initializes the class with appropriate parameters.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Open data file for highscore.
        try:
            #Open, read highscore and save.
            load_data = open("data/highscore.txt", 'r')
            self.__highscore = int(load_data.read())
            #Close data file.
            load_data.close()            
        
        #If file error, just set highscore to 0.
        except IOError and ValueError: 
            #Brand new highscore.
            self.__highscore = 0
            
        #Load image as main surface.
        self.image = pygame.image.load("images/score_tab.png").convert()     
        
        #Life frames image loading
        self.__life_frames = []
        for frame in range(2):
            self.__life_frames.append(pygame.image.load("images/life"+str(frame)+".png").convert_alpha())         
        
        #Bomb frames image loading
        self.__bomb_frames = []
        for frame in range(2):
            self.__bomb_frames.append(pygame.image.load("images/bomb"+str(frame)+".png").convert_alpha())         
        
        #Set default instances.
        self.rect = self.image.get_rect() #Get the rectangle of the image
        self.rect.center = (screen.get_width()-self.rect.width/2,\
                            screen.get_height()/2)
        self.__screen = screen #Set the screen
        self.__font = pygame.font.Font("fonts/Pixeltype.ttf", 40) #Set the font
        self.__score = 0 #Set the initial score
        self.__scores = ["HIGHSCORE", ("%10s" %(str(self.__highscore))).replace(" ", "0"),
                        "SCORE",("%10s" %(str(self.__score))).replace(" ", "0")] #Set the scores
        self.__score_labels = [] #Set the score labels
        self.__lives = 2 #Set the initial lives
        self.__bombs = 1 #Set the initial bombs
        self.__stats = ["LIVES", "BOMBS"] #Set the stats
        self.__stat_labels = [] #Set the stat labels
        self.__score_colour = (255,255,255) #Set the colour
        self.__stat_colour = (255,255,255) #Set the colour
        self.__colour_frames = 15 #Set the colour frames
        self.__temp_colour_frames = self.__colour_frames #Set the temp colour frames
        
    def add_points(self, point_type):
        '''This method add to the points value depending on the type of added 
        points. The type determines how much points are added'''
        
        #Grazing points
        if point_type == 0:
            self.__score += 1
        #Enemy type based points 1-5
        elif point_type == 1:
            self.__score += 30
        elif point_type == 2:
            self.__score += 35
        elif point_type == 3:
            self.__score += 50
        elif point_type == 4:
            self.__score += 10
        elif point_type == 5:
            self.__score += 15
        #Drop type based points
        elif point_type == 6:
            self.__score += 5
        elif point_type == 7:
            self.__score += 10
        #Life and bomb drops. If full capacity points are given instead.
        elif point_type == 8:
            if self.__lives < 3:
                self.__lives += 1
            else:
                self.__score += 100
        elif point_type == 9:
            if self.__bombs < 3:
                self.__bombs += 1
            else:
                self.__score += 50
            
    def life_loss(self):
        '''This method mutates the lives instance by decreasing it by 1.'''
                
        #Decrease lives by 1 after death.
        self.__lives -= 1   
        self.reset()
    
    def reset(self):
        '''This method resets the bomb count after successful respawn.'''
        
        #Reset bombs to 1 if game not over yet.
        if self.__lives != 0:
            self.__bombs = 1
    
    def bomb_used(self):
        '''This method mutates the bombs instance by decreasing it by 1.'''
                    
        #Decrease lives by 1 after death.
        self.__bombs -= 1     
            
    def get_highscore(self):
        '''This method returns the instance highscore to be saved in main.'''
        
        #Return instance.
        return self.__highscore
    
    def get_lives(self):
        '''This method returns the instance lives to be read in main.'''
        
        #Return instance.
        return self.__lives
    
    def get_bombs(self):
        '''This method returns the instance lives to be read in main.'''
        
        #Return instance.
        return self.__bombs
            
    def update(self):
        '''This method is called once per frame to update the score tab.'''
        
        #Compare scores, flash colours at constant rate if score is highscore.
        if self.__score >= self.__highscore:
            self.__highscore = self.__score
            if self.__temp_colour_frames > 0:
                self.__temp_colour_frames -=1
            if self.__temp_colour_frames == 0:
                if self.__score_colour == (255,255,255):
                    self.__score_colour = (255,99,71)
                else:
                    self.__score_colour = (255,255,255)
                self.__temp_colour_frames = self.__colour_frames      
        
        #Refresh scores for refreshed labels
        self.__scores = ["HIGHSCORE", ("%10s" %(str(self.__highscore))).replace(" ", "0"),
                        "SCORE",("%10s" %(str(self.__score))).replace(" ", "0")]        
        
        #Reset score labels
        self.__score_labels = []   
        self.__stat_labels = []  
        
        #Render all score labels
        for score in self.__scores:
            label = self.__font.render(score, 1, (self.__score_colour)) 
            self.__score_labels.append(label)
            
        #Render all stat labels
        for stat in self.__stats:
            label = self.__font.render(stat, 1, (self.__stat_colour)) 
            self.__stat_labels.append(label)        
                    
        #Blit image on to surface. 
        self.image = pygame.image.load("images/score_tab.png").convert()
        
        #Blit labels accordinging to their y position.
        y_pos = -20
        for label_num in range(len(self.__score_labels)):
            if label_num %2 == 0:
                y_pos += 50
            else:
                y_pos += 25
            self.image.blit(self.__score_labels[label_num], (10,y_pos))   
        
        y_pos = 235
        for label_num in range(len(self.__stat_labels)):
            y_pos += 75          
            self.image.blit(self.__stat_labels[label_num], (10,y_pos))  
        
        #Blit 3 life and bomb images with appropriate shade depending on amount.
        x_pos = 0
        for num in range(1, 4):
            if self.__lives >= num: 
                self.image.blit(self.__life_frames[1], (10+x_pos, 345))
            else:
                self.image.blit(self.__life_frames[0], (10+x_pos, 345))
            x_pos += 40
        x_pos = 0
        for num in range(1, 4):
            if self.__bombs >= num: 
                self.image.blit(self.__bomb_frames[1], (10+x_pos, 420))
            else:
                self.image.blit(self.__bomb_frames[0], (10+x_pos, 420))
            x_pos += 40        
        
class Cloud(pygame.sprite.Sprite):
    '''This is a cloud class that is used to make background more lively.'''
    
    def __init__(self, screen):
        '''This method initializes the cloud class using the screen parameter 
        as bounaries.'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
        
        #Set instances, randomize properties upon creation.
        self.__screen = screen
        self.__type = 0
        self.__dx = 0
        self.__dy = 0        
        self.random_type()
        self.random_speed()
        
        #Image loading 
        self.image = pygame.image.load("images/cloud"
            +str(self.__type)+".png").convert_alpha()
        self.rect = self.image.get_rect()
        
        #Set position.
        self.random_reset()
        
    def random_type(self):
        '''This method randomizes the type of the cloud for different images.'''
        
        #Randomize type value between 0-2
        self.__type = random.randrange(3)
        
    def random_speed(self):
        '''This method randomizes the speed of the cloud.'''
        
        #Randomize direction of x vector between -1 or 1.
        self.__dx = random.randrange(-1, 2, 2) 
        
        #Randomize values of y vector between 2-4
        self.__dy = random.randrange(2, 5)
        
    def random_reset(self):
        '''This method randomizes the position of the cloud near the top of the
        screen.'''
        
        #x pos is static
        x_pos = (self.__screen.get_width()-200)/2
        #y pos is randomized for varied cloud appearance
        y_pos = random.randrange(-200, -39, 2)
        
        #Position cloud.
        self.rect.center = (x_pos, y_pos)
        
    def update(self):
        '''This method automatically runs once per frame to update the cloud. 
        Reset cloud if appropriate.'''
        
        #Update position using vectors.
        self.rect.centerx += self.__dx
        self.rect.centery += self.__dy
        
        #Reset cloud if out of bottom.
        if self.rect.top > self.__screen.get_height():
            self.random_type()
            self.random_speed()
            self.random_reset()
    
class Background(pygame.sprite.Sprite):
    '''This class defines a surface sprite to blit the scrolling background on.
    This background will reset at a specific position while scrolling to give 
    illusion of infinite height.'''
        
    def __init__(self):
        '''This initializer creates surface, loads background and initializes
        other instances needed for scrolling in update'''
        
        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)
    
        # Create surface initialize rect, position.
        self.image = pygame.Surface((440, 480))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = (0,0)
        
        #Load image and initialize other instances.
        self.__background = pygame.image.load("images/background.png").convert()
        self.__background_y = -440
        self.__dy = 1
        
    def get_surface(self):
        '''This method returns the surface of the background which is needed for
        the clear method in main.'''
        
        #Return instance.
        return self.image
        
    def update(self):
        '''This method will be called automatically to reposition the
        background image on the surface, seemingly scrolling.'''
        
        #Update image.
        self.__background_y += self.__dy
        
        #Blit image on to surface.
        self.image.blit(self.__background, (0, self.__background_y))
        
        #Reset image to origin when appropriate
        if self.__background_y >= 0:
            self.__background_y = -440
