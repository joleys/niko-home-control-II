DOMAIN = 'nhc2'
KEY_GATEWAY = 'nhc2_gateway'
KEY_TOKEN_TIMER_CANCEL = 'nhc2_token_timer_cancel'
KEY_STATISTICS_TIMER_CANCEL = 'nhc2_statistics_timer_cancel'
KEY_MEASUREMENTS_CLIENT = 'nhc2_measurements_client'
KEY_STATISTICS_COORDINATOR = 'nhc2_statistics_coordinator'
BRAND = 'Niko'

DEFAULT_USERNAME = 'hobby'
DEFAULT_PORT = 8884

SERVICE_SET_LIGHT_BRIGHTNESS = 'set_light_brightness'
ATTR_LIGHT_BRIGHTNESS = 'light_brightness'

CONF_ENABLE_STATISTICS = 'enable_statistics'
CONF_IMPORT_HISTORICAL_STATISTICS = 'import_statistics'
CONF_HISTORICAL_STATISTICS_IMPORTED = 'historical_statistics_imported'

# Properties starting with these prefixes will have their measurements retrieved from REST API
MEASUREMENT_PROPERTIES_FILTER = ['ElectricalEnergy', 'WaterVolume', 'GasVolume']
# How far back to retrieve historical data (in days)
MEASUREMENT_HISTORY_DAYS = 3650  # 10 years
