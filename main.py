"""
AI Research Assistant using CrewAI
A multi-agent system for comprehensive research and report generation
"""

import os
import sys
from datetime import datetime
from crew.research_crew import ResearchCrew
from config.settings import settings


def ensure_output_directory():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(settings.OUTPUT_DIR):
        os.makedirs(settings.OUTPUT_DIR)
        print(f"Created output directory: {settings.OUTPUT_DIR}")

def get_research_topic():
    """Get research topic from user"""
    print("\n" + "="*80)
    print("🔬 AI Research Assistant Crew")
    print("="*80)
    print("\nThis system will:")
    print("  1. Research your topic using web search")
    print("  2. Analyze findings for insights and contradictions")
    print("  3. Fact-check all claims")
    print("  4. Generate a comprehensive report")
    print("\n" + "-"*80)

    topic = input("\n Enter a research topic: ").strip()

    if not topic:
        print("Error: You need to give a research topic")
        sys.exit(1)
    
    return topic

def display_results(result):
    """Display research results"""
    print("\n" + "="*80)
    print(f"RESEARCH RESULTS:\n {result}")
    print("\n" + "="*80)

def main():
    try:
        ensure_output_directory()

        topic = get_research_topic()

        print(f"\nTopic confirmed: '{topic}'")
        print(f"Starting research... (this may take several minutes)")

        crew = ResearchCrew(topic)
        result = crew.run()

        display_results(result=result)


        try:
            metrics = crew.get_usage_metrics()
            print("\n Usage Metrics:")
            print(f"   {metrics}")
        except:
            pass
    
        report_path = os.path.join(settings.OUTPUT_DIR, "research_report.md")
        if os.path.exists(report_path):
                print(f"\n Report saved to: {report_path}")
            
        print("\nResearch completed successfully!\n")
    
    except KeyboardInterrupt:
        print("\n\n Research interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()