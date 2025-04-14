from pathlib import Path
from typing import Dict

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Demo:
    """Crew for evaluating Android developer candidates"""

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

    @agent
    def resume_screener(self) -> Agent:
        return Agent(
            config=self.agents_config['resume_screener'],
            verbose=True
        )

    @agent
    def evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['evaluator'],
            verbose=True
        )

    @task
    def screen_resume(self) -> Task:
        return Task(
            config=self.tasks_config['screen_resume']
        )

    @task
    def evaluate_candidate(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_candidate']
        )

    @crew
    def crew(self) -> Crew:
        """Create the candidate evaluation crew"""
        return Crew(
            agents=[
                self.resume_screener(),
                self.evaluator()
            ],
            tasks=[
                self.screen_resume(),
                self.evaluate_candidate()
            ],
            verbose=True,
            process=Process.sequential
        )
