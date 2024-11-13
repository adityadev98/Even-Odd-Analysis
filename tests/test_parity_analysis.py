import unittest
from src.cfg_builder import build_cfg
from src.parity_analysis import analyze_cfg, Parity

class TestParityAnalysis(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()