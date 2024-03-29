
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

    def test_1_point_falls_between_two_points(self):
        endpoint_a = EntityPosition(x = 0, y = -3)
        endpoint_b = EntityPosition(x = 0, y = 3)
        some_point = EntityPosition(x = 0, y = 30)
        result = math_utils.point_falls_between_two_points(endpoint_a, endpoint_b, some_point)
        expected_result = False
        self.assertEqual(result, expected_result, f"y = 30 cannot possibly be between y = [-3, 3] when x = 0")

    def test_2_point_falls_between_two_points(self):
        endpoint_a = EntityPosition(x = -45, y = 3)
        endpoint_b = EntityPosition(x = 45, y = -3)
        some_point = EntityPosition(x = 0, y = 0)
        result = math_utils.point_falls_between_two_points(endpoint_a, endpoint_b, some_point)
        expected_result = True
        self.assertEqual(result, expected_result, f"Origin is between two points (x = -45, y = 3) and (x = 45, y = -3)")


if __name__ == "__main__":
    unittest.main()
