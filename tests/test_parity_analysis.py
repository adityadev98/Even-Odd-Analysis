import unittest
from src.cfg_builder import build_cfg
from src.parity_analysis import analyze_cfg, Parity

class TestParityAnalysis(unittest.TestCase):

    def test_simple_even(self):
        code = "x = 2"
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[2]['x'], Parity.EVEN)

    def test_simple_odd(self):
        code = "x = 3"
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[2]['x'], Parity.ODD)

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

    def test_top_result_from_operation(self):
        code = """
x = 2        # Even
y = 3        # Odd
z = x + y    # Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[4]['z'], Parity.ODD)

    def test_unknown_propagation(self):
        code = """
x = input()  # Unknown input
y = 2        # Even
z = x + y    # Still unknown
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[4]['z'], Parity.UNKNOWN)

    def test_top_from_comparison(self):
        code = """
x = input()  # Unknown input
if x > 0:
    y = x    
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        x_nodes = [node for node in result.keys() if 'x' in result[node]]
        x_node = max(x_nodes)
        self.assertEqual(result[x_node]['x'], Parity.UNKNOWN)

    def test_even_odd_operation(self):
        code = """
x = 2        # Even
y = 3        # Odd
z = x * y    # Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[4]['z'], Parity.EVEN)

    def test_complex_operation(self):
        code = """
x = 2        # Even
y = 3        # Odd
z = 4        # Even
w = x + y * z  # Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[5]['w'], Parity.EVEN)

    def test_unknown_in_complex_operation(self):
        code = """
x = input()  # Unknown
y = 2        # Even
z = 3        # Odd
w = x + y * z  # Unknown
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertEqual(result[5]['w'], Parity.UNKNOWN)

    def test_top_propagation(self):
        code = """
x = input()  # Unknown
if x > 0:
    y = x    # x and y become TOP
z = y + 1    # z is TOP
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        z_nodes = [node for node in result.keys() if 'z' in result[node]]
        z_node = max(z_nodes)
        self.assertEqual(result[z_node]['z'], Parity.UNKNOWN)

if __name__ == '__main__':
    unittest.main()