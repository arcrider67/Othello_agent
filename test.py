import unittest
import reporting
import client

class TestPrepareResponse(unittest.TestCase):
  def test_prepare_response_returns_a_valid_response(self):
    self.assertEqual(client.prepare_response([2, 3]), b'[2, 3]\n')

class TestPlayer(unittest.TestCase):


  def testscan_for_cap(self):
    boardState = client.BoardState()

    player = client.Player(boardState)

    board = [[1, 2, 2, 2, 1, 2, 1, 2],
              [1, 2, 1, 2, 1, 1, 2, 2],
              [0, 2, 2, 1, 1, 2, 1, 2],
              [0, 2, 2, 1, 1, 2, 1, 2],
              [0, 2, 1, 1, 1, 1, 2, 1],
              [0, 0, 1, 2, 0, 1, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

    boardState.update(board)
    player.update(2, board)
    result = player.scan_for_cap([3,3],[4,5])
    print("scan result:",result)
    assert result == [True, 1]

  def testGetValidMoves(self):
    boardState = client.BoardState()

    player = client.Player(boardState)

    board = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]

    boardState.update(board)
    player.update(2, board)    

    moves = player.get_valid_moves()
    assert moves == []

    board = [[0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 2, 2, 0, 0, 0],
              [0, 0, 0, 1, 2, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]
    
    boardState.update(board)
    player.update(2, board)    
    moves = player.get_valid_moves()
    print("moves",moves)
    assert moves == [[4,3],[4,2],[3,2]]


class TestRepBoard(unittest.TestCase):
  def testBoardPlacement(self):
    board = [[1, 2, 2, 2, 1, 2, 1, 2],
              [1, 2, 1, 2, 1, 1, 2, 2],
              [0, 2, 2, 1, 1, 2, 1, 2],
              [0, 2, 2, 1, 1, 2, 1, 2],
              [0, 2, 1, 1, 1, 1, 2, 1],
              [0, 0, 1, 2, 0, 1, 0, 0],
              [0, 0, 0, 2, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0]]
    complexBoard = reporting.ReportingBoard()
    complexBoard.update(board)

    complexBoard.place_piece(2, [5,4])

    print(F"Result: {complexBoard.board}")


    assert complexBoard.board ==[ [1, 2, 2, 2, 1, 2, 1, 2],
                                  [1, 2, 1, 2, 1, 1, 2, 2],
                                  [0, 2, 2, 1, 1, 2, 1, 2],
                                  [0, 2, 2, 1, 1, 2, 2, 2],
                                  [0, 2, 1, 2, 1, 2, 2, 1],
                                  [0, 0, 1, 2, 2, 1, 0, 0],
                                  [0, 0, 0, 2, 0, 0, 0, 0],
                                  [0, 0, 0, 0, 0, 0, 0, 0]]


if __name__ == '__main__':
  unittest.main()