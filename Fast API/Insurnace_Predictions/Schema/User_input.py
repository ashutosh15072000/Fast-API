from pydantic import BaseModel,computed_field,Field,field_validator
from typing import Literal,Annotated
from config.city_tier import tier_1_cities,tier_2_cities
## Pydantic Model to validate incoming date
class UserInput(BaseModel):
    age:Annotated[int,Field(...,gt=0,lt=120,description="Age of the User")]
    weight:Annotated[float,Field(...,gt=0,description="Weight of the User")]
    height:Annotated[float,Field(...,gt=0,lt=2.5,description="Height of the User")]
    income_lpa:Annotated[float,Field(...,gt=0,description="Annual salary of the User in lpa")]
    smoker: Annotated[bool,Field(...,description="IS a User a smoker")]
    city:Annotated[str,Field(...,description="City of the user")]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description="Occupation of th user")]
    
    @field_validator("city")
    @classmethod
    def normalize_city(cls,v:str) -> str:
        v=v.strip().title()
        return v    
    
    
    @computed_field
    @property
    def bmi(self) ->float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk(self) ->str:
        if self.smoker["smoker"] and self.bmi["bmi"] > 30:
            return "high"
        elif self.smoker["smoker"] or self.bmi["bmi"] > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self):
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"

    @computed_field
    @property
    def city_tier(self)-> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3