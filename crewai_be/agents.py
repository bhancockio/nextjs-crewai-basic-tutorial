from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.minimal_web_scrapper import ScrapeWebsiteTool


class CompanyResearchAgents():

    def __init__(self):
        self.scrapeWebsiteTool = ScrapeWebsiteTool()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def research_manager(self, companies: List[str], positions: List[str]) -> Agent:
        return Agent(
            role="Company Research Manager",
            goal=f"""Generate a markdown report containing the researched information for each position in each company.
             
                Companies: {companies}
                Positions: {positions}

                Important:
                - The final report must include all companies and positions. Do not leave any out.
                - If you can't find information for a specific position, fill in the information with the word "MISSING".
                """,
            backstory="""As a Company Research Manager, you are responsible for aggregating all the researched information
                into a markdown report.""",
            llm=self.llm,
            verbose=True,
            allow_delegation=True,
            max_iter=7
        )

    def company_research_agent(self) -> Agent:
        return Agent(
            role="Company Research Agent",
            goal="""Look up the specific positions for a given company and the person's name, 
                public business email, and LinkedIn URL. It is your job to return this collected information in a 
                bulleted list""",
            backstory="""As a Company Research Agent, you are responsible for looking up specific positions 
                within a company and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!""",
            tools=[self.scrapeWebsiteTool],
            llm=self.llm,
            verbose=True
        )
