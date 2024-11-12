import unittest
from io import StringIO
from contextlib import redirect_stdout
from src.cfg_builder import build_cfg
from src.parity_analysis import analyze_cfg
from src.utils import print_cfg, print_analysis_results

class TestUtils(unittest.TestCase):
    def test_print_cfg(self):
        code = "x = 5"
        cfg = build_cfg(code)
        
        with StringIO() as buf, redirect_stdout(buf):
            print_cfg(cfg)
            output = buf.getvalue()
        
        self.assertIn("Node 1:", output)
        self.assertIn("Node 2:", output)
        self.assertIn("Instruction: {'type': 'assign', 'lhs': 'x', 'rhs': {'type': 'constant', 'value': 5}}", output)

    def test_print_analysis_results(self):
        code = "x = 5"
        cfg = build_cfg(code)
        results = analyze_cfg(cfg)
        
        with StringIO() as buf, redirect_stdout(buf):
            print_analysis_results(results)
            output = buf.getvalue()
        
        self.assertIn("Node 1:", output)
        self.assertIn("Node 2:", output)
        self.assertIn("x: O", output)

if __name__ == '__main__':
    unittest.main()