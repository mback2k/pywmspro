from .const import WMS_WebControl_pro_API_actionType, WMS_WebControl_pro_API_actionDescription

class Action:
    def __init__(self, control, id, actionType, actionDescription, **kwargs):
        self._control = control
        self._id = id
        self._actionType = WMS_WebControl_pro_API_actionType(actionType)
        self._actionDescription = WMS_WebControl_pro_API_actionDescription(actionDescription)
        self._data = kwargs

    def __str__(self):
        return str(self.actionDescription)

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

    def _refresh(self, **kwargs):
        self._data.update(kwargs)

    # TODO: serialize action
