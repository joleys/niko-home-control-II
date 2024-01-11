# Niko Home Control II Home Assistant Integration

License: [MIT](LICENSE)

This custom component will allow you to integrate you Niko Connected Controller II in Home Assistant.
You can use a touchscreen profile or the Hobby API account.

This integration communicates directly with the controller. You only need internet when activating/renewing the Hobby
API. If you use a touch screen profile, this isn't even needed.

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

### NHC All Off Action

This action is exposed as a button.

#### Entities

It has some extra entities that can be used in automations:

* **AllOff Active Binary Sensor**, Is on only upon activation of the action. Off when one of the assigned participants
  in the action had a state change. Be aware that this state is only updated as the button is pressed, not when all
  devices are off.
* **Basic State Binary Sensor**, The state is according the state of all assigned players as configured for that action.

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

### NHC Basic Alarm Action & NHC Panic Mode Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

This action is exposed as alarm control panel.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Enum Sensor**, which represents the Basic State. It is on when bell button is press, off when no call

### NHC BellButton Action (untested)

This action exposes a switch and a lock.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Switch**
* **Basic State Enum Sensor**, which represents the Basic State. It is on when bell button is press, off when no call
  is active. The switch uses the same information but will not take `Intermediate` into account.
* **Lock**, used to unlock the doorlock.
* **Decline Call Applied On All Devices Binary Sensor**, which represents the Decline Call Applied On All Devices state.

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

### NHC Free Start Stop Actions

This action is exposed as a switch.

#### Entities

It has some extra entities that can be used in automations:

* **Start Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action has a state change.

### NHC Garage Door Action

This action is exposed as a cover.

#### Entities

* **Basic State Enum Sensor**, which represents the Basic State. On means the gate is opened, off means the gate is
  closed. Intermediate means the gate is moving, only when optional moving sensor is available.
* **Port Closed Binary Sensor**, undocumented.

### NHC House Mode Actions

This action is exposed as a switch.

#### Entities

It has some extra entities that can be used in automations:

* **Start Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action has a state change.

### NHC HVAC Thermostat (untested)

__Remark:__ this is untested as I don't own a device of this type.

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
* **Overrule Setpoint Temperature Sensor**, the current overruled setpoint temperature.
* **Overrule Time Duration Sensor**, duration of the overrule period in minutes.
* **EcoSave Switch**, marks if the EcoSave mode is active. When active the program keeps going, but the
  setpointtemperature is altered (+3 when cooling, -3 when heating).

### NHC Touch Switch

This is exposed as a climate entity.

#### Entities

* **Setpoint Temperature Sensor**, the desired setpoint in the current program.
* **Overrule Active Switch**, marks if the overrule-time will be used instead of setpoint as defined in program mode.
* **Overrule Setpoint Temperature Sensor**, the current overruled setpoint temperature.
* **Overrule Time Duration Sensor**, duration of the overrule period in minutes.
* **EcoSave Switch**, marks if the EcoSave mode is active. When active the program keeps going but limits the
  temperature range to the value configured.

### NHC Mood Action

This action is exposed as a button.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Binary Sensor**, is on or off according to the state of all assigned players as configured for that
  action.
* **Mood Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action had a state change.

### NHC Motor Action

This is exposed as a cover entity.

#### Entities

* **Aligned Binary Sensor**, this is on when all motors have the same position.
* **Moving Binary Sensor**, this is on when any motor is running.
* **Last Direction Sensor**, last movement direction. only used to keep the direction for "one button motor".

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

### NHC Virtual flag

This is exposed as switch.

### NHC Relay Action (light, socket, switched-fan, switched-generic)

Lights are exposed as lights. Others are exposed as switches.

### NHC Reynaers Action (untested)

This is exposed as a cover entity.

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Status Sensor**, status feedback of the Reynaers motor.

### NHC Velux Action

This is exposed as a cover entity.

#### Entities

* **Feedback Enum Sensor**, (only if supported), undocumented.

### NHC Zigbee Smart plug

This is the energy metering linked to a zigbee smart plug. The smart plug itself is a different device.

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Feedback Enabled Binary Sensor**. On if the feedback led shows the relay status. Off if the feedback led is
  disabled.
* **Measuring Only Binary Sensor**. If on, the relay will always be on.
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.

__Remark:__ The totals are not available as they are not (yet) exposed by the API.

### Generic Zigbee Smart plug

This is the energy metering linked to a generic zigbee smart plug. The smart plug itself is a different device.

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.

__Remark:__ The totals are not available as they are not (yet) exposed by the API.

Totals are available via a Helper. Goto 'Settings' > 'Devices & Services' and click 'Helpers' at the top. Click the '+
Create Helper' button at the bottom right and select 'Integration - Riemann sum integral sensor'.
Type a name for the Helper and select the relevant 'energyhome' entity (i.e. 'Electrical Power to Grid') from the 'Input
sensor' dropdown. Integration method 'Trapezoidal rule' should give the most accurate integrated value. Set 'Precision'
to '3' and set the 'Metric prefix' to 'k (kilo)'. Leave the time unit at 'Hours'.
At least two helpers are needed: one for the consumption total and one for the production total.
These helpers can be used in the HA Energy Dashboard.

### Electricity Metering module (with clamp)

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Flow Sensor**, Producer or Consumer
* **Segment Sensor**, Central or Subsegment
* **Clamp Type Sensor**, (only if supported), 63A or 120A
* **Disable Report Instant Usage Re-enabling Switch**, a toggle to disable the automatic re-enabling of the
  Report Instant Usage property. This is useful if you don't need Electrical Power reporting.

__Remark:__ The totals are not available as they are not (yet) exposed by the API.

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

### RobinsIP Videodoorstation

__Remark:__ This device is not documented/supported by Niko.

This is exposed as a camera.

#### Entities

* **Call Status 01 Enum Sensor**
* **IP Adress Sensor**
* **Status Enum Sensor**

__Remark:__ Note that this will only work if your camera is not directly connected to the controller. The controller
uses its own DHCP server and there is nothing in place to connect to the streams. In older versions of the controller
there was port forwarding, but this is disabled (confirmed by Niko).

### NHC Condition Action

__Remark:__ This device is not documented/supported by Niko.

This is exposed as a switch.

### NHC Timeschedule Action

__Remark:__ This device is not documented/supported by Niko.

#### Entities

* **Active Binary Sensor**

### NHC Heating Cooling Action

__Remark:__ This device is not documented/supported by Niko.

#### Entities

* **Cooling Mode Binary Sensor**
* **Heating Mode Binary Sensor**

### Electrical Heating Action (untested)

__Remark:__ This device is not documented/supported by Niko.

This action is exposed as a button.

#### Entities

* **Basic State Binary Sensor**, the current status of the action.

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