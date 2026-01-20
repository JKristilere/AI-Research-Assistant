from crewai import Agent, LLM
from config.settings import settings

def create_writer_agent():
    """
    Creates the Writer Agent responsible for producing the final report
    """
    llm = LLM(
        model=settings.MODEL_NAME,
        base_url=settings.GROQ_BASE_URL,
        api_key=settings.GROQ_API_KEY,
        temperature=0.7,
        max_tokens=settings.MAX_TOKENS,
    )
    
    return Agent(
        role="Expert Technical Writer",
        goal="Create clear, comprehensive, and well-structured research reports that effectively communicate findings to the target audience",
        backstory=(
            "You are a skilled technical writer with a talent for transforming complex research findings "
            "into clear, engaging, and accessible content. You understand how to structure information logically, "
            "highlight key insights, and present data in a way that resonates with readers. Your reports are "
            "known for their clarity, precision, and professional quality. You always cite sources properly "
            "and ensure that your writing is both informative and engaging. You have a gift for taking dense, "
            "technical information and making it understandable without losing its nuance or accuracy."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False,
        max_iter=8,
        memory=True
    )