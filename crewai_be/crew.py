from datetime import datetime
from typing import Callable
from langchain_openai import ChatOpenAI
from agents import CompanyResearchAgents
from tasks import CompanyResearchTasks
from crewai import Crew, Process

from dotenv import load_dotenv
load_dotenv()


class CompanyResearchCrew:
    def __init__(self, job_id: str, append_event: Callable[[str, str], None], companies: list[str], positions: list[str], additional_details: str):
        self.job_id = job_id
        self.append_event = append_event
        self.companies = companies
        self.positions = positions
        self.additional_details = additional_details

        self.manager_llm = ChatOpenAI(
            model="gpt-4-turbo-preview"
        )

        agents = CompanyResearchAgents()
        tasks = CompanyResearchTasks(
            append_event=self.append_event, job_id=self.job_id)

        # Define agents
        self.research_manager = agents.research_manager(
            companies, positions, additional_details)
        self.company_research_agent = agents.company_research_agent()

        # Define tasks
        company_research_tasks = []
        for company in companies:
            company_research_tasks.append(
                tasks.company_research(
                    self.company_research_agent, company, positions)
            )

        self.manage_research_task = tasks.manage_research(
            self.research_manager, companies, positions, additional_details)

        # Setup Crew
        self.crew = Crew(
            agents=[self.research_manager, self.company_research_agent],
            tasks=[self.manage_research_task, *company_research_tasks],
            process=Process.hierarchical,
            manager_llm=self.manager_llm
        )

    def kickoff(self):
        self.append_event(self.job_id, "Task Started")
        results = self.crew.kickoff()
        self.append_event(self.job_id, "Task Complete")
        return results
