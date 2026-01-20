# AI-Research-Assistant
Multi-agent AI system built with CrewAI that conducts comprehensive research, analyzes findings, verifies facts, and generates professional reports.


## Features
- **Intelligent Research**: Autonomous web searching and content extraction
- **Deep Analysis**: Pattern recognition, insight extraction, and contradiction detection
- **Fact Verification**: Cross-referencing claims against multiple sources
- **Professional Reporting**: Structured, well-cited research reports.
- **Mult-Agent Collaboration**: Four specialized agents working in harmony


## Architecture
### Agents
1. **Research Agent** (`research_agent.py`)
    - Searches the web for the relevant information
    - Scrapes and extracts content from sources
    - Evaluates source credibility

2. **Analyst Agent** (`analyst_agent.py`)
    - Identifies patterns and themes
    - Extract key insights
    - Detects contradictions and inconsistencies

3. **Fact-Checker Agent** (`fact_checker_agent.py`)
    - Verifies claims against sources 
    - Assesses information credibility
    - Flags potential misinformation

4. **Writer Agent** (`writer_agent.py`)
    - Synthesizes all findings
    - Produces structured reports
    - Ensures clarity and professionalism

### Custom Tools

- **WebSearchTool**: DuckDuckGo-based web search
- **WebScraperTool**: Intelligent content extraction
- **AnalysisTool**: Pattern detection and insight extraction
- **FactCheckTool**: Claim verification system

## Quick Run

### Prerequisites

- Python 3.10 or higher
- Groq API key ([Get one here](https://console.groq.com))
- GROQ Base url ([GROQ_BASE_URL](https://api.groq.com/openai/v1))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/ai-research-crew.git
cd ai-research-crew
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GROQ_API_KEY and GROQ_BASE_URL
```

### Usage

**Basic Usage:**
```bash
python main.py
```

The system will prompt you for a research topic and will then:
1. Search the web for relevant sources
2. Analyze the findings
3. Verify all claims
4. Generate a comprehenisive report in `outputs/research_report.md`

**Example topics:**
- "Latest developments in quantum computing"
- "Impact of renewable energy on global economy"
- "Advancements in CRISPR gene editing technology"

## Repo Structure

```
ai-research-crew/
├── config/              # Configuration and settings
│   └── settings.py
├── agents/              # Agent definitions
│   ├── research_agent.py
│   ├── analyst_agent.py
│   ├── fact_checker_agent.py
│   └── writer_agent.py
├── tasks/               # Task definitions
│   ├── research_tasks.py
│   ├── analysis_tasks.py
│   ├── fact_check_tasks.py
│   └── writing_tasks.py
├── tools/               # Custom tools
│   ├── web_search_tool.py
│   ├── web_scraper_tool.py
│   ├── analysis_tool.py
│   └── fact_check_tool.py
├── crew/                # Crew orchestration
│   └── research_crew.py
├── outputs/             # Generated reports
├── main.py              # Entry point
└── requirements.txt
```

## ⚙️ Configuration

Edit `config/settings.py` to customize:

- **Model settings**: Change model, temperature, max tokens
- **Research settings**: Adjust search result limits, scraping timeouts
- **Output settings**: Configure report format and directory

## Advanced Usage

### Programmatic Usage

```python
from crew.research_crew import ResearchCrew

# Create crew
crew = ResearchCrew(topic="Artificial Intelligence in Healthcare")

# Run research
result = crew.run()

# Get metrics
metrics = crew.get_usage_metrics()
print(f"Tokens used: {metrics}")
```

##  Output Format in Markdown

Reports include:
- **Executive Summary**: Key findings overview
- **Introduction**: Background and context
- **Main Findings**: Organized by themes
- **Analysis**: Insights and patterns
- **Contradictions**: Identified inconsistencies
- **Conclusions**: Recommendations and takeaways
- **References**: All sources cited

##  Contributing

Contributions are more than welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

##  Acknowledgments

- Built with [CrewAI](https://github.com/joaomdmoura/crewAI)
- Powered by [Groq](https://groq.com) and Llama 3.3 70B
- Web search via DuckDuckGo API

##  Contact

Your Name - [@JedTheEngineer](https://twitter.com/JedTheEngineer)

Project Link: [https://github.com/JKristilere/AI-Research-Assistant](https://github.com/JKristilere/AI-Research-Assistant)

##  Troubleshooting

**Common issues:**

1. **"GROQ_API_KEY not found"**
   - Ensure `.env` file exists with valid API key

2. **Timeout errors**
   - Increase `SCRAPING_TIMEOUT` in `config/settings.py`

3. **No search results**
   - Try rephrasing your research topic
   - Check internet connection

---

If you find this project useful, please consider giving it a star!