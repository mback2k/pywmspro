from types import MappingProxyType
from .const import (
    WMS_WebControl_pro_API_animationType,
    WMS_WebControl_pro_API_actionType,
    WMS_WebControl_pro_API_actionDescription,
    WMS_WebControl_pro_API_drivingCause,
)
from .action import Action
from .room import Room
import logging

_LOGGER = logging.getLogger(__name__)


class Destination:
    def __init__(
        self, control, id: int, names: list, actions: list, animationType: int
    ) -> None:
        self._control = control
        self._id = id
        self._names = names
        self._actions = {action["id"]: Action(self, **action) for action in actions}
        self._animationType = WMS_WebControl_pro_API_animationType(animationType)
        self._drivingCause = WMS_WebControl_pro_API_drivingCause.Unknown
        self._unknownProducts = {}
        self._heartbeatError = None
        self._blocking = None
        self._status = {}

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Destination {self.id}: {self}>"

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
    def actions(self) -> dict:
        return self._actions

    @property
    def animationType(self) -> WMS_WebControl_pro_API_animationType:
        return self._animationType

    @property
    def drivingCause(self) -> WMS_WebControl_pro_API_drivingCause:
        return self._drivingCause

    @property
    def room(self) -> Room:
        for room in self._control.rooms.values():
            if self._id in room._destination_ids:
                return room
        return None

    @property
    def available(self) -> bool:
        return not (self._heartbeatError or self._blocking)

    @property
    def status(self) -> dict:
        return MappingProxyType(self._status)

    # --- Public methods ---

    async def refresh(self) -> bool:
        status = await self._control._getStatus(self._id)
        if not status:
            _LOGGER.warning("Failed to get status for %s (%s)", self, self._id)
            return False
        self._status = status
        if "details" not in status:
            _LOGGER.warning("No details in status for %s (%s)", self, self._id)
            return False
        refreshed = False
        for detail in status["details"]:
            if detail["destinationId"] != self._id:
                continue
            if "data" not in detail:
                continue
            refreshed = True
            data = detail["data"]
            if "drivingCause" in data:
                self._drivingCause = WMS_WebControl_pro_API_drivingCause(
                    data["drivingCause"]
                )
            if "heartbeatError" in data:
                self._heartbeatError = data["heartbeatError"]
            if "blocking" in data:
                self._blocking = data["blocking"]
            for product in data["productData"]:
                actionId = product["actionId"]
                if actionId in self._actions and "value" in product:
                    self._actions[actionId]._update_params(product["value"])
                else:
                    _LOGGER.warning(
                        "Unknown actionId %s in productData for %s (%s)",
                        actionId,
                        self,
                        self._id,
                    )
                    self._unknownProducts[actionId] = product
        return refreshed

    def action(
        self,
        actionDescription: WMS_WebControl_pro_API_actionDescription,
        actionType: WMS_WebControl_pro_API_actionType = None,
    ) -> Action:
        for action in self._actions.values():
            if action.actionDescription == actionDescription and (
                actionType is None or actionType == action.actionType
            ):
                return action
        _LOGGER.warning(
            "Failed to get action with description %s and type %s in %s (%s)",
            actionDescription,
            actionType,
            self,
            self._id,
        )
        return None

    def diag(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "room": {self.room.id: self.room.name},
            "actions": {k: v.diag() for k, v in self._actions.items()},
            "animationType": self.animationType.name,
            "drivingCause": self.drivingCause.name,
            "available": self.available,
            "unknownProducts": self._unknownProducts,
            "heartbeatError": self._heartbeatError,
            "blocking": self._blocking,
            "status": self._status,
        }
