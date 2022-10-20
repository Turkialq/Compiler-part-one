import json

import graphviz

OPERATORS = set(["+", "*", "(", ")", "."])
PRIORITY = {"+": 1, ".": 2, "*": 3}


class nfa:
    def __init__(self):
        self.states = []
        self.letters = []
        self.transition_function = []
        self.start_state = "S1"
        self.final_states = []


nfa = nfa()


class CharType:
    SYMBOL = 1
    CONCAT = 2
    UNION = 3
    STAR = 4


class NFAState:
    def __init__(self):
        self.next_state = {}


class ExpressionTree:
    def __init__(self, charType, value=None):
        self.charType = charType
        self.value = value
        self.left = None
        self.right = None


def to_exp_tree(regexpostf):
    stack = []
    for c in regexpostf:
        if c == "+":
            tree = ExpressionTree(CharType.UNION)
            tree.right = stack.pop()
            tree.left = stack.pop()
            stack.append(tree)
        elif c == ".":
            tree = ExpressionTree(CharType.CONCAT)
            tree.right = stack.pop()
            tree.left = stack.pop()
            stack.append(tree)
        elif c == "*":
            tree = ExpressionTree(CharType.STAR)
            tree.left = stack.pop()
            stack.append(tree)
        elif c == "(" or c == ")":
            continue
        else:
            stack.append(ExpressionTree(CharType.SYMBOL, c))
    return stack[0]


def epsilon_nfa(exp_tree):
    # returns E-NFA
    if exp_tree.charType == CharType.CONCAT:
        return concat(exp_tree)
    elif exp_tree.charType == CharType.UNION:
        return or_union(exp_tree)
    elif exp_tree.charType == CharType.STAR:
        return star(exp_tree)
    else:
        return symbol(exp_tree)


def symbol(exp_tree):
    start = NFAState()
    end = NFAState()

    start.next_state[exp_tree.value] = [end]
    return start, end


def concat(exp_tree):
    left_nfa = epsilon_nfa(exp_tree.left)
    right_nfa = epsilon_nfa(exp_tree.right)

    left_nfa[1].next_state["ϵ"] = [right_nfa[0]]
    return left_nfa[0], right_nfa[1]


def or_union(exp_tree):
    start = NFAState()
    end = NFAState()

    first_nfa = epsilon_nfa(exp_tree.left)
    second_nfa = epsilon_nfa(exp_tree.right)

    start.next_state["ϵ"] = [first_nfa[0], second_nfa[0]]
    first_nfa[1].next_state["ϵ"] = [end]
    second_nfa[1].next_state["ϵ"] = [end]

    return start, end


def star(exp_tree):
    start = NFAState()
    end = NFAState()

    starred_nfa = epsilon_nfa(exp_tree.left)

    start.next_state["ϵ"] = [starred_nfa[0], end]
    starred_nfa[1].next_state["ϵ"] = [starred_nfa[0], end]

    return start, end


def arrange_transitions(state, states_done, symbol_table):
    nfa.transition_function
    nfa.letters
    nfa.states
    if state in states_done:
        return

    states_done.append(state)

    for symbol in list(state.next_state):
        if symbol not in nfa.letters:
            nfa.letters.append(symbol)
        for ns in state.next_state[symbol]:
            if ns not in symbol_table:
                symbol_table[ns] = sorted(symbol_table.values())[-1] + 1
                s_state = "S" + str(symbol_table[ns])
                nfa.states.append(s_state)
            nfa.transition_function.append(
                ["S" + str(symbol_table[state]), symbol, "S" + str(symbol_table[ns])]
            )

        for ns in state.next_state[symbol]:
            arrange_transitions(ns, states_done, symbol_table)


def arrange_nfa(fa):

    nfa.start_state

    nfa.states.append("S1")
    arrange_transitions(fa[0], [], {fa[0]: 1})

    final_st_dfs()


def final_st_dfs():
    nfa.final_states
    for st in nfa.states:
        count = 0
        for val in nfa.transition_function:
            if val[0] == st and val[2] != st:
                count += 1
        if count == 0 and st not in nfa.final_states:
            nfa.final_states.append(st)


def infix_to_postfix(expression):
    stack = []
    output = ""
    for char in expression:
        if char not in OPERATORS:
            output += char
        elif char == "(":
            stack.append("(")
        elif char == ")":
            while stack and stack[-1] != "(":
                output += stack.pop()
            stack.pop()
        else:
            while stack and stack[-1] != "(" and PRIORITY[char] <= PRIORITY[stack[-1]]:
                output += stack.pop()
            stack.append(char)
    while stack:
        output += stack.pop()
    return output


def vizualize():
    graph = graphviz.Digraph("epsilon-NFA diagram", format="png")
    for node in nfa.states:
        if node not in nfa.final_states:
            graph.node(node, shape="circle")
        else:
            graph.node(node, shape="doublecircle")
    for state in nfa.transition_function:
        graph.edge(state[0], state[2], label=state[1])
    graph.node("Start", shape="plaintext")
    graph.edge("Start", nfa.start_state)
    graph.render(directory=".", view=True)


def output_nfa():
    print(f"States {nfa.states}")
    print(f"Letter {nfa.letters}")
    print(f"Transiitons {nfa.transition_function}")
    print(f"Starting State: {nfa.start_state}")
    print(f"Final States {nfa.final_states}")


def api_call(str):
    regex = json.loads(str)
    print(regex)
    postreg = infix_to_postfix(regex["str"])
    exp_tree = to_exp_tree(postreg)
    e_nfa = epsilon_nfa(exp_tree)
    arrange_nfa(e_nfa)
    vizualize()
    st = nfa.states
    let = nfa.letters
    tran = nfa.transition_function
    start = nfa.start_state
    final = nfa.final_states
    nfa.states=[]
    nfa.letters=[]
    nfa.transition_function=[]
    nfa.start_state="S1"
    nfa.final_states=[]
    return (st, let, tran, start, final)
    
