
from resources.containers import EntityPosition

def euclidean_distance(a: EntityPosition, b: EntityPosition) -> float:
    return ((a.x - b.x)**2 + (a.y - b.y)**2) ** 0.5

def distance_from_point_to_line_between_two_points(endpoint_a: EntityPosition, endpoint_b: EntityPosition, some_point: EntityPosition) -> list[float, EntityPosition]:
    """
        Given 3 points, this function returns:
        - shortest distance from some_point to the line segment joining the two endpoints (endpoint_a and endpoint_b)
        - closest point to some_point on the line segment
    """
    if endpoint_a == endpoint_b:
        shortest_distance = euclidean_distance(some_point, endpoint_a)
        return [shortest_distance, endpoint_a]

    [a, b, c] = get_equation_coeff_of_line_from_two_points(endpoint_a, endpoint_b)

    # distance and point on the line (https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_an_equation)
    x0, y0 = some_point.x, some_point.y
    a2_b2 = a ** 2 + b ** 2
    ac = a * c
    bc = b * c
    a_y0 = a * y0
    b_x0 = b * x0
    shortest_distance = (abs(a * x0 + b * y0 + c)) / (a2_b2 ** 0.5)
    nearest_point = EntityPosition(
        x = (b * (b_x0 - a_y0) - ac) / a2_b2,
        y = (a * (a_y0 - b_x0) - bc) / a2_b2
    )
    return [shortest_distance, nearest_point]

def get_equation_coeff_of_line_from_two_points(point_a: EntityPosition, point_b: EntityPosition) -> list[int, int, int]:
    """
        Get coefficients A, B, C for equation of a line where Ax + By + C = 0 (https://stackoverflow.com/a/13242831/6010333)
    """
    x1, y1 = point_a.x, point_a.y
    x2, y2 = point_b.x, point_b.y
    a = y1 - y2
    b = x2 - x1
    c = (x1 - x2) * y1 + (y2 - y1) * x1
    return [a, b, c]

def point_falls_between_two_points(endpoint_a: EntityPosition, endpoint_b: EntityPosition, some_point: EntityPosition) -> bool:
    """
        Returns whether a point falls in the region between two points.
        See https://math.stackexchange.com/questions/1915322/determine-if-a-point-lies-between-two-parallel-lines
    """
    [a, b, _] = get_equation_coeff_of_line_from_two_points(endpoint_a, endpoint_b)

    """
        Working out the math to obtain equation of line passing through some_point and being perpendicular to the line
        connecting endpoint_a and endpoint_b, the new coefficients are:
            A' = -B
            B' = A
            C' = (B * some_point.x) - (A * some_point.y)
    """

    def get_signed_distance(A, B, C, X, Y) -> float:
        numerator = (A * X) + (B * Y) + C
        denominator = (A**2 + B**2) ** 0.5
        return (numerator / denominator)

    # normal line
    a_normal = -b
    b_normal = a

    c_endpoint_a = (b * endpoint_a.x) - (a * endpoint_a.y)
    c_endpoint_b = (b * endpoint_b.x) - (a * endpoint_b.y)

    dist1 = get_signed_distance(a_normal, b_normal, c_endpoint_a, some_point.x, some_point.y)
    dist2 = get_signed_distance(a_normal, b_normal, c_endpoint_b, some_point.x, some_point.y)

    falls_between = (dist1 <= 0 and dist2 >= 0) or (dist1 >= 0 and dist2 <= 0)  # dist1 and dist2 should have opposite sites
    return falls_between
