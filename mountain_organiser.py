from __future__ import annotations

from mountain import Mountain

class MountainOrganiser:

    def __init__(self) -> None:
        raise NotImplementedError()

    def cur_position(self, mountain: Mountain) -> int:
        raise NotImplementedError()

    def add_mountains(self, mountains: list[Mountain]) -> None:
        raise NotImplementedError()
