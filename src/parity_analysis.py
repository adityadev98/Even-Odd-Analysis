import networkx as nx

class Parity:
    TOP = 'T'
    EVEN = 'E'
    ODD = 'O'
    UNKNOWN = 'U'

def join(a, b):
    if a == b:
        return a
    if Parity.UNKNOWN in (a, b):
        return Parity.UNKNOWN
    if {a, b} == {Parity.EVEN, Parity.ODD}:
        return Parity.TOP
    return Parity.TOP

def add(a, b):
    if Parity.UNKNOWN in (a, b):
        return Parity.UNKNOWN
    if Parity.TOP in (a, b):
        return Parity.TOP
    if a == b:
        return Parity.EVEN
    return Parity.ODD

def multiply(a, b):
    if Parity.UNKNOWN in (a, b):
        return Parity.UNKNOWN
    if Parity.TOP in (a, b):
        return Parity.TOP
    if Parity.EVEN in (a, b):
        return Parity.EVEN
    return Parity.ODD

def analyze_cfg(cfg):
    state = {node: {} for node in cfg.nodes()}
    
    entry_node = [n for n, d in cfg.in_degree() if d == 0][0]
    state[entry_node] = {var: Parity.UNKNOWN for var in get_variables(cfg)}
    
    worklist = list(nx.topological_sort(cfg))
    while worklist:
        node = worklist.pop(0)
        old_state = state[node].copy()
        
        if node != entry_node:
            predecessors = list(cfg.predecessors(node))
            if len(predecessors) == 1:
                state[node] = state[predecessors[0]].copy()
            else:
                state[node] = {var: join(*(state[p].get(var, Parity.UNKNOWN) for p in predecessors)) 
                               for var in set().union(*(state[p].keys() for p in predecessors))}
        
        if 'instruction' in cfg.nodes[node]:
            instruction = cfg.nodes[node]['instruction']
            update_state(state[node], instruction)
        
        # Check for changes to propagate further
        if state[node] != old_state:
            worklist.extend(cfg.successors(node))
    
    return state

def update_state(state, instruction):
    if instruction['type'] == 'assign':
        lhs = instruction['lhs']
        rhs = instruction['rhs']
        if rhs['type'] == 'constant':
            state[lhs] = Parity.EVEN if rhs['value'] % 2 == 0 else Parity.ODD
        elif rhs['type'] == 'variable':
            state[lhs] = state.get(rhs['name'], Parity.UNKNOWN)
        elif rhs['type'] == 'binary_op':
            state[lhs] = get_parity(state, rhs)
    elif instruction['type'] == 'if':
        test = instruction['test']
        if test['type'] == 'compare':
            left = get_parity(state, test['left'])
            right = get_parity(state, test['right'])
            # If either side is known (not UNKNOWN), set both sides to TOP
            if left != Parity.UNKNOWN or right != Parity.UNKNOWN:
                if isinstance(test['left'], dict) and test['left']['type'] == 'variable':
                    state[test['left']['name']] = Parity.TOP
                if isinstance(test['right'], dict) and test['right']['type'] == 'variable':
                    state[test['right']['name']] = Parity.TOP

def get_parity(state, expr):
    if isinstance(expr, dict):
        if expr['type'] == 'constant':
            return Parity.EVEN if expr['value'] % 2 == 0 else Parity.ODD
        elif expr['type'] == 'variable':
            return state.get(expr['name'], Parity.UNKNOWN)
        elif expr['type'] == 'binary_op':
            left = get_parity(state, expr['left'])
            right = get_parity(state, expr['right'])
            if expr['op'] == '+':
                return add(left, right)
            elif expr['op'] == '*':
                return multiply(left, right)
    return Parity.UNKNOWN

def get_variables(cfg):
    variables = set()
    for node in cfg.nodes():
        if 'instruction' in cfg.nodes[node]:
            instr = cfg.nodes[node]['instruction']
            if instr['type'] == 'assign':
                variables.add(instr['lhs'])
                if isinstance(instr['rhs'], dict):
                    variables.update(get_variables_from_expr(instr['rhs']))
            elif instr['type'] == 'if':
                variables.update(get_variables_from_expr(instr['test']))
    return variables

def get_variables_from_expr(expr):
    variables = set()
    if expr['type'] == 'variable':
        variables.add(expr['name'])
    elif expr['type'] == 'binary_op':
        variables.update(get_variables_from_expr(expr['left']))
        variables.update(get_variables_from_expr(expr['right']))
    elif expr['type'] == 'compare':
        variables.update(get_variables_from_expr(expr['left']))
        variables.update(get_variables_from_expr(expr['right']))
    return variables