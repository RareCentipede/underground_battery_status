import numpy as np
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
    time_assigned: float = -1.0

    @property
    def data(self) -> List:
        return [
            self.id,
            self.color.name,
            self.voltage,
            self.status.name,
            self.assigned_to_at[0] if self.assigned_to_at else "",
            self.assigned_to_at[1] if self.assigned_to_at else "",
            self.time_assigned,
        ]

    def update_status(self, assigned: bool = False) -> None:
        old_status = self.status
        if self.voltage < 21.0:
            self.status = batt_status.LOW if self.status != batt_status.CHARGING else self.status
            self.assigned_to_at = None

        if assigned:
            self.status = batt_status.IN_USE

        if self.voltage <= 20.0:
            self.status = batt_status.DEFECT

        if old_status != self.status:
            print(  # Debug print
                f'Battery {self.id} status updated to {self.status.name} with voltage {self.voltage}V'
            )

    def __str__(self) -> str:
        bat_id = f"Battery {self.id} {self.color.name}"
        bat_voltage = f"Voltage: {self.voltage}V"
        bat_status = f"Status: {self.status.name}"
        bat_assigned = f"Assigned to: {self.assigned_to_at[0]} at {self.assigned_to_at[1]}" if self.assigned_to_at else "Not assigned"
        return f"{bat_id} | {bat_voltage} | {bat_status} | {bat_assigned}"