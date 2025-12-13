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
    box: int
    assigned_to: str # Make an Enum of team names later
    status: batt_status = batt_status.STORED