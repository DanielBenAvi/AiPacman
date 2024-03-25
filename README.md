# AI Pacman

## Summary
This project is a simple implementation of the Pacman 
Both the Pacman and the Ghosts are controlled by AI algorithms.
## Game Mechanics
1. Each second one coin is created.
2. Each Second one coin is deleted.
3. If the pacman eats a coin, the score is increased by 1.
4. If the pacman is getting to the range of the ghost, after 1 second its start running away from the ghost.
5. After the pacman escaped from the ghost, the pacman will continue to run away for 1 more seconds.
6. If the ghost catches the pacman, the game is over.
7. If the 2 ghosts are Threatening, the game is over. 

## Algorithms
The project uses the following algorithms:
- Breadth First Search - for the pacman finding the shortest path to the food
- Best First Search - for pacman running away from the closest ghost and finding it
- A* Search - for the ghost to find the pacman

## How to run
To run the project, you need to have Python 3 installed. Then, you can run the following command:
```bash
cd AiPacman
pip3 install -r requirements.txt
```
After that, you can run the following command:
```bash
python3 main.py
```