# hass-nhc2

License: [MIT](LICENSE)

This 'custom_component' provides you with a NHC2 Platform

It uses the pypi package [nhc2-coco](https://github.com/filipvh/nhc2-coco) that I've written too.

__LIMITED__ to switches/lights as it stands now

## How to get it running

There a two setup methods. If you use HASS.IO [Method 1](#installmethod1) is recommended, as you need to change a file in HA to make [Method 2](#installmethod2) work (as it stands now) 

### <a name="installmethod1"></a>Method 1 - Using configuration.yaml

1. Add all the files inside a folder called `<CONFIG_FOLDER>/custom_components/nhc2/`
2. Add config to your `configuration.yaml file`

example:

```yaml
nhc2:
  host: '192.168.0.2'
  port: 8883
  username: 'abcdefgh-ijkl-mnop-qrst-uvwxyz012345'
  password: !secret nhc2_password
```

### <a name="installmethod2"></a>Method 2 -  Using Integrations Web UI

1. Add all the files inside a folder called `<CONFIG_FOLDER>/custom_components/nhc2/`
2. Add 'nhc2' to the static list `FLOWS` in `homeassistant/config_entries.py` (this in until HA can auto populate this for custom components)
3. Create credentials (see next paragraph)
4. Do the __Niko Connected Controller__ setup in `Setting > Integrations` the Web Ui  

see: [Home Assistant dev docs - Integration Configuration](https://developers.home-assistant.io/docs/en/config_entries_config_flow_handler.html) 
## How to get the credentials

### Step 1 - Creating the profile
First you will need to setup a touchscreen profile to the controller setup.
(see [Creating and modifying touchscreen profiles](http://guide.niko.eu/pages/viewpage.action?pageId=10978290))
The password you enter there, will be the password you will need for the connection.
The username is the ID this profile gets. There are 3 ways of extracting this information.

### Step 2 - Extracting the username

#### Method 1 - Not Yet Available
 In a later version of the integration, I hope to make Method 3 automatic, so the user can select the profile from a dropdown in the Web UI

#### Method 2 - Zip & SQLite
 1. The project file from the Niko software is a zip,
    extract it using your (un)zip tool of choice.
 2. Open the Config.sqlite with [DB Browser for SQLite](https://sqlitebrowser.org/dl/)
 3. Go to tab 'Browse Data' and open the table called __Profile__
 4. Look for the __CreationId__ that corresponds with the desired profile, that's the username 
 
#### Method 3 - MQTT Client
 1. Connect to the MQTT broker on the Connected Controller, on port 8883, 
 using the CA cert you can find in the [nhc2-coco GitHub Repo](https://github.com/filipvh/nhc2-coco/blob/master/nhc2_coco/coco_ca.pem)
 2. Subscribe to the topic `public/authentication/rsp`
 3. Publish on topic `public/authentication/cmd` with payload `{"Method":"profiles.list"}`
 4. Extract the __Uuid__ that corresponds with the desired profile

## What is supported

 * Baisc configuration trough the integration UI
 * NHC2 'light' as a HA Light (light connected to switch using a Basic Action)
 * NHC2 'switched-generic' as a ha Switch (virtual output connected to switch using a Basic Action)
 
## FAQ

 Q: When I restart HA with the custom component I get an error the `nhc2-coco` dependency is missing.\
 A: Last time I got this, a second restart fixed it.   
 
## What can you do to help?

 * Contribute to this project with constructive issues, suggestions, PRs, etc.
 * Help me in any way to get support for more entities (eg dimmer)
