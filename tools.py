from elevenlabs.conversational_ai.conversation import ClientTools
from langchain_community.tools import DuckDuckGoSearchRun
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import os
import requests

load_dotenv()  


def searchWeb(parameters):
    """Search the web using DuckDuckGo."""
    query = parameters.get("query")
    if not query:
        return "Error: No query provided."
    try:
        search = DuckDuckGoSearchRun()
        results = search.run(query)
        return results
    except Exception as e:
        return f"Search failed: {e}"


def save_to_txt(parameters):
    """Save text to a file."""
    filename = parameters.get("filename")
    data = parameters.get("data")
    if not filename or data is None:
        return "Error: 'filename' and 'data' are required."
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(str(data) + "\n")
        return f"Saved to {filename} successfully."
    except Exception as e:
        return f"Failed to save file: {e}"


def create_html_file(parameters):
    """Create an HTML file with given title and content."""
    filename = parameters.get("filename")
    data = parameters.get("data")
    title = parameters.get("title", "Untitled")
    if not filename or data is None:
        return "Error: 'filename' and 'data' are required."
    try:
        formatted_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
</head>
<body>
    <h1>{title}</h1>
    <div>{data}</div>
</body>
</html>"""
        with open(filename, "w", encoding="utf-8") as file:
            file.write(formatted_html)
        return f"HTML file '{filename}' created successfully."
    except Exception as e:
        return f"Failed to create HTML file: {e}"


def generate_image(parameters):
    """Generate an image using Pollinations AI (free, no API key needed)."""
    prompt = parameters.get("prompt")
    filename = parameters.get("filename", "generated.png")
    save_dir = parameters.get("save_dir", "generated_images")

    if not prompt:
        return "Error: 'prompt' is required."

    try:
        os.makedirs(save_dir, exist_ok=True)

        if not filename.lower().endswith((".png", ".jpg", ".jpeg")):
            filename += ".png"

        filepath = os.path.join(save_dir, filename)
        print(f"[DEBUG] Saving to: {filepath}")
        
        encoded_prompt = requests.utils.quote(prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true"
        print(f"[DEBUG] Fetching from: {image_url}")

        image_response = requests.get(image_url, timeout=60)
        image_response.raise_for_status()
        print(f"[DEBUG] Downloaded {len(image_response.content)} bytes")

        image = Image.open(BytesIO(image_response.content))
        image.save(filepath)
        print(f"[DEBUG] Image saved to: {filepath}")

        return f"Image saved to {filepath}"

    except requests.RequestException as e:
        print(f"[ERROR] Download failed: {e}")
        return f"Failed to download image: {e}"
    except Exception as e:
        print(f"[ERROR] Unexpected: {e}")
        return f"Image generation failed: {e}"


client_tools = ClientTools()
client_tools.register("searchWeb", searchWeb)
client_tools.register("saveToTxt", save_to_txt)
client_tools.register("createHtmlFile", create_html_file)
client_tools.register("generateImage", generate_image)
