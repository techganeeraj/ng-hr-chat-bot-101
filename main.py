from dialogflow_client import DialogflowClient
import uuid

def main():
    # Create an instance of the DialogflowClient
    client = DialogflowClient()
    
    # Generate a random session ID
    session_id = str(uuid.uuid4())
    
    print("Chat started! (Type 'quit' to exit)")
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        if user_input.lower() == 'quit':
            break
            
        try:
            # Detect intent
            response = client.detect_intent(user_input, session_id)
            
            # Get the response text
            bot_response = client.get_response_text(response)
            
            # Print the response
            print(f"Bot: {bot_response}")
            
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 