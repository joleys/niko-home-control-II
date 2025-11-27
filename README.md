# Niko Home Control II Home Assistant Integration

License: [MIT](LICENSE)

This custom component will allow you to integrate you Niko Connected Controller II in Home Assistant.
You can use a touchscreen profile or the Hobby API account.

This integration communicates directly with the controller. You only need internet when activating/renewing the Hobby
API. If you use a touch screen profile, this isn't even needed.

**IMPORTANT**: There is an issue with the touch profiles, so the only supported way to configure the controller is the
Niko Hobby API.

## Acknowledgements

This custom component is a [spin-off of the hard and excellent work by @filipvh](https://github.com/filipvh/hass-nhc2).
Thanks!

A big thanks to Johan and Koen from Niko for their support and providing the test equipment.

Some people who made this possible, and should be mentioned:

* @nexus256
* @joleys
* @tijsverkoyen

## What works now?

Everything is developed against the Niko documentation. The version that was used can be found
at [docs/documentation.pdf](./docs/documentation.pdf).

### General

The integration provides multiple devices and entities. See below for a list of entities that each type of device
exposes.

#### Entities

The integration itself exposes the following entities:

* **Latest Controller Config Update Entity**, If you upload a new configuration to your controller you need to restart
  Home Assistant. Otherwise the integration will not work correctly. This entity will be on when a new configuration is
  loaded.

### NHC Dimmer Action

This action is exposed as a light.

#### Entities

* **Aligned Binary Sensor**, this is on when:
    * all dimmers are on and have the same brightness
    * all dimmers are off, regardless of the brightness

#### Services

The integration exposes a service to set the brightness of a light. This can be used to set the brightness without
turning the lights on. For instance if you want your lights to have a certain brightness at night. See Developer Tools →
Services → Niko Home Control II: Set brightness for light.

### NHC Fan Action

This is exposed as a fan entity.

### NHC Motor Action

This is exposed as a cover entity.

#### Entities

* **Aligned Binary Sensor**, this is on when all motors have the same position.
* **Moving Binary Sensor**, this is on when any motor is running.
* **Last Direction Sensor**, last movement direction. only used to keep the direction for "one button motor".

### NHC Relay Action (light, socket, switched-fan, switched-generic)

Lights are exposed as lights. Others are exposed as switches.

### NHC Reynaers Action

This is exposed as a cover entity.

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Status Sensor**, status feedback of the Reynaers motor.

### NHC Velux Action

This is exposed as a cover entity.

#### Entities

* **Feedback Enum Sensor**, (only if supported), undocumented.

### NHC Access Control Action

This action is exposed as a switch (if supported), and a lock (if supported)

#### Entities

* **Lock**, (only if supported), used to unlock the doorlock.
* **Basic State Enum Sensor**, (only if supported), This is only available for ring-and-come-in routine. It
  indicates if the ring-and-come-in is enabled or not. The switch uses the same information but will not
  take `Intermediate` into account.
* **Call Answered Binary Sensor**, (only if supported), Call is picked up.
* **Call Pending Binary Sensor**, (only if supported), Call is pending.
* **Decline Call Applied On All Devices Binary Sensor**, which represents the Decline Call Applied On All Devices state.

### NHC BellButton Action

This action exposes a switch and a lock.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Switch**
* **Basic State Enum Sensor**, which represents the Basic State. It is on when bell button is press, off when no call
  is active. The switch uses the same information but will not take `Intermediate` into account.
* **Lock**, used to unlock the doorlock.
* **Decline Call Applied On All Devices Binary Sensor**, which represents the Decline Call Applied On All Devices state.

### NHC Garage Door Action

This action is exposed as a cover.

#### Entities

* **Basic State Enum Sensor**, which represents the Basic State. On means the gate is opened, off means the gate is
  closed. Intermediate means the gate is moving, only when optional moving sensor is available.
* **Port Closed Binary Sensor**, undocumented.

### NHC Basic Alarm Action & NHC Panic Mode Action

__Remark:__ this is untested as I don't own a device of this type.

This action is exposed as alarm control panel.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Enum Sensor**, which represents the Basic State. It is on when bell button is press, off when no call

### NHC Mood Action

This action is exposed as a button.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Binary Sensor**, is on or off according to the state of all assigned players as configured for that
  action.
* **Mood Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action had a state change.
* **All Started Binary Sensor**, (only if supported), Is on when all outputs have reached their "Started" value.

### NHC All Off Action

This action is exposed as a button.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Binary Sensor**, The state is according the state of all assigned players as configured for that action.
* **AllOff Active Binary Sensor**, Is on only upon activation of the action. Off when one of the assigned participants
  in the action had a state change. Be aware that this state is only updated as the button is pressed, not when all
  devices are off.
* **AllStarted Binary Sensor**, (only if supported), Is on when all outputs have reached their "Started" value

### NHC Free Start Stop Actions

This action is exposed as a switch.

#### Entities

It has some extra entities that can be used in automations:

* **Start Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action has a state change.
* **All Started Binary Sensor**, (only if supported), Is on when all outputs have reached their "Started" value.

### NHC House Mode Actions

This action is exposed as a switch.

#### Entities

It has some extra entities that can be used in automations:

* **Start Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action has a state change.
* **All Started Binary Sensor**, (only if supported), Is on when all outputs have reached their "Started" value.

### NHC PIR Action

This action is exposed as a switch.

__Remark__: the switch represents the state of the override button. If you need the output of the PIR sensor in Home
Assistant you can link a "Virtual on/off device" in the Niko Home Control Programming Software to be switched on when
the PIR sensor initiates the routine.

### NHC Presence Simulation Action

This action is exposed as a switch.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Enum Sensor**, the value of the Basic State. The switch uses the same information but will not
  take `Intermediate` into account.

### NHC Player status action

__Remark:__ this is untested as I don't own a device of this type.

__Remark:__ This device can not be controlled. It is a virtual device that shows the status for another player.

#### Entities

* **BasicState Binary Sensor**, follows the on/off state of the player.
* **FeedbackMessage Sensor**, the state description

### NHC Conditional action

This is exposed as a switch. Is "On" when the evaluation is in the IF state, returns value "Off" when he evaluation is
in the ELSE state.

### NHC PeakMode action

This action is exposed as a switch. Is "On", "Off" according the state of the action (active/inactive).

### NHC SolarMode action

This action is exposed as a switch. Is "On", "Off" according the state of the action (active/inactive).

### NHC Timeschedule action

__Remark:__ This device can not be controlled.

#### Entities

* **Active Binary Sensor**, Time schedule is active

### NHC HVAC Thermostat

This is exposed as a climate entity.

#### Entities

* **Setpoint Temperature Sensor**, the desired setpoint in the current program.
* **Overrule Active Switch**, marks if the overrule-time will be used instead of setpoint as defined in program mode.
* **Overrule Setpoint Temperature Sensor**, the current overruled setpoint temperature.
* **Overrule Time Duration Sensor**, duration of the overrule period in minutes.
* **EcoSave Switch**, marks if the EcoSave mode is active. When active the program keeps going, but the
  setpointtemperature is altered (+3 when cooling, -3 when heating).
* **Protect Mode Switch**, marks if the Protect mode is active. This is the system off mode with temperature protection.
  Heating is activated when temperature is too low Cooling is activated when temperature is too high.
* **Thermostat on Switch**, indicates wheter the thermostat is turned on or off.
* **HVAC On Binary Sensor**, indicates that the HVAC indoor unit is online.

### NHC Thermostat

This is exposed as a climate entity.

#### Entities

* **Setpoint Temperature Sensor**, the desired setpoint in the current program.
* **Overrule Active Switch**, marks if the overrule-time will be used instead of setpoint as defined in program mode.
* **Overrule Setpoint Temperature Sensor**, (only if supported), the current overruled setpoint temperature.
* **Overrule Time Duration Sensor**, (only if supported), duration of the overrule period in minutes.
* **EcoSave Switch**, (only if supported), marks if the EcoSave mode is active. When active the program keeps going, but
  the setpointtemperature is altered (+3 when cooling, -3 when heating).

### NHC Touch Switch Thermostat

This is exposed as a climate entity.

#### Entities

* **Setpoint Temperature Sensor**, the desired setpoint in the current program.
* **Overrule Active Switch**, marks if the overrule-time will be used instead of setpoint as defined in program mode.
* **Overrule Setpoint Temperature Sensor**, the current overruled setpoint temperature.
* **Overrule Time Duration Sensor**, duration of the overrule period in minutes.
* **EcoSave Switch**, marks if the EcoSave mode is active. When active the program keeps going but limits the
  temperature range to the value configured.

### NHC Thermo switch

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **HeatIndex Temperature Sensor**, (only if supported)
* **Ambient Temperature Sensor**, (only if supported)
* **Humidity Sensor**, (only if supported)

### NHC Virtual Thermostat

This is exposed as a climate entity.

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Setpoint Temperature Sensor**, the desired setpoint in the current program.
* **Overrule Active Switch**, marks if the overrule-time will be used instead of setpoint as defined in program mode.
* **Overrule Setpoint Temperature Sensor**, (only if supported), the current overruled setpoint temperature.
* **Overrule Time Duration Sensor**, (only if supported), duration of the overrule period in minutes.
* **EcoSave Switch**, (only if supported), marks if the EcoSave mode is active. When active the program keeps going, but
  the setpointtemperature is altered (+3 when cooling, -3 when heating).

### NHC Virtual flag

This is exposed as switch.

### NHC Battery Metering Clamp, ZigBee Battery Metering Clamp, NHC ZigBee Electricity Metering module (with clamp) & NHC Electricity Metering module (with clamp)

#### Entities

* **Electrical Power Sensor**, (only if supported), the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Electrical Power 1 Sensor**, (only if supported), the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Electrical Power 2 Sensor**, (only if supported), the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Electrical Power 2 Sensor**, (only if supported), the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.
* **Inverted Binary Sensor**, (only if supported)
* **Inverted 1 Binary Sensor**, (only if supported), Phase 1 inverted
* **Inverted 2 Binary Sensor**, (only if supported), Phase 2 inverted
* **Inverted 3 Binary Sensor**, (only if supported), Phase 3 inverted
* **Flow Sensor**, (only if supported), Producer or Consumer
* **Segment Sensor**, (only if supported), Central or Subsegment
* **Clamp Type Sensor**, (only if supported), 63A, 80A, or 120A
* **Inverter Type Sensor**, (only if supported), Production, Hybrid or Battery

__Remark:__ The totals are not available as they are not (yet) exposed by the API.

### NHC Zigbee Smart plug

This is the energy metering linked to a zigbee smart plug.

__Remark__: The smart plug itself can be controlled through the Status Switch. But it will also be exposed as a NHC
Relay
Action Switch.

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Status Switch**, (only if supported), a switch to turn on/off the Smart plug.
* **Feedback Enabled Binary Sensor**. On if the feedback led shows the relay status. Off if the feedback led is
  disabled.
* **Measuring Only Binary Sensor**. If on, the relay will always be on.
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.
* **Switching Only Binary Sensor**

__Remark:__ The totals are not available as they are not (yet) exposed by the API.

### Generic Zigbee Smart plug

This is the energy metering linked to a generic zigbee smart plug. The smart plug itself is a different device.

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Status Switch**, (only if supported), a switch to turn on/off the Smart plug.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.
* **Switching Only Binary Sensor**

__Remark:__ The totals are not available as they are not (yet) exposed by the API.

#### Calculated totals

Totals can be calculated via a Helper:

Goto 'Settings' > 'Devices & Services' and click 'Helpers' at the top. Click the '+ Create Helper' button at the bottom
right and select 'Integration - Riemann sum integral sensor'. Type a name for the Helper and select the relevant '
energyhome' entity (i.e. 'Electrical Power to Grid') from the 'Input sensor' dropdown. Integration method 'Trapezoidal
rule' should give the most accurate integrated value. Set 'Precision' to '3' and set the 'Metric prefix' to 'k (kilo)'.
Leave the time unit at 'Hours'.

At least two helpers are needed: one for the consumption total and one for the production total.
These helpers can be used in the HA Energy Dashboard.

### Energy Home

#### Entities

* **Electrical Power to Grid Sensor**, (only if supported), the realtime power usage in W as a sum for all central
  meters.
* **Electrical Power from Grid Sensor**, (only if supported), the realtime power consumption in W as a sum for all
  central meters.
* **Electrical Power Production Sensor**, (only if supported), the realtime power production in W as a sum for all
  producers.
* **Electrical Power Self Consumption Sensor**, (only if supported), electrical power production minus power to grid.
* **Electrical Power Consumption Sensor**, (only if supported), electrical power self production + electrical power from
  grid.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Electrical Power Production Threshold Exceeded Binary Sensor**, this is on when the central meters electrical power
  production is greater than the threshold of 300W (+ 5W hysteresis)
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.

__Remark:__ There a more properties to this device, but these are not documented so it is difficult to know what they
report exactly.

### NHC Outdoor Video Door Station

This is exposed as a camera.

__Remark:__ Note that this will only work if your camera is not directly connected to the controller. The controller
uses its own DHCP server and there is nothing in place to connect to the streams. In older versions of the controller
there was port forwarding, but this is disabled (confirmed by Niko).

#### Entities

* **Call Status 01 Enum Sensor**, Call status for this VDS bell button, if supported
* **Call Status 02 Enum Sensor**, Call status for this VDS bell button, if supported
* **Call Status 03 Enum Sensor**, Call status for this VDS bell button, if supported
* **Call Status 04 Enum Sensor**, Call status for this VDS bell button, if supported
* **Status Enum Sensor**, Connection status for the VDS device
* **IP Adress Sensor**, Current IP address of the VDS

#### Mute/Unmute/Hangup

Add the following [Shell Commands](https://www.home-assistant.io/integrations/shell_command/) in
your `configuration.yaml`.

```yaml
shell_command:
  doorphone_hangup: curl -u admin:123qwe http://192.168.X.X/api/v1/call_hangup
  doorphone_mute: curl -u admin:123qwe http://192.168.X.X/api/v1/mute_set?mute=tones_incoming
  doorphone_unmute: curl -u admin:123qwe http://192.168.X.X/api/v1/mute_set?mute=off
```

__Remark:__ Replace the IP address with the IP address of your doorstation. Note that this will only work if your camera
is not directly connected to the controller.

More information can be found in the API documention and manual of the RobinsIP doorstation:

* [API manual (dutch)](https://www.robintele.com/images/downloads/How-To_The_Robin_API_v3.6.0_NL.pdf)
* [Manual (dutch)](https://www.robintele.com/images/downloads/Manual-Robin-SV-3211NL.pdf)

### NHC Audio Control Action

This action is exposed as media player.

#### Entities

It has some extra entities that can be used in automations:

* **Volume Aligned Binary Sensor**, on when all speakers / groups have the same volume.
* **Title Aligned Binary Sensor**, on when all speakers / groups have the title.
* **Connected Binary Sensor**, on when all speakers are connected.
* **Speaker Sensor**, the UUID of the speaker to fetch the favourites from.

#### Not yet implemented

* [ ] Setting the favourite

### Generic Ventilation Implementation

This is exposed as a fan entity.

#### Entities

* **Boost Switch**, (only if supported), enable/disable boost mode.
* **CO2 Sensor**, (only if supported), the CO2 level.
* **Humidity Sensor**, (only if supported), the humidity level.
* **Coupling Status Enum Sensor**, (only if supported), the connectivity status of the system.

__Remark:__ Some ventilation systems can not be turned off. Home Assistant Fan Entity does not support this. This means
you will be able to turn it off in Home Assistant, but this will not have any effect.

### Generic Heating/Cooling Implementation

This is exposed as a climate entity.

#### Entities

* **Overrule Active Binary Sensor**, (only if supported), is the overrule mode active or not.
* **Coupling Status Enum Sensor**, the connectivity status of the system.

### Generic Warm Water Implementation

#### Entities

* **Domestic Hot Water Temperature Number**, control the temperature.
* **Program Select**, (only if supported), select the program.
* **Boost Switch**, enable/disable boost mode.
* **Coupling Status Enum Sensor**, the connectivity status of the system.

### Generic ZigBee Heating/Cooling Implementation

__Remark:__ this is untested as I don't own a device of this type.

This is exposed as a climate entity.

#### Entities

* **Overrule Active Binary Sensor**, (only if supported), is the overrule mode active or not.

### Generic Charging Station

This is exposed as a switch.

#### Entities

* **Charging Mode Select**, (only if supported), select the charging mode.
* **Charging Status Enum sensor**, (only if supported), The current charging status.
* **EV Status Enum sensor**, (only if supported).
* **Electrical Power sensor**, (only if supported).
* **Coupling Status Enum Sensor**, (only if supported), the connectivity status of the system.
* **Boost Switch**, (only if supported), boost mode for capacity tariff Flanders
* **TargetDistance Number Sensor**, (only if supported), distance to be charged additionally when in Smart mode
* **TargetTime Time Entity**, (only if supported), charging completion time when in Smart mode
* **ReachableDistance Number Sensor**, (only if supported), estimated max driving distance that could be charged during
  the Smart mode session
* **TargetReached Binary Sensor**, (only if supported), charging target is reached during this Smart mode session
* **NextChargingTime Time Sensor**, (only if supported), estimated time when charging will start in Smart Mode

### NHC Heating Cooling Action

__Remark:__ This device is not documented/supported by Niko.

#### Entities

* **Cooling Mode Binary Sensor**
* **Heating Mode Binary Sensor**

### Electrical Heating Action

__Remark:__ This device is not documented/supported by Niko.

This action is exposed as a button.

#### Entities

* **Basic State Binary Sensor**, the current status of the action.

### Generic Inverter

__Remark:__ This device is not documented/supported by Niko.

#### Entities

* **Coupling Status Enum Sensor**, (only if supported), the connectivity status of the system.
* **Electrical Power Production Sensor**, (only if supported), the realtime power production in W.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Binary Sensor**, The state is according the state of all assigned players as configured for that action.

### Generic Thermometer

__Remark:__ This device is not documented/supported by Niko.

This is exposed as a temperature sensor.

### Color Action

This is exposed as a light entity.

#### Entities

* **Brightness Aligned Binary Sensor**
* **Color Aligned Binary Sensor**

__Remark:__ This device is not documented/supported by Niko.

### Tunable White Action

This is exposed as a light entity.

#### Entities

* **Brightness Aligned Binary Sensor**
* **Color Aligned Binary Sensor**

__Remark:__ This device is not documented/supported by Niko.


### Tunable White and Color Action

This is exposed as a light entity.

#### Entities

* **Brightness Aligned Binary Sensor**
* **Color Aligned Binary Sensor**

__Remark:__ This device is not documented/supported by Niko.

## Not yet supported

* Sonos Speaker
* Bose Speaker

## How to get it running

Note: Make sure you have a recent version of Home Assistant!

This integration is not part of the default Home Assistant installation.

The easiest way to install it is through [HACS (Home Assistant Community Store)](https://hacs.xyz/). Once you have HACS
installed you can search for "Niko Home Control II". Make sure you select the correct one. Ours has the following
description:

> Home Assistant Custom integration for Niko Home Control II

Once this is done you can install the integration in Home Assistant:

1. Go to Settings → Devices & Services Integrations
2. Add an integration, search for Niko Home Control II, and click on it
3. Follow the wizard

## FAQ

### The integration is not working after power outage

It is expected behouviour that the integration may not work after a power outage. Please restart Home Assistant. or
after a new configuration is uploaded.

### The integration is not working after uploading a new configuration

if you uploaded a new configuration to the connected controller / hub, please restart Home Assistant.

### The integration is not working after an IP change

Please make sure that the IP of the connected controller / hub does not change. If the IP changes you will need to
remove and re-add the integration.

### I see a lot of "Report Instant Usage re-enabled" messages in the log

This will only appear in the logs if you have set your log-level to `debug`.

The Electricity Metering module (with clamp), Energy Home, NHC Zigbee Smart plug and Generic Zigbee Smart plug only
report their power usage for 30 seconds when the "Report Instant Usage" is enabled. So as soon as it becomes disabled
this integration re-enables it.

### I see "Class CocoXXX not found" in the log

This is because this device is not supported (yet) or this device can't be controlled through the API.

Feel free to create an [issue on Github](https://github.com/joleys/niko-home-control-II/issues). Please include your
[device list](#i-need-to-see-the-device-list).

### I don't have/use the Energy Home, but it is present in the integration

Each installation exposes an Energy Home device. At this point there is no good way to detect if the Energy Home is
used.

If you do not want to see / record / ... you can disable the device in the integration.

### I need to see the device list

First you will need to enable debug logging for the integration. You can enable debug logging for this integration by
adding the following to your `configuration.yaml` file:

```yaml
logger:
  default: warning
  logs:
    custom_components.nhc2: debug
```

When this is done you will need to restart Home Assistant. After that you can see the device list in the logs. You can
find it by searching for `Received device list:`. The device list itself is a large JSON string.

If you don't feel comfortable sharing this device list in a public issue, you can send it to me via
mail: `niko-ha [at] verkoyen [dot] eu`.

## Development

### Adding support for new Device models

* Add a new class for the device in `nhccoco/devices`. The name of the file is `{model}_{type}.py`. The classname is
  `Coco{Model}{Type}`.
* Import the class in `nhccoco/coco.py`. This allows the Coco class to create an instance when the device is present in
  the device list.
* Create the needed entities in `entities`
* Add the entities that should be created in the correct platform-file.

### Testing without having the real devices?

If you don't own a device but want to test the integration, and you have the relevant device info (eg. through a device
list your received). You can fake the devices returned from the MQTT broker.

1. Create a folder `debugging` in the root of the project.
2. Add the device list json in this folder.
3. Open [coco.py](./custom_components/nhc2/nhccoco/coco.py)
4. Search for `def _process_devices_list(self, response):` and edit the code to look like:

```python
def _process_devices_list(self, response):
    """Convert the response of devices.list into device instances."""
    _LOGGER.debug(f'Received device list: {response}')

    # REMOVE ME START
    from pathlib import Path
    import ast

    path = Path(str(Path(__file__).parent.resolve()) + '/../../../debugging/device_list.json').resolve()
    f = open(path)
    response = ast.literal_eval(f.read())
    # REMOVE ME END
```

__Remark:__ This is a hackish way, and you will not able to test it for real. You will not receive updates. Check the
logs to see if messages are correctly send to the MQTT broker.

## Found a bug?

If you found a bug you can create an [issue on GitHub](https://github.com/joleys/niko-home-control-II/issues).

Before creating an issue:

1. Check if the issue is already reported
2. Make sure you are running the latest version of Home Assistant.
3. Make sure you are running the latest version of this integration.

If you create an issue:

* Mention which version of Home Assistant you are using.
* Include relevant logs from Home Assistant. You can enable debug logging for this integration by adding the following
  to
  your `configuration.yaml` file:

```yaml
logger:
  default: warning
  logs:
    custom_components.nhc2: debug
```

* If possible include the steps to reproduce the issue. Explain what is wrong and what you expected to happen.

## Want to help?

As you can see in this README, there are still untested devices. These are devices that are implemented based on the
available documentation from Niko. If you own one of these devices, please help me out by testing it. Let us know,
through an issue, what is working or not.

If you see missing features, feel free to create pull requests. Add missing devices, ...