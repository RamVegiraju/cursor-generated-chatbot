# Claude Sonnet QnA Chatbot

A Streamlit-based question-answering chatbot powered by Amazon Bedrock's Claude Sonnet model.

## Prerequisites

- Python 3.9 or higher
- AWS account with access to Amazon Bedrock and Claude Sonnet
- AWS credentials with appropriate permissions

## Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure AWS Credentials**

   The app uses a `.env` file to store AWS credentials. This file is already created with your credentials.
   
   ⚠️ **IMPORTANT**: Never commit the `.env` file to version control. It's already included in `.gitignore`.

3. **Run the Application**

   ```bash
   streamlit run app.py
   ```

   The app will be available at http://localhost:8501 in your browser.

## Using the Chatbot

1. Open the app in your browser
2. Type your question in the input box
3. Press Enter to submit
4. The chatbot will process your question and display Claude Sonnet's response

## Security Considerations

- Keep your AWS credentials secure and never share them
- Consider using AWS IAM roles for production deployments
- Regularly rotate your access keys
- Limit the permissions of the AWS user to only what's needed for Amazon Bedrock

## Troubleshooting

- Ensure your AWS credentials have access to Amazon Bedrock
- Check that your AWS region is correctly set in the `.env` file
- Verify that the Claude Sonnet model is available in your AWS region
- Make sure you have the correct permissions to invoke the model 