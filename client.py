#!/usr/bin/python

import sys
import json
import socket

import random

#takes in an ordered pair
#[row, col]
#returns true if its on the board
#false if the location is off the board
def is_valid_square(location):
  #assumes a default board size of 8x8 indexed from 0
  #this is safe since there are no commands in the game host to modify the board size

  if(location[0] > 7 or location[1] > 7):
    #loction to high of a position
    return False
  if(location[0] < 0 or location[1] < 0):
    #location is too low
    return False
  
  return True

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

    self.dicts[0] = [[0,0], [0,7], [7,0], [7,7]]
    self.dicts[1] = []
    for space in self.dicts[0]:
      adj = self.get_adj_spaces(space)
      for item in adj:
          self.dicts[1].append(item)

  def get_phase(self):
      return int(self.move_number / 20)

  def get_square_type(self,location):
    if(location in self.dicts[0]):
      return 0
    
    if(location in self.dicts[1]):
      return 1

    return 3


  def get_adj_spaces(self, location):
    #look around a piece and find all adjecent squares
    
    #creats a list of adjecent squares 
    #ordered N, NE, E, SE, S, SW, W, NW 
    adjacent_squares = [[location[0]-1,location[1]], [location[0]-1,location[1]+1], [location[0],location[1]+1], [location[0]+1,location[1]+1], [location[0]+1, location[1]], [location[0]+1, location[1]-1], [location[0], location[1]-1], [location[0]-1, location[1]-1]]
    
    #ensure that all squares in the return list are valid
    valid_adj_squares = []
    for space in adjacent_squares:
      if(is_valid_square(space)):
        valid_adj_squares.append(space)
    return valid_adj_squares



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

  def scan_board(self):
    for row_num, row in enumerate(board):
      for col_num, value in enumerate(row):
        self.player_spaces[value].append([row_num, col_num])

  def output(self):
    print(F"empty spaces: {self.player_scores[0]}")
    print(F"player 1 score: {self.player_scores[1]}")
    print(F"player 2 score: {self.player_scores[2]}")




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

  def update(self, player, board):

      self.move_factors = {}

      self.set_board(board)
      self.set_player(player)

      self.phase = self.boardState_.get_phase()



  def get_adj_spaces(self, location):
    #look around a piece and find all adjecent squares
    
    #creats a list of adjecent squares 
    #ordered N, NE, E, SE, S, SW, W, NW 
    adjacent_squares = [[location[0]-1,location[1]], [location[0]-1,location[1]+1], [location[0],location[1]+1], [location[0]+1,location[1]+1], [location[0]+1, location[1]], [location[0]+1, location[1]-1], [location[0], location[1]-1], [location[0]-1, location[1]-1]]
    
    #ensure that all squares in the return list are valid
    valid_adj_squares = []
    for space in adjacent_squares:
      if(is_valid_square(space)):
        valid_adj_squares.append(space)
    return valid_adj_squares

  def get_board_val(self, location):
    return(self.board[location[0]][location[1]])


  #starts at a given position and scans along a path until the piece changes
  #or hits the edge of the board

  #returns true if the piece at startlocation can be capped
  #by placing a piece along the given direction
  def scan_for_cap(self,start_location, direction):
    cur_location = start_location
    start_value = self.get_board_val(start_location)

    more_to_search = True
    length_of_cap = 0


    while(more_to_search):
        piece_val = self.get_board_val(cur_location)
        if(piece_val != start_value):
          #the player value at that location has changed
          if(piece_val != 0):
            #the space is occupied
            if(piece_val == self.player):
              return True, length_of_cap
          else:
              return False

        cur_location = [cur_location[0]+direction[0], cur_location[1] + direction[1]]
        if(is_valid_square(cur_location)):
          length_of_cap += 1
        else:
          #edge of board hit
          more_to_search = False
    return False


  def get_valid_moves(self):

    board = self.board
    player = self.player

    #will contain all empty spaces near opposing pieces
    valid_moves = []
    for row_num, row in enumerate(board):
      for col_num, column in enumerate(row):
        if (column != 0 and column != self.player):          
          #enemy piece scan it    
          location = [row_num, col_num]
          adjacent = self.get_adj_spaces(location)      
          
          #now we have all adjacent squares
          #filter down to spaces that are unoccupied
          
          for space in adjacent:
            value = self.get_board_val(space)
            #print(value)
            if( value == 0):

              #determine the direction of the empty space (constant time so not inefficient)
              direction = [space[0] - location[0], space[1]-location[1]]
              direction[0] = direction[0]*-1
              direction[1] = direction[1]*-1

              result = self.scan_for_cap(location, direction)
              if(result):
                if(tuple(space) not in self.move_factors):
                  self.move_factors[tuple(space)] = 0
                #saves the capture length for later
                self.move_factors[tuple(space)] =+ result[1]
                valid_moves.append(space)    
    
    return(valid_moves)

  def get_move(self, player, board):
    # TODO determine valid moves

    #currently works
    #could be optimized to make use of the board class for some of the calculations
    #not neccessary for strategy
    moves = self.get_valid_moves()



    # TODO determine best move
    move_scores= []

    for move in moves:
      
      #first check if a corner is available
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

    highest_score = max(move_scores)
    #fun printing
    if(highest_score == 100):
        print("took a corner, 1 point guaranteed")
    elif(highest_score == 0):
        print("forced to take space adj to corner")
        print("life points going down")


    move = moves[move_scores.index(highest_score)]
    return move

  def score_move(self, location):
    #will prioritize different factors based on the stage of the game

    #early game will cap as few pieces as possible
    if(self.phase == 3):
      cap_size = self.move_factors[tuple(location)]
      score = (cap_size / 64) * 100
    else:
      cap_size = self.move_factors[tuple(location)]
      score = (1- (cap_size / 64)) * 100
      
    #late game will capture as many as possible


    return score



def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))

    complex_board = BoardState()
    player_ai = Player(complex_board)

    while True:
      
      data = sock.recv(1024)
      if not data:
        #score final move to predict winner
        
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']

      print(player, maxTurnTime, board)

      player_ai.update(player, board)
      complex_board.update(board)


      move = player_ai.get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
