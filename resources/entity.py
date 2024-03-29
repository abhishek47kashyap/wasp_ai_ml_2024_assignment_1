
from resources.containers import EntityPosition
from resources.math_utils import euclidean_distance, distance_from_point_to_line_between_two_points, point_falls_between_two_points

class Entity:
    def __init__(self, initial_position: EntityPosition, perception_radius: float, id: int, radius: float = 0.3):
        self.id = id
        self.radius = radius
        self.perception_radius = perception_radius
        self.current_position = initial_position

        # If an entity is not a root, it means it will never move for fulfilling a game policy.
        # By default, entity is assumed to move as the game progresses. 
        self._is_root = True

        # maintaing history
        self._initial_position = initial_position
        self._history_n = 5 # no. of positions to track
        self._last_n_positions = [initial_position] # FIFO of fixed length

    def has_converged(self) -> bool:
        """
            Checks entity's tracked history to determine if movements have been following a non-increasing order
            i.e. distances covered have either decreased or stayed the same.
        """
        if len(self._last_n_positions) < self._history_n:
            return False

        # grab pairs from history: https://stackoverflow.com/a/5764948/6010333
        delta = []
        for previous, next in zip(self._last_n_positions, self._last_n_positions[1:]):
            delta.append(euclidean_distance(previous, next))

        # check if movements are decreasing or staying the same (i.e. should not be increasing)
        not_increasing = all(earlier >= later for earlier, later in zip(delta, delta[1:]))  # https://stackoverflow.com/a/12734228/6010333
        return not_increasing

    def get_tracking_history(self) -> list[EntityPosition]:
        return self._last_n_positions

    def is_root(self) -> bool:
        return self._is_root

    def mark_as_not_root(self):
        self._is_root = False

    def move_somewhere_on_the_line_connecting(self, position_a: EntityPosition, position_b: EntityPosition, step_size: float = None) -> None:
        """
            Move towards the closest point on the line connecting position_a and position_b. This closest point on the line
            becomes the target_position for which move_towards() can be called.

            This closest point doesn't necessarily need to lie on the line *segment* connecting position_a and position_b.
        """
        if position_a == position_b:
            return self.move_towards(position_a, step_size)

        _, closest_point_on_line = distance_from_point_to_line_between_two_points(position_a, position_b, self.current_position)
        return self.move_towards(closest_point_on_line, step_size)

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
            self.update_current_position(target_position)
            return

        # since step_size has been specified, we want to take a step in the direction of target_position
        dx = target_position.x - self.current_position.x
        dy = target_position.y - self.current_position.y
        vector = (dx, dy)
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if step_size >= distance:
            self.update_current_position(target_position)     # we don't want to overshoot
        else:
            unit_vector = tuple(i / distance for i in vector)
            self.current_position.x += unit_vector[0] * step_size
            self.current_position.y += unit_vector[1] * step_size
            self._update_tracking_history(self.current_position)

    def move_towards_halfway_between(self, position_a: EntityPosition, position_b: EntityPosition, step_size: float = None) -> None:
        """
            Move towards the halfway mark between position_a and position_b. The halfway mark
            becomes the target_position for which move_towards() can be called.
        """
        if position_a == position_b:
            return self.move_towards(position_a, step_size)

        halfway_mark = EntityPosition(
            x = (position_a.x + position_b.x) / 2.0,
            y = (position_a.y + position_b.y) / 2.0
        )

        return self.move_towards(halfway_mark, step_size)

    def move_behind_entity(self, shield_from: EntityPosition, use_as_shield: EntityPosition, step_size: float = None, dist_behind: float = None) -> None:
        if shield_from == use_as_shield:
            return

        if point_falls_between_two_points(endpoint_a=shield_from, endpoint_b=self.current_position, some_point=use_as_shield):
            self.move_somewhere_on_the_line_connecting(shield_from, use_as_shield, step_size)
        else:
            # create vector pointing FROM shield_from TO use_as_shield 
            dx = use_as_shield.x - shield_from.x
            dy = use_as_shield.y - shield_from.y
            vector = (dx, dy)
            distance = (dx ** 2 + dy ** 2) ** 0.5
            unit_vector = tuple(i / distance for i in vector)
            # find position dist_behind relative to use_as_shield in the direction of the vector
            target_position = EntityPosition(
                x = use_as_shield.x + (unit_vector[0] * dist_behind),
                y = use_as_shield.x + (unit_vector[1] * dist_behind)
            )
            # move to that position
            self.move_towards(target_position, step_size)

    def update_current_position(self, position: EntityPosition) -> None:
        """
            Updates entity's current position and updates tracking history
        """
        self.current_position = position
        self._update_tracking_history(position)

    def _update_tracking_history(self, position: EntityPosition) -> None:
        """
            Stores last N positions of entity thereby tracking history
        """
        if len(self._last_n_positions) > self._history_n:
            self._last_n_positions.pop(0)

        self._last_n_positions.append(position)


    def __repr__(self) -> str:
        return f"Id {self.id}: position ({self.current_position.x:.3f}, {self.current_position.y:.3f})"
