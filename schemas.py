from pydantic import BaseModel


class Person(BaseModel):
    id: int
    name: str
    age: int


class Person_data(BaseModel):
    name: str
    age: int