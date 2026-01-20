from crewai import Task

def create_analysis_task(agent, research_task):
    """
    Creates an analysis task for examining research findings
    """

    return Task(
        description=(
            "Analyze the research findings provided by the Research Agent.\n\n"
            "Your responsibilities:\n"
            "1. Use the Content Analysis Tool to examine all gathered sources\n"
            "2. Identify common themes and patterns across sources\n"
            "3. Extract key insights and main arguments\n"
            "4. Detect any contradictions or inconsistencies between sources\n"
            "5. Evaluate the strength and quality of evidence presented\n"
            "6. Identify gaps in the research or areas needing further investigation\n"
            "7. Synthesize findings into coherent categories\n\n"
            "Focus on:\n"
            "- Patterns and trends in the data\n"
            "- Areas of consensus vs. disagreement among sources\n"
            "- Quality and reliability of information\n"
            "- Logical connections and relationships between concepts\n"
            "- Potential biases or limitations in sources\n\n"
            "Provide an analytical report highlighting your findings."
        ),
        expected_output=(
            "A detailed analytical report containing:\n"
            "- Key themes and patterns identified (5-10 themes)\n"
            "- Main insights extracted from the research\n"
            "- List of contradictions or inconsistencies found\n"
            "- Assessment of source quality and reliability\n"
            "- Identified gaps or areas for further research\n"
            "- Recommendations for the writing phase\n"
            "- Confidence score for the overall research quality"
        ),
        agent=agent,
        context=[research_task]
        )