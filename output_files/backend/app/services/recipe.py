# backend/app/services/recipe.py
import json
import os
from typing import Dict, List

from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.core.llm import generate_text
from backend.app.db.database import get_db
from backend.app.db.models import Recipe


async def get_recipes(user: str, db: Session = Depends(get_db)):
    try:
        with open("backend/data/sample_recipes.json", "r") as f:
            recipes = json.load(f)
            if not recipes:
                return "No Recipes Found"
            for recipe_data in recipes:
                recipe = Recipe(**recipe_data, user_id=1)
                db.add(recipe)
                db.commit()
        return f"Recipes Loaded from local file, found {len(recipes)}"
    except Exception as e:
        print(f"An error occurred while loading recipes from file: {e}")
        return "An error occurred while loading recipes"
