
class Scene:
    def __init__(self, control, id, names):
        self._control = control
        self._id = id
        self._names = names

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Scene {self.id}: {self}>'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._names[0]
