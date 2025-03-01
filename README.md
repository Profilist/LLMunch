# LLMunch 🍔
> A Python application that uses voice commands to control YouTube video playback. 

Simply say "Max" followed by what you want to watch, and the AI Agent will do the work while you can enjoy your lunch!

## Features

- Voice-activated YouTube control with "Max" as the trigger word
- Intelligent search query processing using Gemini and Browser Use
- Handles continuous voice commands without needing to restart

## Technology Stack

- **Speech Recognition**: `speech_recognition` with Google Speech-to-Text API
- **Browser Automation**: Browser Use with Playwright and Browser Use
- **AI Processing**: Google Gemini 2.0 Flash Experimental for query optimization
- **Async Operations**: `asyncio` for CPU optimization and non-blocking operations

## Prerequisites

1. Python 3.11 or higher
2. Google Chrome browser installed
3. A microphone for voice input
4. Required environment variables:
   - `CHROME_PATH`: Path to Chrome executable (C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe for Windows)
   - `GEMINI_API_KEY`: Google Gemini API key

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Profilist/LLMunch.git
   cd LLMunch/backend
   ```

2. Activate/create a virtual environment:
   ```bash
   uv venv --python 3.11

   # For Mac/Linux:
   source .venv/bin/activate

   # For Windows:
   .venv\Scripts\activate
   ```

3. Install required packages:
   ```bash
   pip install -r "requirements.txt"
   playwright install
   ```

3. Create a `.env` file in the backend directory with your configuration:
   ```env
   CHROME_PATH=C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe
   GEMINI_API_KEY=your-api-key-here
   ```

## Usage

1. Close all instances of Chrome

2. Run the application:
   ```bash
   python services/agent_test.py
   ```

3. Use voice commands like:
   - "Max play funny cat videos"
   - "Max show me cooking tutorials"
   - "Max I want to watch basketball highlights"

## Project Structure

- `backend/services/agent.py`: Core YouTube service implementation
- `backend/services/agent_test.py`: Voice command interface and main application
- `.env`: Configuration file for API keys and paths

## How It Works

1. The application continuously listens for the trigger word "Max"
2. When detected, it captures the following speech as the video request
3. The Gemini AI processes the request to extract relevant search terms
4. Browser Use automates YouTube to search and play the video
5. The browser context is maintained for seamless video switching

## License

This project is licensed under the MIT License - see the LICENSE file for details.
