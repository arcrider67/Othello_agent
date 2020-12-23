#!/usr/bin/python

import sys
import json
import socket

import random

import reporting


#takes in an ordered pair
#[row, col]
#returns true if its on the board
#false if the location is off the board



#class to keep track of board related variables
#scores
#turn number
#number of empty spaces
class BoardState():
  def __init__(self):
    #assumes a 8x8 othello board
    
    #this is going to hold mappings to subsets of spaces for quick lookup 
    #0 is corner spaces
    #1 is spaces adjacent to corners
    #more can be added as player is interested
    #these will be constant throughout the game
    
    self.dicts = {}
    self.move_number = 0

    #ordered N, NE, E, SE, S, SW, W, NW 
    self.directions = [[-1,0], [-1,1], [0,1], [1,1], [1, 0], [1, -1], [0, -1], [-1,-1]]
    
    #dicts serves to catagorize spaces that may be significant
    self.dicts[0] = [[0,0], [0,7], [7,0], [7,7]]
    self.dicts[1] = []
    for space in self.dicts[0]:
      adj = self.get_adj_spaces(space)
      for item in adj:
          self.dicts[1].append(item)

  def get_phase(self):
      return int(self.move_number / 20)

  def get_square_type(self,location):
    if(location in self.dicts[0]): return 0 
    elif(location in self.dicts[1]): return 1
    else: return 3


  def get_adj_spaces(self, location):
    #look around a piece and find all adjecent squares
    
    #creats a list of adjecent squares 
    #ordered N, NE, E, SE, S, SW, W, NW 
    adjacent_squares = []
    for direc in self.directions:
      adjacent_squares.append([location[0]+direc[0], location[1]+direc[1]])
    
    #ensure that all squares in the return list are on the board
    valid_adj_squares = []
    for space in adjacent_squares:
      if(self.is_valid_square(space)):
        valid_adj_squares.append(space)
    return valid_adj_squares


#forces the board to recalculate all the lists and scores
  def update(self, board):
      self.board = board
      self.player_spaces = [[],[],[]]
      
      self.scan_board()

      self.player_scores = [0,0,0]
      self.player_scores[0] = len(self.player_spaces[0])
      self.player_scores[1] = len(self.player_spaces[1])
      self.player_scores[2] = len(self.player_spaces[2])

      
      self.move_number = 64 - len(self.player_spaces[0]) 

      self.output()

  #sorts all the board locations into one of 3 categories
  #creates a list of lists with 3 categories
  #index 0 is all empty squares
  #index 1 is all player 1 pieces
  #index 2 is all player 2 pieces
  def scan_board(self):
    for row_num, row in enumerate(self.board):
      for col_num, value in enumerate(row):
        self.player_spaces[value].append([row_num, col_num])

  #returns the number of empty spaces
  def get_empty_count(self):
    return self.player_scores[0]

  #returns the list of empty spaces
  def get_empty_spaces(self):  
    return self.player_spaces[0]
  
  #returns the list of player 1 piece locations
  def get_p1_spaces(self):
    return self.player_spaces[1]
  
  #returns the list of player 2 piece locations
  def get_p2_spaces(self):
    return self.player_spaces[2]

  #returns player 1s numerical score
  def get_p1_score(self):
    return self.player_scores[1]
  
  #returns player 2s numerical score
  def get_p2_score(self):
    return self.player_scores[2]

  #returns true if a given location is on the board
  #false otherwise
  def is_valid_square(self, location):
  #assumes a default board size of 8x8 indexed from 0
  #this is safe since there are no commands in the game host to modify the board size

    if(location[0] > 7 or location[1] > 7):
      #loction to high of a position
      return False
    if(location[0] < 0 or location[1] < 0):
      #location is too low
      return False
    
    return True

  #print scores and number of empty spaces left
  def output(self):
    print("empty spaces:",self.player_scores[0])
    print("player 1 score:",self.player_scores[1])
    print("player 2 score:",self.player_scores[2])


#player class
#takes information from the boardState class and makes move decisions base on that information
class Player:

  def __init__(self, BoardState):

    self.boardState_ = BoardState

    #will keep information about the potential "goodness" of a move
    #things like how many pieces this move will cap  
    self.move_factors = {}


  def set_player(self, player_num):
    self.player = player_num 
  
  def set_board(self, board):
    self.board = board

  #forces the board into a new state with given board layout and 
  #the given players turn
  def update(self, player, board):
      self.move_factors = {} #reset all move scores
      self.set_board(board) #reset the board
      self.set_player(player) #set the player (incase of weird server issue where player changes mid game)
      self.phase = self.boardState_.get_phase() #set the current aprox phase of the game

  def get_board_val(self,location):
    return self.board[location[0]][location[1]]

  #starts at a given position and scans along a path until the piece changes
  #or hits the edge of the board

  #returns true if the piece at startlocation can be capped
  #by placing a piece along the given location
  #start location is the occupied space
  #space is the empty space
  def scan_for_cap(self,occupied_space, empty_space):

    #determine the direction of the empty space relative to the occupied space
    direction = [empty_space[0] - occupied_space[0], empty_space[1]-occupied_space[1]]
    direction[0] = direction[0]*-1
    direction[1] = direction[1]*-1

    cur_location = occupied_space
    start_value = self.get_board_val(occupied_space) #the piece color that will be flipped
    more_to_search = True #false when the capture has ended
    length_of_cap = 0 #track the length of the cap for decision making later

    #scan the pieces oposite the empty space and determine if a capture can be made in that direction
    #formatted recursively without a recursive call
    while(more_to_search):
        piece_val = self.get_board_val(cur_location)
        if(piece_val != start_value):
          #the player value at that location has changed
          if(piece_val != 0):
            #the space is occupied
            if(piece_val == self.player):
              return [True, length_of_cap]
          else:
              #the space is empty
              return False
        else:
          pass
          #the piece we are looking at coud be captured but no action needs to be taken
        cur_location = [cur_location[0]+direction[0], cur_location[1] + direction[1]]
        if(self.boardState_.is_valid_square(cur_location)):
          length_of_cap += 1
        else:
          #edge of board hit
          more_to_search = False

    return False


  #generates all valid moves for the currently set board position
  def get_valid_moves(self):

    board = self.board
    player = self.player

    #will contain all empty spaces near opposing pieces
    valid_moves = []
    if(self.player == 1):
      opposing_pieces = self.boardState_.get_p2_spaces()
    else:
      opposing_pieces = self.boardState_.get_p1_spaces()
    #print(opposing_pieces)
    for location in opposing_pieces:
          #look at every enemy piece
          #check if there are empty spaces around it 
          adjacent = self.boardState_.get_adj_spaces(location)      
          
          #now we have all adjacent squares
          #filter down to spaces that are unoccupied
          for space in adjacent:
            value = self.get_board_val(space)
            #print(value)
            if( value == 0):

              result = self.scan_for_cap(location, space)
              if(result):
                if(tuple(space) not in self.move_factors):
                  self.move_factors[tuple(space)] = 0
                #saves the capture length for later
                self.move_factors[tuple(space)] =+ result[1]
                valid_moves.append(space)    
    
    return(valid_moves)

  def get_move(self):

    #Determine valid moves
    #could be optimized to make use of the board class for some of the calculations
    #not neccessary for strategy
    moves = self.get_valid_moves()

    # TODO determine best move
    move_scores= []

    #score each move from 0(bad) to 100(very good)
    for move in moves:
      
      #first check what kind of space this is
      #corner, adjcent to corner or other
      space_type = self.boardState_.get_square_type(move)

      if(space_type == 0):
        #always take corners since they are always stable pieces (cant be flipped)
        move_scores.append(100)

      elif(space_type == 1):
        #never take spaces next to corners unless required to
        move_scores.append(0)

      else:
        #program any additional factors here
        #things like piece capture count
        #current game phase
        move_scores.append(self.score_move(move))

    #pick the best score
    highest_score = max(move_scores)
    
    #fun printing
    """
    if(highest_score == 100):
        print("took a corner, 1 point guaranteed")
    elif(highest_score == 0):
        print("forced to take space adj to corner")
        print("life points going down")
    """
    move = moves[move_scores.index(highest_score)]
    return move

  #given a location will score the "goodness" of placing a piece there from 0 to 100
  def score_move(self, location):
    #will prioritize different factors based on the stage of the game

    if(self.phase == 3):
      #late game will capture as many as possible
      cap_size = self.move_factors[tuple(location)]
      score = (cap_size / 64) * 100
    else:
      #early game and mid game will cap as few pieces as possible
      cap_size = self.move_factors[tuple(location)]
      score = (1- (cap_size / 64)) * 100

    return score



def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1338
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  #optional parameter that will output the final known board state to a file 
  report = sys.argv[3] if (len(sys.argv) > 3 and sys.argv[3]) else "False"

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:

    sock.connect((host, port))

    complex_board = BoardState()
    player_ai = Player(complex_board)

    while True:
      
      data = sock.recv(1024)
      if not data:
        #if no data is recieved disconnect and output the final known result if the flag is set
        if(report == "True"):
          reporting.final_score(board, move, player)
  
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']

      print(player, maxTurnTime, board)

      #update the client's player_ai and the boardstate information
      player_ai.update(player, board)
      complex_board.update(board)

      #generate next move based on latest board
      move = player_ai.get_move()
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
