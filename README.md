# Zania-QA-ChatBOT from PDF

This repository contains a Slack-based chat bot for QA (Question Answering) from a PDF document. The bot allows users to ask questions related to a PDF document uploaded to a Slack channel and provides answers based on the content of the document.

## Requirements

- **Slack Setup**: Follow the instructions provided in [this YouTube tutorial](https://www.youtube.com/watch?v=Luujq0t0J7A) for setting up Slack integration. Ensure that the "OAuth & Permissions>>Scopes>>Bot Token Scopes" has `files.write` and `files.read` access scopes.
- **Slack BOT & APP Key**: Obtain BOT & APP Key from "https://api.slack.com/apps/" for your app.
- **OpenAI API Key**: Obtain an API key from OpenAI.
- **Python**: Ensure Python is installed on your system.
- **Installation**: Install the required Python packages by running `pip install -r requirements.txt`.
- **Update Credentials**: Update the `creds.env` file with the token generated during Slack setup.

## Usage

1. **Setup Slack**: Follow the instructions in the provided YouTube tutorial to set up Slack integration. Ensure the bot token has appropriate permissions.
2. **Start the App**: Run `python app.py` command to start the application.
3. **Ask Questions**: Once the app is running, use the Slack app to ask questions related to the PDF documents.

## Input Requirements

- Provide PDF documents containing the information relevant to the expected questions.
- Questions should be separated by new lines within the Slack chat interface.

## Limitations

- **Chunk Size**: The provided chunk size for processing PDF documents might not always find the most similar content for answering questions. Further fine-tuning of the embedding and chunking techniques may be necessary for improved accuracy.
- **Time**: the time is proportional to document size as the indexing, embedding and chatgpt call happens for every request.
## Demo Video

The complete usage of the app is shown in below video
[Demo Video](https://drive.google.com/file/d/179Gc3Gbv-jUvT7MhqDCGapjfzWvjf56S/view?usp=sharing)

## Notes

- This README provides basic setup and usage instructions. 
- For any issues or improvements, feel free to open an issue or submit a pull request.

## Disclaimer

This project is provided as-is without any warranties. Users are responsible for ensuring compliance with Slack API usage policies and any other relevant terms of service.
