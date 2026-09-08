my_vehicle = {
    "model": "Ford",
    "make": "Explorer",
    "year": 2018,
    "mileage": 40000
}

for key, value in my_vehicle.items():
    print(f"{key}: {value}")

vehicle2 = my_vehicle.copy()

vehicle2["number_of_tires"] = 4

# del vehicle2["mileage"]
vehicle2.pop("mileage")

for item in vehicle2:
    print(item)