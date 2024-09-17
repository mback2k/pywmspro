from typing import Any
from .room import Room

class Scene:
    def __init__(self, control, id: int, names: list):
        self._control = control
        self._id = id
        self._names = names

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<Scene {self.id}: {self}>'

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    # --- Properties ---

    @property
    def host(self) -> str:
        return self._control.host

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._names[0]

    @property
    def room(self) -> Room:
        for room in self._control.rooms.values():
            if self._id in room._scene_ids:
                return room
        return None

    # --- Public methods ---

    async def __call__(self, **kwargs) -> Any:
        return await self._control._sceneActions(self._id, **kwargs)

    def diag(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "room": {self.room.id: self.room.name},
        }
