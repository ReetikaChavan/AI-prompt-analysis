# AI Prompt Analysis

In this project, we have developed an AI-based system to evaluate and analyze user-submitted prompts. The system uses a machine learning model to provide a score and feedback based on the quality and relevance of the input prompt.

## Project Overview

This project includes a WebSocket server and a simple web-based interface that allows users to submit prompts. The server evaluates the prompt and provides feedback and a score in real-time, which is then displayed on the frontend. The evaluation is powered by a machine learning model trained to analyze the structure, clarity, and relevance of the prompt.

### Key Components:
- **server.py**: The Python script that runs the WebSocket server. It loads the machine learning model, evaluates prompts, and sends the results (score and feedback) back to the client.
- **index.html**: The frontend file that contains the layout of the chat interface where users input their prompts. It interacts with the WebSocket server to submit prompts and receive evaluation results.

## Important Notes

### 1. Running the WebSocket Server:
- The WebSocket server is responsible for receiving user prompts and sending back the evaluation (score and feedback).
- To start the server, execute the `server.py` file:

    ```bash
    python server.py
    ```

### 2. Frontend Setup (Web Interface):
- The frontend (`index.html`) allows users to type their prompts into a chat interface.
- After submission, the prompts are sent to the WebSocket server, which evaluates the input and sends back a score and feedback. This is displayed in real-time in the user interface.
  
- Open the `index.html` file in your browser to interact with the chat interface.

### 3. Running a Local HTTP Server (Optional):
If you prefer to run the frontend on a local HTTP server, you can use Python’s built-in HTTP server to serve the `index.html` file.

1. Navigate to the directory where `index.html` is located:
    ```bash
    cd path/to/your/project
    ```

2. Run the following command to start the HTTP server:
    ```bash
    python -m http.server
    ```

3. After the server starts, you can open your browser and go to `http://localhost:8000` to access the web interface.

## Repository Contents

In this repository, you will find the following files:

- **server.py**: Python script that starts the WebSocket server and loads the trained machine learning model to evaluate prompts.
- **index.html**: The HTML file for the user interface, where prompts are entered and responses are displayed.

## Instructions

To run the AI Prompt Analysis system:

1. Clone this repository to your local machine.

2. Ensure you have Python installed along with the required libraries (such as `websocket-server`, `scikit-learn`, and any other dependencies):

    Install dependencies via `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. Start the WebSocket server by running `server.py`:

    ```bash
    python server.py
    ```

4. Optionally, you can run a local HTTP server to serve the `index.html` file using the following command:

    ```bash
    python -m http.server
    ```

5. Open the `index.html` file in your browser (or access `http://localhost:8000` if using the HTTP server) to interact with the frontend.

6. Enter a prompt in the chat interface. After submitting the prompt, the server will analyze it and provide a score along with feedback, which will appear in the chat interface.

## Requirements

- Python 3.x
- Required Python libraries:
    - `websocket-server`
    - `scikit-learn`
    - `pickle`
- HTML/CSS/JS for the frontend (handled in `index.html`)

To install necessary dependencies, you can create a `requirements.txt` file (if not already provided) and use the following command to install the required packages:

```bash
pip install -r requirements.txt
