# 👨‍🍳 Chat Chef - AI Recipe Generator

A modern, interactive web application that generates personalized recipes using AI based on your available ingredients and cuisine preferences. Features a beautiful chat-style interface with cuisine selection tiles and real-time conversation with an AI chef bot.
This project demonstrates backend development with AI integration, focusing on API design, data storage, and user interaction.”
  
![Chat Chef Interface](https://img.shields.io/badge/Interface-Modern%20Chat%20UI-blue)
![AI Powered](https://img.shields.io/badge/AI-Google%20Gemini-green)
![Tech Stack](https://img.shields.io/badge/Tech-FastAPI%20%2B%20HTML%2FJS-orange)

## ✨ Features

### 🎨 Modern UI/UX
- **Interactive Cuisine Tiles**: Beautiful circular tiles with food emoji icons for different cuisines
- **Chat-Style Interface**: Natural conversation with AI chef bot using chat bubbles
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Ingredient Parsing**: Smart parsing of ingredient lists from natural language
- **Visual Feedback**: Smooth animations and hover effects for better user experience

### 🤖 AI-Powered Recipe Generation
- **Google Gemini Integration**: Uses advanced Gemini AI model for recipe creation
- **Multi-Cuisine Support**: 10+ cuisine types including North Indian, South Indian, Chinese, Italian, Mexican, Japanese, Thai, American, Mediterranean
- **Difficulty Levels**: Beginner, Intermediate, and Expert recipe options
- **Ingredient Exclusion**: Ability to exclude specific ingredients (allergies, preferences)
- **Smart Recipe Creation**: Context-aware recipe generation based on available ingredients

### 💾 Recipe Management
- **Save Recipes**: Store your favorite generated recipes
- **Recipe History**: View and manage all saved recipes
- **Easy Loading**: Click to reload any saved recipe
- **Recipe Deletion**: Remove unwanted recipes from your collection

### 🔧 Technical Features
- **RESTful API**: Clean FastAPI backend with proper endpoints
- **SQLite Database**: Local storage for recipe persistence
- **CORS Enabled**: Cross-origin requests supported
- **Auto-reload**: Development server with hot reloading
- **Error Handling**: Comprehensive error messages and validation

## 🏗️ Technology Stack

### Frontend
- **HTML5**: Modern semantic markup
- **CSS3**: Advanced styling with gradients, animations, and responsive design
- **Vanilla JavaScript**: Pure JS for interactivity and API communication
- **Font**: Segoe UI system font stack

### Backend
- **FastAPI**: Modern Python web framework
- **Pydantic**: Data validation and serialization
- **Google Generative AI**: Gemini model integration
- **SQLite**: Lightweight database for recipe storage

## ▶️ Local development (quick start)

Follow these steps to run the frontend and backend locally during development:

1. Start the backend (FastAPI):

```powershell
cd D:\Projects\Chef\Chef
python main.py
```

This runs the API and also serves `index.html` from the same folder at http://localhost:8000

2. Use Live Server (optional)

- If you prefer to use VS Code Live Server to serve the static frontend, open the workspace root you normally use.
- If you open `D:\Projects\Chef` as the workspace root, Live Server should be configured to serve the `Chef` subfolder. See the workspace `.vscode/settings.json`.

3. Static-only preview (no backend):

```powershell
cd D:\Projects\Chef\Chef
python -m http.server 5505
start http://127.0.0.1:5505/index.html
```

4. Health check (backend running):

```powershell
Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/health | Select-Object -ExpandProperty Content
```

If you run into Live Server connection issues, prefer opening the backend URL `http://localhost:8000` - it serves the same `index.html` and the API.

If you want me to re-check your Live Server setup, tell me and I'll walk through the VS Code Live Server Output and developer console logs.
- **Uvicorn**: ASGI server for development and production

### Dependencies
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
google-generativeai==0.7.2
python-multipart==0.0.6
python-dotenv==1.0.0
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key

### Step 1: Clone/Download the Project
```bash
# If you have the project files
cd kooK
```

### Step 2: Set Up Python Virtual Environment
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Server Configuration (Optional)
HOST=0.0.0.0
PORT=8000

# Database Configuration (Optional)
DATABASE_PATH=recipes.db
```

**Getting a Gemini API Key:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the key and paste it in your `.env` file

### Step 5: Start the Backend Server
```bash
# Start the FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Started reloader process [xxxxx] using WatchFiles
Available Gemini models:
Successfully initialized Gemini Flash Latest model (free tier)
INFO:     Application startup complete.
```

### Step 6: Open the Frontend
1. Open `index.html` in your web browser
2. Or serve it via a local web server for better performance:
```bash
# Using Python's built-in server
python -m http.server 3000
# Then open http://localhost:3000
```

## 🎯 Usage Guide

### Basic Usage
1. **Select Cuisine**: Click on any cuisine tile (North Indian, Chinese, Italian, etc.)
2. **Add Ingredients**: Type ingredients in the chat interface like "chicken, tomatoes, onions"
3. **Set Difficulty**: Choose your cooking skill level (optional)
4. **Exclude Ingredients**: Add any ingredients you want to avoid (optional)
5. **Generate Recipe**: Click "Generate My Recipe" button
6. **View & Save**: Review the generated recipe and save it if you like it

### Chat Interface Tips
- **Natural Language**: Type ingredients naturally: "I have chicken, some tomatoes, and garlic"
- **Comma Separated**: List ingredients with commas: "rice, vegetables, soy sauce"
- **Multiple Lines**: Use Enter for new lines, Shift+Enter to send
- **Real-time Parsing**: The AI will extract and add ingredients automatically

### Advanced Features
- **Recipe History**: Switch to "Saved Recipes" tab to view your collection
- **Recipe Loading**: Click any saved recipe to view it again
- **Recipe Management**: Delete recipes you no longer want
- **Mobile Usage**: The interface is fully responsive and touch-friendly

## 📁 Project Structure

```
kooK/
├── README.md              # This file
├── index.html            # Frontend application
├── main.py              # FastAPI backend server
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
├── recipes.db          # SQLite database (auto-created)
├── .venv/              # Virtual environment (auto-created)
└── __pycache__/        # Python cache (auto-created)
```

## 🔌 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### Generate Recipe
```http
POST /generate-recipe
Content-Type: application/json

{
  "ingredients": ["chicken", "tomatoes", "garlic"],
  "exclude_ingredients": ["nuts", "dairy"],
  "cuisine": "Italian",
  "difficulty": "Beginner"
}
```

#### Save Recipe
```http
POST /save-recipe?cuisine=Italian&difficulty=Beginner
Content-Type: application/json

{
  "title": "Chicken Pasta",
  "ingredients": ["chicken", "pasta", "tomatoes"],
  "steps": ["Cook pasta", "Prepare chicken", "Mix together"],
  "prep_time": "30 minutes"
}
```

#### Get Saved Recipes
```http
GET /saved-recipes
```

#### Delete Recipe
```http
DELETE /saved-recipes/{recipe_id}
```

## 🎨 UI Components

### Cuisine Selection Grid
- **Interactive Tiles**: Hover and click effects
- **Visual Icons**: Food emoji for each cuisine type
- **Responsive Layout**: Adapts to screen size (3 columns on mobile, 2 on small screens)
- **Selection Feedback**: Visual indication of selected cuisine

### Chat Interface
- **Message Bubbles**: Distinct styling for user and bot messages
- **Avatars**: User (👤) and Chef Bot (🤖) avatars
- **Auto-scroll**: Automatically scrolls to latest messages
- **Typing Indicator**: Visual feedback during ingredient parsing

### Recipe Display
- **Structured Layout**: Clean presentation of recipe details
- **Ingredient List**: Organized list with styling
- **Step-by-Step Instructions**: Numbered steps with visual indicators
- **Save Functionality**: One-click recipe saving

## 🔧 Customization

### Adding New Cuisines
1. **Frontend**: Add new cuisine tile in `index.html`:
```html
<div class="cuisine-card" data-cuisine="Korean">
    <div class="cuisine-icon">🥘</div>
    <div class="cuisine-name">Korean</div>
</div>
```

2. **Backend**: The AI model will automatically handle new cuisine types

### Modifying Chat Responses
Edit the chat response messages in `index.html`:
```javascript
// In addIngredientFromChat() function
const response = `Your custom message here!`;
addChatMessage(response, false);
```

### Styling Changes
All styles are in the `<style>` section of `index.html`. Key classes:
- `.cuisine-card`: Individual cuisine tiles
- `.chat-message`: Chat bubble styling
- `.recipe-card`: Recipe display layout
- `.btn`: Button styling

## 🐛 Troubleshooting

### Common Issues

#### "Failed to generate recipe" Error
- **Check API Key**: Ensure your Gemini API key is valid in `.env`
- **Check Server**: Verify the backend server is running on port 8000
- **Check Network**: Ensure no firewall blocking localhost connections

#### Server Won't Start
- **Virtual Environment**: Make sure it's activated
- **Dependencies**: Run `pip install -r requirements.txt`
- **Port Conflict**: Check if port 8000 is already in use

#### Chat Interface Not Working
- **JavaScript Errors**: Check browser console for errors
- **CORS Issues**: Ensure backend CORS is properly configured
- **API Endpoint**: Verify frontend is pointing to correct backend URL

#### Mobile Display Issues
- **Viewport**: Check meta viewport tag is present
- **CSS Grid**: Ensure CSS Grid is supported by browser
- **Touch Events**: Test on actual mobile device, not just browser resize

### Debug Mode
Enable debug logging in `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Development Notes

### Code Organization
- **Separation of Concerns**: Frontend handles UI, backend handles AI and data
- **Error Handling**: Comprehensive error handling on both ends
- **Validation**: Pydantic models for request/response validation
- **State Management**: Simple JavaScript state management for ingredients

### Performance Considerations
- **AI Response Time**: Gemini API calls may take 2-5 seconds
- **Database Queries**: SQLite operations are fast for this scale
- **Frontend Rendering**: Minimal DOM manipulation for smooth performance
- **Memory Usage**: Chat messages accumulate - consider cleanup for long sessions

### Security Notes
- **API Key**: Keep Gemini API key secure and never commit to version control
- **CORS**: Currently set to allow all origins - restrict for production
- **Input Validation**: Backend validates all inputs, but frontend should also validate
- **SQL Injection**: Using parameterized queries to prevent SQL injection

## 🚀 Deployment

### Local Production
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Docker Deployment
Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Cloud Deployment
- **Heroku**: Use Procfile with gunicorn
- **Railway**: Direct deployment with auto-detection
- **Vercel**: Deploy frontend separately, backend as API
- **AWS/GCP**: Use container services or serverless functions

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Bug Reports**: Open an issue with details and reproduction steps
2. **Feature Requests**: Suggest new features via issues
3. **Code Contributions**: Fork, create branch, make changes, submit PR
4. **Documentation**: Improve README, add code comments, write guides
5. **Testing**: Test on different devices and report issues

### Development Setup
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test thoroughly
4. Commit changes: `git commit -m "Add feature"`
5. Push branch: `git push origin feature-name`
6. Open Pull Request

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/chat-chef/issues)
- **Documentation**: This README file
- **Email**: your.email@example.com

## 🙏 Acknowledgments

- **Google Gemini**: AI model for recipe generation
- **FastAPI**: Modern Python web framework
- **Emoji Icons**: Unicode emoji for cuisine representation
- **CSS Grid**: For responsive layout design
- **Community**: Open source Python and JavaScript communities

---

**Made with ❤️ for food lovers and coding enthusiasts**

Happy cooking! 👨‍🍳✨