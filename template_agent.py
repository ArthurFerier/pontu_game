from agent import AlphaBetaAgent
import minimax

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

  """
  This is the skeleton of an agent to play the Tak game.
  """
  def get_action(self, state, last_action, time_left):
    self.last_action = last_action
    self.time_left = time_left
    return minimax.search(state, self)

  """
  The successors function must return (or yield) a list of
  pairs (a, s) in which a is the action played to reach the
  state s.
  """
  def successors(self, state):
    successor_list=[]
    for act in state.get_current_player_actions():
      state_copy=state.copy()
      state_copy.apply_action(act)
      successor_list.append((act, state_copy))
    return successor_list

  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
    if state.game_over() or depth>=1:
      return True
    return False


  """
  The evaluate function must return an integer value
  representing the utility function of the board.
  """
  def evaluate(self, state):
    """
    sum=0
    id=self.id
    if id:
      id=0
    else:
      id=1
    for (xpawn,ypawn) in state.cur_pos[id]:

      if xpawn > state.size-1: # check if pawn at horizontal right border
        if not state.h_bridges[xpawn][ypawn]:
          sum+=1
        if xpawn > 0: # check if pawn at horizontal left border
          if not state.h_bridges[xpawn-1][ypawn]:
            sum += 1

      if ypawn > state.size - 1: # check if paw at vertical down border
        if not state.v_bridges[xpawn][ypawn]:
          sum+=1
        if ypawn > 0: # check if pawn at vertical up border
          if not state.v_bridges[xpawn][ypawn-1]:
            sum += 1
    return sum"""

    # todo : can we move the two matricies in the definition of the class ?
    # setting False on the matricies when the pawn is next to a border
    horizontal_bridges = []
    for line in state.h_bridges:
      line_updated = [False]
      for boolean in line:
        line_updated.append(boolean)
      line_updated.append(False)
      horizontal_bridges.append(line_updated)

    vertical_bridges = [[False for _ in range(state.size)]]
    for column in state.v_bridges:
      vertical_bridges.append(column)
    vertical_bridges.append([False for _ in range(state.size)])

    sum = 0
    id = 1 - self.id
    for (x_pawn, y_pawn) in state.cur_pos[id]:
      # upper bridge
      if not vertical_bridges[y_pawn][x_pawn]:
        sum += 1
      # down bridge
      if not vertical_bridges[y_pawn+1][x_pawn]:
        sum += 1
      # left bridge
      if not horizontal_bridges[y_pawn][x_pawn]:
        sum += 1
      # right bridge
      if not horizontal_bridges[y_pawn][x_pawn+1]:
        sum += 1

    return sum


  def reachable(self, state, pos, max_moves):
    """
    pos = list of pawn positions
    max_moves = max number of moves to evaluate
    returns ordered list of number of reachable tiles in x moves with x = list_id+1
    """
    horizontal_bridges = []
    for line in state.h_bridges:
      line_updated = [False]
      for boolean in line:
        line_updated.append(boolean)
      line_updated.append(False)
      horizontal_bridges.append(line_updated)

    vertical_bridges = [[False for _ in range(state.size)]]
    for column in state.v_bridges:
      vertical_bridges.append(column)
    vertical_bridges.append([False for _ in range(state.size)])


    explored_pos=[[]]*(max_moves+1)
    explored_pos[0]=pos
    for i in range(1,max_moves+2):
      for (x_pawn, y_pawn) in pos[i-1]:
        # upper bridge
        if not vertical_bridges[y_pawn][x_pawn]:
          explored_pos[i].append()
        # down bridge
        if not vertical_bridges[y_pawn + 1][x_pawn]:
          sum += 1
        # left bridge
        if not horizontal_bridges[y_pawn][x_pawn]:
          sum += 1
        # right bridge
        if not horizontal_bridges[y_pawn][x_pawn + 1]:
          sum += 1

    return [len(explored_pos[i]) for i in range(1,max_moves+2)]#modify





  def evaluate(self, state):
    # Set the weights for different factors that affect the score
    weights = [5, 3, 1, 0.5]

    # Get the positions of the player's pawns and opponent's pawns
    player_pawns = state.cur_pos[self.id]
    opponent_pawns = state.cur_pos[1 - self.id]

    #Calculate numbers of reachable positions per moves
    player_reachable = self.reachable(state, player_pawns, len(weights))
    opponent_reachable =self.reachable(state, opponent_pawns, len(weights))

    score = 0
    # Compute the score based on the difference in reachable positions for each weight
    for j in range(len(weights)):
      score += (player_reachable[j] - opponent_reachable[j]) * weights[j]

    # Return the final score
    return score





