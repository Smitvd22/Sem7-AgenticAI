import random

rooms = {
    "A": "Dirty",
    "B": "Dirty"
}

location = "A"

score = 0

for step in range(20):

    print("\nStep", step + 1)

    print("Rooms:", rooms)

    print("Location:", location)

    if rooms[location] == "Dirty":

        rooms[location] = "Clean"

        score += 10

        print("Action: Suck")

    else:

        if location == "A":
            location = "B"
        else:
            location = "A"

        score -= 1

        print("Action: Move")

    if random.random() < 0.1:

        room = random.choice(["A", "B"])

        rooms[room] = "Dirty"

        print(room, "became Dirty again")

print("\nFinal Rooms")

print(rooms)

print("Performance Score:", score)