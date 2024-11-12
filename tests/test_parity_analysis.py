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

if __name__ == '__main__':
    unittest.main()