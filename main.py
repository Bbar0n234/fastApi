from fastapi import FastAPI

from person_views import router as person_router

import model_views
from model_views import router as model_router

app = FastAPI()
app.include_router(person_router)
app.include_router(model_router)

model_views.__init_model__()



