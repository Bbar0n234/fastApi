from fastapi import FastAPI

import person_views
from person_views import router as person_router

import model_views
from model_views import router as model_router

from dotenv import dotenv_values

config = dotenv_values(".env")

host = config["HOST"]
user = config["USERNAME"]
password = config["PASSWORD"]
db_name = config["DB_NAME"]

app = FastAPI()
app.include_router(person_router)
app.include_router(model_router)

model_views.__init_model__()
person_views.connect_to_db(host, user, password, db_name)



