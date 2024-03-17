
from resources.containers import EntityPosition
from resources.math_utils import distance_from_point_to_line_between_two_points

class Entity:
    def __init__(self, initial_position: EntityPosition, perception_radius: float, id: int, radius: float = 0.3):
        self.id = id
        self.radius = radius
        self.perception_radius = perception_radius
        self.current_position = initial_position

        self._initial_position = initial_position

    def move_towards(self, target_position: EntityPosition, step_size: float = None) -> None:
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

    def move_towards_somewhere_between(self, position_a: EntityPosition, position_b: EntityPosition, step_size: float = None) -> None:
        """
            Move towards the closest point on the line connecting position_a and position_b. This closest point on the line
            becomes the target_position for which move_towards() can be called.
        """
        if position_a == position_b:
            return self.move_towards(position_a, step_size)

        _, closest_point_on_line = distance_from_point_to_line_between_two_points(position_a, position_b, self.current_position)
        return self.move_towards(closest_point_on_line, step_size)

    def update_current_position(self, position: EntityPosition):
        self.current_position = position

    def __repr__(self) -> str:
        return f"Id {self.id}: position ({self.current_position.x:.3f}, {self.current_position.y:.3f})"
