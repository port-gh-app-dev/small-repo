class Transportation:
    """Represents a mode of transportation."""

    def __init__(self, name: str, speed: float, capacity: int, fuel_type: str = "gasoline"):
        self.name = name
        self.speed = speed          # km/h
        self.capacity = capacity    # number of passengers
        self.fuel_type = fuel_type
        self.current_passengers = 0
        self.is_moving = False

    def board(self, passengers: int) -> str:
        available = self.capacity - self.current_passengers
        if passengers > available:
            return f"Not enough space! Only {available} seat(s) available."
        self.current_passengers += passengers
        return f"{passengers} passenger(s) boarded. ({self.current_passengers}/{self.capacity} seats filled)"

    def disembark(self, passengers: int) -> str:
        if passengers > self.current_passengers:
            return f"Only {self.current_passengers} passenger(s) on board."
        self.current_passengers -= passengers
        return f"{passengers} passenger(s) disembarked. ({self.current_passengers}/{self.capacity} seats filled)"

    def depart(self) -> str:
        if self.current_passengers == 0:
            return "Cannot depart with no passengers."
        self.is_moving = True
        return f"{self.name} is now moving at {self.speed} km/h."

    def stop(self) -> str:
        if not self.is_moving:
            return f"{self.name} is already stopped."
        self.is_moving = False
        return f"{self.name} has stopped."

    def travel_time(self, distance: float) -> str:
        hours = distance / self.speed
        minutes = hours * 60
        return f"Estimated travel time for {distance} km: {hours:.2f} hrs ({minutes:.0f} mins)"

    def __repr__(self):
        status = "moving" if self.is_moving else "stopped"
        return (
            f"Transportation(name={self.name!r}, speed={self.speed} km/h, "
            f"capacity={self.capacity}, fuel={self.fuel_type}, status={status})"
        )


# --- Example usage ---
if __name__ == "__main__":
    bus = Transportation("City Bus", speed=60, capacity=40, fuel_type="diesel")

    print(bus.board(15))
    print(bus.board(30))       # exceeds remaining capacity
    print(bus.depart())
    print(bus.travel_time(120))
    print(bus.disembark(5))
    print(bus.stop())
    print(bus)
```

**What it includes:**

- **`__init__`** — sets up name, speed, capacity, fuel type, and tracks passengers + motion state
- **`board(n)`** — adds passengers with capacity validation
- **`disembark(n)`** — removes passengers safely
- **`depart()`** — starts movement (requires at least one passenger)
- **`stop()`** — halts the vehicle
- **`travel_time(distance)`** — estimates travel duration for a given distance
- **`__repr__`** — clean string representation for debugging

**Sample output:**
```
15 passenger(s) boarded. (15/40 seats filled)
Not enough space! Only 25 seat(s) available.
City Bus is now moving at 60 km/h.
Estimated travel time for 120 km: 2.00 hrs (120 mins)
5 passenger(s) disembarked. (10/40 seats filled)
City Bus has stopped.
Transportation(name='City Bus', speed=60 km/h, capacity=40, fuel=diesel, status=stopped)
