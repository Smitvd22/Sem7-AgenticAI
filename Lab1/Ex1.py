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


class ModelBasedAgent:

    def __init__(self):

        self.memory = {
            "A": "Unknown",
            "B": "Unknown"
        }

    def action(self, percept):

        location, status = percept

        self.memory[location] = status

        if status == "Dirty":
            return "Suck"

        if self.memory["A"] == "Clean" and self.memory["B"] == "Clean":
            return "NoOp"

        if location == "A":
            return "Right"

        return "Left"


env = VacuumEnvironment()

agent = ModelBasedAgent()

for step in range(20):

    percept = env.percept()

    action = agent.action(percept)

    print("Step", step + 1)
    print("Percept:", percept)
    print("Action:", action)

    env.execute(action)

    print("Rooms:", env.rooms)
    print("Memory:", agent.memory)
    print("Score:", env.performance)
    print("--------------------------")

print("\nFinal Score =", env.performance)