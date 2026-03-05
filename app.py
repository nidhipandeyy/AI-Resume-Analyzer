from flask import Flask, render_template, request, send_file, jsonify
import google.generativeai as genai
import os
from fpdf import FPDF
from dotenv import load_dotenv
import re

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configure Gemini AI
# Try both API key names for compatibility
api_key = os.getenv('GOOGLE_API_KEY') or os.getenv('API_KEY')
if not api_key:
    print("Warning: API_KEY not found in environment variables")
    print("Please set GOOGLE_API_KEY or API_KEY in your .env file")

# Configure the API with proper error handling
try:
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully")
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

class PDF(FPDF):
    def header(self):
        # Set font for header
        self.set_font('Arial', 'B', 16)
        # Move to the right
        self.cell(80)
        # Title
        self.cell(30, 10, 'PROFESSIONAL RESUME', 0, 0, 'C')
        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Arial italic 8
        self.set_font('Arial', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')

    def chapter_title(self, label):
        # Arial 12
        self.set_font('Arial', 'B', 12)
        # Background color
        self.set_fill_color(200, 220, 255)
        # Title
        self.cell(0, 6, label, 0, 1, 'L', 1)
        # Line break
        self.ln(4)

    def chapter_body(self, body):
        # Times 12
        self.set_font('Times', '', 12)
        # Output justified text
        self.multi_cell(0, 5, body)
        # Line break
        self.ln()

    def add_chapter(self, title, body):
        self.chapter_title(title)
        self.chapter_body(body)

@app.route('/')
def index():
    """Render the home page with the form"""
    # Always pass results as empty list for GET requests
    return render_template('index.html', results=[])

@app.route('/generate', methods=['POST'])
def generate_resume():
    """Generate resume and related documents using Gemini AI"""
    try:
        # Get form data safely with default values
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        phone = request.form.get('phone', '')
        skills = request.form.get('skills', '')
        education = request.form.get('education', '')
        projects = request.form.get('projects', '')
        experience = request.form.get('experience', '')
        career_objective = request.form.get('career_objective', '')
        target_role = request.form.get('target_role', '').strip()
        
        # Validate required fields
        if not target_role:
            return render_template('result.html', results=[], error="Please select a target job/role from the dropdown menu.")
        
        if not name or not email or not phone or not skills or not education or not projects or not experience or not career_objective:
            return render_template('result.html', results=[], error="Please fill in all required fields before generating your resume.")

        # Combine all inputs into formatted profile data
        profile_data = f"""
FULL NAME: {name}
EMAIL: {email}
PHONE: {phone}
TARGET JOB ROLE: {target_role}
SKILLS: {skills}
EDUCATION: {education}
PROJECTS: {projects}
EXPERIENCE: {experience}
CAREER OBJECTIVE: {career_objective}
"""

        # Initialize Gemini model with latest supported model
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            print("Gemini model initialized successfully")
        except Exception as model_error:
            print(f"Error initializing model: {model_error}")
            # Fallback to older model if needed
            try:
                model = genai.GenerativeModel("gemini-pro")
                print("Using fallback gemini-pro model")
            except Exception as fallback_error:
                raise Exception(f"Failed to initialize any Gemini model: {fallback_error}")

        # Generate Resume with proper error handling
        try:
            resume_prompt = f"Create a professional resume for a {target_role} position using this profile:\n{profile_data}"
            resume_response = model.generate_content(resume_prompt)
            resume_text = resume_response.text
        except Exception as resume_error:
            print(f"Error generating resume: {resume_error}")
            resume_text = f"Error generating resume: {str(resume_error)}"

        # Generate Cover Letter with proper error handling
        try:
            cover_letter_prompt = f"Write a cover letter for a {target_role} position using this profile:\n{profile_data}"
            cover_letter_response = model.generate_content(cover_letter_prompt)
            cover_letter_text = cover_letter_response.text
        except Exception as cover_letter_error:
            print(f"Error generating cover letter: {cover_letter_error}")
            cover_letter_text = f"Error generating cover letter: {str(cover_letter_error)}"

        # Generate Portfolio About Section with proper error handling
        try:
            portfolio_prompt = f"Write a modern portfolio About Me section for a {target_role} using:\n{profile_data}"
            portfolio_response = model.generate_content(portfolio_prompt)
            portfolio_text = portfolio_response.text
        except Exception as portfolio_error:
            print(f"Error generating portfolio: {portfolio_error}")
            portfolio_text = f"Error generating portfolio: {str(portfolio_error)}"

        # Generate Short Professional Bio with proper error handling
        try:
            bio_prompt = f"Write a short professional bio (3-4 lines) for a {target_role} suitable for LinkedIn headline or Instagram profile using:\n{profile_data}"
            bio_response = model.generate_content(bio_prompt)
            bio_text = bio_response.text
        except Exception as bio_error:
            print(f"Error generating bio: {bio_error}")
            bio_text = f"Error generating bio: {str(bio_error)}"

        # Store results in session or pass to template
        results = {
            'name': name,
            'resume': resume_text,
            'cover_letter': cover_letter_text,
            'portfolio': portfolio_text,
            'bio': bio_text
        }

        return render_template('result.html', results=results)

    except Exception as e:
        # Always pass results as empty list even when there's an error
        error_message = str(e)
        print(f"Application error: {error_message}")
        
        # Provide user-friendly error messages
        if "API key" in error_message.lower():
            friendly_error = "API Key Error: Please check your GOOGLE_API_KEY in the .env file. Make sure you have a valid Google Gemini API key."
        elif "model" in error_message.lower():
            friendly_error = "Model Error: The AI model is currently unavailable. Please try again later."
        elif "quota" in error_message.lower() or "rate" in error_message.lower():
            friendly_error = "API Quota Error: You have reached the API limit. Please check your Google AI Studio quota and try again later."
        else:
            friendly_error = f"An error occurred: {error_message}"
        
        return render_template('result.html', results=[], error=friendly_error)

@app.route('/download_pdf')
def download_pdf():
    """Generate and download PDF resume"""
    try:
        # Get the resume text from the query parameter
        resume_text = request.args.get('resume_text', '')
        name = request.args.get('name', 'Resume')

        # Create PDF instance
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        
        # Add name as header
        pdf.cell(0, 10, name.upper(), 0, 1, 'C')
        pdf.ln(10)
        
        # Clean and format the resume text
        # Remove any special characters that might cause issues
        cleaned_text = re.sub(r'[^\x00-\x7F]+', '', resume_text)
        
        # Split text into sections and add to PDF
        sections = cleaned_text.split('\n\n')
        for section in sections:
            if section.strip():
                # Check if it's a header (all caps or contains common resume section names)
                if any(keyword in section.upper() for keyword in ['SUMMARY', 'EXPERIENCE', 'EDUCATION', 'SKILLS', 'PROJECTS', 'OBJECTIVE']):
                    pdf.set_font('Arial', 'B', 12)
                    pdf.set_fill_color(200, 220, 255)
                    pdf.cell(0, 8, section.strip(), 0, 1, 'L', 1)
                    pdf.ln(4)
                else:
                    pdf.set_font('Times', '', 11)
                    pdf.multi_cell(0, 6, section.strip())
                    pdf.ln(2)

        # Save PDF to file
        pdf_output = 'smart_resume.pdf'
        pdf.output(pdf_output)

        return send_file(pdf_output, as_attachment=True, download_name='smart_resume.pdf')

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
