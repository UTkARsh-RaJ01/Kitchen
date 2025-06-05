import streamlit as st
import os
import random
from PIL import Image
import hashlib

def get_local_chef_images():
    """Get list of available local chef images"""
    images_dir = "images"
    if not os.path.exists(images_dir):
        return []
    
    chef_images = []
    for i in range(1, 11):  # chef_1.jpg to chef_10.jpg
        image_path = os.path.join(images_dir, f"chef_{i}.jpg")
        if os.path.exists(image_path):
            chef_images.append(image_path)
    
    return chef_images

@st.cache_data
def get_chef_image_for_recipe(recipe_name):
    """Get a consistent chef image for a specific recipe"""
    chef_images = get_local_chef_images()
    
    if not chef_images:
        return None
    
    # Use hash to ensure same recipe always gets same chef image
    recipe_hash = hashlib.md5(recipe_name.encode()).hexdigest()
    image_index = int(recipe_hash, 16) % len(chef_images)
    
    try:
        selected_image_path = chef_images[image_index]
        image = Image.open(selected_image_path)
        return image
    except Exception as e:
        print(f"Error loading local chef image: {e}")
        return None

def display_chef_image(recipe_name):
    """Display chef image for a recipe"""
    image = get_chef_image_for_recipe(recipe_name)
    
    if image:
        st.image(image, width=300, caption="Professional Chef")
    else:
        st.markdown("👨‍🍳 **Professional Chef**")