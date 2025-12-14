import datetime
import numpy as np
import pandas as pd
import threading
import time

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

    columns = [
        "id",
        "color",
        "voltage",
        "status",
        "assigned_to",
        "assigned_at",
    ]
    bat_df = pd.DataFrame(columns=columns)

    danger_batts = []
    thread = threading.Thread(target=time_since_assigned_callback, args=[batteries])
    thread.start()

    # Read user input loop
    cmd = ""
    while cmd.lower() != "q":
        assigned = False
        print("\nCurrent battery statuses:")
        for battery in batteries:
            bat_df.loc[battery.id] = battery.data

        print(bat_df.to_string(index=False))
        print()

        bat_id = input("Select battery by id: ")

        try:
            bat_id = int(bat_id)

            if bat_id in danger_batts:
                print(f"Warning: Battery {bat_id} is DEFECT!")
                continue

            if bat_id < 0 or bat_id >= len(batteries):
                print("Invalid battery id (0-9).")
                continue

        except:
            print("Invalid battery id (0-9) or not integer.")
            continue

        selected_battery = batteries[bat_id]
        cmd = input(f"Choose action:\nv: update voltage\ns: update status\na: assign to team\nq: quit\n")

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
                selected_battery.time_assigned = time.time()
                assigned = True

            case _:
                print("Invalid command.")

        selected_battery.update_status(assigned=assigned)
        if selected_battery.status == batt_status.DEFECT:
            danger_batts.append(selected_battery.id)

def time_since_assigned_callback(batteries: List[Battery]):
    while True:
        time.sleep(5)

        for battery in batteries:
            time_assigned = battery.time_assigned
            if time_assigned and battery.assigned_to_at:
                elapsed_time = time.time() - time_assigned
                if elapsed_time > 10:  # 10 minutes
                    print(f"\nReminder: Battery {battery.id} assigned to {battery.assigned_to_at[0]} for over 10 minutes. Please check voltage.")

if __name__ == "__main__":
    main()