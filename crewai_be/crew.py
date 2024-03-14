from datetime import datetime
from typing import Callable
from langchain_openai import ChatOpenAI
from agents import CompanyResearchAgents
from tasks import CompanyResearchTasks
from crewai import Crew, Process


class CompanyResearchCrew:
    def __init__(self, job_id: str, append_event: Callable[[str, str], None]):
        self.job_id = job_id
        self.append_event = append_event
        self.crew = None
        self.manager_llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def setup_crew(self, companies: list[str], positions: list[str], additional_details: str):
        agents = CompanyResearchAgents()
        tasks = CompanyResearchTasks(
            append_event=self.append_event, job_id=self.job_id)

        research_manager = agents.research_manager(
            companies, positions, additional_details)
        company_research_agent = agents.company_research_agent()

        company_research_tasks = [
            tasks.company_research(company_research_agent, company, positions)
            for company in companies
        ]

        manage_research_task = tasks.manage_research(
            research_manager, companies, positions, additional_details)

        self.crew = Crew(
            agents=[research_manager, company_research_agent],
            tasks=[manage_research_task, *company_research_tasks],
            process=Process.hierarchical,
            manager_llm=self.manager_llm
        )

    def kickoff(self):
        if not self.crew:
            self.append_event(self.job_id, "Crew not set up")
            return "Crew not set up"

        self.append_event(self.job_id, "Task Started")
        try:
            results = self.crew.kickoff()
            self.append_event(self.job_id, "Task Complete")
            return results
        except Exception as e:
            self.append_event(self.job_id, f"An error occurred: {e}")
            return str(e)
