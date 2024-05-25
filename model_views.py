from fastapi import APIRouter
from fastapi import File, UploadFile
from ml.model import ModelInterface, BaseLineModel, idx_to_cls_dict
from PIL import Image

from io import BytesIO

WEIGHTS_PATH = "./ml/baseline_model_weights.pth"

__all__ = (
    "router",
    "__init_model__"
)

router = APIRouter(prefix="/model", tags=["Model"])


@router.post("/")
async def predict_image(image: UploadFile = File(...)):
    contents = await image.read()

    input_image = Image.open(BytesIO(contents))

    return model.predict(input_image)


def __init_model__():
    global model
    model = ModelInterface(BaseLineModel, weights_path=WEIGHTS_PATH, idx_to_cls_dict=idx_to_cls_dict)