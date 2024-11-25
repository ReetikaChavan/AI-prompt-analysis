import asyncio
import websockets
import json
import logging
from transformers import pipeline

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize a text classification pipeline with a DistilBERT model for sentiment analysis
evaluator = pipeline("sentiment-analysis", model="distilbert-base-uncased")

# Function to evaluate the response with adjusted scoring logic
async def evaluate_response(response: str) -> int:
    """
    Evaluate the response using a pre-trained model for sentiment analysis,
    and adjust the score based on sentiment and prompt length.
    """
    logging.info(f"Evaluating response: {response}")
    
    try:
        # Get sentiment analysis result (labels can be 'LABEL_0' for negative, 'LABEL_1' for positive)
        result = evaluator(response)
        logging.info(f"Model result: {result}")  # Debugging line to print raw model output
        
        # We assume that a positive sentiment corresponds to a better response
        sentiment = result[0]['label']
        sentiment_score = 0
        feedback_message = ""

        if sentiment == 'POSITIVE':
            sentiment_score = 7
            feedback_message = "The prompt is well-structured, relevant, and clear."
        else:
            sentiment_score = 3
            feedback_message = "The prompt might benefit from further clarification and better structure."

        # Adjust the score based on the length of the input prompt
        length_adjustment = min(len(response.split()) / 10, 1)  # Normalize length to a max of 1

        # Final score combines sentiment score and length adjustment, scaled to 0-10
        final_score = sentiment_score + length_adjustment * 3  # Sentiment weighted more heavily
        logging.info(f"Final adjusted score: {final_score}")
        
        # Ensure the score is within the range of 1 to 10
        final_score = max(1, min(final_score, 10))

        # Provide feedback based on the score
        if final_score >= 9:
            feedback_message = "Excellent prompt! Well-structured, clear, and informative."
        elif final_score >= 6:
            feedback_message = "Good prompt. Clear, but could use more detail or refinement."
        elif final_score >= 3:
            feedback_message = "Needs improvement. Some areas may be unclear or lacking in detail."
        else:
            feedback_message = "Poor prompt. It lacks clarity or sufficient structure."

        return int(final_score), feedback_message
    
    except Exception as e:
        logging.error(f"Error during evaluation: {e}")
        return 5, "An error occurred during the evaluation process."

# Handle the WebSocket connection
async def handle_connection(websocket):
    total_score = 0  # Accumulate total score across prompts
    try:
        logging.info("New client connected.")
        while True:
            try:
                # Receive and parse the message from the client
                message = await websocket.recv()
                data = json.loads(message)
                if data.get("type") == "end":  # End the session if "end" is received
                    break
                user_prompt = data.get("content")
                logging.info(f"Received prompt: {user_prompt}")

                # Skip evaluation if the prompt is empty
                if not user_prompt:
                    await websocket.send(json.dumps({"error": "Empty prompt received"}))
                    continue

                # Evaluate the response and update the total score
                score, feedback = await evaluate_response(user_prompt)
                total_score += score  # Update total score

                # Send feedback to the client with the score
                feedback_response = {
                    "type": "feedback",
                    "score": score,
                    "total_score": total_score,  # Include the total score
                    "feedback": feedback,  # Include the feedback message
                }
                logging.info(f"Sending feedback: {feedback_response}")
                await websocket.send(json.dumps(feedback_response))

            except websockets.exceptions.ConnectionClosed:
                logging.info("Client disconnected.")
                break
            except Exception as e:
                logging.error(f"Error receiving message: {e}")
                break

    except Exception as e:
        logging.error(f"Error in connection handler: {e}")
    finally:
        await websocket.close()

# Main function to start the WebSocket server
async def main():
    logging.info("Starting WebSocket server on ws://localhost:8080")
    async with websockets.serve(handle_connection, "localhost", 8080):
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
