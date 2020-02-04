# vectorgame
VectorGame with python3 and pygame for 4 joysticks

## necessary installs
  * see https://www.python.org to install python3 (under linux: 'sudo apt install python3')
  * see https://www.pygame.org to install pygame for python3 (under linux: 'sudo pip3 installs pygame')
  


## how to play
player1 can play with cursor keys and pageup/pagedown and home/end

Up to 4 players can play with joysticks. 
use buttons to switch aiming-mode between those states:
  * "free": you can move the crosshair and it remains at this (world) angle
  * "fixed": you can move the crosshair and it remains at this angle relative to the player. It rotates with the player. 
  * "forward": you can not move the crosshair, it always looks in the same direction as the player. aim with the whole player
  * "locked": you can not move the crosshair, it automatically aims at one of those targets:
     * "nearest": aims at the nearest player
     * "yellow": aims at the yellow player 
     * "red": aims at the red player
     * "blue": aims at the blue player
     * "green": aims at the green player
  

# screenshot

![screenshot](screenshot.png)
