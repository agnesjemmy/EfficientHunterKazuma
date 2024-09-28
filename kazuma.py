from flask import Flask, jsonify, request
import json

app = Flask(__name__)

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
                efficiency -= monsters[i]

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
                efficiency += monsters[tempIdxMostEfficiency]

            # Move i to the next PTC or end
            i = j
        else:
            i += 1

    return efficiency

@app.route('/efficient-hunter-kazuma', methods=['POST'])
def evaluate_endpoint():
    # Get JSON data from the request
    data = request.get_json()

    efficiency = []  # Initialize empty list for efficiencies

    for monsters in data:
        # Create a dictionary to pass to the optimization function
        monsters_data = {'monstersArray': monsters['monsters']}
        optimalMoves = movesetOptimization(monsters_data)
        efficiency.append({"efficiency": optimalMoves})

    print(efficiency)
    return jsonify(efficiency)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
