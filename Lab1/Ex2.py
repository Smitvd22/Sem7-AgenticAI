import random

N = 6

rooms = []

for i in range(N):
    rooms.append(random.choice(["Dirty", "Clean"]))

location = 0

score = 0

print("Initial Rooms")

print(rooms)

for step in range(N):

    print("\nStep", step + 1)

    print("Current Position:", location)

    print("Status:", rooms[location])

    if rooms[location] == "Dirty":

        rooms[location] = "Clean"

        score += 10

        print("Action: Suck")

    else:

        print("Action: Move Right")

        if location < N - 1:
            location += 1
            score -= 1

print("\nFinal Rooms")

print(rooms)

print("Performance Score:", score)