
class Room:
    def __init__(self, control, id: int, name: str, destinations: list, scenes: list):
        self._control = control
        self._id = id
        self._name = name
        self._destination_ids = destinations
        self._scene_ids = scenes

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<Room {self.id}: {self}>'

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
        return self._name

    @property
    def destinations(self) -> dict:
        return {dest_id: self._control.dests[dest_id] for dest_id in self._destination_ids}

    @property
    def scenes(self) -> dict:
        return {scene_id: self._control.scenes[scene_id] for scene_id in self._scene_ids}

    # --- Public methods ---

    def diag(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "destinations": {dest.id: dest.name for dest in self.destinations.values()},
            "scenes": {scene.id: scene.name for scene in self.scenes.values()},
        }
