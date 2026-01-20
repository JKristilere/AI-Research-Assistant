from crewai import Task

def create_writing_task(agent, topic: str, research_task, analysis_task, fact_check_task):
    """
    Creates a writing task for producing the final report
    """
    return Task(
        description=(
            f"Create a comprehensive, well-structured research report on: '{topic}'\n\n"
            "Your responsibilities:\n"
            "1. Synthesize all verified findings from research, analysis, and fact-checking\n"
            "2. Structure the report with clear sections and logical flow\n"
            "3. Present information in an accessible yet professional manner\n"
            "4. Include proper citations and source attributions\n"
            "5. Highlight key insights and main conclusions\n"
            "6. Address any contradictions or uncertainties transparently\n"
            "7. Provide actionable takeaways or recommendations\n\n"
            "Report structure should include:\n"
            "- Executive Summary (2-3 paragraphs)\n"
            "- Introduction and Background\n"
            "- Main Findings (organized by themes)\n"
            "- Analysis and Insights\n"
            "- Contradictions or Limitations (if any)\n"
            "- Conclusions and Recommendations\n"
            "- Sources and References\n\n"
            "Writing guidelines:\n"
            "- Clear, professional, and engaging tone\n"
            "- Logical progression of ideas\n"
            "- Proper use of headings and subheadings\n"
            "- Evidence-based statements with citations\n"
            "- Balanced presentation of different perspectives"
        ),
        expected_output=(
            "A complete research report in Markdown format with:\n"
            "- Title and metadata (date, topic, word count)\n"
            "- Executive summary (150-250 words)\n"
            "- Full report body (1500-2500 words)\n"
            "- Clear section headings and structure\n"
            "- Inline citations in [Source Name](URL) format\n"
            "- Key insights highlighted\n"
            "- Comprehensive reference list\n"
            "- Professional formatting and readability"
        ),
        agent=agent,
        context=[research_task, analysis_task, fact_check_task],
        output_file=f"outputs/{topic}_research_report.md"
    )