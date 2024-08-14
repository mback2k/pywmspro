from .const import WMS_WebControl_pro_API_animationType, WMS_WebControl_pro_API_actionDescription, WMS_WebControl_pro_API_drivingCause
from .action import Action

class Destination:
    def __init__(self, control, id, names, actions, animationType):
        self._control = control
        self._id = id
        self._names = names
        self._actions = {action["id"]: Action(self, **action) for action in actions}
        self._animationType = WMS_WebControl_pro_API_animationType(animationType)
        self._drivingCause = WMS_WebControl_pro_API_drivingCause.Unknown
        self._heartbeatError = None
        self._blocking = None

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

    async def refresh(self) -> bool:
        status = await self._control._getStatus(self._id)
        if not "details" in status:
            return False
        refreshed = False
        for detail in status["details"]:
            if detail["destinationId"] != self._id:
                continue
            if not "data" in detail:
                continue
            refreshed = True
            data = detail["data"]
            if "drivingCause" in data:
                self._drivingCause = WMS_WebControl_pro_API_drivingCause(data["drivingCause"])
            if "heartbeatError" in data:
                self._heartbeatError = data["heartbeatError"]
            if "blocking" in data:
                self._blocking = data["blocking"]
            for product in data["productData"]:
                self._actions[product["actionId"]]._update(parameters=product["value"])
        return refreshed

    def action(self, actionDescription: WMS_WebControl_pro_API_actionDescription):
        for action in self._actions.values():
            if action.actionDescription == actionDescription:
                return action
        return None
