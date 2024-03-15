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
                               
                Important:
                - The persons name and linkedin are public information, but the email is not always public.
                    So keep searching until you find the name and email.
                               
                Example Output for companies Tesla and Ford & positions CEO:
                    # Tesla
                    ## CEO
                    - Name: Elon Musk
                    - Email: elon@tesla.com
                    - LinkedIn: Missing
                    # Tesla
                    ## Google
                    - Name: Jim Farley
                    - Email: jfarley@ford.com
                    - LinkedIn: https://www.linkedin.com/in/jim-farley/
                """),
            agent=agent,
            expected_output=dedent(f"""A markdown file containing the researched information for each position in each company.
                                   
                                  
                                """),
            callback=self.append_event_callback,
            context=tasks
        )

    def company_research(self, agent: Agent, company: str, positions: list[str]):
        return Task(
            description=dedent(f"""Research the position {positions} for the {company} company. 
                For each position, find the person's name, public business email, and LinkedIn profile URL.
                Return this collected information in a bulleted list.
                               
                Helpful Tips:
                - To find the information, perform searches on Google such like the following:
                    - "{company} [POSITION HERE] name"
                    - "{company} [POSITION HERE] email address"
                    - "{company} [POSITION HERE] linkedin"
                - Once you find a persons name, you can search for their email and LinkedIn url:
                    - "[NAME HERE] email address"
                    - "[NAME HERE] LinkedIn profile"
                               
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - The persons name and linkedin are public information, but the email is not always public.
                    So keep searching until you find the name and email.

                """),
            agent=agent,
            expected_output=dedent(f"""
                                   
                Bullet list of the researched information for each position in the company.
                                   
                Example Output:
                - Company: [COMPANY NAME]
                    - Position: [Position]
                        - Name: [Name of the person]
                        - Email: [Email address]
                        - LinkedIn: [LinkedIn profile URL]
                """),
            callback=self.append_event_callback
        )
