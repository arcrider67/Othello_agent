# Python 3 Othello Agent
Disclaimer: developed with Python 3.8.6, tested with Python 2.7.6 - not guaranteed to work with other versions

## Instructions
To run the client, run: `python client.py [optional port] [optional hostname] [optional output flag (True/False)]`



To run all tests, run `python -m unittest`
To run all tests in "test.py" tests, run `python -m unittest test`
To run the TestGetMove class in "test.py", run `python -m unittest test.TestGetMove`

## info on output
The output flag will enable the result of the game to be written to a file. Setting the flag to true will result in a .csv ouput in the working directory of the client.

Since the client does not recieve the final gamestate from the server the result is extrapolated. This is done by using this agent to play out the last 1 or 2 moves. Since this is usually the max number of left over moves the result is consistant with using a random agent for the other player.


## Recommended Software
* Python 3.8.6



## Strategy

The agent plays as follows: In the early game the goal is to maximize mobility. This comes from capturing the least possible number of pieces. For the first 40 moves the agent will take moves that result in the smallest points gained.

After move 40 the agent will consider this to be the "end game" and seek to capture as many pieces as possible with each move. 

Throughout the game the agent will always take a corner space, if it is available, and will avoid spaces adjacent to corners.  