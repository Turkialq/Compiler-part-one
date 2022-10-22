from answerss.tree import TreeNode
from answerss.graph import GraphNode

def regexToDFA(regex):
    equation, answer = execute(regex)
    answer = f'Postfix Equation: (({equation})) The Answer: {answer}'
    return answer


def infix_to_postfix(newRe):
    letters = []
    operand = []
    for elemet in newRe:

        if elemet in ['*', '$', 'a', 'b', 'c', 'd']:
            letters.append(elemet)
        else:
            if elemet == '|':
                if len(operand) >= 1:
                    if operand[-1] == '.':
                        letters.append(operand.pop())
                        operand.append(elemet)
                    else:
                        operand.append(elemet)
                else:
                    operand.append(elemet)
            else:
                operand.append(elemet)
        if elemet == ')':
            operand.pop()
            while True:
                if len(operand) >= 1:
                    temp = operand.pop()
                    if temp == '(':
                        break
                    letters.append(temp)
                else:
                    break
    while True:
        letters.append(operand.pop())
        if len(operand) < 1:
            break

    str1 = ''
    for i in letters:
        str1 = str1+i
    # print(str1)
    return str1, letters


def makeTree(postFix):
    nodeStack = []
    checkStack = []

    for c in postFix:
        if c in ['$', 'a', 'b']:
            node = TreeNode(c)
            nodeStack.append(node)
            checkStack.append(node)

        elif c in ['.', '|']:
            node = TreeNode(c)
            right = nodeStack.pop()
            left = nodeStack.pop()
            node.addRight(right)
            node.addLeft(left)
            nodeStack.append(node)
            checkStack.append(node)

        elif c == '*':
            node = TreeNode(c)
            right = nodeStack.pop()
            node.addRight(right)
            nodeStack.append(node)
            checkStack.append(node)

    return checkStack


def firstLastPos(tree):
    pos = 1
    for t in tree:
        if t.getData() in ['a', 'b', '$']:
            t.addFirPos([pos])
            t.addLasPos([pos])
            t.addNullable(False)
            pos += 1

        elif t.getData() == '|':
            t.addFirPos(t.getLeft().getFirPos() + t.getRight().getFirPos())
            t.addLasPos(t.getLeft().getLasPos() + t.getRight().getLasPos())
            if t.getLeft().isNullable() or t.getRight().isNullable():
                t.addNullable(True)
            else:
                t.addNullable(False)

        elif t.getData() == '.':
            if t.getLeft().isNullable():
                t.addFirPos(t.getLeft().getFirPos() + t.getRight().getFirPos())
            else:
                t.addFirPos(t.getLeft().getFirPos())

            if t.getRight().isNullable():
                t.addLasPos(t.getLeft().getLasPos() + t.getRight().getLasPos())
            else:
                t.addLasPos(t.getRight().getLasPos())

            if t.getLeft().isNullable() and t.getRight().isNullable():
                t.addNullable(True)
            else:
                t.addNullable(False)

        elif t.getData() == '*':
            t.addNullable(True)
            t.addFirPos(t.getRight().getFirPos())
            t.addLasPos(t.getRight().getLasPos())
    return tree


def addConcats(re):

    index = 0
    reWithConcat = []

    while True:
        l = re[index]

        if l in ['$']:
            reWithConcat.append(l)
            break

        elif l in ['a', 'b', '*'] and re[index+1] not in [')', '|']:
            reWithConcat.append(l)
            reWithConcat.append('.')
        elif l in [')'] and re[index+1] not in ['*']:
            reWithConcat.append(l)
            reWithConcat.append('.')
        else:
            reWithConcat.append(l)

        index += 1

    return reWithConcat


def calcFollowPos(tree):
    followPos = [[]]
    followNodes = [[]]

    for i in tree:
        if i.getData() in ['$', 'a', 'b', 'c', 'd']:
            followPos.append([])
            followNodes.append([i.getData()])

    for element in tree:
        if element.getData() == '.':
            for i in element.getLeft().getLasPos():
                followPos[i] = followPos[i] + element.getRight().getFirPos()

        elif element.getData() == '*':
            for i in element.getLasPos():
                followPos[i] = followPos[i] + element.getFirPos()

    nodes = []
    for i in followNodes:
        nodes = nodes + i

    # followPos.pop(0)
    nodes.insert(0, '')
    return nodes, followPos


def toDFA(start, fnode, fpos):

    nodes = []
    nodeStack = []
    tested = []
    start = GraphNode(start)
    nodes.append(start)

    aarr = []
    barr = []

    while True:
        if len(nodes) == 0:
            break

        node = nodes.pop()
        tested.append(node)
        nodeTemp = node.getData()
        for p in nodeTemp:  # 1
            if fnode[p] == 'a':
                aarr = aarr + fpos[p]
                aarr = [*set(aarr)]
            elif fnode[p] == 'b':
                barr = barr + fpos[p]
                barr = [*set(barr)]

        if len(aarr) > 0:
            a = GraphNode(aarr)

        if len(barr) > 0:
            b = GraphNode(barr)

        c1 = True
        c2 = True
        for t in tested:
            if len(aarr) > 0:
                if t.data == a.data:
                    node.addA(t)

                    c1 = False

            if len(barr) > 0:
                if t.data == b.data and len(barr) > 0:
                    node.addB(t)

                    c2 = False

        if c1 and len(aarr) > 0:
            node.addA(a)
            nodes.append(a)

        if c2 and len(barr) > 0:
            node.addB(b)
            nodes.append(b)

        nodeStack.append(node)
        aarr = []
        barr = []

    anss = printAns(nodeStack, fpos)
    return anss


def printAns(nodeStack, fpos):
    letters = ['A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L',
               'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X',
               'Y', 'Z']

    initNode = True
    goalNode = False
    index = 0
    ans = []
    answer = []

    for node in nodeStack:
        ans.append([letters[index], node.getData()])
        str1 = f'Node {letters[index]} = {node.getData()}'
        answer.append(str1)
        print(str1)
        index += 1

    index = 0
    for n in nodeStack:

        dfaNode = letters[index]
        index += 1
        # dfaNode = n.getData()

        if len(fpos) - 1 in n.getData():
            goalNode = True

        if n.getA() is None:
            a = "None"
        else:
            for an in ans:
                if n.getA().getData() in an:
                    a = an[0]

        if n.getB() is None:
            b = "None"
        else:
            for an in ans:
                if n.getB().getData() in an:
                    b = an[0]
        if initNode:
            answer.append(f'Start Node:{dfaNode}   a:{a}   b:{b}')
            print(f'Start Node:{dfaNode}   a:{a}   b:{b}')
            initNode = False
        elif goalNode:
            answer.append(f'Goal Node:{dfaNode}   a:{a}   b:{b}')
            print(f'Goal  Node:{dfaNode}   a:{a}   b:{b}')
            goalNode = False
        else:
            answer.append(f'Node:{dfaNode}   a:{a}   b:{b}')
            print(f'      Node:{dfaNode}   a:{a}   b:{b}')

    return answer


def execute(regex):
    regex = str(regex)
    regex = regex[slice(2, -1, 1)]

    equation, postFix = infix_to_postfix(addConcats(list(f'{regex}$')))
    tree = makeTree(postFix)
    newTree = firstLastPos(tree)
    root = newTree[-1]
    root.drawTree()
    followNodes, followPos = calcFollowPos(newTree)
    initialState = root.getFirPos()
    return equation, toDFA(initialState, followNodes, followPos)
