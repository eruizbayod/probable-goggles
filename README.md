# probable-goggles

GIT REP

This git folder contains different folders for the weekly tasks of the unit and a folder called GAME containing all the files needed for the game launch and the python file that runs the game.

2 PLAYER GAME

On the GAME/Game.py we can see all the code needed for the game. Some setting can be edited on the code to change the experience of how the game is played:

-	WIDTH and HEIGHT, to change the size of the window. Not recommended to change.
-	SPACESHIP SPEED: adjust to change the speed of how fast players move around the map.
-	BULLETS_SPEED: to define how fast the bullets are moving.
-	FPS: define how many frames per second we want the screen to refresh.
-	SPACESHIP_WIDTH and HEIGHT: to increase or decrease the spaceships sizes.
-	MAX_NUM_BULLETS: defines the maximum number of bullets that each player can spam on the window.
-	
On GAME/Assets are located the files that are used in the game, more can be added if we want to give different images for the spaceships or have different backgrounds. Also different sound effects can be added to create a different game experience.

HOW TO PLAY

-	Each player’s health has a maximum value of 10, this can be adjusted in the code inside play_game function (p1_health and p2_health).

-	Player on the left side moves around the map with WASD keys and player on the right with ARROW keys.

-	Each player can shoot with ALT key, left for left player and right key for the other player. 

-	First player to get hit 10 times with bullets losses the game.
