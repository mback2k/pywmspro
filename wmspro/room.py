
class Room:
    def __init__(self, control, id, name, destinations, scenes):
        self._control = control
        self._id = id
        self._name = name
        self._destination_ids = destinations
        self._scene_ids = scenes

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Room {self.id}: {self}>'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def destinations(self):
        return {dest_id: self._control.dests[dest_id] for dest_id in self._destination_ids}

    @property
    def scenes(self):
        return {scene_id: self._control.scenes[scene_id] for scene_id in self._scene_ids}
