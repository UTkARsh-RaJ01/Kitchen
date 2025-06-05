<<<<<<< HEAD
import pandas as pd
import numpy as np
import ast
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz, process
import pickle
import requests
from PIL import Image
from io import BytesIO

class RecipeRecommender:
    def __init__(self):
        self.recipes_df = None
        self.ingredients_map = None
        self.tfidf_matrix = None
        self.vectorizer = None
        self.load_data()
        
    def load_data(self):
        try:
            print("Loading recipe data...")
            self.recipes_df = pd.read_csv('RAW_recipes.csv')
            
            self.recipes_df['ingredients_clean'] = self.recipes_df['ingredients'].apply(
                lambda x: self.clean_ingredients(x) if pd.notna(x) else []
            )
            
            try:
                with open('ingr_map.pkl', 'rb') as f:
                    self.ingredients_map = pickle.load(f)
            except:
                print("Ingredient map not available, using direct ingredient names")
                self.ingredients_map = None
                
            self.create_tfidf_matrix()
            
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def clean_ingredients(self, ingredients_str):
        try:
            if isinstance(ingredients_str, str):
                ingredients_list = ast.literal_eval(ingredients_str)
            else:
                ingredients_list = ingredients_str
                
            cleaned = []
            for ingredient in ingredients_list:
                clean_ingredient = re.sub(r'[^\w\s]', '', str(ingredient).lower())
                clean_ingredient = ' '.join(clean_ingredient.split())
                if clean_ingredient:
                    cleaned.append(clean_ingredient)
                    
            return cleaned
        except:
            return []
    
    def create_tfidf_matrix(self):
        ingredients_text = self.recipes_df['ingredients_clean'].apply(
            lambda x: ' '.join(x) if x else ''
        )
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(ingredients_text)
        
    def find_matching_recipes(self, user_ingredients, top_n=3):
        user_ingredients_clean = [ing.lower().strip() for ing in user_ingredients]
        user_ingredients_text = ' '.join(user_ingredients_clean)
        
        user_vector = self.vectorizer.transform([user_ingredients_text])
        
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[-top_n*3:][::-1]
        
        recommendations = []
        for idx in top_indices:
            recipe = self.recipes_df.iloc[idx]
            recipe_ingredients = recipe['ingredients_clean']
            
            match_score = self.calculate_ingredient_match(user_ingredients_clean, recipe_ingredients)
            
            can_make = self.can_make_recipe(user_ingredients_clean, recipe_ingredients)
            
            recommendations.append({
                'recipe': recipe,
                'similarity_score': similarities[idx],
                'ingredient_match_score': match_score,
                'can_make': can_make,
                'missing_ingredients': self.get_missing_ingredients(user_ingredients_clean, recipe_ingredients)
            })
            
            if len([r for r in recommendations if r['can_make']]) >= top_n:
                break
                
        if len([r for r in recommendations if r['can_make']]) < top_n:
            similar_recipes = [r for r in recommendations if not r['can_make']]
            similar_recipes.sort(key=lambda x: x['similarity_score'], reverse=True)
            recommendations = [r for r in recommendations if r['can_make']] + similar_recipes[:top_n]
            
        return recommendations[:top_n]
    
    def calculate_ingredient_match(self, user_ingredients, recipe_ingredients):
        if not recipe_ingredients:
            return 0
            
        matches = 0
        for recipe_ing in recipe_ingredients:
            for user_ing in user_ingredients:
                if fuzz.partial_ratio(user_ing, recipe_ing) > 80:
                    matches += 1
                    break
                    
        return (matches / len(recipe_ingredients)) * 100
    
    def can_make_recipe(self, user_ingredients, recipe_ingredients, threshold=70):
        if not recipe_ingredients:
            return False
            
        available_count = 0
        for recipe_ing in recipe_ingredients:
            for user_ing in user_ingredients:
                if fuzz.partial_ratio(user_ing, recipe_ing) > threshold:
                    available_count += 1
                    break
                    
        return (available_count / len(recipe_ingredients)) >= 0.7
    
    def get_missing_ingredients(self, user_ingredients, recipe_ingredients):
        missing = []
        for recipe_ing in recipe_ingredients:
            found = False
            for user_ing in user_ingredients:
                if fuzz.partial_ratio(user_ing, recipe_ing) > 80:
                    found = True
                    break
            if not found:
                missing.append(recipe_ing)
        return missing

 
    def format_recipe_steps(self, steps_str):
        try:
            if isinstance(steps_str, str):
                steps_list = ast.literal_eval(steps_str)
            else:
                steps_list = steps_str
                
            formatted_steps = []
            for i, step in enumerate(steps_list, 1):
                formatted_steps.append(f"{i}. {step}")
                
            return formatted_steps
        except:
            return ["Recipe steps not available"]
    
    def format_ingredients_list(self, ingredients):
        if isinstance(ingredients, list):
            return ingredients
        try:
            if isinstance(ingredients, str):
                return ast.literal_eval(ingredients)
            return []
        except:
=======
import pandas as pd
import numpy as np
import ast
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz, process
import pickle
import requests
from PIL import Image
from io import BytesIO

class RecipeRecommender:
    def __init__(self):
        self.recipes_df = None
        self.ingredients_map = None
        self.tfidf_matrix = None
        self.vectorizer = None
        self.load_data()
        
    def load_data(self):
        try:
            print("Loading recipe data...")
            self.recipes_df = pd.read_csv('RAW_recipes.csv')
            
            self.recipes_df['ingredients_clean'] = self.recipes_df['ingredients'].apply(
                lambda x: self.clean_ingredients(x) if pd.notna(x) else []
            )
            
            try:
                with open('ingr_map.pkl', 'rb') as f:
                    self.ingredients_map = pickle.load(f)
            except:
                print("Ingredient map not available, using direct ingredient names")
                self.ingredients_map = None
                
            self.create_tfidf_matrix()
            
        except Exception as e:
            print(f"Error loading data: {e}")
            
    def clean_ingredients(self, ingredients_str):
        try:
            if isinstance(ingredients_str, str):
                ingredients_list = ast.literal_eval(ingredients_str)
            else:
                ingredients_list = ingredients_str
                
            cleaned = []
            for ingredient in ingredients_list:
                clean_ingredient = re.sub(r'[^\w\s]', '', str(ingredient).lower())
                clean_ingredient = ' '.join(clean_ingredient.split())
                if clean_ingredient:
                    cleaned.append(clean_ingredient)
                    
            return cleaned
        except:
            return []
    
    def create_tfidf_matrix(self):
        ingredients_text = self.recipes_df['ingredients_clean'].apply(
            lambda x: ' '.join(x) if x else ''
        )
        
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2)
        )
        
        self.tfidf_matrix = self.vectorizer.fit_transform(ingredients_text)
        
    def find_matching_recipes(self, user_ingredients, top_n=3):
        user_ingredients_clean = [ing.lower().strip() for ing in user_ingredients]
        user_ingredients_text = ' '.join(user_ingredients_clean)
        
        user_vector = self.vectorizer.transform([user_ingredients_text])
        
        similarities = cosine_similarity(user_vector, self.tfidf_matrix).flatten()
        
        top_indices = similarities.argsort()[-top_n*3:][::-1]
        
        recommendations = []
        for idx in top_indices:
            recipe = self.recipes_df.iloc[idx]
            recipe_ingredients = recipe['ingredients_clean']
            
            match_score = self.calculate_ingredient_match(user_ingredients_clean, recipe_ingredients)
            
            can_make = self.can_make_recipe(user_ingredients_clean, recipe_ingredients)
            
            recommendations.append({
                'recipe': recipe,
                'similarity_score': similarities[idx],
                'ingredient_match_score': match_score,
                'can_make': can_make,
                'missing_ingredients': self.get_missing_ingredients(user_ingredients_clean, recipe_ingredients)
            })
            
            if len([r for r in recommendations if r['can_make']]) >= top_n:
                break
                
        if len([r for r in recommendations if r['can_make']]) < top_n:
            similar_recipes = [r for r in recommendations if not r['can_make']]
            similar_recipes.sort(key=lambda x: x['similarity_score'], reverse=True)
            recommendations = [r for r in recommendations if r['can_make']] + similar_recipes[:top_n]
            
        return recommendations[:top_n]
    
    def calculate_ingredient_match(self, user_ingredients, recipe_ingredients):
        if not recipe_ingredients:
            return 0
            
        matches = 0
        for recipe_ing in recipe_ingredients:
            for user_ing in user_ingredients:
                if fuzz.partial_ratio(user_ing, recipe_ing) > 80:
                    matches += 1
                    break
                    
        return (matches / len(recipe_ingredients)) * 100
    
    def can_make_recipe(self, user_ingredients, recipe_ingredients, threshold=70):
        if not recipe_ingredients:
            return False
            
        available_count = 0
        for recipe_ing in recipe_ingredients:
            for user_ing in user_ingredients:
                if fuzz.partial_ratio(user_ing, recipe_ing) > threshold:
                    available_count += 1
                    break
                    
        return (available_count / len(recipe_ingredients)) >= 0.7
    
    def get_missing_ingredients(self, user_ingredients, recipe_ingredients):
        missing = []
        for recipe_ing in recipe_ingredients:
            found = False
            for user_ing in user_ingredients:
                if fuzz.partial_ratio(user_ing, recipe_ing) > 80:
                    found = True
                    break
            if not found:
                missing.append(recipe_ing)
        return missing

 
    def format_recipe_steps(self, steps_str):
        try:
            if isinstance(steps_str, str):
                steps_list = ast.literal_eval(steps_str)
            else:
                steps_list = steps_str
                
            formatted_steps = []
            for i, step in enumerate(steps_list, 1):
                formatted_steps.append(f"{i}. {step}")
                
            return formatted_steps
        except:
            return ["Recipe steps not available"]
    
    def format_ingredients_list(self, ingredients):
        if isinstance(ingredients, list):
            return ingredients
        try:
            if isinstance(ingredients, str):
                return ast.literal_eval(ingredients)
            return []
        except:
>>>>>>> 5721058aece639a2cf8937488a7e554fd4d90702
            return []