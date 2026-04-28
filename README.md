# FRIDAY_my_personal_AI_Assistant
FRIDAY is a Python-based voice-enabled AI assistant built using ElevenLabs Conversational AI. It integrates custom tools to perform real-world tasks such as web search, file creation, HTML generation, and image generation.

This project serves as a modular foundation for building a more advanced, multimodal AI assistant.



 -Features-
 --Real-time Voice Interaction using ElevenLabs
 --Web Search via DuckDuckGo
 --Text File Saving (notes, outputs, etc.)
 --HTML File Generation (basic web pages)
 --AI Image Generation using Pollinations API
 --General Query Handling through conversational AI
-Tech Stack-
--Python
--ElevenLabs Conversational AI
--LangChain Community Tools (DuckDuckGo Search)
--Pillow (PIL) – image processing
--python-dotenv – environment management
--Requests – API calls

-FRIDAY/
│── main.py                                    # Voice assistant entry point (handles conversation lifecycle)
│── tools/                                     # Custom tools (search, file handling, HTML, image generation)
│── .env                                       # API keys (not included in repo)
│── requirements.txt                           # Dependencies
│── README.md

-INSTALLATION
--Clone the repository
git clone https://github.com/Arc12345/FRIDAY.git
cd FRIDAY

--Create a virtual environment
python -m venv venv
venv\Scripts\activate

--Install dependencies
pip install -r requirements.txt

--Set up environment variables
Create a .env file and add your API keys:
ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here

 Usage

Run the assistant:

python main.py

Once started, FRIDAY can:

Respond to queries
Generate HTML content
Create simple plans and images
Interact via voice (if configured)

--Current Status

This project is in an early development stage.
Features are basic and may not be fully stable or optimized.

--Future Improvements
Advanced voice interaction
GUI/Web interface
Better reasoning and task execution
Integration with more APIs and tools
Real-time automation capabilities

--Contributing

Contributions are welcome!
Feel free to fork the repo, create a branch, and submit a pull request.

--License

This project is licensed under the MIT License.

--Acknowledgements

Developed with assistance from Claude.








