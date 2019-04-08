# hass-nhc2

License: MIT

This is in pre-alpha state... things will explode :p

This 'custom_component' provides you with a NHC2 Platform 'Niko Home Control II / Connected controller'

## How to get it running

Besides adding all the files inside a folder called \*CONFIG_FOLDER\*/custom_components/nhc2/,
(since only config trough the web UI is provided (at this point))
hass requires you to add 'nhc2' to the static list in `homeassistant/config_entries.py`

see: https://developers.home-assistant.io/docs/en/config_entries_config_flow_handler.html 