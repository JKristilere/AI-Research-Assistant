from crewai import Agent, LLM
from config.settings import settings
from tools.web_search_tool import WebSearchTool
from tools.web_scraper_tool import WebScraperTool
from crewai_tools import SerperDevTool


def create_research_agent():
    """
    Creates the Research Agent responsible for gathering information
    """

    llm = LLM(
        model=settings.MODEL_NAME,
        base_url=settings.GROQ_BASE_URL,
        api_key=settings.GROQ_API_KEY,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )

    return Agent(
        role="Senior Research Specialist",
        goal="Conduct comprehensive research on given topics by finding and extracting relevant information from credible sources",
        backstory=(
            "You are an expert research specialist with years of experience in information gathering. "
            "You excel at finding relevant sources, evaluating their credibility, and extracting key information. "
            "You understand the importance of using multiple sources and always verify the reliability of your findings. "
            "You're methodical, thorough, and leave no stone unturned in your research."
        ),
        tools=[WebScraperTool(), 
               WebSearchTool(),
            #    SerperDevTool()
               ],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=15,
        memory=True
    )