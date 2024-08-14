from .const import WMS_WebControl_pro_API_actionType, WMS_WebControl_pro_API_actionDescription

class Action:
    def __init__(self, dest, id, actionType, actionDescription, **kwargs):
        self._dest = dest
        self._id = id
        self._actionType = WMS_WebControl_pro_API_actionType(actionType)
        self._actionDescription = WMS_WebControl_pro_API_actionDescription(actionDescription)
        self._data = kwargs

    def __str__(self):
        return self.actionDescription.name

    def __repr__(self):
        return f'<Action {self.id}: {self}>'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    @property
    def id(self):
        return self._id

    @property
    def actionType(self):
        return self._actionType

    @property
    def actionDescription(self):
        return self._actionDescription

    @property
    def data(self):
        return self._data

    def _update(self, **kwargs):
        self._data.update(kwargs)

    async def __call__(self, **kwargs):
        return await self._dest._control._action(actions=[
            {"destinationId": self._dest.id,
             "actionId": self.id,
             "parameters": kwargs}
        ])
