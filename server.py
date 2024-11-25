import asyncio
import websockets
import json
import logging
from transformers import pipeline


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


evaluator = pipeline("sentiment-analysis", model="distilbert-base-uncased")

# Function to evaluate the response with adjusted scoring logic
async def evaluate_response(response: str) -> int:
    """
    Evaluate the response using a pre-trained model for sentiment analysis,
    and adjust the score based on sentiment and prompt length.
    """
    logging.info(f"Evaluating response: {response}")
    
    try:
       
        result = evaluator(response)
        logging.info(f"Model result: {result}")  
        
       
        sentiment = result[0]['label']
        sentiment_score = 0
        feedback_message = ""

        if sentiment == 'POSITIVE':
            sentiment_score = 7
            feedback_message = "The prompt is well-structured, relevant, and clear."
        else:
            sentiment_score = 3
            feedback_message = "The prompt might benefit from further clarification and better structure."

    
        length_adjustment = min(len(response.split()) / 10, 1)  

       
        final_score = sentiment_score + length_adjustment * 3 
        logging.info(f"Final adjusted score: {final_score}")
        
      
        final_score = max(1, min(final_score, 10))

      
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

# WebSocket connection
async def handle_connection(websocket):
    total_score = 0  
    try:
        logging.info("New client connected.")
        while True:
            try:
               
                message = await websocket.recv()
                data = json.loads(message)
                if data.get("type") == "end":  
                    break
                user_prompt = data.get("content")
                logging.info(f"Received prompt: {user_prompt}")

              
                if not user_prompt:
                    await websocket.send(json.dumps({"error": "Empty prompt received"}))
                    continue

            
                score, feedback = await evaluate_response(user_prompt)
                total_score += score  

             
                feedback_response = {
                    "type": "feedback",
                    "score": score,
                    "total_score": total_score,  
                    "feedback": feedback,  
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
        await asyncio.Future() 
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Server stopped by user")
