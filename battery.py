from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum

batt_colors = Enum('batt_colors', 'GRAY BLUE')
batt_status = Enum('batt_status', 'IN_USE CHARGING STORED DEFECT LOW')

@dataclass
class Battery:
    id: int
    color: batt_colors
    voltage: float
    assigned_to_at: Tuple[str, str] | None = None # Team name and timestamp, make an Enum of team names later
    status: batt_status = batt_status.STORED

    @property
    def data(self) -> List:
        return [
            self.id,
            self.color.name,
            self.voltage,
            self.status.name,
            self.assigned_to_at[0] if self.assigned_to_at else "",
            self.assigned_to_at[1] if self.assigned_to_at else "",
        ]

    def __str__(self) -> str:
        bat_id = f"Battery {self.id} {self.color.name}"
        bat_voltage = f"Voltage: {self.voltage}V"
        bat_status = f"Status: {self.status.name}"
        bat_assigned = f"Assigned to: {self.assigned_to_at[0]} at {self.assigned_to_at[1]}" if self.assigned_to_at else "Not assigned"
        return f"{bat_id} | {bat_voltage} | {bat_status} | {bat_assigned}"