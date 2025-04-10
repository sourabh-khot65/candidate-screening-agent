from pathlib import Path
from typing import Dict

from crewai import Agent, Crew, Process, Task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

class Demo:
    """
    A demo crew for screening candidates based on their resumes.
    """

    def __init__(self):
        """Initialize the demo crew."""
        self.config_path = Path(__file__).parent / "config"
        self.agents_config = self._load_yaml(self.config_path / "agents.yaml")
        self.tasks_config = self._load_yaml(self.config_path / "tasks.yaml")

    def _load_yaml(self, path: Path) -> Dict:
        """Load YAML configuration file."""
        import yaml
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def crew(self) -> Crew:
        """
        Create and return a crew for candidate screening.
        
        Returns:
            Crew: A configured crew instance
        """
        # Create agents
        resume_analyzer = Agent(
            role=self.agents_config["resume_analyzer"]["role"],
            goal=self.agents_config["resume_analyzer"]["goal"],
            backstory=self.agents_config["resume_analyzer"]["backstory"],
            verbose=True
        )
        
        screening_decision_maker = Agent(
            role=self.agents_config["screening_decision_maker"]["role"],
            goal=self.agents_config["screening_decision_maker"]["goal"],
            backstory=self.agents_config["screening_decision_maker"]["backstory"],
            verbose=True
        )

        # Create tasks
        analyze_config = self.tasks_config["analyze_resume"].copy()
        analyze_task = Task(
            description=analyze_config["description"],
            expected_output=analyze_config["expected_output"],
            agent=resume_analyzer
        )
        
        decision_config = self.tasks_config["make_screening_decision"].copy()
        decision_task = Task(
            description=decision_config["description"],
            expected_output=decision_config["expected_output"],
            agent=screening_decision_maker,
            context=[analyze_task]
        )

        # Create and return the crew
        return Crew(
            agents=[resume_analyzer, screening_decision_maker],
            tasks=[analyze_task, decision_task],
            process=Process.sequential,
            verbose=True
        )
