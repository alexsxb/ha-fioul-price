from homeassistant.const import Platform

DOMAIN = "fioul"

CONF_POLLRATE = "pollrate"
DEFAULT_POLLRATE = 2

PLATFORMS: list[Platform] = [Platform.SENSOR]
