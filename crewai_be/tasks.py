from crewai import Task, Agent
from textwrap import dedent


from models import PositionInfo
from model_factory import create_company_info_list_model
from utils.logging import logger


class CompanyResearchTasks():

    def __init__(self, append_event, job_id):
        self.append_event = append_event
        self.job_id = job_id

    def append_event_callback(self, task_output):
        logger.info("Callback called: %s", task_output)
        self.append_event(self.job_id, task_output.exported_output)

    def manage_research(self, agent: Agent, companies: list[str], positions: list[str], tasks: list[Task]):
        model = create_company_info_list_model(len(companies))
        return Task(
            description=dedent(f"""Based on the list of companies {companies} and the positions {positions},
                use the results from the Company Research Agent to research each position in each company.
                to put together a report containing the URLs and titles for 3 blog articles, 3 YouTube interviews, 
                and a URL to a picture of the person for each position in each company.
                               
                Important:
                - The persons name and linkedin are public information, but the email is not always public.
                    So keep searching until you find the name and email.
                """),
            agent=agent,
            expected_output=dedent(
                "A report containing the URLs and titles for 3 blog articles, 3 YouTube interviews, and a URL to a picture of the person for each position in each company."),
            callback=self.append_event_callback,
            context=tasks,
            output_json=model
        )

    def company_research(self, agent: Agent, company: str, positions: list[str]):
        return Task(
            description=dedent(f"""Research the position {positions} for the {company} company. 
                For each position, find the URLs and titles for 3 blog articles, 3 YouTube interviews, and a URL to a picture of the person.
                Return this collected information in a JSON object.
                               
                Helpful Tips:
                - To find the blog article and picture URLs, perform searches on Google such like the following:
                    - "{company} [POSITION HERE] blog articles"
                    - "{company} [POSITION HERE] picture"
                - To find the youtube interviews, perform searches on YouTube such as the following:
                    - "{company} [POSITION HERE] interview"
                               
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Do not generate fake information. Only return the information you find. Nothing else!
                """),
            agent=agent,
            expected_output="""A JSON object containing the researched information for each position in the company.""",
            callback=self.append_event_callback,
            output_json=PositionInfo,
        )
