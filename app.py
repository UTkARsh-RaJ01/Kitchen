<<<<<<< HEAD
import streamlit as st
import pandas as pd
from recipe_recommender import RecipeRecommender
from image_handler import display_chef_image
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="🍳 Smart Recipe Recommender",
    page_icon="🍳",
    layout="wide"
)

st.markdown("""
<style>
    .recipe-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .ingredient-tag {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 4px 8px;
        border-radius: 15px;
        margin: 2px;
        font-size: 12px;
        display: inline-block;
    }
    .missing-ingredient {
        background-color: #ffebee;
        color: #c62828;
        padding: 4px 8px;
        border-radius: 15px;
        margin: 2px;
        font-size: 12px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    return RecipeRecommender()

def display_recipe_card(recommendation, index):
    recipe = recommendation['recipe']
    match_score = recommendation['ingredient_match_score']
    can_make = recommendation['can_make']
    missing_ingredients = recommendation['missing_ingredients']
    
    with st.container():
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            display_chef_image(recipe['name'])
        
        with col2:
            st.markdown(f"### {recipe['name'].title()}")
            
            status_text = "✅ Can Make!" if can_make else "⚠️ Missing Ingredients"
            st.markdown(f"**Match Score:** {match_score:.1f}%")
            st.markdown(f"**Status:** {status_text}")
            st.write(f"⏱️ **Prep Time:** {recipe.get('minutes', 'N/A')} minutes")
            st.write(f"📖 **Steps:** {recipe.get('n_steps', 'N/A')}")
            
            description = recipe.get('description', 'No description available')
            if not isinstance(description, str) or pd.isna(description):
                description = 'No description available'
            elif len(description) > 200:
                description = description[:200] + "..."
            st.write(f"📝 **Description:** {description}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander(f"🛒 Ingredients for {recipe['name']}", expanded=False):
            ingredients = st.session_state.recommender.format_ingredients_list(recipe['ingredients'])
            
            col_ing1, col_ing2 = st.columns(2)
            
            with col_ing1:
                st.write("**Available Ingredients:**")
                available_ingredients = [ing for ing in ingredients if ing not in missing_ingredients]
                for ingredient in available_ingredients:
                    st.markdown(f'<span class="ingredient-tag">✅ {ingredient}</span>', unsafe_allow_html=True)
            
            with col_ing2:
                if missing_ingredients:
                    st.write("**Missing Ingredients:**")
                    for ingredient in missing_ingredients:
                        st.markdown(f'<span class="missing-ingredient">❌ {ingredient}</span>', unsafe_allow_html=True)
                else:
                    st.write("**🎉 You have all ingredients!**")
        
        with st.expander(f"👩‍🍳 Cooking Instructions for {recipe['name']}", expanded=False):
            steps = st.session_state.recommender.format_recipe_steps(recipe['steps'])
            for i, step in enumerate(steps, 1):
                st.write(f"**{i}.** {step}")
        
        st.markdown("---")

def main():
    st.sidebar.title("🍳 Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["🏠 Home", "🔍 Find Recipes", "ℹ️ About"])
    
    if page == "🏠 Home":
        st.title("🍳 Smart Recipe Recommender")
        st.markdown("""
        ### Welcome to your personal cooking assistant! 👨‍🍳
        
        **What can this app do for you?**
        - 🥘 Find recipes based on ingredients you have
        - 📸 Get beautiful chef images for each recipe  
        - 📋 Step-by-step cooking instructions
        - 🎯 Smart matching when you don't have all ingredients
        - ⭐ Get 3 personalized recipe recommendations
        
        **How to use:**
        1. Go to "Find Recipes" page
        2. Enter the ingredients you have (comma-separated)
        3. Get instant recipe recommendations!
        4. View detailed instructions and ingredient lists
        
        ---
        **Ready to start cooking?** Head over to the "Find Recipes" page! 🚀
        """)
        
        st.markdown("### 💡 Sample Ingredients to Try:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🥗 **Salad Lover**\nLettuce, tomato, cucumber, olive oil")
        with col2:
            st.info("🍝 **Pasta Night**\nPasta, garlic, cheese, butter")
        with col3:
            st.info("🥘 **Asian Cuisine**\nRice, soy sauce, ginger, chicken")
    
    elif page == "🔍 Find Recipes":
        st.title("🔍 Find Perfect Recipes")
        
        if 'recommender' not in st.session_state:
            with st.spinner("Loading recipe database... This may take a moment 📊"):
                st.session_state.recommender = load_recommender()
        
        st.markdown("### 🛒 What ingredients do you have?")
        
        ingredients_input = st.text_area(
            label="Enter your ingredients (comma-separated)",
            placeholder="e.g., chicken, rice, onion, garlic, tomato, cheese",
            height=100,
            help="List all ingredients you have available. The more specific, the better!"
        )
        
        if st.button("🔮 Find My Recipes!", type="primary"):
            if ingredients_input.strip():
                user_ingredients = [ing.strip() for ing in ingredients_input.split(',') if ing.strip()]
                
                with st.spinner("Finding perfect recipes for you... 🔍"):
                    recommendations = st.session_state.recommender.find_matching_recipes(
                        user_ingredients, top_n=3
                    )
                
                if recommendations:
                    st.success(f"Found {len(recommendations)} amazing recipes for you! 🎉")
                    st.markdown("---")
                    
                    for i, rec in enumerate(recommendations):
                        display_recipe_card(rec, i)
                else:
                    st.warning("No recipes found with those ingredients. Try adding more common ingredients!")
            else:
                st.error("Please enter some ingredients first! 🥕")
        
        st.markdown("### 🔥 Popular Ingredient Combinations")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🍕 Pizza Night"):
                st.session_state.suggested_ingredients = "flour, cheese, tomato sauce, pepperoni, mushrooms"
        with col2:
            if st.button("🥗 Fresh Salad"):
                st.session_state.suggested_ingredients = "lettuce, cucumber, tomato, olive oil, vinegar"
        with col3:
            if st.button("🍜 Comfort Soup"):
                st.session_state.suggested_ingredients = "chicken, carrots, celery, onion, noodles"
                
        if 'suggested_ingredients' in st.session_state:
            st.info(f"Try these ingredients: {st.session_state.suggested_ingredients}")
    
    elif page == "ℹ️ About":
        st.title("ℹ️ About Smart Recipe Recommender")
        st.markdown("""
        ### 🎯 How It Works
        
        This app uses advanced machine learning algorithms to recommend recipes based on your available ingredients:
        
        1. **TF-IDF Vectorization**: Converts recipe ingredients into numerical vectors
        2. **Cosine Similarity**: Calculates similarity between your ingredients and recipe databases
        3. **Fuzzy Matching**: Handles ingredient name variations and typos
        4. **Smart Filtering**: Prioritizes recipes you can actually make
        
        ### 📊 Dataset Information
        
        - **Recipe Database**: Over 200,000 recipes from Recipe.com
        - **Ingredients**: Thousands of unique ingredients mapped and processed
        - **Features**: Recipe names, ingredients, cooking steps, prep time, and more
        
        ### 🚀 Features
        
        ✅ **Ingredient-based recommendations**  
        ✅ **Chef image integration for each recipe**  
        ✅ **Step-by-step cooking instructions**  
        ✅ **Missing ingredient identification**  
        ✅ **Similarity scoring and matching**  
        ✅ **Responsive and modern UI**  
        
        ---
        **Happy Cooking! 👨‍🍳👩‍🍳**
        """)

if __name__ == "__main__":
=======
import streamlit as st
import pandas as pd
from recipe_recommender import RecipeRecommender
from image_handler import display_chef_image
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(
    page_title="🍳 Smart Recipe Recommender",
    page_icon="🍳",
    layout="wide"
)

st.markdown("""
<style>
    .recipe-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .ingredient-tag {
        background-color: #e3f2fd;
        color: #1976d2;
        padding: 4px 8px;
        border-radius: 15px;
        margin: 2px;
        font-size: 12px;
        display: inline-block;
    }
    .missing-ingredient {
        background-color: #ffebee;
        color: #c62828;
        padding: 4px 8px;
        border-radius: 15px;
        margin: 2px;
        font-size: 12px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_recommender():
    return RecipeRecommender()

def display_recipe_card(recommendation, index):
    recipe = recommendation['recipe']
    match_score = recommendation['ingredient_match_score']
    can_make = recommendation['can_make']
    missing_ingredients = recommendation['missing_ingredients']
    
    with st.container():
        st.markdown('<div class="recipe-card">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            display_chef_image(recipe['name'])
        
        with col2:
            st.markdown(f"### {recipe['name'].title()}")
            
            status_text = "✅ Can Make!" if can_make else "⚠️ Missing Ingredients"
            st.markdown(f"**Match Score:** {match_score:.1f}%")
            st.markdown(f"**Status:** {status_text}")
            st.write(f"⏱️ **Prep Time:** {recipe.get('minutes', 'N/A')} minutes")
            st.write(f"📖 **Steps:** {recipe.get('n_steps', 'N/A')}")
            
            description = recipe.get('description', 'No description available')
            if not isinstance(description, str) or pd.isna(description):
                description = 'No description available'
            elif len(description) > 200:
                description = description[:200] + "..."
            st.write(f"📝 **Description:** {description}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander(f"🛒 Ingredients for {recipe['name']}", expanded=False):
            ingredients = st.session_state.recommender.format_ingredients_list(recipe['ingredients'])
            
            col_ing1, col_ing2 = st.columns(2)
            
            with col_ing1:
                st.write("**Available Ingredients:**")
                available_ingredients = [ing for ing in ingredients if ing not in missing_ingredients]
                for ingredient in available_ingredients:
                    st.markdown(f'<span class="ingredient-tag">✅ {ingredient}</span>', unsafe_allow_html=True)
            
            with col_ing2:
                if missing_ingredients:
                    st.write("**Missing Ingredients:**")
                    for ingredient in missing_ingredients:
                        st.markdown(f'<span class="missing-ingredient">❌ {ingredient}</span>', unsafe_allow_html=True)
                else:
                    st.write("**🎉 You have all ingredients!**")
        
        with st.expander(f"👩‍🍳 Cooking Instructions for {recipe['name']}", expanded=False):
            steps = st.session_state.recommender.format_recipe_steps(recipe['steps'])
            for i, step in enumerate(steps, 1):
                st.write(f"**{i}.** {step}")
        
        st.markdown("---")

def main():
    st.sidebar.title("🍳 Navigation")
    page = st.sidebar.selectbox("Choose a page:", ["🏠 Home", "🔍 Find Recipes", "ℹ️ About"])
    
    if page == "🏠 Home":
        st.title("🍳 Smart Recipe Recommender")
        st.markdown("""
        ### Welcome to your personal cooking assistant! 👨‍🍳
        
        **What can this app do for you?**
        - 🥘 Find recipes based on ingredients you have
        - 📸 Get beautiful chef images for each recipe  
        - 📋 Step-by-step cooking instructions
        - 🎯 Smart matching when you don't have all ingredients
        - ⭐ Get 3 personalized recipe recommendations
        
        **How to use:**
        1. Go to "Find Recipes" page
        2. Enter the ingredients you have (comma-separated)
        3. Get instant recipe recommendations!
        4. View detailed instructions and ingredient lists
        
        ---
        **Ready to start cooking?** Head over to the "Find Recipes" page! 🚀
        """)
        
        st.markdown("### 💡 Sample Ingredients to Try:")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info("🥗 **Salad Lover**\nLettuce, tomato, cucumber, olive oil")
        with col2:
            st.info("🍝 **Pasta Night**\nPasta, garlic, cheese, butter")
        with col3:
            st.info("🥘 **Asian Cuisine**\nRice, soy sauce, ginger, chicken")
    
    elif page == "🔍 Find Recipes":
        st.title("🔍 Find Perfect Recipes")
        
        if 'recommender' not in st.session_state:
            with st.spinner("Loading recipe database... This may take a moment 📊"):
                st.session_state.recommender = load_recommender()
        
        st.markdown("### 🛒 What ingredients do you have?")
        
        ingredients_input = st.text_area(
            label="Enter your ingredients (comma-separated)",
            placeholder="e.g., chicken, rice, onion, garlic, tomato, cheese",
            height=100,
            help="List all ingredients you have available. The more specific, the better!"
        )
        
        if st.button("🔮 Find My Recipes!", type="primary"):
            if ingredients_input.strip():
                user_ingredients = [ing.strip() for ing in ingredients_input.split(',') if ing.strip()]
                
                with st.spinner("Finding perfect recipes for you... 🔍"):
                    recommendations = st.session_state.recommender.find_matching_recipes(
                        user_ingredients, top_n=3
                    )
                
                if recommendations:
                    st.success(f"Found {len(recommendations)} amazing recipes for you! 🎉")
                    st.markdown("---")
                    
                    for i, rec in enumerate(recommendations):
                        display_recipe_card(rec, i)
                else:
                    st.warning("No recipes found with those ingredients. Try adding more common ingredients!")
            else:
                st.error("Please enter some ingredients first! 🥕")
        
        st.markdown("### 🔥 Popular Ingredient Combinations")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🍕 Pizza Night"):
                st.session_state.suggested_ingredients = "flour, cheese, tomato sauce, pepperoni, mushrooms"
        with col2:
            if st.button("🥗 Fresh Salad"):
                st.session_state.suggested_ingredients = "lettuce, cucumber, tomato, olive oil, vinegar"
        with col3:
            if st.button("🍜 Comfort Soup"):
                st.session_state.suggested_ingredients = "chicken, carrots, celery, onion, noodles"
                
        if 'suggested_ingredients' in st.session_state:
            st.info(f"Try these ingredients: {st.session_state.suggested_ingredients}")
    
    elif page == "ℹ️ About":
        st.title("ℹ️ About Smart Recipe Recommender")
        st.markdown("""
        ### 🎯 How It Works
        
        This app uses advanced machine learning algorithms to recommend recipes based on your available ingredients:
        
        1. **TF-IDF Vectorization**: Converts recipe ingredients into numerical vectors
        2. **Cosine Similarity**: Calculates similarity between your ingredients and recipe databases
        3. **Fuzzy Matching**: Handles ingredient name variations and typos
        4. **Smart Filtering**: Prioritizes recipes you can actually make
        
        ### 📊 Dataset Information
        
        - **Recipe Database**: Over 200,000 recipes from Recipe.com
        - **Ingredients**: Thousands of unique ingredients mapped and processed
        - **Features**: Recipe names, ingredients, cooking steps, prep time, and more
        
        ### 🚀 Features
        
        ✅ **Ingredient-based recommendations**  
        ✅ **Chef image integration for each recipe**  
        ✅ **Step-by-step cooking instructions**  
        ✅ **Missing ingredient identification**  
        ✅ **Similarity scoring and matching**  
        ✅ **Responsive and modern UI**  
        
        ---
        **Happy Cooking! 👨‍🍳👩‍🍳**
        """)

if __name__ == "__main__":
>>>>>>> 5721058aece639a2cf8937488a7e554fd4d90702
    main()