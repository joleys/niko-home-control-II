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

### NHC Access Control Action

#### Entities

* **Button**, (only if supported), used to enable/disable ring-and-come-in.
* **Basic State Binary Sensor**, (only if supported), This is only available for ring-and-come-in guided action. It
  indicates if the ring-and-come-in is enabled or not.
* **Call Answered Binary Sensor**, (only if supported), undocumented.
* **Call Pending Binary Sensor**, (only if supported), undocumented.
* **Decline Call Applied On All Devices Binary Sensor**, which represents the Decline Call Applied On All Devices state.
* **Lock**, (only if supported), used to unlock the doorlock.

### NHC All Off Action

This action is exposed as a switch. The state is according the state of all assigned players as configured for that
action.

#### Entities

It has some extra entities that can be used in automations:

* **AllOff Active Binary Sensor**, Is on only upon activation of the action. Off when one of the assigned participants
  in the action had a state change. Be aware that this state is only updated as the button is pressed, not when all
  devices are off.

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

### NHC BellButton Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

This action exposes a button and a lock.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Binary Sensor**, which represents the Basic State. It is on when bell button is press, off when no call
  is active.
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

### NHC Fan Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

This is exposed as a fan entity.

### NHC Free Start Stop Actions

This action is exposed as a switch.

#### Entities

It has some extra entities that can be used in automations:

* **Start Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action has a state change.

### NHC Garage Door Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Basic State Enum Sensor**, which represents the Basic State. On means the gate is opened, off means the gate is
  closed. Intermediate means the gate is moving, only when optional moving sensor is available.

### NHC House Mode Actions (untested)

__Remark:__ this is untested as I don't own a device of this type.

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

### NHC Thermostat (untested)

__Remark:__ this is untested as I don't own a device of this type.

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

This action is exposed as a switch.

#### Entities

It has some extra entities that can be used in automations:

* **Mood Active Binary Sensor**, is on upon activation of the action. It is off when one of the assigned participant in
  the action had a state change.

### NHC Motor Action

This is exposed as a cover entity.

#### Entities

* **Aligned Binary Sensor**, this is on when all motors have the same position.
* **Moving Binary Sensor**, this is on when any motor is running.
* **Last Direction Sensor** (undocumented).

### NHC PIR Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

This action is exposed as a switch.

Remark: the Basic State is the override button. If you need the output of the PIR sensor in Home Assistant you can link
a "Virtual on/off device" in the Niko Home Control Programming Software to be switched on when the PIR sensor initiates
the routine.

### NHC Presence Simulation Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

This action is exposed as a button.

#### Entities

It has some extra entities that can be used in automations:

* **Basic State Enum Sensor**

### NHC Virtual flag (untested)

__Remark:__ this is untested as I don't own a device of this type.

This is exposed as switch.

### NHC Relay Action (light, socket, switched-fan, switched-generic)

Lights are exposed as lights. Others are exposed as switches.

### NHC Reynaers Action (untested)

This is exposed as a cover entity.

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Status Sensor**, status feedback of the Reynaers motor.

### NHC Velux Action (untested)

This is exposed as a cover entity.

__Remark:__ this is untested as I don't own a device of this type.

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

#### Remarks

The totals are not available as they are not (yet) exposed by the API.

### Generic Zigbee Smart plug (untested)

__Remark:__ this is untested as I don't own a device of this type.

This is the energy metering linked to a generic zigbee smart plug. The smart plug itself is a different device.

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Positive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.

#### Remarks

The totals are not available as they are not (yet) exposed by the API.

### Electricity Metering module (with clamp) (untested)

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Possitive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Flow Sensor**. Producer or Consumer
* **Segment Sensor**. Central or Subsegment
* **Clamp Type Sensor**. 63A or 120A

### Energy Home (untested)

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Electrical Power to Grid Sensor**, the realtime power usage in W as a sum for all central meters.
* **Electrical Power from Grid Sensor**, the realtime power consumption in W as a sum for all central meters.
* **Electrical Power Production Sensor**, the realtime power production in W as a sum for all producers.
* **Electrical Power Self Consumption Sensor**, electrical power production minus power to grid.
* **Electrical Power Consumption Sensor**, electrical power self production + electrical power from grid.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Electrical Power Production Threshold Exceeded Binary Sensor**, this is on when the central meters electrical power
  production is greater than the threshold of 300W (+ 5W hysteresis)

### Generic Warm Water Implementation (untested)

__Remark:__ this is untested as I don't own a device of this type.

#### Entities

* **Domestic Hot Water Temperature Number**, control the temperature.
* **Program Select**, select the program.
* **Boost Switch**, enable/disable boost mode.
* **Coupling Status Enum Sensor**, the connectivity status of the system.

### Generic Heating/Cooling Implementation (untested)

__Remark:__ this is untested as I don't own a device of this type.

This is exposed as a climate entity.

#### Entities

* **Overrule Active Binary Sensor**, is the overrule mode active or not.
* **Coupling Status Enum Sensor**, the connectivity status of the system.

## Not yet supported

* Sonos Speaker
* Bose Speaker
* Generic Ventilation Implementation

## How to get it running

Note: Make sure you have a recent version of Home Assistant!

1. Install this custom component
2. Go to Configuration > Integrations
3. Add an integration, search for Niko Home Control II, and click on it
4. Follow the wizard

## Development

### Adding support for new Device models

* Add a new class for the device in `nhccoco/devices`. The name of the file is `{model}_{type}.py`. The classname is
  `Coco{Model}{Type}`.
* Import the class in `nhccoco/coco.py`. This allows the Coco class to create an instance when the device is present in
  the device list.
* Create the needed entities in `entities`
* Add the entities that should be created in the correct platform-file.

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