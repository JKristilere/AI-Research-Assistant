from crewai import Task

def create_fact_check_task(agent, analysis_task):
    """
    Creates a fact-checking task for verifying claims
    """
    return Task(
        description=(
            "Verify the accuracy of key claims and statements from the analysis.\n\n"
            "Your responsibilities:\n"
            "1. Extract major claims and assertions from the analysis\n"
            "2. Use the Fact Verification Tool to cross-check each claim against sources\n"
            "3. Identify any unverified or potentially misleading statements\n"
            "4. Flag contradictions that need resolution\n"
            "5. Assess the overall credibility of the findings\n"
            "6. Provide verification status for each major claim\n"
            "7. Suggest corrections or clarifications where needed\n\n"
            "Focus on:\n"
            "- Factual accuracy of statistics and data\n"
            "- Proper attribution of claims to sources\n"
            "- Consistency of information across sources\n"
            "- Detection of potential misinformation\n"
            "- Verification of expert quotes and statements\n\n"
            "Be thorough but balanced in your assessment."
        ),
        expected_output=(
            "A comprehensive fact-check report containing:\n"
            "- List of verified claims with confidence levels\n"
            "- List of unverified or questionable claims\n"
            "- Specific contradictions that need addressing\n"
            "- Overall credibility score (0-100%)\n"
            "- Recommendations for corrections or clarifications\n"
            "- Summary of verification methodology used\n"
            "- Green-light status (yes/no) for proceeding to final report"
        ),
        agent=agent,
        context=[analysis_task]
    )