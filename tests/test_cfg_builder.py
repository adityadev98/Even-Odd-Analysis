import unittest
from src.cfg_builder import build_cfg

class TestCFGBuilder(unittest.TestCase):
    def test_simple_assignment(self):
        code = "x = 5"
        cfg = build_cfg(code)
        self.assertEqual(len(cfg.nodes), 3)  # Entry + Assignment + Exit
        self.assertEqual(cfg.nodes[2]['instruction']['type'], 'assign')
        self.assertEqual(cfg.nodes[2]['instruction']['lhs'], 'x')
        self.assertEqual(cfg.nodes[2]['instruction']['rhs']['type'], 'constant')
        self.assertEqual(cfg.nodes[2]['instruction']['rhs']['value'], 5)

    def test_if_statement(self):
        code = """
if x > 0:
    y = 1
else:
    y = 2
"""
        cfg = build_cfg(code)
        self.assertGreater(len(cfg.nodes), 3)  # At least Entry, If, Then, Else
        if_node = [n for n, d in cfg.nodes(data=True) if d.get('label') == 'If'][0]
        self.assertEqual(cfg.nodes[if_node]['instruction']['type'], 'if')

if __name__ == '__main__':
    unittest.main()