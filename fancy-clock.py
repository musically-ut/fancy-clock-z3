import z3


def makeZ3Prob(words, width, height):
    """Creates a Z3 problem which will provide a solution to packing
       the provided words in a board of alphabet of size width * height."""
    board = []
    s = z3.Solver()
    for i in range(width):
        row_i = []
        for j in range(height):
            pos_i_j = []
            for a in range(ord('A'), ord('Z') + 1):
                v = z3.Bool('board[{}, {}, {}]'.format(i, j, chr(a)))
                pos_i_j.append(v)

            # Exactly one of the booleans must be true
            exactlyOne = []
            for k in range(len(pos_i_j)):
                left = pos_i_j[:k]
                right = pos_i_j[k+1:]
                others = left + right
                exactlyOne.append(z3.And(pos_i_j[k], z3.Not(z3.Or(*others))))

            s.add(z3.Or(*exactlyOne))
            row_i.append(pos_i_j)

        board.append(row_i)

    wordVars = {}

    for word in words:
        # The word can be vertically placed
        wordVars[word] = {}
        wordPositions = []

        wordVars[word]['vertical'] = []
        for i in range(width):
            row_i = []
            for j in range(height - len(word) + 1):
                # To determine where the word starts from
                v = z3.Bool('vertical_{}[{}, {}]'
                            .format(word, i, j))
                row_i.append(v)

                # All the correct words in the vertical column should
                # be turned on
                conditionVars = [v]
                for k in range(len(word)):
                    x, y, z = i, j + k, ord(word[k]) - ord('A')
                    conditionVars.append(board[x][y][z])

                wordPositions.append(z3.And(*conditionVars))

            wordVars[word]['vertical'].append(row_i)

        wordVars[word]['horizontal'] = []
        for i in range(width - len(word) + 1):
            row_i = []
            for j in range(height):
                v = z3.Bool('horizontal_{}[{},{}]'
                            .format(word, i, j))
                row_i.append(v)

                conditionVars = [v]
                for k in range(len(word)):
                    x, y, z = i + k, j, ord(word[k]) - ord('A')
                    conditionVars.append(board[x][y][z])

                wordPositions.append(z3.And(*conditionVars))

            wordVars[word]['horizontal'].append(row_i)

        s.add(z3.Or(*wordPositions))

    return s, board, wordVars


def reconstructBoard(board, model):
    """Reconstructs the board."""
    chars = []
    for row in board:
        rowChars = []
        for alphabets in row:
            for idx, c in enumerate(alphabets):
                if z3.is_true(model.eval(c)):
                    rowChars.append(chr(ord('A') + idx))

        chars.append(rowChars)

    return chars

upperWords = ['FIVE', 'TEN', 'QUARTER', 'TWENTY', 'HALF']
lowerWords = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN',
              'EIGHT', 'NINE', 'TEN', 'ELEVEN', 'TWELVE']

# Model definition

upperSolver, upperBoard, upperWordVar = makeZ3Prob(upperWords, 3, 9)
middleBoardSoln = list('XIPASTOED')
lowerSolver, lowerBoard, lowerWordVar = makeZ3Prob(lowerWords, 5, 9)

# Model solution

upperSolver.check()
upperModel = upperSolver.model()
upperBoardSoln = reconstructBoard(upperBoard, upperModel)


lowerSolver.check()
lowerModel = lowerSolver.model()
lowerBoardSoln = (reconstructBoard(lowerBoard, lowerModel))

# Printing the solution

fullBoard = []
fullBoard.extend([' '.join(x) for x in upperBoardSoln])
fullBoard.append(' '.join(middleBoardSoln))
fullBoard.extend([' '.join(x) for x in lowerBoardSoln])

for row in fullBoard:
    print(row)
