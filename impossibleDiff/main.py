from getDiffChain import getDiffChain
from findContradiction import findLongestContraRound
from itertools import product
INFOPRINT = True


def main():
    """L=[x1, x2], R=[y1, y2]"""
    diffChoice = [0, 1, 2, 3]  # 0 1* 1 2 ?(useless)
    # generate all downChain
    downChainAll = []
    for ele in product(diffChoice, repeat=4):
        L, R = list(ele[:2]), list(ele[2:])
        if L[0] + R[0] == 0 or L[1] + R[1] == 0:  # remove some infinite cases
            continue
        downChainAll.append(getDiffChain(L, R, True))
    # iter upChain to find the longest contradiction
    longestRound = 0
    imDiffRecord = []  # ele form: (inputDiff, outputDiff)
    for ele in product(diffChoice, repeat=4):
        L, R = list(ele[:2]), list(ele[2:])
        if L[0] + R[0] == 0 or L[1] + R[1] == 0:  # remove some infinite cases
            continue
        upChain = getDiffChain(L, R, False)

        for downChain in downChainAll:
            length = findLongestContraRound(upChain, downChain)
            if length < longestRound:  # no longer impossible path
                continue
            elif longestRound == length:
                imDiffRecord.append((upChain[0], downChain[0]))
            else:
                longestRound = length  # reset after a longer path
                imDiffRecord = [(upChain[0], downChain[0])]
    # Info Print
    if INFOPRINT:
        print('longestRound:', longestRound, 'Found', len(imDiffRecord), 'in', 256 * 256)
        print('impossible Diff:')
        temp = 0
        for ele in imDiffRecord:
            if ele[0] != temp:
                print('-' * 20)
                print('DiffIn: ', ele[0][0] + ele[0][1])
                print('DiffOut: ')
            print('        ', ele[1][0] + ele[1][1])
            temp = ele[0]


if __name__ == "__main__":
    main()
