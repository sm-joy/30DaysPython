# Falling Sand : Cellular Automata

Falling Sand simulation is very simple and plain, but looks like a real physics engine's work. This note explores its generation using `PyGame(Python)`.

## Logic Explanation

The Falling Sand simulation works with three simple rules for creating a `Cellular Autmata` like simulation. The simulation looks very real, depending on the sand size or the cell size. The smaller the sand, the more real it looks. The simulation works with these three rules:

Every cell has a Boolean `state`. If the cell is a `Sand Cell`, the state is true else the state is false. We check every cell in the grid and if the cell's `state` is true meaning it's a sand cell, then

> Logic
> - #### 1.  If there isn't a sand cell underneath the current cell: 
> 	- then we mark the underneath cell's `state` as `true` and mark the current cell's `state` as `false`. With this the current sand moves down one block.
> - #### 2. Else If there is a sand cell underneath the current cell:
> 
> 	- ##### 1. If the underneath cell's right cell is not a sand cell(or the `state` is `true`):
> 		- then we mark the underneath cell's right cell's `state` as `true` and the current cell's `state` as `false`.
> 	- ##### 2. Else if the underneath cell's left cell is not a sand cell:
> 		-  then we mark the underneath cell's left cell's `state` as `true` and the current cell's `state` as `false`

### Import The Necessary Libraries
```python
import pygame as pygame  
from random import randint
```
We need the random library for more randomness in choosing which cell to check first (the right cell or the left cell).

### The `Block` `Class`
We need a structure to hold the cell's state and the PyGame `rect` object for easy rendering.

Here's the class
```python
class Block:  
    def __init__(self, row: int, col: int,  w: int) -> None:  
        self.rect: pygame.rect.Rect = pygame.rect.Rect(col*w, row*w, w, w)  
        self.state: bool = False
  
    def render(self, surface: pygame.surface) -> None:  
        pygame.draw.rect(surface, 
				         (225, 225, 0) if self.state else (0, 200, 255),
				         self.rect)
  
    def hover(self) -> bool:  
        return self.rect.collidepoint(pygame.mouse.get_pos())  
  
    def check_pressed(self, event: pygame.event) -> None:  
        if event.type == pygame.MOUSEBUTTONDOWN and self.hover():  
            self.state = True
```

In this class we have three methods. We can render each individual cell with `render`, and we can use `check_pressed` check for mouse button pressed in one the cell for simulation purpose. The `hover` method is needed for the `check_pressed` method.

The Block class takes in three parameters, `row`, `col` and `w` is needed for calculating its position in the PyGame coordinate system. 

$$positionX = column*size\_of\_the\_block$$$$positionY = row*size\_of\_the\_block$$

I personally like to make a main function and then run it, so it becomes more like a compiled language like code. So,
```python
def main() -> int:  
    all_the_code_goes_here
    
if __name__ == "__main__":  
    main()
```

In the `main` function we first initialize some variables
```python
width: int = 500  
height: int = 500  
w: int = 5  
rows: int = int(width/w) 
cols: int = int(height/w)
fps: int = 60  
run: bool = True  
  
cells: list[list[Block]] = [[  
    Block(i, j, w)  
    for j in range(cols)]  
    for i in range(rows)]  
  
window, clock = pygame_run(width, height)
```
`rows`, `cols` makes it easier to iterate over the all the cells. And we initialize the cells array that holds the `Block` objects. I made a separate function for initializing the PyGame window. It returns the PyGame's built in window or screen object and the clock object.

Here's the implementation of the `pygame_run` function
```python
def pygame_run(width: int, height: int) -> tuple[pygame.surface, pygame.time.Clock]:  
    pygame.init()  
    pygame.display.set_caption("Falling Sand")  
    window: pygame.surface = pygame.display.set_mode((width, height))  
    clock: pygame.time.Clock = pygame.time.Clock()  
    return window, clock
```

then we have the main loop for handling event, updating and rendering the cells.
```python
while run:  
    for event in pygame.event.get():  
        if event.type == pygame.QUIT:  
            run = False  
        for i in cells:  
            for j in i:  
                j.check_pressed(event)  
  
    # Update
  
    # Render  
    for i in range(rows):  
        for j in range(cols):  
            cells[i][j].render(window)
  
    pygame.display.flip()  
    clock.tick(fps)
```
the `render` method of the the `Block` object renders the PyGame `rect` with black color if the cell's `state` is false, else render the `rect` with yellow color, representing sand.

And now we have the updating part, where we apply the logic. In the main loop we update each cell with the function `update`
```python
row: int = rows-1  
while row >= 0:  
    col: int = cols - 1  
    while col >= 0:  
        update(cells, row, col, rows, cols)  
        col -= 1  
    row -= 1
```

Notice we reverse update the cells in the `cells` array because, if we update the cells in straight order, it doenst work properly and the rendering becomes sloppy.
In the `update` function we update the current cell based on the three rules.
```python
def update(cells, row: int, col: int, rows: int, cols: int) -> None:  
    if not cells[row][col].settled:  
        if cells[row][col].state and row == rows-1:  
            cells[row][col].settled = True  
        if cells[row][col].state and row != rows - 1:  
            if cells[row][col].visited:  
                cells[row][col].visited = False  
            else:  
                if not cells[row + 1][col].state:  
                    cells[row][col].state = False  
                    cells[row + 1][col].state = True  
                    cells[row + 1][col].visited = True  
                elif cells[row + 1][col].state and not cells[row + 1][col].settled:  
                    pass  
                elif randint(1, 2) == 1:  
                    if col != cols - 1 and not cells[row + 1][col + 1].state:  
                        cells[row][col].state = False  
                        cells[row + 1][col + 1].state = True  
                        cells[row + 1][col + 1].visited = True  
                    elif col != 0 and not cells[row + 1][col - 1].state:  
                        cells[row][col].state = False  
                        cells[row + 1][col - 1].state = True  
                        cells[row + 1][col - 1].visited = True  
                    else:  
                        cells[row][col].settled = True  
                else:  
                    if col != 0 and not cells[row + 1][col - 1].state:  
                        cells[row][col].state = False  
                        cells[row + 1][col - 1].state = True  
                        cells[row + 1][col - 1].visited = True  
                    elif col != cols - 1 and not cells[row + 1][col + 1].state:  
                        cells[row][col].state = False  
                        cells[row + 1][col + 1].state = True  
                        cells[row + 1][col + 1].visited = True  
                    else:  
                        cells[row][col].settled = True
```

### Explanation of the `update` Function

The `update` function follows these rules:

**1. Check if the current cell is settled**:
```python
if not cells[row][col].settled:
```
If a cell is settled, it means it has reached a stable state and no longer needs updating. (For saving resources and computation time. Its not needed for the actual simulation)

**2. Check if the current cell is a sand cell and at the bottom row**:
```python
if cells[row][col].state and row == rows - 1: 
	cells[row][col].settled = True
```
If a sand cell is at the bottom row, it is settled because it cannot move further.

**3. Check if the current cell is a sand cell and not at the bottom row**:

**3.1. If the cell has been visited**:
```python
if cells[row][col].visited: 
	cells[row][col].visited = False
```
If a cell has been visited, it means it has already been updated in the current frame. We reset the `visited` state and skip further updates.

**3.2. If there is no sand cell underneath**:
```python
if not cells[row + 1][col].state: 
	cells[row][col].state = False 
	cells[row + 1][col].state = True 
	cells[row + 1][col].visited = True
```
If the cell below is empty, the current sand cell falls down to the next row.

**3.3. If the cell underneath is not settled**:
```python
elif cells[row + 1][col].state and not cells[row + 1][col].settled: 
	pass
```
If the cell below is occupied but not settled, we skip further updates for this cell. If there are 2 or more cell falling in the same column, then we move the cell that is the most closure to the ground first, then above that and so on. So we stop simulating the current cell if there is a cell under it that is also falling.

3.4. **If the cell underneath is settled**:
```python
elif randint(1, 2) == 1: 
	if col != cols - 1 and not cells[row + 1][col + 1].state: 
		cells[row][col].state = False cells[row + 1][col + 1].state = True 
		cells[row + 1][col + 1].visited = True 
	elif col != 0 and not cells[row + 1][col - 1].state: 
		cells[row][col].state = False 
		cells[row + 1][col - 1].state = True 
		cells[row + 1][col - 1].visited = True 
	else: 
		cells[row][col].settled = True
```

If the cell underneath is settled, the current cell tries to move diagonally. If both diagonal cells are occupied or out of bounds, the current cell becomes settled.
We random check any of the right or left diagonal cell. the last portion of the update function is the same as this one, just a little bit randomness while choosing which cell to check first for going diagonal.

This approach ensures that each cell is updated correctly, simulating the natural behavior of falling sand. The `visited` state prevents redundant updates within the same frame, and the `settled` state optimizes the simulation by skipping cells that have reached a stable state.

> ***Note: I may modify or update the main source for more optimization in the future, but the concept of the simulation remains the same.***