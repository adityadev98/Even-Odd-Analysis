import unittest
from src.cfg_builder import build_cfg
from src.parity_analysis import analyze_cfg, Parity

class TestParityAnalysis(unittest.TestCase):
    import unittest
from src.cfg_builder import build_cfg
from src.parity_analysis import analyze_cfg, Parity

class TestParityAnalysis(unittest.TestCase):
    def test_odd_plus_even_not_even(self):
        code = """
x = 3        # Odd
y = 2        # Even
z = x + y    # Should be Odd, not Even
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertNotEqual(result[4]['z'], Parity.EVEN)

    def test_unknown_input_remains_unknown(self):
        code = """
x = input()  # Unknown
y = 2        # Even
z = x + y    # Should be Unknown, not Even or Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertNotEqual(result[4]['z'], Parity.EVEN)
        self.assertNotEqual(result[4]['z'], Parity.ODD)

    def test_even_times_even_not_odd(self):
        code = """
x = 2        # Even
y = 4        # Even
z = x * y    # Should be Even, not Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertNotEqual(result[4]['z'], Parity.ODD)

    def test_complex_expression_with_unknown(self):
        code = """
x = input()  # Unknown
y = 2        # Even
z = 3        # Odd
w = (x + y) * z  # Should be Unknown, not Even or Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertNotEqual(result[5]['w'], Parity.EVEN)
        self.assertNotEqual(result[5]['w'], Parity.ODD)

    def test_variable_reassignment(self):
        code = """
x = 2        # Even
x = 3        # Now Odd
y = x + 1    # Should be Even, not Odd
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertNotEqual(result[4]['y'], Parity.ODD)
        self.assertEqual(result[4]['y'], Parity.EVEN)

    def test_undefined_variable_usage(self):
        code = """
y = x + 1    # x is undefined
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        self.assertNotEqual(result[2]['y'], Parity.EVEN)
        self.assertNotEqual(result[2]['y'], Parity.ODD)
        self.assertEqual(result[2]['y'], Parity.UNKNOWN)
    

if __name__ == '__main__':
    unittest.main()