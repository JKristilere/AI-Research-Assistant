from crewai import Task


def create_research_task(agent, topic: str):
    """
    Create a research task for gathering information on a topic.
    """

    return Task(
        description=(
            f"Conduct comprehensive research on the following topic: '{topic}'\n\n"
            "Your responsibilities:\n"
            "1. Use the Web Search Tool to find relevant and credible sources\n"
            "2. Identify at least 5-7 high-quality sources covering different aspects of the topic\n"
            "3. Use the Web Scraper Tool to extract detailed content from each source\n"
            "4. Evaluate the credibility and relevance of each source\n"
            "5. Organize the gathered information systematically\n"
            "6. Note the URL, title, and key points from each source\n\n"
            "Focus on:\n"
            "- Recent and up-to-date information\n"
            "- Authoritative and credible sources\n"
            "- Diverse perspectives on the topic\n"
            "- Factual data, statistics, and expert opinions\n\n"
            "Provide a structured summary of your findings with source citations."
        ),
        expected_output=("A comprehensive research summary in JSON format containing:\n"
            "- List of sources with URLs, titles, and credibility ratings\n"
            "- Key findings and main points from each source\n"
            "- Relevant statistics, data, and expert quotes\n"
            "- Brief overview of different perspectives found\n"
            "- Total word count and number of sources analyzed"
            ),
        agent=agent
        )