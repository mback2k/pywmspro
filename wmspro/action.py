from typing import Any
from .const import WMS_WebControl_pro_API_actionType, WMS_WebControl_pro_API_actionDescription

class Action:
    def __init__(self, dest, id: int, actionType: int, actionDescription: int, **kwargs) -> None:
        self._dest = dest
        self._id = id
        self._actionType = WMS_WebControl_pro_API_actionType(actionType)
        self._actionDescription = WMS_WebControl_pro_API_actionDescription(actionDescription)
        self._attrs = kwargs
        self._params = {}

    def __str__(self) -> str:
        return self.actionDescription.name

    def __repr__(self) -> str:
        return f'<Action {self.id}: {self} ({self.actionType.name})>'

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    # --- Properties ---

    @property
    def host(self) -> str:
        return self._dest.host

    @property
    def id(self) -> int:
        return self._id

    @property
    def actionType(self) -> WMS_WebControl_pro_API_actionType:
        return self._actionType

    @property
    def actionDescription(self) -> WMS_WebControl_pro_API_actionDescription:
        return self._actionDescription

    # --- Private methods ---

    def _update_params(self, value: dict) -> None:
        self._params.update(value)

    # --- Public methods ---

    def __getattr__(self, name: str) -> Any:
        return self._attrs.get(name)

    def __getitem__(self, name: str) -> Any:
        return self._params.get(name)

    async def __call__(self, **kwargs) -> Any:
        return await self._dest._control._action(actions=[
            {"destinationId": self._dest.id,
             "actionId": self.id,
             "parameters": kwargs}
        ])

    def diag(self) -> dict:
        return {
            "id": self.id,
            "actionType": self.actionType.name,
            "actionDescription": self.actionDescription.name,
            "attrs": self._attrs,
            "params": self._params,
       }
