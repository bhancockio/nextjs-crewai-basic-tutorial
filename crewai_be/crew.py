from agents import CompanyResearchAgents
from tasks import CompanyResearchTasks


class CompanyResearchCrew:
    def __init__(self, company: str, positions: list[str], additional_details: str):
        self.company = company
        self.positions = positions
        self.additional_details = additional_details

        agents = CompanyResearchAgents()
        tasks = CompanyResearchTasks()
