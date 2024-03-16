from typing import List
from crewai import Agent
from langchain_openai import ChatOpenAI
from tools.minimal_web_scrapper import ScrapeWebsiteTool
from tools.youtube_search_tools import YoutubeVideoSearchTool


class CompanyResearchAgents():

    def __init__(self):
        self.scrapeWebsiteTool = ScrapeWebsiteTool()
        self.youtubeSearchTool = YoutubeVideoSearchTool()
        self.llm = ChatOpenAI(model="gpt-4-turbo-preview")

    def research_manager(self, companies: List[str], positions: List[str]) -> Agent:
        return Agent(
            role="Company Research Manager",
            goal=f"""Generate a report containing the urls and titles for 3 blog articles, 3 YouTube interviews, 
                and a URL to a picture of the person for each position in each company.

                How to generate report:
                1. For each company and position, use the results from the Company Research Agent to research each position in each company.
                2. As you find the information, fill in the report with the researched information.
                3. Once you've found all the information, return the report including all companies and all position.
             
                Companies: {companies}
                Positions: {positions}

                Important:
                - The final report must include all companies and positions. Do not leave any out.
                - If you can't find information for a specific position, fill in the information with the word "MISSING".
                - Do not generate fake information. Only return the information you find. Nothing else!
                """,
            backstory="""As a Company Research Manager, you are responsible for aggregating all the researched information
                into a report.""",
            llm=self.llm,
            verbose=True,
        )

    def company_research_agent(self) -> Agent:
        return Agent(
            role="Company Research Agent",
            goal="""Look up the specific positions for a given company and find urls and titles for 3 blog articles, 
                3 YouTube interviews, and a URL to a picture of the person. It is your job to return this collected information in a 
                JSON object""",
            backstory="""As a Company Research Agent, you are responsible for looking up specific positions 
                within a company and gathering relevant information.
                
                Important:
                - Once you've found the information, immediately stop searching for additional information.
                - Only return the requested information. NOTHING ELSE!
                - Do not generate fake information. Only return the information you find. Nothing else!
                - The search tool you are using won't be able to scrape LinkedIn pages. 
                    So, if you find a LinkedIn URL that you think is the right one, stop searching and return it.
                """,
            tools=[self.scrapeWebsiteTool, self.youtubeSearchTool],
            llm=self.llm,
            verbose=True
        )
