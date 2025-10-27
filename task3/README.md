## Server for requests to Stable Diffusion 1.5

## Installation

```
pip install -r requirements.txt
```

## Usage Example

1. Run the server with command: python stable-diffusion/stable_diffusion.py
2. Use cURL to get generated b64encoded JPEG image, e.g.:
```
curl -H "Content-Type: application/json" -d '{"prompt": "Space background, stars, the Moon surface, the austronaut, lunar station, country flag"}' --output "austronaut.png" http://localhost:10000/generate
```
3. base64 -d austronaut.png > austronaut.png
