# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import io

from extractor import extract_lab_tests_from_image

app = FastAPI()

@app.post("/get-lab-tests")
async def get_lab_tests(file: UploadFile = File(...)):
    try:
        # read the uploaded bytes and open as a PIL image
        contents = await file.read()
        img = Image.open(io.BytesIO(contents))

        # run the extractor
        tests = extract_lab_tests_from_image(img)

        return JSONResponse(content={"is_success": True, "data": tests})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"is_success": False, "error": str(e)}
        )
