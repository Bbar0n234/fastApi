from fastapi import APIRouter
from schemas import Person, Person_data
from fastapi import Path

from typing import Annotated
import json

import psycopg2


def connect_to_db(host, user, password, db_name):
    global connection
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=db_name
    )
    connection.autocommit = True


def select_person_and_fetch(cursor, person_id):
    cursor.execute(
        f"SELECT * FROM users WHERE id = {person_id};"
    )

    return cursor.fetchone()


router = APIRouter(prefix="/person", tags=["Persons"])


@router.get("/{person_id}")
def get_person_by_id(person_id: Annotated[int, Path(gt=0, lt=1_000_000)]):
    with connection.cursor() as cursor:

        result = select_person_and_fetch(cursor, person_id)

        if result is None:
            return f"No person with id {person_id}!"
        else:
            result_dict = {}
            columns = [column[0] for column in cursor.description]

            for i, value in enumerate(result):
                result_dict.update({columns[i]: value})

            return result_dict


@router.post("/")
def add_person(person: Person):
    with connection.cursor() as cursor:
        person_id = person.id

        cursor.execute(
            f"INSERT INTO users (id, name, age) VALUES {tuple(vars(person).values())};"
        )

        result = select_person_and_fetch(cursor, person_id)

        if result is None:
            return f"Error with adding person!"
        else:
            result_dict = {}
            columns = [column[0] for column in cursor.description]

            for i, value in enumerate(result):
                result_dict.update({columns[i]: value})

            return result_dict


@router.delete("/{person_id}")
def del_person_by_id(person_id: Annotated[int, Path(gt=0, lt=1_000_000)]):
    with connection.cursor() as cursor:

        cursor.execute(
            f"DELETE FROM users WHERE id = {person_id};"
        )

        result = select_person_and_fetch(cursor, person_id)

        if result is None:
            return "Person del successfully"
        else:
            return "Error with del"


@router.put("/{person_id}")
def upd_person_by_id(person_data: Person_data, person_id: Annotated[int, Path(gt=0, lt=1_000_000)]):
    with connection.cursor() as cursor:
        cursor.execute(
            f"UPDATE users SET name = \'{person_data.name}\', age = {person_data.age} WHERE id = {person_id};"
        )

        result = select_person_and_fetch(cursor, person_id)

        result_dict = {}
        columns = [column[0] for column in cursor.description]

        for i, value in enumerate(result):
            result_dict.update({columns[i]: value})

        return result_dict
