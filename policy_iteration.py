import random
# from timeit import default_timer

class MDP(object):
    states = [None] * 81
    actions = {"NORTH", "EAST", "SOUTH", "WEST"}
    reward = [None] * 81
    discount = 0.99

class PolicyIteration(object):
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

    def policyIteration(mdp, matrixN, matrixE, matrixS, matrixW, reward):
        matrixU = [0.0 for x in xrange(81)]
        policy = [None for x in xrange(81)]
        changedM = [0 for x in xrange(81)]

        for i in range(0,81):
            if mdp.reward[i] != 0:
                matrixU[i] = mdp.reward[i]

        # for val in range(len(policy)):
        #     randNum = random.randrange(4)
        #     policy[val] = randNum

        for x in range(0,81):
            for y in range(0,81):
                # print matrixN[x][y]
                if matrixN[x][y] != 0:
                    randNum = random.randrange(4)
                    policy[x] = randNum
                    if x != y:
                        changedM[x] = 1

        # print policy
        unchanged = False
        while not unchanged:

            for x in range(0, 81):
                for z in range(0, 81):
                    sumUtil = 0.0
                    for y in range(0, 81):
                            if policy[z] == 0:          #case: north
                                if matrixN[z][y] != 0:
                                    sumUtil += matrixN[z][y] * float(matrixU[y])
                            if policy[z] == 1:          #case: east
                                if matrixE[z][y] != 0:
                                    sumUtil += matrixE[z][y] * float(matrixU[y])
                            if policy[z] == 2:          #case: south
                                if matrixS[z][y] != 0:
                                    sumUtil += matrixS[z][y] * float(matrixU[y])
                            if policy[z] == 3:          #case: west
                                if matrixW[z][y] != 0:
                                    sumUtil += matrixW[z][y] * float(matrixU[y])

                    matrixU[z] = (sumUtil * mdp.discount) + float(mdp.reward[z])

            # print matrixU
            unchanged = True
            for x in range(0, 81):
                sumUtilN = 0.0
                sumUtilE = 0.0
                sumUtilS = 0.0
                sumUtilW = 0.0
                # case north
                for y in range(0, 81):
                    if matrixN[x][y] != 0:
                        sumUtilN += matrixN[x][y] * float(matrixU[y])

                # case east
                for y in range(0,81):
                    if matrixE[x][y] != 0:
                        sumUtilE += matrixE[x][y] * float(matrixU[y])

                # case south
                for y in range(0, 81):
                    if matrixS[x][y] != 0:
                        sumUtilS += matrixS[x][y] * float(matrixU[y])

                # case west
                for y in range(0, 81):
                    if matrixW[x][y] != 0:
                        sumUtilW += matrixW[x][y] * float(matrixU[y])

                maxSumUtil = max(sumUtilN, sumUtilE, sumUtilS, sumUtilW)

                sumPolicy = 0.0
                for y in range(0, 81):
                        if policy[x] == 0:          #case: north
                            if matrixN[x][y] != 0:
                                sumPolicy += matrixN[x][y] * float(matrixU[y])
                        if policy[x] == 1:          #case: east
                            if matrixE[x][y] != 0:
                                sumPolicy += matrixE[x][y] * float(matrixU[y])
                        if policy[x] == 2:          #case: south
                            if matrixS[x][y] != 0:
                                sumPolicy += matrixS[x][y] * float(matrixU[y])
                        if policy[x] == 3:          #case: west
                            if matrixW[x][y] != 0:
                                sumPolicy += matrixW[x][y] * float(matrixU[y])

                if maxSumUtil > sumPolicy:

                    prior = policy
                    if maxSumUtil == sumUtilN:
                         policy[x] = 0
                    elif maxSumUtil == sumUtilE:
                        policy[x] = 1
                    elif maxSumUtil == sumUtilS:
                        policy[x] = 2
                    elif maxSumUtil == sumUtilW:
                        policy[x] = 3
                    unchanged = False

        for x in range(0, 81):
            if changedM[x] != 0:
                if policy[x] == 0:
                    print x + 1, "NORTH"
                elif policy[x] == 1:
                    print x + 1, "EAST"
                elif policy[x] == 2:
                    print x + 1, "SOUTH"
                elif policy[x] == 3:
                    print x + 1, "WEST"

        return policy

    # start = default_timer()
    mdp.reward, matrixN, matrixE, matrixS, matrixW = loadAllFiles(mdp)
    policy = policyIteration(mdp, matrixN, matrixE, matrixS, matrixW, mdp.reward)
    # for x in range(0, 81):
    #     if policy[x] == 0:
    #         print x+1, "NORTH"
    #     elif policy[x] == 1:
    #         print x+1, "EAST"
    #     elif policy[x] == 2:
    #         print x+1, "SOUTH"
    #     elif policy[x] == 3:
    #         print x+1, "WEST"
    # print "Policy Iteration: ", default_timer() - start
