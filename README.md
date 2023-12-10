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
4. On one machine, run `python main.py` to launch the game and press "Initialize Game"
5. On another machine, repeat steps 1-4 and run `python main.py` to launch the game. Press "Join Game" and type the host's IP address

## Screenshots
![Main Menu](<screenshots/Screenshot from 2023-12-10 11-23-47.png>) 
![Waiting Menu](<screenshots/Screenshot from 2023-12-10 11-25-47.png>) 
![Countdown Screen](<screenshots/Screenshot from 2023-12-10 11-26-30.png>) 
![Game Screen](<screenshots/Screenshot from 2023-12-10 11-26-44.png>) 
![Game Over Screen](<screenshots/Screenshot from 2023-12-10 11-27-07.png>)