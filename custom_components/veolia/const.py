"""Constants for Veolia."""

from homeassistant.components.sensor import DOMAIN as SENSOR

# Base component constants
NAME = "Veolia"
DOMAIN = "veolia"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.1.0"

ISSUE_URL = "https://github.com/tetienne/veolia-custom-component/issues"

# Platforms
PLATFORMS = [SENSOR]


# Configuration and options
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN
API = "api"
COORDINATOR = "coordinator"


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
