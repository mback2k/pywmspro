import aiofiles
import json
from aiofiles.os import makedirs
from typing import Any
from .const import (
    WMS_WebControl_pro_API_actionType,
    WMS_WebControl_pro_API_actionDescription,
    WMS_WebControl_pro_API_responseType,
)


class ActionList(list):
    def __init__(self, control) -> None:
        super().__init__()
        self._control = control

    async def __call__(
        self, responseType=WMS_WebControl_pro_API_responseType.Instant
    ) -> Any:
        if len(self) == 0:
            raise ValueError("ActionList is empty")
        return await self._control._action(
            actions=self,
            responseType=responseType,
        )


class Action:
    def __init__(
        self, dest, id: int, actionType: int, actionDescription: int, **kwargs
    ) -> None:
        self._dest = dest
        self._id = id
        self._persist = (dest._persist / f"{id}.json") if dest._persist else None
        self._actionType = WMS_WebControl_pro_API_actionType(actionType)
        self._actionDescription = WMS_WebControl_pro_API_actionDescription(
            actionDescription
        )
        self._attrs = kwargs
        self._params = {}
        self._overwrites = {}
        self._needs_load = True
        self._needs_save = False

    def __str__(self) -> str:
        return self.actionDescription.name

    def __repr__(self) -> str:
        return f"<Action {self.id}: {self} ({self.actionType.name})>"

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

    async def _load_persists(self) -> None:
        if self._persist and self._persist.exists():
            async with aiofiles.open(self._persist, mode='r') as f:
                self._overwrites = json.loads(await f.read()).get("overwrites", {})

    async def _save_persists(self) -> None:
        if self._persist:
            await makedirs(self._persist.parent, exist_ok=True)
            async with aiofiles.open(self._persist, mode='w') as f:
                await f.write(json.dumps({"overwrites": self._overwrites}))

    # --- Public methods ---

    async def sync(self) -> None:
        if self._needs_load:
            await self._load_persists()
            self._needs_load = False
        if self._needs_save:
            await self._save_persists()
            self._needs_save = False

    def __getattr__(self, name: str) -> Any:
        if name in self._overwrites:
            return self._overwrites[name]
        if name.startswith("wms__"):
            name = name[5:]
        return self._attrs.get(name)

    def __getitem__(self, name: str) -> Any:
        if name in self._overwrites:
            return self._overwrites[name]
        return self._params.get(name)

    def __setitem__(self, name: str, value: Any) -> None:
        if name in self._attrs:
            self._overwrites[name] = value
            self._needs_save = True
        elif name in self._params:
            self._params[name] = value

    def __delitem__(self, name: str) -> None:
        if name in self._overwrites:
            del self._overwrites[name]
            self._needs_save = True

    def prep(self, **kwargs) -> ActionList:
        actionList = ActionList(self._dest._control)
        actionList.append({
            "destinationId": self._dest.id,
            "actionId": self.id,
            "parameters": kwargs,
        })
        return actionList

    async def __call__(
        self, responseType=WMS_WebControl_pro_API_responseType.Instant, **kwargs
    ) -> Any:
        return await self._dest._control._action(
            actions=self.prep(**kwargs),
            responseType=responseType,
        )

    def diag(self) -> dict:
        return {
            "id": self.id,
            "actionType": self.actionType.name,
            "actionDescription": self.actionDescription.name,
            "attrs": self._attrs,
            "params": self._params,
            "overwrites": self._overwrites,
        }
