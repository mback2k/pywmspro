from .const import WMS_WebControl_pro_API_animationType
from .action import Action

class Destination:
    def __init__(self, control, id, names, actions, animationType):
        self._control = control
        self._id = id
        self._names = names
        self._actions = {action["id"]: Action(self._control, **action) for action in actions}
        self._animationType = WMS_WebControl_pro_API_animationType(animationType)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Destination {self.id}: {self}>'

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

    @property
    def actions(self):
        return self._actions

    @property
    def animationType(self):
        return self._animationType

    @property
    def room(self):
        for room in self._control.rooms.values():
            if self._id in room._destination_ids:
                return room
        return None

    async def refresh(self):
        status = await self._control._getStatus(self._id)
        for detail in status["details"]:
            if detail["destinationId"] != self._id:
                continue

            for product in detail["data"]["productData"]:
                self._actions[product["actionId"]]._refresh(value=product["value"])
