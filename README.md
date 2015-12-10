# Let's hunt the little bears!

The game about hunting the bears. Control by micro-controller board. Developed by pygame.

### Project developer
* Jenwich Rattanayenjai
* Booranasit Piyavatcharavijit
* Panupong Maneerut

### Department
Practicum for Computer Engineering, Department of Computer Engineering, Faculty of Engineering, Kasetsart University

## Project Description
This game is about hunting the bears. We can control the archer to move left or right. We can adjust force and angle of arrow. And we also blow the sound censor on the board to clear all bears when it ready.

### Language used in this project
* C
* Arduino
* Python

### Library used in this project
* pyusb
* pygame

### Detail about files
1. Game files
	* `main.py` - main file for run the game
	* `player.py` - contains class and function about player
	* `bear.py` - contains class and function about bear
	* `arrow.py` - contains class and function about arrow
	* `gamemap.py` - contains class and function about map
2. Files about communicate to micro-controller board
	* `peri.py`
	* `practicum.py`
	* `usb-generic/usb-generic.ino`
	* `usb-generic/usbconfig.ino`
3. Images and sound
	* `src/images/`
	* `src/sounds/`
4. Files about schematic
	* `schematic/`

### Hardware
* Practicum Board
* PCB board
* LDR * 3
* LED * 3
* Switch * 1
* Header 40 pin
* Sound Sensor

## License
Let's hunt the little bears project is freely distributable under the terms of the MIT license.
