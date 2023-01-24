# Niko Home Control II Home Assistant Integration

License: [MIT](LICENSE)

This custom component will allow you to integrate you Niko Connected Controller II in Home Assistant.
You can use a touchscreen profile or the Hobby API account.

This integration communicates directly with the controller. You only need internet when activating/renewing the Hobby
API. If you use a touch screen profile, this isn't even needed.

## Acknowledgements

This custom component is a [spin-off of the hard and excellent work by @filipvh](https://github.com/filipvh/hass-nhc2).
Thanks!

## What works now?

### NHC Access Control Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

This action exposes a button, camera and lock.

#### Entities

It has some extra entities that can be used in automations:

* **Access Control Basic State Binary Sensor**, which represents the Basic State. This is only available for
  ring-and-come-in guided action. It indicates if the ring-and-come-in is enabled or not.
* **Decline Call Applied On All Devices Binary Sensor**, which represents the Decline Call Applied On All Devices state.

### NHC All Off Action

This action is exposed as a button.

#### Entities

It has some extra entities that can be used in automations:

* **AllOff Active Binary Sensor**, which represents the AllOffActive state. Be aware that this state is only updated as
  the
  button is pressed, not when all devices are off.
* **AllOff Basic State Binary Sensor**, which represents the Basic State of the AllOff.

### NHC Basic Alarm Action (untested)

__Remark:__ this is untested as I don't own a device of this type.

This action is exposed as alarm control panel.

### NHC Dimmer Action

This action is exposed as a light.

#### Entities

* **Aligned Binary Sensor**, this is on when:
    * all dimmers are on and have the same brightness
    * all dimmers are off, regardless of the brightness

#### Services

The integration exposes a service to set the brightness of a light. This can be
used to set the brightness without turning the lights on. For instance if you want
your lights to have a certain brightness at night. See Developer Tools → Services → Niko Home Control II: Set brightness
for light.

### NHC Thermostat (untested)

This is exposed as a climate entity.

#### Todo

* [ ] [Check if we can implement target_temperature_high, target_temperature_low, target_temperature_step](https://github.com/joleys/niko-home-control-II/blob/master/custom_components/nhc2/nhccoco/coco_climate.py#L103)
* [ ] [Check if we can implement max_temp, min_temp](https://github.com/joleys/niko-home-control-II/blob/master/custom_components/nhc2/nhccoco/coco_climate.py#L112)
* [ ] [Check if we can populate preset_modes from the description](https://github.com/joleys/niko-home-control-II/blob/master/custom_components/nhc2/nhccoco/coco_climate.py#L120)

#### Entities

* **Setpoint Temperature Sensor**, the desired setpoint in the current program.
* **Overrule Active Binary Sensor**, marks if the overrule-time will be used instead of setpoint as defined in program
  mode.
* **Overrule Setpoint Temperature Sensor**, the current overruled setpoint temperature.
* **Overrule Time Duration Sensor**, duration of the overrule period in minutes.
* **EcoSave Binary Sensor**, marks if the EcoSave mode is active. When active the program keeps going, but the
  setpointtemperature is altered (+3 when cooling, -3 when heating).

### NHC Relay Action (light, socket, switched-fan, switched-generic)

Lights are exposed as lights. Others are exposed as switches.

### NHC Zigbee Smart plug

This is the energy metering linked to a zigbee smart plug. The smart plug itself is a different device.

#### Entities

* **Electrical Power Sensor**, the realtime power usage in W. Possitive means power consumed, negative is power
  produced.
* **Report Instant Usage Binary Sensor**, indicates if the Electrical Power is received. When disabled, it will
  automatically be enabled.
* **Feedback Enabled Binary Sensor**. On if the feedback led shows the relay status. Off if the feedback led is
  disabled.
* **Measuring Only Binary Sensor**. If on, the relay will always be on.

#### Remarks

The totals are not available as they are not exposed by the API.

## Not yet supported

* NHC Audio Control Action
* NHC BellButton Action
* NHC Fan Action
* NHC Free Start Stop Actions
* NHC Garage Door Action
* NHC House Mode Action
* NHC HVAC Thermostat
* NHC Touch Switch
* NHC Mood Action
* NHC Motor Action (rolldownshutter | sunblind | gate | venetianblind)
* NHC Panic Mode Action
* NHC PIR Action
* NHC Presence Simulation Action
* NHC Virtual flag
* NHC Reynaers Action
* NHC Velux Action
* Generic Zigbee Smart plug
* Sonos Speaker
* Bose Speaker
* Electricity Metering module (with clamp)
* Energy Home
* Generic Ventilation Implementation
* Generic Heating/Cooling Implementation
* Generic Warm Water Implementation

## How to get it running

Note: Make sure you have a recent version of Home Assistant!

1. Install this custom component
2. Go to Configuration > Integrations
3. Add an integration, search for Niko Home Control II, and click on it
4. Follow the wizard

## Adding an Energy Meter?

This currently requires some manual action in your configuration.yaml.

You need to add (and possibly tweak) the following:

    sensor:
        - platform: integration
            source: sensor.elektriciteitsmeting
            name: energy_elektriciteit
            unit_prefix: k
            round: 3
            method: left

    utility_meter:
        energy_daily:
            source: sensor.energy_elektriciteit
            cycle: daily
        energy_monthly:
            source: sensor.energy_elektriciteit
            cycle: monthly

## Found a bug?

When and if you find a bug, please document it as good as possible (how to reproduce, logs, screenshots, etc)

## Want to help?

Make a PR, contact me, test new releases, code new entities ...
