import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyB67ODMRdgcm0jIAlnoRyS5O-EuRtwm7ew"
genai.configure(api_key=GOOGLE_API_KEY)

def list_gemini_models():
    print("Available Gemini models:")
    for model in genai.list_models():
        print(model)

def get_wikipedia_content(url):
    """Download and extract content from Wikipedia page."""
    response = requests.get(url)
    print("\nRaw HTML (first 1000 chars):\n")
    print(response.text[:1000])
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("\nAll divs with their ids/classes:")
    for div in soup.find_all('div'):
        print(f"div: id={div.get('id')}, class={div.get('class')}")
    
    # Get the main content
    content_div = soup.find('div', {'id': 'mw-content-text'})
    if content_div:
        parser_output = content_div.find('div', class_='mw-parser-output')
        if parser_output:
            text = parser_output.get_text()
            print("\nExtracted article text (first 1000 chars):\n")
            print(text[:1000])
            return text
        else:
            print("No 'mw-parser-output' div found inside 'mw-content-text'.")
            return None
    return None

def analyze_with_gemini(content, model_name):
    """Analyze content with Gemini and extract aircraft/artifacts information."""
    model = genai.GenerativeModel(model_name)
    
    prompt = """
    Please analyze the following Wikipedia content about the Intrepid Museum and create a comprehensive list of all aircraft and other significant artifacts/exhibits mentioned. 
    Format the output as a clear, organized list with categories.
    
    Content:
    {content}
    """
    
    response = model.generate_content(prompt.format(content=content))
    return response.text

def main():
    url = "https://en.wikipedia.org/wiki/Intrepid_Museum"
    
    list_gemini_models()
    
    print("\nDownloading Wikipedia content...")
    content = get_wikipedia_content(url)
    
    if content:
        print("\nAnalyzing content with Gemini...")
        # Try with the most likely model name
        try:
            analysis = analyze_with_gemini(content, "models/gemini-1.5-pro-latest")
            print("\nResults:")
            print(analysis)
        except Exception as e:
            print(f"Gemini analysis failed: {e}")
    else:
        print("Failed to retrieve Wikipedia content")

if __name__ == "__main__":
    main() 