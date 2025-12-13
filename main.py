import datetime
import numpy as np
import pandas as pd

from typing import List, Dict
from battery import Battery, batt_colors, batt_status

def main():
    num_gray_batteries = 8
    num_blue_batteries = 2

    batteries: List[Battery] = []

    for i in range(num_blue_batteries+num_gray_batteries):
        battery = Battery(
            id=i,
            color=batt_colors.GRAY if i < num_gray_batteries else batt_colors.BLUE,
            voltage=24.6,
        )

        batteries.append(battery)

    bat_stats: Dict[int, batt_status] = {
        0: batt_status.IN_USE,
        1: batt_status.CHARGING,
        2: batt_status.STORED,
        3: batt_status.DEFECT,
        4: batt_status.LOW,
    }

    # Read user input loop
    cmd = ""
    while cmd.lower() != "q":
        for battery in batteries:
            print(battery)

        bat_id = input("Select battery by id: ")

        try:
            bat_id = int(bat_id)
        except:
            print("Invalid battery id (0-9) or not integer.")
            continue

        selected_battery = batteries[bat_id]
        cmd = input(f"Choose action:\nv: update voltage\ns: update status\na: assign to team\nr: remove from team\nq: quit\n")

        match cmd.lower():
            case "v":
                voltage = input("Enter new voltage:\n")
                try:
                    voltage = float(voltage)
                    selected_battery.voltage = voltage
                except:
                    print("Invalid voltage (not float).")

            case "s":
                status = input("Enter new status (0: IN_USE, 1: CHARGING, 2: STORED, 3: DEFECT, 4: LOW):\n")
                try:
                    selected_battery.status = batt_status[bat_stats[int(status)].name]
                except:
                    print("Invalid status.")

            case "a":
                team_name = input("Enter team name: ")
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                selected_battery.assigned_to_at = (team_name, timestamp)

            case _:
                print("Invalid command.")

if __name__ == "__main__":
    main()