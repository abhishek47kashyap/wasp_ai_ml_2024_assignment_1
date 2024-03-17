
"""
    Run this as 'python -m tests.math_utils' as advised here: https://stackoverflow.com/a/11536794/6010333
"""

from resources import math_utils
from resources.containers import EntityPosition

import unittest

class TestMathUtils(unittest.TestCase):
    def test_euclidean_distance(self):
        a = EntityPosition(x = 3, y = 0)
        b = EntityPosition(x = 0, y = 4)
        result = math_utils.euclidean_distance(a, b)
        expected_result = 5.0
        self.assertEqual(result, expected_result, f"Expected {expected_result} but got {result}")

    def test_1_distance_from_point_to_line_between_two_points(self):
        some_point = EntityPosition(x = 0, y = 0)
        endpoint_a = EntityPosition(x = 3, y = -3)
        endpoint_b = EntityPosition(x = 3, y = 3)
        result = math_utils.distance_from_point_to_line_between_two_points(endpoint_a, endpoint_b, some_point)
        expected_result = [3.0, EntityPosition(x = 3.0, y = 0.0)]
        self.assertEqual(result, expected_result, f"Expected {expected_result} but got {result}")

    def test_2_distance_from_point_to_line_between_two_points(self):
        some_point = EntityPosition(x = 0, y = 30)
        endpoint_a = EntityPosition(x = 3, y = -3)
        endpoint_b = EntityPosition(x = 3, y = 3)
        result = math_utils.distance_from_point_to_line_between_two_points(endpoint_a, endpoint_b, some_point)
        expected_result = [3.0, EntityPosition(x = 3.0, y = 30.0)]
        self.assertEqual(result, expected_result, f"Expected {expected_result} but got {result}")


if __name__ == "__main__":
    unittest.main()