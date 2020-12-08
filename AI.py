from copy import deepcopy

class Checkers:
    def __init__(self, player, coord, isKing):
        self.player = player
        self.isKing = isKing
        self.coord = coord

    def _isKing(self):
        return self.isKing

    def makeKing(self):
        self.isKing = True

    def updateCoords(self, x, y):
        if self.player == 1 and y == 7:
            self.makeKing()
        if self.player == 2 and y == 0:
            self.makeKing()
        self.coord = [x, y]


class State:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def game_over(self):
        if len(self.player1) == 0 or len(self.player2) == 0:
            return True
        return False


    def evaluateState(self, turn):
        ans = 0
        if turn == 1:
            ans = 10 * (len(self.player1) - len(self.player2))
            for x in self.player1:
                if x._isKing():
                    ans += 5
            for x in self.player2:
                if x._isKing():
                    ans -= 5
        else:
            ans = 10 * (len(self.player2) - len(self.player1))
            for x in self.player2:
                if x._isKing():
                    ans += 5
            for x in self.player1:
                if x._isKing():
                    ans -= 5
        return ans

    def move(self, oldCoord, newCoord):
        check = self.getCheckerObject(oldCoord[0], oldCoord[1])
        check.updateCoords(newCoord[0], newCoord[1])

    def getCheckerObject(self, x, y):
        for i in self.player1:
            if i.coord == [x, y]:
                return i
        for i in self.player2:
            if i.coord == [x, y]:
                return i

    def occupiedStatus(self, x, y):
        if x >= 8 or x < 0 or y >= 8 or y < 0:
            return -1

        obj_ = self.getCheckerObject(x, y)

        if not obj_:
            return 0
        else:
            return obj_.player
        
    def delete(self, x, y):
        for i in range(len(self.player1)):
            if self.player1[i].coord == [x, y]:
                del self.player1[i]
                break

        for i in range(len(self.player2)):
            if self.player2[i].coord == [x, y]:
                del self.player2[i]
                break


def solve(player1, player2, turn, depth):
    player1_, player2_ = [], []
    for x in player1:
        player1_.append(Checkers(x.player, x.coord, x._isKing()))

    for x in player2:
        player2_.append(Checkers(x.player, x.coord, x._isKing()))
    currState = State(player1_, player2_)
    return MiniMax(currState, turn, depth, True, turn)


def MiniMax(state, turn, depth, max_player, starter):
    if depth == 0 or state.game_over():
        return [state.evaluateState(starter), None]

    if max_player:
        best = -10000000
        bestMove = None
        for [newState, moves] in make_move(state, turn) + make_jump_move(state, turn):
            stateVal = MiniMax(newState, flipTurn(turn), depth - 1, False, starter)[0]
            if stateVal >= best:
                best = stateVal
                bestMove = moves
        return [best, bestMove]

    else:
        worst = 10000000
        bestMove = None
        for [newState, moves] in make_move(state, turn):
            stateVal = MiniMax(newState, flipTurn(turn), depth - 1, True, starter)[0]
            if stateVal <= worst:
                worst = stateVal
                bestMove = moves
        return [worst, bestMove]


def flipTurn(turn):
    return 1 if turn == 2 else 2


def make_move(state, turn):
    ans = []
    checkers = state.player1 if turn == 1 else state.player2

    for piece in checkers:
        moves = []
        if piece.player == 1 or piece._isKing():
            moves.append([-1, 1])
            moves.append([1, 1])
        if piece.player == 2 or piece._isKing():
            moves.append([1, -1])
            moves.append([-1, -1])

        [x, y] = piece.coord

        for i in moves:
            if state.occupiedStatus(i[0] + x, i[1] + y) == 0:
                state1 = deepcopy(state)
                state1.move([x, y], [i[0] + x, i[1] + y])
                ans.append([state1, [[x, y], [i[0] + x, i[1] + y]]])
    return ans


def make_jump_move(state, turn):
    ans = []
    checkers = state.player1 if turn == 1 else state.player2

    for piece in checkers:
        moves = []
        if piece.player == 1 or piece._isKing():
            moves.append([-1, 1])
            moves.append([1, 1])
        if piece.player == 2 or piece._isKing():
            moves.append([1, -1])
            moves.append([-1, -1])

        [x, y] = piece.coord

        for i in moves:
            if state.occupiedStatus(2 * i[0] + x, 2 * i[1] + y) == 0 and state.occupiedStatus(i[0] + x, i[1] + y) != piece.player and state.occupiedStatus(i[0] + x, i[1] + y) > 0:
                state1 = deepcopy(state)
                state1.move([x, y], [2*i[0] + x, 2*i[1] + y])
                state1.delete(x+i[0], y+i[1])
                ans.append([state1, [[x, y], [2*i[0] + x, 2*i[1] + y]]])
    return ans