import os
import google.generativeai as genai
from fpdf import FPDF
import json

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyB67ODMRdgcm0jIAlnoRyS5O-EuRtwm7ew"
genai.configure(api_key=GOOGLE_API_KEY)

def create_information_directory():
    """Create the information directory if it doesn't exist."""
    if not os.path.exists("information"):
        os.makedirs("information")

def generate_object_info(object_name):
    """Generate detailed information about an object using Gemini."""
    model = genai.GenerativeModel("models/gemini-1.5-pro-latest")
    
    prompt = f"""
    Please provide a detailed technical analysis of the {object_name} from the Intrepid Museum. Focus on the following aspects:

    1. Design and Engineering:
       - Innovative design features and their purpose
       - Materials used and their significance
       - Engineering challenges overcome
       - Unique technical solutions implemented

    2. Technical Specifications:
       - Detailed performance characteristics
       - Powerplant/engine details
       - Structural design elements
       - Avionics and systems (if applicable)
       - Dimensions and weight specifications

    3. Historical Technical Context:
       - How this design compared to contemporary aircraft/vehicles
       - Technical innovations that made it unique
       - Design evolution and modifications
       - Impact on future designs

    4. Operational Technical Details:
       - Maintenance requirements
       - Operational limitations
       - Technical challenges in service
       - Notable technical achievements

    5. Current Technical State:
       - Current condition and preservation status
       - Technical modifications for museum display
       - Notable technical features visible to visitors

    Please format the response with clear sections and bullet points where appropriate. Focus on technical details that would be interesting to engineering and aviation enthusiasts.
    """
    
    response = model.generate_content(prompt)
    return response.text

def create_pdf(object_name, content):
    """Create a PDF with the object information."""
    pdf = FPDF()
    pdf.add_page()
    
    # Add DejaVu font for Unicode support
    pdf.add_font('DejaVu', '', '/System/Library/Fonts/Supplemental/Arial Unicode.ttf', uni=True)
    
    # Add title
    pdf.set_font('DejaVu', '', 16)
    pdf.cell(0, 10, f"{object_name} - Intrepid Museum", ln=True, align="C")
    pdf.ln(10)
    
    # Add content
    pdf.set_font('DejaVu', '', 12)
    
    # Split content into lines and add to PDF
    for line in content.split('\n'):
        # Handle bullet points
        if line.strip().startswith('•'):
            pdf.ln(5)
            pdf.multi_cell(0, 10, line)
        else:
            pdf.multi_cell(0, 10, line)
    
    # Save PDF
    safe_filename = object_name.replace(" ", "_").replace("/", "_")
    pdf_path = os.path.join("information", f"{safe_filename}.pdf")
    pdf.output(pdf_path)
    return pdf_path

def main():
    # Create information directory
    create_information_directory()
    
    # List of objects to process
    objects = [
        "A-12 Blackbird",
        "Concorde",
        "Space Shuttle Enterprise",
        "Grumman F-14 Tomcat",
        "Grumman F-11 Tiger",
        "Grumman TBF Avenger",
        "Lockheed A-12",
        "McDonnell Douglas F-4 Phantom II",
        "MiG-15",
        "MiG-21",
        "North American FJ-3 Fury",
        "North American T-2C Buckeye",
        "Vought A-7 Corsair II"
    ]
    
    print("Generating PDFs for each object...")
    for object_name in objects:
        print(f"\nProcessing {object_name}...")
        try:
            # Generate information
            content = generate_object_info(object_name)
            
            # Create PDF
            pdf_path = create_pdf(object_name, content)
            print(f"Created PDF: {pdf_path}")
            
        except Exception as e:
            print(f"Error processing {object_name}: {e}")

if __name__ == "__main__":
    main() 