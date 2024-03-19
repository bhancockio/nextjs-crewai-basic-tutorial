from crewai import Task, Agent
from textwrap import dedent


from job_manager import append_event
from models import PositionInfo, PositionInfoList
from utils.logging import logger


class CompanyResearchTasks():

    def __init__(self, job_id):
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        append_event(self.job_id, task_output.exported_output)

    def manage_research(self, agent: Agent, companies: list[str], positions: list[str], tasks: list[Task]):
        return Task(
            description=dedent(f"""Based on the list of companies {companies} and the positions {positions},
                use the results from the Company Research Agent to research each position in each company.
                to put together a json object containing the URLs for 3 blog articles, the URLs and title 
                for 3 YouTube interviews for each position in each company.
                               
                """),
            agent=agent,
            expected_output=dedent(
                """A json object containing the URLs for 3 blog articles and the URLs and 
                    titles for 3 YouTube interviews for each position in each company."""),
            callback=self.append_event_callback,
            context=tasks,
            output_json=PositionInfoList
        )

    def company_research(self, agent: Agent, company: str, positions: list[str]):
        return Task(
            description=dedent(f"""Research the position {positions} for the {company} company. 
                For each position, 
                               
                               nd the URLs for 3 recent blog articles and the URLs and titles for
                3 recent YouTube interviews for the person in each position.
                Return this collected information in a JSON object.
                               
                Helpful Tips:
                - To find the blog articles names and URLs, perform searches on Google such like the following:
                    - "{company} [POSITION HERE] blog articles"
                - To find the youtube interviews, perform searches on YouTube such as the following:
                    - "{company} [POSITION HERE] interview"
                               
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Do not generate fake information. Only return the information you find. Nothing else!
                - Do not stop researching until you find the requested information for each position in the company.
                """),
            agent=agent,
            expected_output="""A JSON object containing the researched information for each position in the company.""",
            callback=self.append_event_callback,
            output_json=PositionInfo,
            async_execution=True
        )
