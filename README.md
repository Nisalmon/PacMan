*This project has been created as part of the 42 curriculum by nisalmon, erifflar*


## Description
This project is called **Pacman**.  
The goal of the projet is to recreate a similar game to Pacman with a random maze generator.


## Instruction
To run this project, you can either do
```
    python3 main.py config.json
```
or
```
    make run
```
You might also need to install all the dependencies required for this project.
But before it is recommended to do as follow:
```
    make venv
    source .venv/bin/activate
```
Then you can do:
```
    make install
```


## Resources
[Pacman's ghosts algorithm explained](https://www.youtube.com/watch?v=ataGotQ7ir8)  
[Pygame Documentation](https://www.pygame.org/docs/)  
Concerning AI, it was used to try and fix some errors but caused more than it solved.


## Configuration
There are mandatory keys for config.json:  
- width: an integer ranged from 11 to 15  
- height: an integer ranged from 11 to 15  
- highscore_filename: The name of the leaderboard file, must be a .json  
- lives: a positive integer  
- pacgums: a positive integer  
- points_per_pacgum: a positive integer  
- points_per_super_pacgum: a positive integer  
- points_per_ghost: a positive integer  
- seed: a positive integer or 0 if you want first level to also be random  
- level_max_time: a positive integer  
- level: a positive integer  


## Highscore
The Highscore system work as follow:  
- 1 - Load the highscore file into a dictionnary  
- 2 - Once the game ended and the player entered a username add it to the highscore dictionnary
- 3 - Sort the dictionnary to only have the 10 highest score
- 4 - Dump the dictionnary into the highscore file.

We did it that way because we thought it was the simplest and faster way.


## Maze Generation
Since we have the generic A-maze-ing package provided by 42, it was implemented as follow:

- 1 - We install the package
- 2 - We import it
- 3 - We create an instance of Mazegenerator(), named mazegen, with parameters size and seed
- 4 - And finally, to create the maze, we do mazegen.generate_maze()


## Implementation
We used the A-maze-ing package to generate the level the player will play.  
To be sure that the maze is safe for pacman, we generate a non-perfect maze.  
Meaning that there is not a unique path from a to b and that it can hava loops.


## General Software Architecture
The architecture of our code is "simple".  
  
We have separate class for our player, ghosts and pacgums.  
They can interact with each other is some of their methods.  
For example, the player has a method called *touch_ghost* which check if the player is collinding with a ghost by checking every ghost.  


The last class is Button, this one interact only with the user mouse, checking if the mouse is on it and if it is clicked.



## Project Management
For this project we splitted the work.
- nisalmon:  
    - game routine  
    - menus  
    - Player/Button class  
    - utils  

- erifflar:  
    - sprite  
    - Ghost class  
    - utils  

But you can find more information on that in the file ProjectManagement/management.txt
