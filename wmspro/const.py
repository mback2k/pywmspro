from enum import IntEnum

WMS_WebControl_pro_API_protocolVersion = "1.0"
WMS_WebControl_pro_API_source = 2

WMS_WebControl_pro_API_command_ping = "ping"
WMS_WebControl_pro_API_command_getConfiguration = "getConfiguration"
WMS_WebControl_pro_API_command_getStatus = "getStatus"
WMS_WebControl_pro_API_command_action = "action"
WMS_WebControl_pro_API_command_sceneActions = "sceneActions"

class WMS_WebControl_pro_API_animationType(IntEnum):
    VenetianBlind = 0
    Awning = 1
    RollerShutterBlind = 2
    SlatRoof = 3
    Window = 4
    Switch = 5
    Dimmer = 6
    Unknown = 999

class WMS_WebControl_pro_API_actionType(IntEnum):
    Percentage = 0
    PercentageDelta = 1
    Rotation = 2
    RotationDelta = 3
    Switch = 4
    Toggle = 5
    Stop = 6
    Impulse = 7
    Identify = 8
    Enumeration = 9
    Unknown = 999

class WMS_WebControl_pro_API_actionDescription(IntEnum):
    AwningDrive = 0
    ValanceDrive = 1
    SlatDrive = 2
    SlatRotate = 3
    RollerShutterBlindDrive = 4
    WindowDrive = 5
    LightSwitch = 6
    LoadSwitch = 7
    LightDimming = 8
    LoadDimming = 9
    LightToggle = 10
    LastToggle = 11
    ManualCommand = 12
    Identify = 13
    Unknown = 999

class WMS_WebControl_pro_API_responseType(IntEnum):
    Instant = 0
    Detailed = 1

class WMS_WebControl_pro_API_sceneActionType(IntEnum):
    Relearn = 0
    Execute = 1

class WMS_WebControl_pro_API_drivingCause(IntEnum):
    _None = 0 # No driving cause
    Sun = 1
    DuskDawn = 2
    Wind = 3
    Rain = 4
    Ice = 5
    Temperature = 6
    SwitchingTime = 7
    Scene = 8
    ControlMode = 9
    Manual = 10
    Safety = 11
    Contact = 12
    CentralCommand = 13
    Unknown = 999
