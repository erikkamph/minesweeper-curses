# Minesweeper
The game is not 100% complete, there is still stuff to fix, 
for example if you loose it should reveal where all the bombs where.
The game uses curses library in python to display everything.
How you move in the game and where you are currently at is displayed 
on the right side of the screen, while the game currently is on the 
left side of the screen. So for the moment the game is kinda off but
that will be fixed after I have come up with a way to calculate so
that the game is centered.<br>
<p>The game uses following keys to move around and do stuff</p>

Key | Action
----|-------------
w   | go up one step
a   | go left one step
s   | go down one step
d   | go right one step
f   | flag current position
r   | reveal current position
q   | quit the program

## TODO
- [ ] When loosing reveal all bombs in the game.
- [ ] Have a timer while the game is running
- [ ] (Maybe) Accumulate score based on number in the current tile revealed.
- [ ] Fix better coloring of the program
- [ ] Implement a way to see if the user has won
- [ ] Center the game and put help and other useful stuff to the right of the board

## Examples
![Before entering a size for the board](example.png)
![Having entered a size for the board](example2.png)
![Revealed all positions with 0 while playing the game](example3.png)
![Flagged 2 bombs and revealed numbers around](example4.png)
![When you hit a bomb you get prompted with a question about playing again](example5.png)