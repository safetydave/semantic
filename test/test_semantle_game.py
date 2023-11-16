import unittest

from src.semantle_simulator import SemantleSimulator


class TestSemantleGame(unittest.TestCase):

    def test_guess_target_should_score_100(self):
        simulator = SemantleSimulator()
        score = simulator.score_guess('mystery', target='mystery')
        self.assertAlmostEqual(score, 100.0, 1)