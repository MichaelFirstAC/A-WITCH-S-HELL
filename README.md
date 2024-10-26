# A WITCH'S HELL

A bullet-hell style game powered by python3 and pygame. This project is created for an Algorithm and Programming Assignment in BINUS University International Class.

# Dependencies
+ Python 3
+ PyGame

# Controls
- 'Z' to fire and select an option.
- 'X' to use a bomb and cancel all near projectiles.
- 'Left shift' to slow down movement.

# Tips and Tricks

- To master 'A WITCH'S HELL, one must master all mechanics of the game.
	- Start by learning where your exact hitbox is to have a mental image of your 
	weak point.
	
	- Learn when to use focus mode. You need to use focus mode in tight situations where 
	you are surrounded by bullets, players can play safe and just hold down shift the 
	entire time for precise movements. However, sometimes you may need to move fast to 
	get to a drop in time, unfocus and rush towards to drop!

	- Learn how to bomb effectively (bomb only when you are about to die to avoid death). 
	If players use bombs effectively, they are basically another life instead of a tool.

	- Don't be afraid of bullets! This is a bullet hell game.

	- Last but not least... Have fun!

# Usage
To run the program, simply execute main.py.

# Features
- Touhou styled bullet hell game - one hit, small hitbox and lots of bullets to dodge
- Survive style, no end of level
- Frame data focused game
- Patterns made using degrees
- Bomb feature with accurate hitbox
- Bullet grazing feature!
- Difficulties as time passes
- Enemy limits depending on difficulty
- Different enemies as difficulty increases
- Point drops, life drops, and bomb drops. They fall differently each time
- Menu, pause, gameover screen all have options so that no 
  restart of the application is required to play again.
- Highscore reading from file, long term saving, possible to erase data in-game
- Flashly highscore tab when highscore reached
- Different fire types for player
- Full animation
- Full sounds

# Tutorial 

## Menus and Their Options

To navigate through the options, use arrow keys. To select an option, press z, the fire key.
 - Main Menu
	- Start - starts the game
	- Erase date - reset highscore
	- Quit - quit program
- Pause Menu (called by pressing esc in game)
	- Resume - resume game from where it was paused
	- Main Menu - go back to main menu
- Game Over Menu (called upon losing)
	- Restart - restart game loop 
	- Main Menu - go back to main menu

## Movement

- To move in a direction, press the corresponding direction arrows on the keyboard
	- Used to avoid bullets with imprecise but fast movements

- To slow down while moving, enter the focused mode by holding left shift on the keyboard
	- Used to avoid bullets with precise but slow movementss

## Death

- Player will lose a life the second a bullet touches their bullet hitbox (the red dot that is 
visible in focused mode)

- Player will start with 2 lives and extra lives may be gained through pink star items 
that is dropped by boss type enemies.

- Once player loses all lives, it is game over

## Bombs

- Player has the ability to use a bomb to cancel all bombs in the area with the 'x' button
  
	- This can be used as a last resort to save a life when the player 
	is about the die by bullets

- Bombs reset to 1 each life and extra bombs may be earned by boss drops (gray star items)

## Fire Modes/Focus Types

- Player can shoot bullets by holding the z button to damage in coming enemies 

- Player in the unfocused/default mode has standard spread out bullet type to hit many 
opponents over a slow fire rate

	- Used when there are multiple opponents on the screen

- Player in focused mode (whild holding the left shift key) has a concentrated fire type 
to hit a single enemy over a fast fire rate

	- Used when focusing on a single target for fast takedowns

## Scores

- Scores can be racked up in multiple ways. Highscore is saved in the data folder and can 
be reset in main menu.

	Defeat enemies - Kill enemy for points, depending on the enemy type, 
	different about of points will be yielded.

	Drops - There will be drops after an enemy is defeated, there will be 
	point drops, small and big packs available for drops. As for special drops 
	like lives and bombs, if lives and bombs are already on full capacity,
	points will be gained instead of gaining another life (100 points) or bomb(50 points).
	
	Grazing - when players hug an enemy bullet without getting hit, it is called,
	"grazing a bullet". Grazing a bullet will constantly grant players a small 
	amount of points. It is a risky way to gain points but it is a effective way to do so. 

## Difficulty

- As time passes, the difficulty of the game will increase. The difficulty will increase as 
the rate of spawning goes up, loosen up on the spawning restrictions, and introduce players
to new enemies with more complex bullet patterns. 
	
	Note that as each difficulty increases, spawn rate increases as well.
	Difficulty 0 (0s-30s) - 1 boss type, 2 common types - lowest restriction.
	Difficulty 1 (30s-1min)- 1 boss types, 3 common types, introduce new boss type.
	Difficulty 2 (1min-2min)- 2 boss types, 4 common types, introduce new common type.
	Difficulty 3 (2min-5min)- 2 boss types, 5 common types, introduce new boss type.
	Difficulty 4 (5min+) - 3 boss types, 6 common types.
  
# Important Note
+ I do not own any of the sound or image files containing in this project.

# Files
- Main-menu Music: Color your night - Persona 3 Reload
- Background Music: Its going down now - Persona 3 Reload
- Background Music: Young Girl A - Siinamota
- Background Music: Kingslayer - Bring Me The Horizon (Feat. BabyMetal)

# DO NOTE, ONCE YOU HEAR KINGSLAYER, THE GAME GETS REALLY HARD.

- Sound effects: Project Touhou
- Bullets: Project Touhou
- Player: Project Touhou / Marisa Kirisame
- Background: Project Touhou 
- Enemies: Project Touhou / Shizuha Aki, Hina Kagiyama, Nitori Kawashiro, Aya Shameimaru, Kanako Yasaka
- Icons: Calamity Icon - Terraria / Calamity Mod




