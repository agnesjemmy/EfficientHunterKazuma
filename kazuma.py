# Import Libraries
import json, math

def movesetOptimization(monstersNumArray):
    monsters = monstersNumArray['monstersArray']
    efficiency = 0
    
    # Create an empty list ptc
    moves = [0] * len(monsters)

    # Figure out when to Prepare Transmission Circle (1)
    for i in range(len(monsters) - 1):  # Loop until the second to last element
        if monsters[i] < monsters[i + 1]:  # Compare current and next element
            if i == 0 or moves[i - 1] == 0: # Two 1's cannot be placed next to each other
                moves[i] = 1
                efficiency = efficiency - monsters[i]

    # Figure out when to Attack (2)
    i = 0
    while i < len(moves) - 1:  # Loop until the second to last element
        if moves[i] == 1:  # After PTC, find the best move to Attack at
            tempMostEfficiency = float('-inf')
            tempIdxMostEfficiency = -1  # Initialize as invalid index

            # Look for the most efficient attack placement (stop at the next PTC (1))
            j = i + 1
            while j < len(moves) and moves[j] != 1:
                e = monsters[j] - monsters[j - 1]  # Calculate efficiency
                
                if e > tempMostEfficiency:
                    tempMostEfficiency = e
                    tempIdxMostEfficiency = j
                
                j += 1

            # Mark best spot for Attack
            if tempIdxMostEfficiency != -1 and moves[tempIdxMostEfficiency] != 2:
                moves[tempIdxMostEfficiency] = 2
                efficiency = efficiency + monsters[tempIdxMostEfficiency]

            # Move i to the next PTC or end
            i = j
        else:
            i += 1

    #print(moves)
    #print(efficiency)

    return efficiency


def evaluate():
    # Load 'input.json' File
    with open('input.json', 'r') as file:
        data = json.load(file)

    # Read in Monster data
    monsters = {}  # Initialize empty dictionary
    counter = 0
    
    for monsterInput in data:
        # Extract number of monsters
        numOfMonsters = data[counter]['monsters']
        #sprint(counter, numOfMonsters)

        # Add into monsters dictionary
        monsters[counter] = {
            'monstersArray': numOfMonsters
        }

        # increment counter
        counter += 1 

    # Combine efficiencies into one dictionary    
    efficiency = {} # Initialize empty dictionary
    eCounter = 0

    for row in monsters:
        optimalMoves = movesetOptimization(monsters[row])
        efficiency[eCounter] = optimalMoves
        eCounter += 1

    # Format Efficiency Output
    outputEfficiency = [{"efficiency": value} for value in efficiency.values()]

    # Print output.json File
    with open('output.json', 'w') as output_file:
        json.dump(outputEfficiency, output_file, indent=4)

    return efficiency

if __name__ == "__main__":
    evaluate()
