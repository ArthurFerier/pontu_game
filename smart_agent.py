from agent import AlphaBetaAgent
import minimax, copy

"""
Agent skeleton. Fill in the gaps.
"""
class MyAgent(AlphaBetaAgent):

  """
  This is the skeleton of an agent to play the Tak game.
  """

  def __init__(self):
    self.time_left = None
    self.last_action = None

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

    #evaluate successors
    successor_eval = []
    for successor in successor_list:
      evaluation=self.evaluate(successor[1])
      if evaluation < 0:
        successor_list.remove(successor)
      else:
        successor_eval.append(evaluation)

    #sort them based on evaluation
    successor_eval_pairs = zip(successor_list, successor_eval)
    successor_eval_pairs = sorted(successor_eval_pairs, key=lambda x: x[1])
    successor_list , _ = zip(*successor_eval_pairs)
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

  def reachable(self, state, pos, other_pos, max_moves):
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


    explored_pos_precedent = set()
    explored_pos_global = set()
    explored_pos_list = []
    for position in pos:
      explored_pos_global.add(position)
      explored_pos_precedent.add(position)
    for position in other_pos:
      explored_pos_global.add(position)

    for _ in range(max_moves):
      local_explored_pos = set()
      for (x_pawn, y_pawn) in explored_pos_precedent:
        # upper bridge
        if vertical_bridges[y_pawn][x_pawn] and (x_pawn, y_pawn-1) not in explored_pos_global:
          local_explored_pos.add((x_pawn, y_pawn-1))
          explored_pos_global.add((x_pawn, y_pawn-1))
        # down bridge
        if vertical_bridges[y_pawn + 1][x_pawn] and (x_pawn, y_pawn+1) not in explored_pos_global:
          local_explored_pos.add((x_pawn, y_pawn + 1))
          explored_pos_global.add((x_pawn, y_pawn + 1))
        # left bridge
        if horizontal_bridges[y_pawn][x_pawn] and (x_pawn-1, y_pawn) not in explored_pos_global:
          local_explored_pos.add((x_pawn-1, y_pawn))
          explored_pos_global.add((x_pawn-1, y_pawn))
        # right bridge
        if horizontal_bridges[y_pawn][x_pawn+1] and (x_pawn+1, y_pawn) not in explored_pos_global:
          local_explored_pos.add((x_pawn+1, y_pawn))
          explored_pos_global.add((x_pawn+1, y_pawn))

      explored_pos_precedent = copy.deepcopy(local_explored_pos)
      explored_pos_list.append(len(local_explored_pos))

    return explored_pos_list





  def evaluate(self, state):
    # In case one player cannot move any elves, because another elf is blocking the move,
    # this player has not yet lost. He must only remove a bridge from the board without moving any elves.
    # Set the weights for different factors that affect the score
    weights = [5, 3, 1, 0.5]

    # Get the positions of the player's pawns and opponent's pawns
    player_pawns = state.cur_pos[self.id]
    opponent_pawns = state.cur_pos[1 - self.id]

    #Calculate numbers of reachable positions per moves
    player_reachable = self.reachable(state, player_pawns, opponent_pawns, len(weights))
    opponent_reachable = self.reachable(state, opponent_pawns, player_pawns, len(weights))

    score = 0
    # Compute the score based on the difference in reachable positions for each weight
    for j in range(len(weights)):
      score += (player_reachable[j] - opponent_reachable[j]) * weights[j]

    for i in range(3):
      if state.is_pawn_blocked(1 - self.id, i):
        score += 1
      if state.is_pawn_blocked(self.id, i):
        score -= 1

    # Return the final score
    return score





