from crewai import Agent, LLM
from config.settings import settings
from tools.fact_check_tool import FactCheckTool

def create_fact_checker_agent():
    """
    Creates the Fact-Checker Agent responsible for verifying claims
    """
    llm = LLM(
        model=settings.MODEL_NAME,
        base_url=settings.GROQ_BASE_URL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.3,  # Lower temperature for more factual, consistent checking
        max_tokens=settings.MAX_TOKENS,
    )
    
    return Agent(
        role="Senior Fact-Checker",
        goal="Verify the accuracy of claims and statements by cross-referencing them with reliable sources and identifying any misinformation or inconsistencies",
        backstory=(
            "You are a meticulous fact-checker with an unwavering commitment to truth and accuracy. "
            "With years of experience in journalism and research, you have developed an exceptional ability "
            "to verify information and detect misinformation. You approach every claim with healthy skepticism "
            "and always seek multiple sources for verification. You understand the importance of credible sources "
            "and know how to distinguish between reliable information and speculation. Your work ensures that "
            "only accurate, verified information makes it into the final report. You are thorough, precise, "
            "and take pride in maintaining the highest standards of factual accuracy."
        ),
        tools=[FactCheckTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=10,
        memory=True
    )