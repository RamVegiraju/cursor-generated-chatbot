import os
import json
import streamlit as st
import boto3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Claude Sonnet QnA Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Configure AWS credentials
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION", "us-east-1")

# Initialize Bedrock client
def get_bedrock_client():
    return boto3.client(
        service_name="bedrock-runtime",
        region_name=aws_region,
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )

# Function to call Claude model via Bedrock
def call_claude_model(prompt, chat_history=[]):
    bedrock_client = get_bedrock_client()
    
    # Format messages for Claude
    messages = []
    
    # Add chat history to the messages
    for msg in chat_history:
        role = msg["role"]
        content = msg["content"]
        messages.append({"role": role, "content": content})
    
    # Add the current user message
    messages.append({"role": "user", "content": prompt})
    
    # Prepare request payload for Claude
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.9,
    }
    
    # Invoke the Claude model
    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=json.dumps(request_body)
    )
    
    # Parse the response
    response_body = json.loads(response.get('body').read())
    
    return response_body.get('content')[0].get('text')

# Set up the Streamlit app
def main():
    st.title("🤖 Claude Sonnet QnA Chatbot")
    
    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        with st.chat_message(role):
            st.write(content)
    
    # Input for new question
    if prompt := st.chat_input("Ask me anything..."):
        # Add user message to chat
        user_message = {"role": "user", "content": prompt}
        st.session_state.messages.append(user_message)
        
        # Display the user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Show a spinner while waiting for the response
        with st.spinner("Thinking..."):
            try:
                # Get Claude's response
                response_text = call_claude_model(prompt, st.session_state.messages[:-1])
                
                # Add AI response to chat
                assistant_message = {"role": "assistant", "content": response_text}
                st.session_state.messages.append(assistant_message)
                
                # Display the assistant message
                with st.chat_message("assistant"):
                    st.write(response_text)
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.session_state.messages.pop()  # Remove the user message if there was an error

if __name__ == "__main__":
    main() 