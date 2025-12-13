import datetime
import numpy as np
import pandas as pd

from typing import List, Tuple
from battery import Battery, batt_colors, batt_status

def main():
    num_gray_batteries = 8
    num_blue_batteries = 2

    batteries_b: List[Battery] = []
    batteries_g: List[Battery] = []

    for i in range(num_gray_batteries):
        battery = Battery(
            id=i,
            color=batt_colors.GRAY,
            voltage=np.random.uniform(3.5, 4.2),
            assigned_to_at=(f"Team_{i}", datetime.datetime.now().isoformat())
        )
        batteries_g.append(battery)

    for i in range(num_blue_batteries):
        battery = Battery(
            id=i + num_gray_batteries,
            color=batt_colors.BLUE,
            voltage=np.random.uniform(3.5, 4.2),
            assigned_to_at=(f"Team_{i + num_gray_batteries}", datetime.datetime.now().isoformat())
        )
        batteries_b.append(battery)

if __name__ == "__main__":
    main()