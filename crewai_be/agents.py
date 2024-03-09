from crewai import Agent
from crewai_tools import ScrapeWebsiteTool


class CompanyResearchAgents():

    def __init__(self):
        self.scrapeWebsiteTool = ScrapeWebsiteTool()

    def research_manager(self, companies, positions, additional_details):
        return Agent(
            role="Company Research Manager",
            goal=f"""For each company in the list {companies}, research the specified positions {positions} 
                and gather information as per the additional details: {additional_details}.""",
            backstory="""As a Company Research Manager, you are responsible for overseeing the research process 
                to gather information on specific positions within a list of companies. You delegate tasks to 
                the Company Research Agent to look up each position for one company at a time.""",
            verbose=True,
            allow_delegation=True,
        )

    def company_research_agent(self):
        return Agent(
            role="Company Research Agent",
            goal="""Look up the specific positions for a given company and gather information such as name, 
                email, and LinkedIn profile. It is your job to return this collected information in a 
                bulleted list""",
            backstory="""As a Company Research Agent, you are responsible for looking up specific positions 
                within a company and gathering relevant information.""",
            tools=[self.scrapeWebsiteTool],
            verbose=True
        )
