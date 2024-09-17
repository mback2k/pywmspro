import asyncio, pprint
from aiohttp import ClientSession
from types import MappingProxyType
from typing import Any
from .destination import Destination
from .room import Room
from .scene import Scene
from .const import *

class WebControlPro:
    def __init__(self, host: str, session: ClientSession):
        self._host = host
        self._control = f"http://{host}/commonCommand"
        self._session = session
        self._config = {}
        self._dests = {}
        self._rooms = {}
        self._scenes = {}

    # --- Private methods ---

    async def _commonCommand(self, command: str, **kwargs) -> Any:
        data = {
            "protocolVersion": WMS_WebControl_pro_API_protocolVersion,
            "command": command,
            "source": WMS_WebControl_pro_API_source,
        }
        data.update(kwargs)
        async with self._session.post(url=self._control, json=data) as response:
            return await response.json()

    async def _ping(self) -> Any:
        return await self._commonCommand(WMS_WebControl_pro_API_command_ping)

    async def _getConfiguration(self) -> Any:
        return await self._commonCommand(WMS_WebControl_pro_API_command_getConfiguration)

    async def _getStatus(self, destinationId: int) -> Any:
        return await self._commonCommand(WMS_WebControl_pro_API_command_getStatus, destinations=[destinationId])

    async def _action(self, actions: list, responseType=WMS_WebControl_pro_API_responseType.Instant) -> Any:
        return await self._commonCommand(WMS_WebControl_pro_API_command_action, responseType=responseType, actions=actions)

    async def _sceneActions(self, sceneId: int, sceneActionType=WMS_WebControl_pro_API_sceneActionType.Execute, responseType=WMS_WebControl_pro_API_responseType.Instant) -> Any:
        return await self._commonCommand(WMS_WebControl_pro_API_command_sceneActions, responseType=responseType, sceneId=sceneId, sceneActionType=sceneActionType)

    # --- Public methods ---

    async def ping(self) -> bool:
        ping = await self._ping()
        return ping["status"] == 0

    async def refresh(self) -> None:
        config = await self._getConfiguration()
        self._config = config
        self._dests = {dest["id"]: Destination(self, **dest) for dest in config["destinations"]}
        self._rooms = {room["id"]: Room(self, **room) for room in config["rooms"]}
        self._scenes = {scene["id"]: Scene(self, **scene) for scene in config["scenes"]}

    def dest(self, name: str) -> Destination:
        for dest in self._dests.values():
            if dest.name == name:
                return dest
        return None

    def diag(self) -> dict:
        return {
            "host": self._host,
            "config": self._config,
            "dests": {k: v.diag() for k, v in self._dests.items()},
            "rooms": {k: v.diag() for k, v in self._rooms.items()},
            "scenes": {k: v.diag() for k, v in self._scenes.items()},
        }

    # --- Properties ---

    @property
    def host(self) -> str:
        return self._host

    @property
    def config(self) -> dict:
        return MappingProxyType(self._config)

    @property
    def dests(self) -> dict:
        return MappingProxyType(self._dests)

    @property
    def rooms(self) -> dict:
        return MappingProxyType(self._rooms)

    @property
    def scenes(self) -> dict:
        return MappingProxyType(self._scenes)


async def async_main_test():
    async with ClientSession() as session:
        control = WebControlPro("webcontrol", session)
        pprint.pprint(await control.ping())
        await control.refresh()

        for dest in control.dests.values():
            print((dest.room, dest, dest.animationType))
            await dest.refresh()
            for action in dest.actions.values():
                print((action, action._attrs, action._params))

        for scene in control.scenes.values():
            print(scene)
            if scene.name == "Licht an":
                response = await scene()
                print(response)

        action = control.dest("Licht").action(WMS_WebControl_pro_API_actionDescription.LightDimming, WMS_WebControl_pro_API_actionType.Percentage)
        print(action)
        response = await action(percentage=100)
        print(response)

        pprint.pprint(control.diag())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_main_test())
