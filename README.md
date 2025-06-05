# 🍳 Smart Recipe Recommender

An intelligent recipe recommendation system that suggests recipes based on your available ingredients using machine learning algorithms.

## ✨ Features

- 🥘 **Ingredient-based recommendations** - Find recipes using ingredients you have
- 📸 **Beautiful food images** - Visual representation of each recipe
- 📋 **Step-by-step instructions** - Detailed cooking procedures
- 🎯 **Smart matching** - Recommends similar recipes when you don't have all ingredients
- ⭐ **3 personalized recommendations** - Get exactly 3 top recipe suggestions
- 🔍 **Missing ingredient detection** - Shows what you need to complete a recipe
- 📊 **Match scoring** - Percentage-based similarity scoring

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with scikit-learn, pandas, numpy
- **Machine Learning**: TF-IDF Vectorization, Cosine Similarity
- **Text Processing**: Fuzzy string matching for ingredient matching
- **Images**: Unsplash API integration for recipe images

## 📊 Dataset

The system uses a comprehensive recipe dataset containing:
- Over 200,000 recipes from Recipe.com
- Ingredient mappings and nutritional information
- User interactions and ratings
- Recipe steps, cooking times, and descriptions

## 🚀 Setup and Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone or download the project files**
   ```bash
   # Ensure you have these files in your directory:
   # - RAW_recipes.csv
   # - PP_recipes.csv
   # - ingr_map.pkl
   # - interactions_train.csv
   # - Other CSV files from the dataset
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run deploy.py
   ```

4. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to this URL manually

## 📱 How to Use

### Step 1: Navigate to "Find Recipes"
- Use the sidebar to navigate to the recipe finder

### Step 2: Enter Your Ingredients
- Type ingredients separated by commas
- Be specific (e.g., "chicken breast" vs "chicken")
- Include seasonings and basic ingredients

### Step 3: Get Recommendations
- Click "Find My Recipes!" button
- View 3 personalized recipe recommendations
- Each recipe shows:
  - Recipe image
  - Match percentage
  - Availability status
  - Prep time and steps
  - Available vs missing ingredients

### Step 4: View Details
- Expand ingredient lists to see what you have/need
- View step-by-step cooking instructions
- See recipe descriptions and metadata

## 💡 Example Ingredients

Try these popular combinations:

- **🍕 Pizza Night**: flour, cheese, tomato sauce, pepperoni, mushrooms
- **🥗 Fresh Salad**: lettuce, cucumber, tomato, olive oil, vinegar
- **🍜 Comfort Soup**: chicken, carrots, celery, onion, noodles
- **🌮 Taco Tuesday**: ground beef, tortillas, cheese, lettuce, tomato
- **🍳 Breakfast**: eggs, bacon, butter, bread, milk
- **🍝 Italian Pasta**: pasta, garlic, olive oil, parmesan, basil

## 🔧 Algorithm Details

### 1. Text Processing
- Cleans and normalizes ingredient names
- Handles ingredient variations and typos
- Creates unified ingredient representations

### 2. TF-IDF Vectorization
- Converts recipe ingredients into numerical vectors
- Creates a searchable ingredient space
- Enables similarity calculations

### 3. Cosine Similarity
- Calculates similarity between user ingredients and recipes
- Ranks recipes by relevance score
- Identifies best matches

### 4. Fuzzy Matching
- Uses Levenshtein distance for ingredient matching
- Handles spelling variations and partial matches
- Adjustable similarity thresholds

### 5. Smart Filtering
- Prioritizes recipes you can actually make
- Identifies missing ingredients
- Recommends similar recipes when exact matches aren't available

## 🎯 Additional Requirements for Production

### For Enhanced Image Integration
```bash
# Optional: For better image handling
pip install python-dotenv
# Set up Unsplash API key in .env file:
# UNSPLASH_ACCESS_KEY=your_api_key_here
```

### For Deployment
```bash
# For cloud deployment (Heroku, AWS, etc.)
pip install gunicorn
# Add Procfile for deployment
```

### Performance Optimization
```bash
# For larger datasets
pip install numba  # For faster numerical computations
pip install dask   # For parallel processing
```

## 🚀 Deployment Options

### Local Deployment
```bash
streamlit run deploy.py
```

### Cloud Deployment

#### Streamlit Cloud
1. Upload your code to GitHub
2. Connect to Streamlit Cloud
3. Deploy with one click

#### Heroku
1. Add `Procfile`: `web: streamlit run deploy.py --server.port=$PORT --server.address=0.0.0.0`
2. Push to Heroku
3. Access via provided URL

#### AWS/Docker
1. Create Dockerfile
2. Build and deploy container
3. Configure load balancer

## 📈 Performance Notes

- **Initial Load**: First run takes 1-2 minutes to process recipes
- **Subsequent Searches**: Near-instantaneous recommendations
- **Memory Usage**: ~500MB for full dataset
- **Optimization**: Uses caching for faster repeated access

## 🐛 Troubleshooting

### Common Issues

1. **Long loading time**: Large dataset requires initial processing
2. **Image loading errors**: Check internet connection
3. **No recommendations**: Try more common ingredients
4. **Memory errors**: Consider using a subset of the dataset

### Solutions

- Reduce dataset size for testing
- Ensure all CSV files are in the correct directory
- Check Python version compatibility
- Verify all requirements are installed

## 🤝 Contributing

Feel free to contribute by:
- Adding new recommendation algorithms
- Improving the UI/UX
- Optimizing performance
- Adding new features

## 📄 License

This project is for educational and personal use. Dataset credits go to Recipe.com and the original data providers.

---

**Happy Cooking! 👨‍🍳👩‍🍳**

Start discovering amazing recipes with the ingredients you already have! 