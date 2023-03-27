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
      successor_list.append((act,state_copy.apply_action(act)))
    return successor_list

  """
  The cutoff function returns true if the alpha-beta/minimax
  search has to stop and false otherwise.
  """
  def cutoff(self, state, depth):
    if state.game_over() and depth>=1:
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

    vertical_bridges = [[False for _ in range(state.size - 1)]]
    for column in state.v_bridges:
      vertical_bridges.append(column)
    vertical_bridges.append([False for _ in range(state.size - 1)])

    sum = 0
    id = 1 - self.id
    max_coord = state.size-1
    for (x_pawn, y_pawn) in state.cur_pos[id]:
      # upper bridge
      if vertical_bridges[x_pawn][y_pawn]:
        sum += 1
      # down bridge
      if vertical_bridges[x_pawn+1][y_pawn]:
        sum += 1
      # left bridge
      if horizontal_bridges[x_pawn][y_pawn]:
        sum += 1
      # right bridge
      if horizontal_bridges[x_pawn][y_pawn+1]:
        sum += 1

    return sum




