from crewai import Agent, LLM
from config.settings import settings
from tools.analysis_tool import AnalysisTool

def create_analyst_agent():
    """
    Creates the Analyst Agent responsible for analyzing research findings
    """
    llm = LLM(
        model=settings.MODEL_NAME,
        base_url=settings.GROQ_BASE_URL,
        api_key=settings.GROQ_API_KEY,
        temperature=settings.TEMPERATURE,
        max_tokens=settings.MAX_TOKENS,
    )
    
    return Agent(
        role="Senior Data Analyst",
        goal="Analyze research findings to extract meaningful insights, identify patterns, and detect contradictions or inconsistencies",
        backstory=(
            "You are a brilliant data analyst with expertise in critical thinking and pattern recognition. "
            "You have a keen eye for detail and can spot inconsistencies, contradictions, and hidden connections "
            "that others might miss. You excel at synthesizing information from multiple sources and extracting "
            "actionable insights. Your analytical skills are second to none, and you always approach data with "
            "a skeptical but fair mindset, questioning assumptions and verifying conclusions."
        ),
        tools=[AnalysisTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=10,
        memory=True
    )