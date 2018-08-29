# pyman
pyman is a pacman-like game that is written in python with the pygame multimedia 
library. The main reason for this game is to further practice python, programming
and software engineering with python and in particular game development with 
python and the pygame library. I also had great fun programming this game. 

## Getting Started

### Prerequisites
In order to run the game or participate in its development one should have the `pygame` game development library. One should install it using the following command: 
```
pip install pygame
``` 

### Run
After you have downloaded and installed the pygame library, you can run the game with
```
python3.5 Main.py
```

## Project Architecture

### Project Structure

* `Main.py` - An entry point of the game. The `Main.py` file also contains 
game manager class - the `Game` class. The `Game` class is special class that is 
responsible for handling game events (like key presses) and game manipulations. 

* `Map.py` - This file contains two classes that are responsible for two 
different operations. The first one is the `Map` class which is the logical 
representation of the map and all of it information. The second is the `MapView`
class that is connected to the logical map and responsible for displaying it on 
the screen. Here we have some kind of MVC design pattern. 
 
* `Graph.py` - File contains the algorithmic code for the 
game. It implements the graph search algorithm and allows us to program the 
computer AI for the bad player that chase the user player. Further explanation
can be found inside the file.   
  
* `Terminal.py` - This file contains code that deals with information terminal 
of the game.  
 
* `Helpers.py` - Is the place for general purpose functions, classes and code 
that will be used in other parts. 
  
* `Consts.py` - Contains all constants that is used in different parts of projects. 

## Current Version

* v1.0.0

## Built With

* [Python](https://www.python.org/) - The Python programming language.
* [pygame](https://www.pygame.org/news) - Python library for multimedia applications.

## Authors

* **Avraham Khanukaev** - *Initial work* - [Avraham Khanukaev](https://github.com/avikhanukaev)
