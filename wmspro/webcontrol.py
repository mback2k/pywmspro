import asyncio, pprint
from aiohttp import ClientSession
from .destination import Destination
from .room import Room
from .scene import Scene
from .const import *

class WebControlPro:
    def __init__(self, host: str, session: ClientSession):
        self.control = f"http://{host}/commonCommand"
        self.session = session
        self.dests = {}
        self.rooms = {}
        self.scenes = {}

    # --- Private methods ---

    async def _commonCommand(self, command: str, **kwargs):
        data = {
            "protocolVersion": WMS_WebControl_pro_API_protocolVersion, 
            "command": command, 
            "source": WMS_WebControl_pro_API_source,
        }
        data.update(kwargs)
        async with self.session.post(url=self.control, json=data) as response:
            return await response.json()

    async def _ping(self):
        return await self._commonCommand(WMS_WebControl_pro_API_command_ping)

    async def _getConfiguration(self):
        return await self._commonCommand(WMS_WebControl_pro_API_command_getConfiguration)

    async def _getStatus(self, destination_id: int):
        return await self._commonCommand(WMS_WebControl_pro_API_command_getStatus, destinations=[destination_id])

    async def _action(self, actions: list, responseType=WMS_WebControl_pro_API_responseType.Instant):
        return await self._commonCommand(WMS_WebControl_pro_API_command_action, responseType=responseType, actions=actions)

    # --- Public methods ---

    async def ping(self) -> bool:
        ping = await self._ping()
        return ping["status"] == 0

    async def refresh(self):
        config = await self._getConfiguration()
        self.dests = {dest["id"]: Destination(self, **dest) for dest in config["destinations"]}
        self.rooms = {room["id"]: Room(self, **room) for room in config["rooms"]}
        self.scenes = {scene["id"]: Scene(self, **scene) for scene in config["scenes"]}

    def dest(self, name: str) -> Destination:
        for dest in self.dests.values():
            if dest.name == name:
                return dest
        return None

async def async_main_test():
    async with ClientSession() as session:
        control = WebControlPro("webcontrol", session)
        pprint.pprint(await control.ping())
        await control.refresh()
        for dest in control.dests.values():
            print((dest.room, dest, dest.animationType))
            await dest.refresh()
            for action in dest.actions.values():
                print((action, action.data))

        action = control.dest("Licht").action(WMS_WebControl_pro_API_actionDescription.LightDimming)
        print(action)
        response = await action(percentage=100)
        print(response)

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_main_test())
