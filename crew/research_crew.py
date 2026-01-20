from crewai import Crew, Process
import os
from agents.research_agent import create_research_agent
from agents.analyst_agent import create_analyst_agent
from agents.fact_checker_agent import create_fact_checker_agent
from agents.writer_agent import create_writer_agent
from tasks.research_tasks import create_research_task
from tasks.analysis_tasks import create_analysis_task
from tasks.fact_check_tasks import create_fact_check_task
from tasks.writing_tasks import create_writing_task

class ResearchCrew:
    """
    AI Research Assistant Crew
    Orchestrates multiple agents to conduct comprehensive research.
    """

    def __init__(self, topic: str):
        self.topic = topic
        self.agents = self._create_agents()
        self.tasks = self._create_tasks()
        self.crew = self._create_crew()

    def _create_agents(self):
        """Initialize all agents"""
        return {
            'researcher': create_research_agent(),
            'analyst': create_analyst_agent(),
            'fact_checker': create_fact_checker_agent(),
            'writer': create_writer_agent()
        }
    
    def _create_tasks(self):
        """Initialize all tasks with proper dependencies"""
        research_task = create_research_task(
            self.agents['researcher'],
            topic=self.topic
            )
        
        analysis_task = create_analysis_task(
            agent=self.agents['analyst'],
            research_task=research_task
        )

        fact_check_task = create_fact_check_task(
            agent=self.agents['fact_checker'],
            analysis_task=analysis_task
        )

        writing_task = create_writing_task(
            agent=self.agents['writer'],
            topic=self.topic,
            research_task=research_task,
            analysis_task=analysis_task,
            fact_check_task=fact_check_task
        )

        return {
            'research': research_task,
            'analysis': analysis_task,
            'fact_check': fact_check_task,
            'writing': writing_task
        }
    
    def _create_crew(self): 
        """Create the crew with sequential process"""
        chroma_hf_key = os.getenv("CHROMA_HUGGINGFACE_API_KEY")
        memory_enabled = bool(chroma_hf_key)
        if not memory_enabled:
            print(
                "Note: Crew memory is disabled because CHROMA_HUGGINGFACE_API_KEY is not set. "
                "Set it to enable vector-memory embeddings."
            )

        crew_kwargs = dict(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            process=Process.sequential,
            verbose=True,
            memory=memory_enabled,
        )

        if memory_enabled:
            crew_kwargs["embedder"] = {
                "provider": "huggingface",
                "config": {"model": "sentence-transformers/all-MiniLM-L6-v2"},
            }

        return Crew(
            agents=list(self.agents.values()),
            tasks=list(self.tasks.values()),
            process=Process.sequential,
            verbose=True,
            tracing=True,
            memory=crew_kwargs["memory"],
            **({"embedder": crew_kwargs["embedder"]} if "embedder" in crew_kwargs else {}),
        )
    
    def run(self):
        """
        Execute the research crew
        Returns the final report.
        """
        print(f"\n{'='*80}")
        print(f"Starting AI Research Assistant Crew")
        print(f"Topic: {self.topic}")
        print(f"{'='*80}\n")

        try:
            result = self.crew.kickoff()

            print(f"\n{'='*80}")
            print(f"✅ Research Complete!")
            print(f"{'='*80}\n")
            
            return result
        
        except Exception as e:
            print(f"\n{'='*80}")
            print(f"❌ Error during research: {str(e)}")
            print(f"{'='*80}\n")
            raise
    
    def get_usage_metrics(self):
        """Get token usage and cost metrics."""
        return self.crew.usage_metrics