
from resources.containers import EntityPose

class Entity:
    def __init__(self, initial_position: EntityPose, perception_radius: float, id: int, radius: float = 0.3):
        self.id = id
        self.radius = radius
        self.perception_radius = perception_radius
        self.current_position = initial_position

        self._initial_position = initial_position

    def move_towards(self, target_position: EntityPose, step_size: float = None) -> None:
        """
            Move towards a target_position from current_position, if not already there.

            step_size:
                - If not specified, jump to target_position
                - If specified:
                    - if step_size is less than distance to target_position, only move step_size distance towards target_position
                    - if step_size is equal to or greater than distance to target_position, jump to target_position (overshooting cannot happen)
        """

        # early return if already at target_position
        if target_position == self.current_position:
            return

        # if step_size not specified, then update current_position to target_position and early return
        if step_size is None:
            self.current_position = target_position
            return

        # since step_size has been specified, we want to take a step in the direction of target_position
        dx = target_position.x - self.current_position.x
        dy = target_position.y - self.current_position.y
        vector = (dx, dy)
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if step_size >= distance:
            self.current_position = target_position     # we don't want to overshoot
        else:
            unit_vector = tuple(i / distance for i in vector)
            self.current_position.x += unit_vector[0] * step_size
            self.current_position.y += unit_vector[1] * step_size

    def move_towards_somewhere_between(self, position_a: EntityPose, position_b: EntityPose, step_size: float = None) -> None:
        """
            Move towards the closest point on the line connecting position_a and position_b. This closest point on the line
            becomes the target_position for which move_towards() can be called.
        """
        if position_a == position_b:
            return self.move_towards(position_a, step_size)

        # get coefficients A, B, C for equation of a line where Ax + By + C = 0 (https://stackoverflow.com/a/13242831/6010333)
        x1, y1 = position_a.x, position_a.y
        x2, y2 = position_b.x, position_b.y
        a = y1 - y2
        b = x2 - x1
        c = (x1 - x2) * y1 + (y2 - y1) * x1

        # distance and point on the line (https://en.wikipedia.org/wiki/Distance_from_a_point_to_a_line#Line_defined_by_an_equation)
        x0, y0 = self.current_position.x, self.current_position.y
        a2_b2 = a ** 2 + b ** 2
        ac = a * c
        bc = b * c
        a_y0 = a * y0
        b_x0 = b * x0
        # distance = (abs(a * x0 + b * y0 + c)) / (a2_b2 ** 0.5)
        closest_point_on_line = EntityPose(
            x = (b * (b_x0 - a_y0) - ac) / a2_b2,
            y = (a * (a_y0 - b_x0) - bc) / a2_b2
        )
        return self.move_towards(closest_point_on_line, step_size)

    def update_current_pose(self, pose: EntityPose):
        self.current_position = pose

    def __repr__(self) -> str:
        return f"Id {self.id}: position ({self.current_position.x:.3f}, {self.current_position.y:.3f})"
        
