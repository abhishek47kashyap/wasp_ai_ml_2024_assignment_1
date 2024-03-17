
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

    # get coefficients A, B, C for equation of a line where Ax + By + C = 0 (https://stackoverflow.com/a/13242831/6010333)
    x1, y1 = endpoint_a.x, endpoint_a.y
    x2, y2 = endpoint_b.x, endpoint_b.y
    a = y1 - y2
    b = x2 - x1
    c = (x1 - x2) * y1 + (y2 - y1) * x1

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
