import json
import sys

DFA = {}
NFA = {}
nfa_states = []
dfa_states = []


def load_nfa(nfa_object):
    global NFA
    NFA = nfa_object


def out_dfa():
    global DFA
    return json.dumps(DFA, indent=4)


def get_power_set(nfa_States):
    powerset = [[]]
    for i in nfa_States:
        for sub in powerset:
            powerset = powerset+[list(sub)+[i]]
    return powerset


def api_call(nfa_object):
    tempObject = json.loads(nfa_object)
    load_nfa(tempObject)

    DFA['states'] = []
    DFA['letters'] = NFA['letters']
    DFA['transition_function'] = []

    for state in NFA['states']:
        nfa_states.append(state)

    dfa_states = get_power_set(nfa_states)

    DFA["states"] = []

    for states in dfa_states:
        temp = []
        for state in states:
            temp.append(state)
        DFA["states"].append(temp)

    for states in dfa_states:
        for letter in NFA['letters']:
            q_to_next = []
            for state in states:
                for val in NFA['transition_function']:
                    start = val[0]
                    inp = val[1]
                    end = val[2]
                    if state == start and letter == inp:
                        if end not in q_to_next:
                            q_to_next.append(end)
            q_states = []
            for i in states:
                q_states.append(i)
            DFA['transition_function'].append([q_states, letter, q_to_next])
    DFA['start_states'] = []
    for state in NFA['start_states']:
        DFA['start_states'].append([state])

    DFA['final_states'] = []
    for states in DFA['states']:
        for state in states:
            if state in NFA['final_states'] and states not in DFA['final_states']:
                DFA['final_states'].append(states)
    out_dfa()
