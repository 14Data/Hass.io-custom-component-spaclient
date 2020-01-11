import logging

# Import the device class from the component that you want to support
from custom_components import SpaClient
from homeassistant.components.climate import ClimateDevice
from homeassistant.components.climate.const import (
    SUPPORT_TARGET_TEMPERATURE, HVAC_MODE_HEAT, HVAC_MODE_OFF)
from homeassistant.const import ATTR_TEMPERATURE, TEMP_CELSIUS, TEMP_FAHRENHEIT
from homeassistant.util.temperature import convert as convert_temperature
from datetime import timedelta

_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = SpaClient.INTERVAL

SUPPORT_HVAC = [HVAC_MODE_HEAT, HVAC_MODE_OFF]
SUPPORT_FLAGS = (SUPPORT_TARGET_TEMPERATURE)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    spa_data = SpaClient.NETWORK
    add_devices([SpaTemp(spa_data)])

class SpaTemp(ClimateDevice):
    def __init__(self, data):
        """Initialize the sensor."""
        self._spa = data.spa

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Spa Temperature'

    @property
    def hvac_mode(self):
        """Return current HVAC mode."""
        if self._spa.get_heating():
            return HVAC_MODE_HEAT
        return HVAC_MODE_OFF

    @property
    def hvac_modes(self):
        """Return available HVAC modes."""
        return SUPPORT_HVAC

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return SUPPORT_FLAGS

    @property
    def current_temperature(self):
        """Return true if light is on."""
        return self._spa.get_current_temp()

    @property
    def target_temperature(self):
        return self._spa.get_set_temp()

    def set_temperature(self, **kwargs):
        _LOGGER.info("Setting Temperature")
        self._spa.send_config_request()
        self._spa.set_temperature(kwargs.get(ATTR_TEMPERATURE))

    def set_hvac_mode(self, hvac_mode):
        """Set new target hvac mode."""
        if self._spa.get_heating():
            return HVAC_MODE_HEAT
        return HVAC_MODE_OFF

    @property
    def max_temp(self):
        """Return the maximum temperature."""
        return convert_temperature(104, TEMP_FAHRENHEIT, self.temperature_unit)

    @property
    def temperature_unit(self):
        """Return the unit of measurement used by the platform."""
        return TEMP_FAHRENHEIT

    @property
    def current_operation(self):
        """Return current operation ie. heat, cool, idle."""
        return "Set Temperature"

    def update(self):
        """Fetch new state data for the sensor."""
        self._spa.read_all_msg()

    def turn_off(self):
        pass

    def turn_on(self):
        pass
