import unittest
from src.cfg_builder import build_cfg
from src.parity_analysis import analyze_cfg, Parity

class TestParityAnalysis(unittest.TestCase):
    # False Positive Tests
    def test_false_positive_conditional_assignment(self):
        code = """
if input():  # Unknown condition
    x = 2    # Even
else:
    x = 3    # Odd
y = x + 1    # Should be UNKNOWN, not EVEN or ODD
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        # It would be a false positive if we claimed any specific parity
        self.assertEqual(result[6]['y'], Parity.UNKNOWN)


    # False Negative Tests
    def test_false_negative_multiply_by_zero(self):
        code = """
x = 0        # Even
y = input()  # Unknown
z = x * y    # Always Even (0 * anything = 0)
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        # Currently returns 'U', which is a false negative!
        # This test demonstrates that our analysis could be
        # more precise but is being too conservative
        self.assertEqual(result[4]['z'], Parity.UNKNOWN)  # Current behavior
        # TODO: Enhance analysis to detect that 0 * anything = even
        # self.assertEqual(result[4]['z'], Parity.EVEN)  # Desired future behavior

    def test_false_negative_double_increment(self):
        code = """
x = 2        # Even
x = x + 2    # Still Even
"""
        cfg = build_cfg(code)
        result = analyze_cfg(cfg)
        # Should recognize that adding 2 preserves evenness
        self.assertEqual(result[3]['x'], Parity.EVEN)    
    

if __name__ == '__main__':
    unittest.main()