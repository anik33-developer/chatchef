from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import google.generativeai as genai
import json
import os
from datetime import datetime
import sqlite3
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="Digital Chef API", version="1.0.0")

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount a static directory (safe no-op if not present) so any future assets
# (images, external CSS/JS) can be served from /static. Keeps behavior robust
# when serving index.html from the app root.
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
    raise ValueError("Please set a valid GEMINI_API_KEY in your .env file")

genai.configure(api_key=GEMINI_API_KEY)

# List available models for debugging
try:
    print("Available Gemini models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"  - {m.name}")
except Exception as e:
    print(f"Could not list models: {str(e)}")

# Initialize the free Gemini model
try:
    # Use the latest free Flash model
    model = genai.GenerativeModel('models/gemini-flash-latest')
    print("Successfully initialized Gemini Flash Latest model (free tier)")
except Exception as e:
    print(f"Error initializing Gemini Flash Latest: {str(e)}")
    try:
        # Try the 2.5 flash model
        model = genai.GenerativeModel('models/gemini-2.5-flash')
        print("Successfully initialized Gemini 2.5 Flash model")
    except Exception as e2:
        print(f"Error initializing Gemini 2.5 Flash: {str(e2)}")
        try:
            # Try the 2.0 flash model
            model = genai.GenerativeModel('models/gemini-2.0-flash')
            print("Successfully initialized Gemini 2.0 Flash model")
        except Exception as e3:
            print(f"Error initializing Gemini 2.0 Flash: {str(e3)}")
            try:
                # Try the pro latest as fallback
                model = genai.GenerativeModel('models/gemini-pro-latest')
                print("Successfully initialized Gemini Pro Latest model")
            except Exception as e4:
                raise ValueError(f"Failed to initialize any Gemini model. Check your API key and model availability. Last error: {str(e4)}")

# Database initialization
def init_db():
    conn = sqlite3.connect('recipes.db')
    c = conn. cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS saved_recipes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            prep_time TEXT,
            ingredients TEXT,
            steps TEXT,
            cuisine TEXT,
            difficulty TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Pydantic Models
class Recipe(BaseModel):
    title: str
    prep_time: str
    ingredients: List[str]
    steps: List[str]
    
    @field_validator('ingredients')
    @classmethod
    def validate_ingredients(cls, v):
        if len(v) < 1:
            raise ValueError('At least one ingredient is required')
        return v
    
    @field_validator('steps')
    @classmethod
    def validate_steps(cls, v):
        if len(v) < 1:
            raise ValueError('At least one step is required')
        return v

class RecipeRequest(BaseModel):
    # Use min_length instead of deprecated min_items (Pydantic v2+)
    ingredients: List[str] = Field(..., min_length=1)
    exclude_ingredients: Optional[List[str]] = []
    cuisine: Optional[str] = None
    difficulty: Optional[str] = None

class SavedRecipe(Recipe):
    id: int
    cuisine: Optional[str]
    difficulty: Optional[str]
    created_at: str

# Helper function to construct AI prompt
def construct_prompt(request: RecipeRequest) -> str:
    prompt = (
        f'Return recipe JSON:\n'
        f'{{"title":"Recipe with {", ".join(request.ingredients)}",\n'
        f'"prep_time":"X min",\n'
        f'"ingredients":["amounts + ingredients"],\n'
        f'"steps":["steps"]}}\n'
        f'Using: {", ".join(request.ingredients)}'
    )
    
    if request.exclude_ingredients:
        prompt += f'\nNo: {", ".join(request.exclude_ingredients)}'
    
    if request.cuisine:
        prompt += f'\nStyle: {request.cuisine}'
    
    if request.difficulty:
        prompt += f'\nLevel: {request.difficulty}'
    
    return prompt
    
    return prompt

# API Endpoints
@app.get("/")
async def root():
    """Serve the main HTML file"""
    html_path = Path(__file__).parent / "index.html"
    if html_path.exists():
        return FileResponse(html_path, media_type="text/html")
    return {
        "message": "Welcome to Digital Chef API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate-recipe",
            "save": "/save-recipe",
            "saved": "/saved-recipes"
        }
    }

@app.get("/api")
async def api_info():
    return {
        "message": "Welcome to Digital Chef API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate-recipe",
            "save": "/save-recipe",
            "saved": "/saved-recipes"
        }
    }


@app.get("/health")
async def health():
    """Simple health check endpoint."""
    return {"status": "ok", "uptime": datetime.utcnow().isoformat()}

@app.post("/generate-recipe", response_model=Recipe)
async def generate_recipe(request: RecipeRequest):
    """
    Generate a recipe based on provided ingredients using Gemini AI
    """
    # Input validation
    if not request.ingredients:
        raise HTTPException(status_code=400, detail="No ingredients provided")
        
    if not GEMINI_API_KEY or GEMINI_API_KEY == "your_gemini_api_key_here":
        raise HTTPException(status_code=500, detail="Gemini API key not configured")

    if not model:
        raise HTTPException(status_code=500, detail="AI model not initialized")

    try:
        # Construct detailed prompt for better recipe generation
        prompt = f'''You are an expert chef assistant. Create a detailed, authentic recipe using these main ingredients: {", ".join(request.ingredients)}

IMPORTANT REQUIREMENTS:
- Create a complete, practical recipe that someone can actually cook
- Include specific measurements and quantities (cups, tablespoons, grams, etc.)
- Provide clear, step-by-step cooking instructions
- Make it flavorful and well-balanced
- Use common cooking techniques and accessible ingredients

Return ONLY valid JSON in this exact format:
{{
  "title": "Descriptive recipe name (e.g., 'Savory Garlic Fried Rice')",
  "prep_time": "X minutes (realistic cooking time)",
  "ingredients": [
    "2 cups cooked rice",
    "1 large onion, diced",
    "3 cloves garlic, minced",
    "2 tablespoons vegetable oil",
    "Salt and pepper to taste"
  ],
  "steps": [
    "Heat 2 tablespoons of vegetable oil in a large skillet over medium-high heat",
    "Add diced onion and sauté for 3-4 minutes until translucent",
    "Add minced garlic and cook for another 30 seconds until fragrant",
    "Add the cooked rice, breaking up any clumps, and stir-fry for 5-7 minutes",
    "Season with salt and pepper to taste and serve hot"
  ]
}}'''

        if request.exclude_ingredients:
            prompt += f"\n\nIMPORTANT: DO NOT include these ingredients: {', '.join(request.exclude_ingredients)}"
            
        if request.cuisine:
            prompt += f"\n\nCUISINE STYLE: Make this a {request.cuisine} recipe with authentic flavors, traditional cooking methods, and typical seasonings/spices from this cuisine."
            
        if request.difficulty:
            difficulty_instructions = {
                "Beginner": "Keep it simple with basic techniques, minimal prep work, and common ingredients. Perfect for someone just learning to cook.",
                "Intermediate": "Use moderate cooking techniques, some specialized ingredients, and assume basic cooking knowledge.",
                "Advanced": "Feel free to use complex techniques, specialized equipment, multiple cooking stages, and professional-level skills."
            }
            if request.difficulty in difficulty_instructions:
                prompt += f"\n\nDIFFICULTY LEVEL: {request.difficulty} - {difficulty_instructions[request.difficulty]}"

        # Add final quality instructions
        prompt += '''

FINAL REQUIREMENTS:
- Make sure ingredients list includes realistic quantities and measurements
- Ensure cooking steps are in logical order and detailed enough to follow
- Include cooking temperatures and timing where relevant
- Add seasoning and flavor enhancement tips
- Return ONLY the JSON object, no extra text or explanations

'''

        print(f"Generating with prompt: {prompt[:200]}...")

        try:
            print("Attempting to generate content...")
            # Generate with simple parameters for free model
            response = model.generate_content(prompt)
            print(f"Response received: {response}")
            
            if not response:
                raise HTTPException(status_code=500, detail="No response received from AI model")
            if not hasattr(response, 'text'):
                raise HTTPException(status_code=500, detail=f"Invalid response format: {str(response)}")
                
        except Exception as e:
            print(f"Error during generation: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")
            
        # Extract and clean response
        response_text = response.text.strip()
        if not response_text:
            raise HTTPException(status_code=500, detail="Empty response from AI model")

        print(f"Raw response: {response_text}")

        # Clean JSON string
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()

        try:
            recipe_data = json.loads(response_text)
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=500, detail=f"Invalid JSON format: {str(e)}")

        # Validate response data
        try:
            recipe = Recipe(**recipe_data)
            return recipe
        except Exception as e:
            raise HTTPException(status_code=422, detail=f"Invalid recipe format: {str(e)}")

    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Recipe generation failed: {str(e)}")

@app.post("/save-recipe")
async def save_recipe(recipe: Recipe, cuisine: Optional[str] = None, difficulty: Optional[str] = None):
    """
    Save a generated recipe to the database
    """
    try:
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        
        c.execute('''
            INSERT INTO saved_recipes (title, prep_time, ingredients, steps, cuisine, difficulty)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            recipe.title,
            recipe.prep_time,
            json.dumps(recipe.ingredients),
            json.dumps(recipe.steps),
            cuisine,
            difficulty
        ))
        
        conn.commit()
        recipe_id = c.lastrowid
        conn.close()
        
        return {"message": "Recipe saved successfully", "id": recipe_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save recipe: {str(e)}")

@app.get("/saved-recipes", response_model=List[SavedRecipe])
async def get_saved_recipes():
    """
    Retrieve all saved recipes from the database
    """
    try:
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        
        c.execute('SELECT * FROM saved_recipes ORDER BY created_at DESC')
        rows = c.fetchall()
        conn.close()
        
        recipes = []
        for row in rows:
            recipes.append({
                "id": row[0],
                "title": row[1],
                "prep_time": row[2],
                "ingredients": json.loads(row[3]),
                "steps": json.loads(row[4]),
                "cuisine": row[5],
                "difficulty": row[6],
                "created_at": row[7]
            })
        
        return recipes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve recipes: {str(e)}")

@app.delete("/saved-recipes/{recipe_id}")
async def delete_recipe(recipe_id: int):
    """
    Delete a saved recipe
    """
    try:
        conn = sqlite3.connect('recipes.db')
        c = conn.cursor()
        
        c.execute('DELETE FROM saved_recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        
        if c.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Recipe not found")
        
        conn.close()
        return {"message": "Recipe deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete recipe: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Read PORT and HOST from environment if provided, otherwise use sensible defaults
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port, log_level="info")