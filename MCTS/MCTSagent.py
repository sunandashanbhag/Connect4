import math
import random
import time
import numpy as np
from connect4 import GameLogic as Game

ROW_RANGE = 6
COL_RANGE = 7

'''
Monte Carlo Tree Search does the job of scanning the search space to learn which moevs maximize probability of winning



'''

class MCTS(Game):
    def __init__(self,row_num, col_num, state, player):
        super(MCTS, self).__init__(row_num, col_num, 1, 2)
        self.state = state
        self.player = player
        self.root_node = (0,)
        self.tunable_constant = 1.0
        self.tree = {self.root_node: {'state': self.state,
                                      'player': self.player,
                                      'children': [],
                                      'parent': None,
                                      'total_node_visits': 0,
                                      'total_node_wins': 0,
                                      'node_score':0}
                     }
        self.total_parent_node_visits = 0

    def checkWinMCTS(self, board, row, col, turn):
        """Check all possible winning combinations to see if user wins"""
        # horizontal
        for c in range(COL_RANGE - 3):
            for r in range(ROW_RANGE):
                if set(board[r, c: c + 4]) == {turn}: return True
        # vertical
        if row < 3 and set(board[row:row + 4, col]) == {turn}: return True
        # if set(board[min(ROW_RANGE-1, row+4)][col])=={1}: return True
        # diagonalupward
        for r in range(ROW_RANGE - 3, ROW_RANGE):
            for c in range(COL_RANGE - 3):
                if (board[r][c] == turn and
                        board[r - 1][c + 1] == turn and
                        board[r - 2][c + 2] == turn and
                        board[r - 3][c + 3] == turn
                ): return True
        # diagonal2
        for r in range(0, ROW_RANGE - 3):
            for c in range(COL_RANGE - 3):
                if (board[r][c] == turn and
                        board[r - 1][c - 1] == turn and
                        board[r - 2][c - 2] == turn and
                        board[r - 3][c - 3] == turn
                ): return True

    def __ucb(self, node):
        '''
            UCB calculation - choose child with max UCB value
        '''

        if self.tree[node]['total_node_visits'] == 0:
            return math.inf
        return (self.tree[node]['total_node_wins']/self.tree[node]['total_node_visits']) + \
               (2 * (math.log(self.total_parent_node_visits) / self.tree[node]['total_node_visits'])) ** 0.5

    def isLeafNode(self,node):
        if len(node['children'])==0:
            return True
        return False

    def selectMove(self):
        '''
        starting with root, we calculate score for all possible children and get the leaf node with max score
        :return: the child node that provides the max UCB score
        '''
        isTerminal = False
        leaf = self.root_node
        while not isTerminal:
            node = leaf
            numChildren = len(self.tree[node]['children'])
            if self.isLeafNode(self.tree[node]):
                leaf = node
                isTerminal=True
            else:
                maxScore = -math.inf
                maxScoreAction = leaf
                for i in range(numChildren):
                    tmpAction = self.tree[node]['children'][i]
                    childId = leaf+(tmpAction,)
                    childScore = self.__ucb(childId)
                    if childScore>maxScore:
                        maxScore = childScore
                        maxScoreAction = tmpAction
                # print('max score', maxScore)
                leaf = leaf+(maxScoreAction,)
        return leaf


    def expandTree(self, leaf):
        '''
        :param leaf:
        :return:
        '''
        currState = self.tree[leaf]['state'].copy()
        currPlayer = self.tree[leaf]['player']
        currBoard = currState
        self.actions_available = [c for c in range(7) if currBoard[0][c]==0]
        childId = leaf
        isAvailaible = False
        done = False

        if len(self.actions_available):
            children = []
            for action in self.actions_available:
                childId = leaf+(action,)
                children.append(action)

                nextBoard = currBoard.copy()
                row = self.getNextRow(action)
                nextBoard[row][action] = currPlayer

                self.tree[childId] = {'state': nextBoard,
                                      'player': currPlayer,
                                      'children': [],
                                      'parent': leaf,
                                       'total_node_visits': 0,
                                      'total_node_wins': 0}

                if self.checkWinMCTS(nextBoard, row, action, currPlayer):
                    bestAction = action
                    isAvailaible = True

            self.tree[leaf]['children'] = children

            if isAvailaible:
                childId = bestAction
            else:
                childId = random.choice(children)

        return leaf + (childId,)


    def simulateGame(self, childId):
        self.total_parent_node_visits += 1
        count=0
        state = self.tree[childId]['state']
        prevPlayer = self.tree[childId]['player']
        winning_player = prevPlayer
        is_terminal = False

        while not is_terminal:
           currBoard = state.copy()
           # print(currBoard)
           self.actions_available = [c for c in range(self.COL_RANGE) if currBoard[0][c] == 0]
           # print(self.actions_available)
           if not len(self.actions_available) or count == 3:
               winning_player = None
               is_terminal = True
           else:
                count+=1
                if prevPlayer == 1:
                    currPlayer = 2
                else:
                    currPlayer = 1

                for action in self.actions_available:
                    row = self.getNextRow(action)
                    currBoard[row][action] = currPlayer
                    # print(currBoard.astype(int))
                    if self.checkWinMCTS(currBoard, row, action, currPlayer):
                        winning_player=currPlayer
                        is_terminal = True
                        break

                prevPlayer=currPlayer
        return winning_player

    def backpropagation(self, child_node_id, winner):
        '''
        Aim - Update the traversed nodes
        '''
        player = self.tree[(0,)]['player']

        if winner == None:
            reward = 0
        elif winner == player:
            reward = 1
        else:
            reward = -10

        node_id = child_node_id
        self.tree[node_id]['total_node_visits'] += 1
        self.tree[node_id]['total_node_wins'] += reward

    def start_the_game(self):
        '''
        Aim - Complete MCTS iteration with all the process running for some fixed time
        '''
        self.initial_time = time.time()
        is_expanded = False

        while time.time() - self.initial_time < 1:
            node_id = self.selectMove()

            if not is_expanded:
                node_id = self.expandTree(node_id)
                is_expanded = True
            winner = self.simulateGame(node_id)
            self.backpropagation(node_id, winner)


        current_state_node_id = (0,)
        action_candidates = self.tree[current_state_node_id]['children']
        total_visits = -math.inf
        for action in action_candidates:
            # print(action)
            action = current_state_node_id + (action,)
            visit = self.tree[action]['total_node_visits']
            if visit > total_visits:
                total_visits = visit
                best_action = action

        return best_action

if __name__ == '__main__':
    # yellowPlayer = Player(1)
    # redPlayer = RandomPlayer(2)
    # c4 = GameLogic(ROW_RANGE, COL_RANGE, yellowPlayer, redPlayer)
    agent = MCTS(ROW_RANGE, COL_RANGE, 1, 2)
    agent.start_the_game()
    # if not is_expanded:
    #     node_id = self.expansion(node_id)
    #     is_expanded = True
    # winner = self.simulation(node_id)
    # self.backpropagation(node_id, winner)

def connect4Agent(obs, config):

    agent = MCTS(config.rows, config.columns, np.asarray(obs.board).reshape(config.rows, config.columns),
                 obs.mark)
    return agent.start_the_game()[1]
