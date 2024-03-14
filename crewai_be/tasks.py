from crewai import Task, Agent
from textwrap import dedent

from utils.logging import logger


class CompanyResearchTasks():

    def __init__(self, append_event, job_id):
        self.append_event = append_event
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        self.append_event(self.job_id, task_output.exported_output)

    def manage_research(self, agent: Agent, companies: list[str], positions: list[str], additional_details: str):
        return Task(
            description=dedent(f"""Manage the research process for the following companies {companies}, focusing on the positions {positions}. 
                Gather information as per the additional details: {additional_details}. 
                Delegate tasks to the Company Research Agent to look up each position for one company at a time."""),
            agent=agent,
            expected_output=dedent(f"""A comprehensive report containing the researched information for each position in each company
                """),
            callback=self.callback
        )

    def company_research(self, agent: Agent, company: str, positions: list[str]):
        return Task(
            description=dedent(f"""Research the position {positions} for the {company} company. 
                Gather information such as name, email, and LinkedIn profile, and return this collected information in a bulleted list.       
                """),
            agent=agent,
            expected_output=dedent(f"""
                - Name: [Name of the person]
                - Email: [Email address]
                - LinkedIn: [LinkedIn profile URL]
                """),
            callback=self.append_event_callback
        )
