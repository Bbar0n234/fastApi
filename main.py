from fastapi import FastAPI
# from fastapi.openapi.utils import get_openapi

from views import router as person_router

app = FastAPI()
app.include_router(person_router)
#
# with open("openapi.yaml", "r") as file:
#     api_spec = file.read()
#
#
# def custom_openapi():
#     openapi_schema = get_openapi(
#         title="Your API",
#         version="1.0.0",
#         description="This is the API documentation",
#         routes=app.routes,
#     )
#
#     openapi_schema.update(api_spec)
#
#     app.openapi_schema = openapi_schema
#
#     return app.openapi_schema


