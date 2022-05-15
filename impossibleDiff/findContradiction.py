"""find the longest contradiction for a specified pair"""
INFOPRINT = False


def judge_contradiction(upDiff: list, downDiff: list) -> bool:
    """if upDiff and downDiff are in contradiction
        Diff->(x1||x2, y1||y2)
        True for no contradiction"""
    upDiff, downDiff = upDiff[0] + upDiff[1], downDiff[0] + downDiff[1]  # [x1, x2, y1, y2]
    contradictionSet = {0: [1, 2],  # 1* 1
                        1: [0, 1, 3],  # 0 1* 2*
                        2: [0],  # 0
                        3: [1],  # 1*
                        4: []}
    result = True
    for i in range(4):
        result = result and (downDiff[i] not in contradictionSet[upDiff[i]])  # notice: not in
    return result


def findLongestContraRound(upChain: list, downChain: list):
    """find longest contradiction for the specified upChain and downChain
        form of ele in chain: [[x1, x2], [y1, y2]]
        begin from the zero round of upChain, last round of downChain"""
    longestRound = 1
    longestRound_up, longestRound_down = 0, 0
    middleDiff_up, middleDiff_down = [0, 0], [0, 0]

    upChainLen, downChainLen = len(upChain), len(downChain)
    for upChainCount in range(upChainLen):
        """begin from the zero round of upChain ~ upChain[0]"""
        temp = longestRound - upChainCount
        betterPoint = temp if temp >= 0 else 0

        for downChainCount in range(betterPoint, downChainLen):
            """last round of downChain ~ downChain[1]"""
            if not judge_contradiction(upChain[upChainCount],
                                       downChain[downChainCount]):  # contradiction
                longestRound_up, longestRound_down = upChainCount, downChainCount
                longestRound = longestRound_up + longestRound_down
                middleDiff_up, middleDiff_down = upChain[upChainCount], downChain[downChainCount]

    if INFOPRINT:
        print(longestRound, 'rounds impossibleDiff: ', upChain[0], '~', downChain[0])
        print('Contradiction appears:\n', longestRound_up, 'round', middleDiff_up)
        print('', longestRound_down, 'round', middleDiff_down)

    return longestRound
