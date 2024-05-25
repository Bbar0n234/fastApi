from pydantic import BaseModel, validator


class Person(BaseModel):
    id: int
    name: str
    age: int

    @validator("age")
    def age_must_be_valid(cls, v):
        if v < 0 or v > 200:
            raise ValueError("Age must be between 0 and 200")
        return v

    @validator("id")
    def id_must_be_valid(cls, id):
        if id< 0 or id > 1_000_000:
            raise ValueError("Id must be between 0 and 200")
        return id


class Person_data(BaseModel):
    name: str
    age: int