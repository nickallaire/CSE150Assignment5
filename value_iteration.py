class MDP(object):
    states = [None] * 81
    actions = {"NORTH", "EAST", "SOUTH", "WEST"}
    reward = [None] * 81
    discount = 0.99


class ValueIteration(object):
    mdp = MDP

    def loadAllFiles(mdp):
        matrixN = [[0.0 for x in xrange(81)] for y in xrange(81)]
        matrixE = [[0.0 for x in xrange(81)] for y in xrange(81)]
        matrixS = [[0.0 for x in xrange(81)] for y in xrange(81)]
        matrixW = [[0.0 for x in xrange(81)] for y in xrange(81)]

        resultFile = open('rewards.txt', 'r')
        i = 0
        for line in resultFile.readlines():
            mdp.reward[i] = line
            # print i, mdp.reward[i]
            i += 1

        # Loads a file into matrix
        fileNorth = open('prob_north.txt', 'r')
        fileEast = open('prob_east.txt', 'r')
        fileSouth = open('prob_south.txt', 'r')
        fileWest = open('prob_west.txt', 'r')

        for line in fileNorth.readlines():
            s, s_, prob = map(float, line.strip().split())
            matrixN[int(s) - 1][int(s_) - 1] = prob
            # print s, s_, prob

        for line in fileEast.readlines():
            s, s_, prob = map(float, line.strip().split())
            matrixE[int(s) - 1][int(s_) - 1] = prob

        for line in fileSouth.readlines():
            s, s_, prob = map(float, line.strip().split())
            matrixS[int(s) - 1][int(s_) - 1] = prob

        for line in fileWest.readlines():
            s, s_, prob = map(float, line.strip().split())
            matrixW[int(s) - 1][int(s_) - 1] = prob

        return mdp.reward, matrixN, matrixE, matrixS, matrixW

    def valueIteration(mdp, matrixN, matrixE, matrixS, matrixW):
        matrixV = [0.0 for x in xrange(81)]
        completeFlag = False
        for i in range(0,81):
            if mdp.reward[i] != 0:
                matrixV[i] = mdp.reward[i]

        while completeFlag == False:
            completeFlag = True
            for x in range(0, 81):
                sumUtilN = 0.0
                sumUtilE = 0.0
                sumUtilS = 0.0
                sumUtilW = 0.0
                # case north
                for y in range(0, 81):
                    if matrixN[x][y] != 0:
                        sumUtilN += matrixN[x][y] * float(matrixV[y])

                # case east
                for y in range(0,81):
                    if matrixE[x][y] != 0:
                        sumUtilE += matrixE[x][y] * float(matrixV[y])

                # case south
                for y in range(0, 81):
                    if matrixS[x][y] != 0:
                        sumUtilS += matrixS[x][y] * float(matrixV[y])

                # case west
                for y in range(0, 81):
                    if matrixW[x][y] != 0:
                        sumUtilW += matrixW[x][y] * float(matrixV[y])

                calculatedUtil = float(mdp.reward[x]) + (mdp.discount * max(sumUtilN, sumUtilE, sumUtilS, sumUtilW))
                if matrixV[x] != calculatedUtil:
                    matrixV[x] = float(mdp.reward[x]) + (mdp.discount * max(sumUtilN, sumUtilE, sumUtilS, sumUtilW))
                    completeFlag = False

        for u in range(0, 81):
            if matrixV[u] != 0:
                s = "V*(" + repr(u+1) + ") = " + repr(matrixV[u])
                # print s
        return matrixV

    def optimalPolicy(matrixN, matrixE, matrixS, matrixW, matrixV):
        matrixO = [None for x in xrange(81)]

        for v in range(0,81):
            floatVal = float(matrixV[v])
            if floatVal != 0.0:
                sumUtilN = 0.0
                sumUtilE = 0.0
                sumUtilS = 0.0
                sumUtilW = 0.0
                # case north
                for y in range(0, 81):
                    if matrixN[v][y] != 0:
                        sumUtilN += matrixN[v][y] * float(matrixV[y])

                # case east
                for y in range(0, 81):
                    if matrixE[v][y] != 0:
                        sumUtilE += matrixE[v][y] * float(matrixV[y])

                # case south
                for y in range(0, 81):
                    if matrixS[v][y] != 0:
                        sumUtilS += matrixS[v][y] * float(matrixV[y])

                # case west
                for y in range(0, 81):
                    if matrixW[v][y] != 0:
                        sumUtilW += matrixW[v][y] * float(matrixV[y])

                bestValue = max(sumUtilN, sumUtilE, sumUtilS, sumUtilW)
                bestDirection = None
                if bestValue == sumUtilN:
                    bestDirection = "NORTH"
                elif bestValue == sumUtilE:
                    bestDirection = "EAST"
                elif bestValue == sumUtilS:
                    bestDirection = "SOUTH"
                elif bestValue == sumUtilW:
                    bestDirection = "WEST"

                retTup = (v+1, matrixV[v], bestDirection)
                matrixO[v] = retTup
        return matrixO

    mdp.reward, matrixN, matrixE, matrixS, matrixW = loadAllFiles(mdp)
    # optimal_policy(mdp, matrixN, matrixE, matrixS, matrixW)
    matrixV = valueIteration(mdp, matrixN, matrixE, matrixS, matrixW)
    retMat = optimalPolicy(matrixN, matrixE, matrixS, matrixW, matrixV)
    for i in range(0,81):
        if retMat[i] != None:
            print retMat[i]
