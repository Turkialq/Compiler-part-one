import json


class nfa_to_dfa:
    def __init__(self):
        self.DFA = {}
        self.NFA = {}
        self.nfa_states = []
        self.dfa_states = []


def api_call(nfa_object):
    tempObject = json.loads(nfa_object)

    convert = nfa_to_dfa()

    convert.NFA = tempObject
    convert.DFA['states'] = []
    convert.DFA['letters'] = convert.NFA['letters']
    convert.DFA['transition_function'] = []
    convert.DFA['final_states'] = []

    for state in convert.NFA['states']:
        convert.nfa_states.append(state)

    powerset = [[]]
    for i in convert.nfa_states:
        for sub in powerset:
            powerset = powerset+[list(sub)+[i]]

    dfa_states = powerset

    for states in dfa_states:
        temp = []
        for state in states:
            temp.append(state)
        convert.DFA["states"].append(temp)

    for states in dfa_states:
        for letter in convert.NFA['letters']:
            q_to_next = []
            for state in states:
                for val in convert.NFA['transition_function']:
                    start = val[0]
                    inp = val[1]
                    end = val[2]
                    if state == start and letter == inp:
                        if end not in q_to_next:
                            q_to_next.append(end)
            q_states = []
            for i in states:
                q_states.append(i)
            convert.DFA['transition_function'].append(
                [q_states, letter, q_to_next])
    convert.DFA['start_states'] = []
    for state in convert.NFA['start_states']:
        convert.DFA['start_states'].append([state])

    for states in convert.DFA['states']:
        for state in states:
            if state in convert.NFA['final_states'] and states not in convert.DFA['final_states']:
                convert.DFA['final_states'].append(states)
    return convert.DFA
