from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

@dataclass(frozen=True)
class EnecoqSensorDescription(SensorEntityDescription):
    scope: str = "today"
    key: str = "usage"

SENSORS: list[EnecoqSensorDescription] = [
    EnecoqSensorDescription(
        key="usage", scope="today",
        name="Today Power Usage",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EnecoqSensorDescription(
        key="cost", scope="today",
        name="Today Power Cost",
        native_unit_of_measurement="JPY",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EnecoqSensorDescription(
        key="co2", scope="today",
        name="Today CO2 Emission",
        native_unit_of_measurement="kg",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EnecoqSensorDescription(
        key="timestamp", scope="today",
        name="Today Timestamp",
    ),

    EnecoqSensorDescription(
        key="usage", scope="month",
        name="Month Power Usage",
        native_unit_of_measurement="kWh",
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EnecoqSensorDescription(
        key="cost", scope="month",
        name="Month Power Cost",
        native_unit_of_measurement="JPY",
        device_class=SensorDeviceClass.MONETARY,
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EnecoqSensorDescription(
        key="co2", scope="month",
        name="Month CO2 Emission",
        native_unit_of_measurement="kg",
        state_class=SensorStateClass.TOTAL_INCREASING,
    ),
    EnecoqSensorDescription(
        key="timestamp", scope="month",
        name="Month Timestamp",
    ),
]

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([EnecoqSensor(coordinator, entry.entry_id, desc) for desc in SENSORS], True)

class EnecoqSensor(CoordinatorEntity, SensorEntity):
    entity_description: EnecoqSensorDescription

    def __init__(self, coordinator, entry_id: str, description: EnecoqSensorDescription):
        super().__init__(coordinator)
        self.entity_description = description

        self._attr_unique_id = f"{entry_id}_{description.scope}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry_id)},
            name="enecoQ",
            manufacturer="FamilyNet Japan / CYBERHOME",
            model="enecoQ",
        )

    @property
    def native_value(self):
        data = (self.coordinator.data or {}).get(self.entity_description.scope) or {}
        return data.get(self.entity_description.key)
