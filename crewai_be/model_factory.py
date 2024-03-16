from typing import List
from pydantic import BaseModel, Field, validator
from models import CompanyInfo


def create_company_info_list_model(length: int):
    class CompanyInfoList(BaseModel):
        companies: List[CompanyInfo] = Field(...,
                                             min_items=length, max_items=length)

        @validator('companies', each_item=True)
        def check_positions_non_empty(cls, company: CompanyInfo):
            if not company.positions:
                raise ValueError(
                    f"Company {company.company} has no positions listed.")
            return company

    return CompanyInfoList
