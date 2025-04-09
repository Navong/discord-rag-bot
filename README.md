# Discord PDF Q&A Bot

This is a Discord bot that allows users to upload PDF documents, ask questions about the content, and receive accurate, context-aware answers. The bot leverages advanced natural language processing and document embedding techniques to provide a seamless experience.

## Overview

The bot is designed to streamline document-based Q&A within Discord. It extracts text from uploaded PDFs, generates embeddings for efficient storage and retrieval, and processes user queries to deliver relevant responses. The project integrates cutting-edge technologies like LangChain for workflow orchestration, Open AI for text embedding and answer generation, and Chroma for managing document embeddings.

### Workflow Diagram

![alt text](/file/image.png)


### Demo Video

![alt text](file/demo.gif)

## Features

- **PDF Upload**: Users can upload PDF documents directly to the bot via Discord.
- **Question Answering**: Ask questions about the uploaded PDFs and receive context-aware answers.
- **Text Extraction**: Automatically extracts text from PDFs for processing.
- **Embedding Generation**: Uses Open AI to create embeddings for efficient document search.
- **Vector Storage**: Stores embeddings in Chroma for fast retrieval of relevant text chunks.
- **Discord Integration**: Fully integrated with the Discord API for a smooth user experience.

## Tech Stack

- **LangChain**: Workflow orchestration and natural language processing.
- **Open AI**: Text embedding and answer generation.
- **Chroma**: Efficient storage and retrieval of document embeddings.
- **Discord API**: Interaction with Discord for bot functionality.
- **Python**: Core programming language for development.

## Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Discord Bot Token (create via [Discord Developer Portal](https://discord.com/developers/applications))
- Open AI API Key
- Grok API Key (optional, if used)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/Navong/discord-rag-bot.git
cd discord-rag-bot
```

### 2. Install Dependencies
Create a virtual environment and install requirements:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a .env file in the root directory:

```bash
DISCORD_BOT_TOKEN=your_discord_bot_token
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_grok_api_key  # Optional
```

### 4. Run Locally

```bash
python bot.py
```

### Usage
1. Invite the Bot: Add the bot to your Discord server using its invite link (generate this from the Discord Developer Portal after creating your bot).
2. Upload a PDF: Use the `/updatedb` command to upload a PDF file in a channel where the bot is active.
3. The bot saves the latest PDF to `./latest/latest.pdf`.
4. Ask Questions: Use the `/query` command followed by your question to interact with the bot and get answers based on the uploaded PDF content.
### Example:
- Type: `/updatedb` and attach document.pdf when prompted.
- Type: `/query` "What are the key points?"
- Bot responds with relevant answers extracted from document.pdf.

