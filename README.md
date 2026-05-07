#  FRIDAY - Personal AI Assistant

## 📌 Project Overview

FRIDAY is a Python-based voice-enabled AI assistant built using ElevenLabs Conversational AI. The assistant integrates multiple custom tools to perform real-world tasks such as web search, file creation, HTML generation, AI image generation, and automated data analysis workflows.

This project serves as a modular foundation for building a more advanced multimodal AI assistant capable of handling intelligent conversations, automation tasks, content generation, and data analytics operations.

---

##  Features

- 🎙️ Real-time Voice Interaction using ElevenLabs
- 🌐 Web Search using DuckDuckGo
- 📝 Text File Saving for notes and outputs
- 💻 HTML File Generation for basic web pages
- 🖼️ AI Image Generation using Pollinations API
- 📊 Automated Data Analysis Workflow
- 🧹 CSV Data Cleaning & Preprocessing
- 📈 Graph & Visualization Generation
- 💾 Export Cleaned CSV Files
- 🖼️ Save Generated Graphs as PNG Files
- 🤖 Conversational AI-based Query Handling
- ⚡ Modular and Extendable Architecture

---

## 📊 Data Analytics Capabilities

FRIDAY now includes a built-in automated data analysis module capable of:

- Loading CSV datasets
- Performing data cleaning
- Handling missing values
- Removing duplicate records
- Generating statistical summaries
- Performing exploratory data analysis (EDA)
- Extracting insights from datasets
- Creating data visualizations and graphs
- Saving cleaned datasets
- Exporting generated graphs as PNG files

This functionality simulates real-world data analyst workflows and demonstrates practical automation using Python.

---

## 🛠️ Tech Stack

- Python
- ElevenLabs Conversational AI
- LangChain Community Tools
- DuckDuckGo Search API
- Pandas
- Matplotlib
- Pillow (PIL)
- python-dotenv
- Requests

---

## 📂 Project Structure

```bash
FRIDAY/
│
├── main.py                     # Main voice assistant entry point
├── tools/                      # Custom tools and utilities
├── output/                     # Saved cleaned CSVs and graph images
├── .env                        # API keys (excluded from repository)
├── requirements.txt            # Project dependencies
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Arc12345/FRIDAY_my_personal_AI_Assistant.git
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

#### Windows
```bash
venv\Scripts\activate
```

#### Linux / Mac
```bash
source venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Configure Environment Variables

Create a `.env` file and add your API keys:

```env
ELEVENLABS_API_KEY=your_key_here
OPENAI_API_KEY=your_key_here
```

---

## ▶️ Usage

Run the assistant:

```bash
python main.py
```

Once started, FRIDAY can:

- Respond to voice queries
- Perform web searches
- Generate HTML content
- Create AI-generated images
- Analyze CSV datasets
- Generate graphs and visualizations
- Save cleaned datasets and reports

---

## 🔄 Workflow

1. User provides voice/text input
2. Assistant processes the request
3. Appropriate tool/module is triggered
4. Data is analyzed or content is generated
5. Output files are saved automatically
6. Results are returned to the user

---

## 📊 Project Highlights

- Voice-enabled AI interaction
- Automated data analysis pipeline
- Real-world task automation
- CSV preprocessing & visualization
- AI-powered assistant architecture
- Modular tool-based design
- Exportable analytics outputs

---

## 🚧 Current Status

This project is currently under active development.

Core functionalities are operational, with additional improvements and advanced AI capabilities planned for future versions.

---

## 🔮 Future Improvements

- Advanced voice interaction
- GUI/Web interface
- Improved reasoning and task execution
- Integration with more APIs and tools
- Real-time automation capabilities
- Advanced analytics dashboards
- AI-powered report generation
- Memory and contextual awareness
- Multimodal AI support

---

## 💡 Skills Demonstrated

- Python Development
- API Integration
- Conversational AI
- Voice AI Systems
- Data Cleaning & Preprocessing
- Exploratory Data Analysis (EDA)
- Data Visualization
- Automation Workflows
- Modular Programming
- AI Tool Development

---

## 🤝 Contributing

Contributions, suggestions, and improvements are welcome.

Feel free to fork the repository, create a new branch, and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Arijit Roy Chowdhury**  
| AI Enthusiast | Data Analytics | 








