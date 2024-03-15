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

    def manage_research(self, agent: Agent, companies: list[str], positions: list[str], tasks: list[Task]):
        return Task(
            description=dedent(f"""Based on the list of companies {companies} and the positions {positions},
                               use the results from the Company Research Agent to research each position in each company.
                               to put together a markdown file containing the researched information for each position in each company.
                               """),
            agent=agent,
            expected_output=dedent(f"""A markdown file containing the researched information for each position in each company.
                                   
                                   Example:
                                    # Company 1
                                    ## Position 1
                                    TODO: Information about the position in a bulleted list
                                """),
            callback=self.append_event_callback,
            context=tasks
        )

    def company_research(self, agent: Agent, company: str, positions: list[str]):
        return Task(
            description=dedent(f"""Research the position {positions} for the {company} company. 
                For each position, find the person's name, email, and LinkedIn profile URL.
                Return this collected information in a bulleted list.       
                """),
            agent=agent,
            expected_output=dedent(f"""
                - Name: [Name of the person]
                - Email: [Email address]
                - LinkedIn: [LinkedIn profile URL]
                """),
            callback=self.append_event_callback
        )
