# AI Smart Resume & Portfolio Generator

A comprehensive web application that uses AI to generate professional resumes, cover letters, portfolio bios, and short professional bios. Built with Flask and powered by Google Gemini AI.

## 🌟 Features

- **Smart Resume Generation**: Create professional resumes tailored to your experience and skills
- **Cover Letter Generation**: Generate personalized cover letters
- **Portfolio Bio Creation**: Write compelling "About Me" sections for portfolios
- **Short Professional Bio**: Generate concise bios perfect for LinkedIn headlines or Instagram profiles
- **Multiple Tone Options**: Choose between Formal, Creative, or Technical writing styles
- **PDF Download**: Export your resume as a professionally formatted PDF
- **Modern Dark Theme UI**: Beautiful, responsive interface with gradient backgrounds
- **Real-time AI Processing**: Instant generation using Google Gemini AI

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Python Flask
- **AI API**: Google Gemini (gemini-pro model)
- **PDF Generation**: FPDF library
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.7 or higher
- Google Gemini API key
- Git (for cloning)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd AI-Smart-Resume-Generator
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit the `.env` file and add your Google Gemini API key:
```
API_KEY=your_google_gemini_api_key_here
```

### 5. Get Google Gemini API Key
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key
5. Add it to your `.env` file

## 🏃‍♂️ How to Run

1. Make sure your virtual environment is activated
2. Ensure you've set up your API key in the `.env` file
3. Run the Flask application:
```bash
python app.py
```

4. Open your web browser and navigate to:
```
http://localhost:5000
```

## 📖 Usage Guide

### 1. Fill Out the Form
- **Personal Information**: Enter your full name, email, and phone number
- **Skills**: List your technical and soft skills
- **Education**: Add your educational background
- **Projects**: Describe your notable projects
- **Experience**: Detail your work experience
- **Career Objective**: Write your career goals
- **Resume Tone**: Choose between Formal, Creative, or Technical

### 2. Generate Documents
- Click "Generate Smart Resume" to process your information
- The AI will create four different documents based on your input

### 3. Review and Download
- Review all generated documents in the result page
- Use the copy buttons to copy individual sections
- Download your resume as a PDF using the download button

## 📁 Project Structure

```
AI-Smart-Resume-Generator/
│ app.py                          # Main Flask application
│ requirements.txt                 # Python dependencies
│ .env.example                    # Environment variables template
│ README.md                       # Project documentation
│
├── templates/
│     index.html                  # Home page with form
│     result.html                 # Results display page
│
└── static/
     style.css                    # Styling and responsive design
```

## 🔧 Configuration

### Environment Variables
- `API_KEY`: Your Google Gemini API key (required)

### Customization
- **UI Theme**: Modify `static/style.css` to change colors and layout
- **AI Prompts**: Edit prompts in `app.py` to customize generated content
- **PDF Layout**: Modify the PDF generation logic in `app.py`

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your API key is correctly set in the `.env` file
   - Check if the API key has sufficient credits

2. **Module Import Errors**
   - Make sure you're in the correct virtual environment
   - Run `pip install -r requirements.txt` again

3. **PDF Generation Issues**
   - Ensure all required text is properly formatted
   - Check for special characters that might cause encoding issues

4. **Flask Server Not Starting**
   - Check if port 5000 is already in use
   - Try running on a different port: `python app.py --port 5001`

### Debug Mode
The application runs in debug mode by default. Check the terminal for detailed error messages.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Google Gemini AI for powering the content generation
- FPDF library for PDF generation
- Flask framework for the web backend

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the troubleshooting section above
2. Create an issue in the repository
3. Contact the development team

---

**Note**: This is a college AI mini project designed for educational purposes. The code is beginner-friendly and well-commented for learning purposes.
