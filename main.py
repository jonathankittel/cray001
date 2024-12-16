print("hello")
import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
print("CUDA version:", torch.version.cuda)
print("GPU Name:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "No GPU found")

import flask

from flask import Flask, request, jsonify, render_template

import time

from blackjack_game import BlackjackGame

app = Flask(__name__)

game = BlackjackGame()

# Main Page
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/second')
def second_page():
    return render_template('second.html')  # Renders the second page

@app.route('/third')
def third_page():
    return render_template('third.html')  # Third Page for matrix input

@app.route('/blackjack')
def blackjack_page():
    return render_template('blackjack.html')  # Third Page for matrix input

# Route to handle POST request from TypeScript
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()  # Parse JSON data
    user_input = data.get("user_input", "")  # Extract user input
    print(f"User submitted: {user_input}")  # Print to command line
    return jsonify({"message": f"Received: {user_input}"})  # Send response

@app.route('/matrix', methods=['POST'])
def matrix_multiplication():
    data = request.get_json()
    size = int(data.get("user_input", 0))  # Extract matrix size

    if size <= 0:
        return jsonify({"error": "Invalid matrix size"}), 400

    # Perform matrix multiplication on the GPU
    try:
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        A = torch.rand(size, size, device=device)
        B = torch.rand(size, size, device=device)

        start_time = time.time()
        C = torch.matmul(A, B)  # Matrix multiplication
        torch.cuda.synchronize()  # Ensure GPU operations complete
        end_time = time.time()

        computation_time = end_time - start_time
        print(f"Matrix multiplication of size {size}x{size} completed in {computation_time:.4f} seconds.")

        return jsonify({"message": f"Matrix multiplication took {computation_time:.4f} seconds."})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred during computation."}), 500


@app.route('/blackjack', methods=['GET'])
def start_game():
    """Start a new Blackjack game."""
    game.reset_game()
    state = game.get_game_state()
    return jsonify({
        "message": "New game started!",
        "user_cards": state["user_cards"],
        "user_score": state["user_score"],
        "dealer_cards": state["dealer_cards"],
    })

@app.route('/blackjack/hit', methods=['POST'])
def hit():
    """User draws a new card."""
    if game.game_over:
        return jsonify({"message": "Game over! Please restart."})

    result = game.user_hit()
    state = game.get_game_state()

    response = {
        "user_cards": state["user_cards"],
        "user_score": state["user_score"],
        "dealer_cards": state["dealer_cards"],
        "message": result if result else "You drew a card. Hit or Stay?",
    }

    return jsonify(response)

@app.route('/blackjack/stay', methods=['POST'])
def stay():
    """User decides to stay. Dealer's turn begins."""
    game.dealer_turn()
    state = game.get_game_state()

    return jsonify({
        "user_cards": state["user_cards"],
        "user_score": state["user_score"],
        "dealer_cards": state["dealer_cards"],
        "dealer_score": state["dealer_score"],
        "message": f"Game Over! Winner: {state['winner']}",
        "winner": state["winner"],
    })

if __name__ == '__main__':
    app.run(debug=True)