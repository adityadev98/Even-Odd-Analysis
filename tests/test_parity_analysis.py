import unittest
from src.cfg_builder import build_cfg
from src.parity_analysis import analyze_cfg, Parity

class TestParityAnalysis(unittest.TestCase):

    def test_unknown_input(self):
        code = "x = input()"
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[2]['x'], Parity.UNKNOWN)

    def test_unknown_result(self):
        code = """
x = input()  # Unknown input
y = x + 1    # Still unknown
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[3]['y'], Parity.UNKNOWN)

    def test_top_result_from_if(self):
        code = """
x = input()  # Unknown input
if x > 0:
    y = 2    # Even
else:
    y = 3    # Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        y_nodes = [node for node in result.keys() if 'y' in result[node]]
        y_node = max(y_nodes)
        self.assertEqual(result[y_node]['y'], Parity.TOP)

if __name__ == '__main__':
    unittest.main()