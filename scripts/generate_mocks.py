import json
import random
from datetime import datetime, timedelta

def generate_realistic_mocks():
    depts = {
        "Engineering": {
            "types": ["Track tamping", "Rail renewal", "Deep screening", "Ballast cleaning"],
            "machinery": ["Tamping Machine", "Ballast Regulator", "Rail Grinding Machine"],
            "severity_range": (4, 9)
        },
        "TRD": {
            "types": ["OHE mast repair", "Feeder cable replacement", "Booster transformer check"],
            "machinery": ["Tower Wagon", "Insulated Ladder"],
            "severity_range": (5, 10)
        },
        "S&T": {
            "types": ["Point machine testing", "Signal post repair", "Track circuit overhaul"],
            "machinery": ["Hand Tools", "Testing Kit"],
            "severity_range": (6, 10)
        }
    }

    tasks = []
    for i in range(60):
        dept = random.choice(list(depts.keys()))
        dept_info = depts[dept]

        start_km = round(random.uniform(1000.0, 1100.0), 3)
        end_km = round(start_km + random.uniform(0.1, 5.0), 3)

        tasks.append({
            "task_id": f"{dept[:3].upper()}-{1000 + i}",
            "dept": dept,
            "type": random.choice(dept_info["types"]),
            "chainage_start_km": start_km,
            "chainage_end_km": end_km,
            "duration_mins": random.choice([60, 120, 180, 240, 360]),
            "severity": random.randint(*dept_info["severity_range"]),
            "days_overdue": random.randint(0, 30),
            "needs_power_block": random.choice([True, False]),
            "machinery_type": random.choice(dept_info["machinery"])
        })

    corridor_availability = []
    start_date = datetime(2026, 10, 1)
    for day in range(30):
        current_date = (start_date + timedelta(days=day)).strftime("%Y-%m-%d")
        # Create 3-4 windows per day
        for w_id in range(3):
            corridor_availability.append({
                "window_id": f"WIN-{day:02d}-{w_id}",
                "date": current_date,
                "start_time": f"{(w_id * 4):02d}:00",
                "end_time": f"{(w_id * 4 + 4):02d}:00",
                "freight_probability": round(random.random(), 2),
                "passenger_train_slots": [f"{(w_id * 4 + 1):02d}:30", f"{(w_id * 4 + 2):02d}:15"]
            })

    train_timetable = []
    for i in range(20):
        train_timetable.append({
            "train_id": f"TRN-{100 + i}",
            "name": f"Passenger Express {i}",
            "arrival_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
            "departure_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
            "chainage_km": round(random.uniform(1000.0, 1100.0), 3)
        })

    freight_forecast = []
    for i in range(15):
        freight_forecast.append({
            "train_id": f"FR-{500 + i}",
            "expected_time": f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}",
            "buffer_mins": 120,
            "probability": round(random.uniform(0.3, 0.9), 2)
        })

    mocks = {
        "tasks": tasks,
        "corridor_availability": corridor_availability,
        "train_timetable": train_timetable,
        "freight_forecast": freight_forecast
    }

    with open('data/mocks.json', 'w') as f:
        json.dump(mocks, f, indent=2)

    print(f"Generated {len(tasks)} tasks and {len(corridor_availability)} windows in data/mocks.json")

if __name__ == "__main__":
    generate_realistic_mocks()
