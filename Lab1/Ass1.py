class VacuumEnvironment:
    def __init__(self):
        self.rooms = {
            "A": "Dirty",
            "B": "Dirty"
        }

        self.location = "A"
        self.performance = 0

    def percept(self):
        return self.location, self.rooms[self.location]

    def execute(self, action):
        if action == "Suck":
            if self.rooms[self.location] == "Dirty":
                self.rooms[self.location] = "Clean"
                self.performance += 10

        elif action == "Right":
            self.location = "B"
            self.performance -= 1

        elif action == "Left":
            self.location = "A"
            self.performance -= 1

        elif action == "NoOp":
            pass


def simple_reflex_agent(percept):
    location, status = percept

    if status == "Dirty":
        return "Suck"

    if location == "A":
        return "Right"

    return "Left"


env = VacuumEnvironment()

steps = 10

print("Initial State")
print(env.rooms)
print()

for step in range(1, steps + 1):

    percept = env.percept()

    action = simple_reflex_agent(percept)

    print(f"Step {step}")
    print("Percept :", percept)
    print("Action  :", action)

    env.execute(action)

    print("Rooms   :", env.rooms)
    print("Location:", env.location)
    print("Score   :", env.performance)
    print("-" * 40)

print("\nFinal State")
print(env.rooms)
print("Final Score =", env.performance)