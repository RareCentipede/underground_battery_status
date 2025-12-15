import datetime
import numpy as np
import os
import pandas as pd
import threading
import time

from typing import List, Dict
from battery import Battery, batt_colors, batt_status

NUM_GRAY_BATTS = 8
NUM_BLUE_BATTS = 2
SAVE_PATH = 'saves/'

BAT_STATS: Dict[int, batt_status] = {
    0: batt_status.IN_USE,
    1: batt_status.CHARGING,
    2: batt_status.STORED,
    3: batt_status.DEFECT,
    4: batt_status.LOW,
}

COLUMNS = [
    "id",
    "color",
    "voltage",
    "status",
    "assigned_to",
    "assigned_at",
]

def main():
    batteries: List[Battery] = []
    saved_file = os.listdir(SAVE_PATH)

    if saved_file:
        print(f'Loading save')
        bat_df = pd.read_csv(SAVE_PATH + saved_file[0])

        for _, row in bat_df.iterrows():
            battery = Battery(
                id=row['id'],
                color=batt_colors[row['color']],
                voltage=row['voltage'],
                assigned_to_at=(row['assigned_to'], row['assigned_at']) if not pd.isna(row['assigned_to']) else ('', ''),
                status=batt_status[row['status']]
            )
            batteries.append(battery)
    else:
        for i in range(NUM_BLUE_BATTS+NUM_GRAY_BATTS):
            battery = Battery(
                id=i,
                color=batt_colors.GRAY if i < NUM_GRAY_BATTS else batt_colors.BLUE,
                voltage=24.6,
            )

            batteries.append(battery)

        bat_df = pd.DataFrame(columns=COLUMNS)

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
                    selected_battery.status = batt_status[BAT_STATS[int(status)].name]
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
        bat_df.to_csv(SAVE_PATH+'save', index=False)
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