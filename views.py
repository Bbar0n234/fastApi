from fastapi import APIRouter
from schemas import Person, Person_data
from fastapi import Path

from typing import Annotated
import json


def read_data(data_dir="main.json"):
    with open(data_dir, "r") as file:
        data = json.load(file)
    return data


def write_data(data, data_dir="main.json"):
    with open(data_dir, "w") as file:
        json.dump(data, file)


router = APIRouter()


@router.get("/person/{person_id}")
def get_person_by_id(person_id: Annotated[int, Path(gt=0, lt=1_000_000)]):
    data = read_data()

    for person in data:
        if person["id"] == person_id:
            return person

    return f"No person with id {person_id}!"


@router.post("/person/")
def add_person(person: Person):
    person_data = {
        "id": person.id,
        "name": person.name,
        "age": person.age
    }

    data = read_data()
    data.append(person_data)
    write_data(data)

    return person_data


@router.delete("/person/{person_id}")
def del_person_by_id(person_id: Annotated[int, Path(gt=0, lt=1_000_000)]):
    data = read_data()

    for i, person in enumerate(data):
        if person["id"] == person_id:
            data.pop(i)
            write_data(data)
            return person


@router.put("/person/{person_id}")
def upd_person_by_id(person_data: Person_data, person_id: Annotated[int, Path(gt=0, lt=1_000_000)]):
    data = read_data()

    for i, person in enumerate(data):
        if person["id"] == person_id:
            person["name"] = person_data.name
            person["age"] = person_data.age

            data[i] = person
            write_data(data)

            return person


