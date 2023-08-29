from __future__ import annotations
from mountain import Mountain

class MountainManager:

    def __init__(self) -> None:
        pass

    def add_mountain(self, mountain: Mountain) -> None:
        raise NotImplementedError()

    def remove_mountain(self, mountain: Mountain) -> None:
        raise NotImplementedError()

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        raise NotImplementedError()

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        raise NotImplementedError()

    def group_by_difficulty(self) -> list[list[Mountain]]:
        raise NotImplementedError()
