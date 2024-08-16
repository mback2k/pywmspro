
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

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._names[0]
