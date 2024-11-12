import ast
import networkx as nx

class CFGBuilder(ast.NodeVisitor):
    def __init__(self):
        self.cfg = nx.DiGraph()
        self.current_node = 0
        self.entry_node = self.new_node('Entry')

    def visit_Module(self, node):
        self.generic_visit(node)
        self.new_node('Exit')

    def visit_Assign(self, node):
        assign_node = self.new_node('Assign')
        self.cfg.nodes[assign_node]['instruction'] = {
            'type': 'assign',
            'lhs': node.targets[0].id,
            'rhs': self.parse_expression(node.value)
        }
    
    def visit_If(self, node):
        if_node = self.new_node('If')
        self.cfg.nodes[if_node]['instruction'] = {
            'type': 'if',
            'test': self.parse_expression(node.test)
        }
        
        then_entry = self.new_node('ThenEntry')
        self.visit(node.body[0])  # Assume single statement in then block
        then_exit = self.current_node

        if node.orelse:
            else_entry = self.new_node('ElseEntry')
            self.visit(node.orelse[0])  # Assume single statement in else block
            else_exit = self.current_node
        else:
            else_entry = else_exit = self.new_node('ElseEmpty')

        merge_node = self.new_node('IfMerge')
        self.cfg.add_edge(if_node, then_entry)
        self.cfg.add_edge(if_node, else_entry)
        self.cfg.add_edge(then_exit, merge_node)
        self.cfg.add_edge(else_exit, merge_node)

    def new_node(self, label):
        self.current_node += 1
        self.cfg.add_node(self.current_node, label=label)
        if self.current_node > 1:
            self.cfg.add_edge(self.current_node - 1, self.current_node)
        return self.current_node


    def parse_expression(self, expr):
        if isinstance(expr, ast.Num):
            return {'type': 'constant', 'value': expr.n}
        elif isinstance(expr, ast.Name):
            return {'type': 'variable', 'name': expr.id}
        elif isinstance(expr, ast.BinOp):
            return {
                'type': 'binary_op',
                'op': self.get_op_symbol(expr.op),
                'left': self.parse_expression(expr.left),
                'right': self.parse_expression(expr.right)
            }
        return {'type': 'unknown'}

    def get_op_symbol(self, op):
        if isinstance(op, ast.Add):
            return '+'
        elif isinstance(op, ast.Mult):
            return '*'
        return 'unknown'

def build_cfg(code):
    tree = ast.parse(code)
    cfg_builder = CFGBuilder()
    cfg_builder.visit(tree)
    return cfg_builder.cfg