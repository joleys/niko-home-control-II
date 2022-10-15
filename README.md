# Niko Home Control II Home Assistant Integration

License: [MIT](LICENSE)

This custom component will allow you to integrate you Niko Connected Controller II in Home Assistant.
You can use a touchscreen profile or the Hobby API account.

This integration communicates directly with the controller. You only need internet when activating/renewing the Hobby API. If you use a touch screen profile, this isn't even needed.

## Acknowledgements

This custom component is a [spin-off of the hard and excellent work by @filipvh](https://github.com/filipvh/hass-nhc2). Thanks!

## What works now?

- Lights
- Switches (relais)
- Sockets
- Thermostats
- Fans
- Energy Meters
- Alloff
- Power metering for Zigbee Smart plugs

## Service
### Set brightness for light
The integration exposes a service to set the brightness of a light. This can be 
used to set the brightness without turning the lights on. For instance if you want 
your lights to have a certain brightness at night.

See Developer Tools → Services → Niko Home Control II: Set brightness for light.


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
