from diffusers import StableDiffusionPipeline
import torch
from flask import Flask, request, send_file
from io import BytesIO
# from PIL import Image
import base64
from logging import getLogger, StreamHandler

# ! Do not use in production
LOGGER = getLogger(__name__)
LOGGER.setLevel("DEBUG")
console = StreamHandler()
console.setFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
LOGGER.addHandler(console)


APP = Flask(__name__)
MODEL_ID = "sd-legacy/stable-diffusion-v1-5"
PIPE = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
PIPE = PIPE.to("cuda")


@APP.route("/generate")
def generate():
    """Generate image using the `prompt` field specified in the JSON data"""
    try:
        data = request.get_json(silent=True) or dict()
        if not data or "prompt" not in data:
            return { "error": "prompt not provided" }, 400

        image = PIPE(prompt).images[0]
        img_io = BytesIO()
        image.save(img_io, 'JPEG')
        img_str = base64.b64encode(img_io.getvalue())
        return { "image": img_str, "description": "base64 encoded PNG image" }
    except Exception as e:
        LOGGER.error("Error generating image: %s", str(e), exc_info=e)
        return "Internal Server Error", 500


if __name__ == "__main__":
    APP.run(host="localhost", port=10000, debug=True)
