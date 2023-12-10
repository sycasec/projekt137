# Keyboard Splatoon
CMSC 137 Final Project

## Dependencies
- `python 3.11`
- `pygame 2.4.0-1` from `pacman -Sy python-pygame` or `pip install pygame`

## Description

Keyboard Splatoon - connect via local network with your friends and play a 1v1 battle

## Installation and Setup
1. Ensure that you have [Python](https://www.python.org/downloads/) installed on your system
2. Clone the repository to your local machine
```
git clone https://github.com/sycasec/projekt137 && cd projekt137
```
3. (OPTIONAL) Create and activate a virtual environment
```
python -m virtualenv venv && venv\scripts\activate
```
4. Install the project's dependencies 
```
pip install -r requirements.txt
```
5. On one machine, run `python main.py` to launch the game and press "Initialize Game"
6. On another machine, repeat steps 1-4 and run `python main.py` to launch the game. Press "Join Game" and type the host's IP address

## Mechanics
When a game of keyboard splatoon is started, players are assigned a color, and a randomly-generated onscreen keyboard is shown where each key is either red or green.

Players must press each key opposite their assigned color and splatoon all over the key, giving the player points and turning that key into their assigned color (i.e, if the player color is green, they have to press the red keys to earn points, turning those keys green).

If a player makes a mistake and splatoons all over their own keys, the opponent earns points, turning the key into their opponent's color. If a player continuously presses the opponent’s keys with no mistakes, they get a combo multiplier that increases the points earned.

If a player manages to fully splatoon all over the onscreen keyboard and fill it up with their own color before the timer ends, that player automatically wins the game. If the timer ends without a decisive winner, the player with the greater amount of points wins.

## Screenshots
![Main Menu](<screenshots/Screenshot from 2023-12-10 11-23-47.png>) 
![Waiting Menu](<screenshots/Screenshot from 2023-12-10 11-25-47.png>) 
![Countdown Screen](<screenshots/Screenshot from 2023-12-10 11-26-30.png>) 
![Game Screen](<screenshots/Screenshot from 2023-12-10 11-26-44.png>) 
![Game Over Screen](<screenshots/Screenshot from 2023-12-10 11-27-07.png>)