import pandas as pd
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import Label, Listbox, Scrollbar, Text, Button
from PIL import Image, ImageTk
import glob

# Load the cleaned product data
df = pd.read_csv('cleaned_product_info.csv')

# Load all cleaned_reviews CSV files
file_pattern = 'cleaned_reviews_*.csv'  # Adjust the pattern if needed
files = glob.glob(file_pattern)

# Load all reviews into a single DataFrame
df_reviews_list = [pd.read_csv(file) for file in files]
df_reviews = pd.concat(df_reviews_list, ignore_index=True)


# Extract unique brand names
unique_brands = df['brand_name'].unique()
unique_brands_list = unique_brands.tolist()
total_brands = len(unique_brands_list)

# Group by brand and sum the loves count
brand_popularity = df.groupby('brand_name')['loves_count'].sum().reset_index()
# Sort brands by loves count in descending order
most_popular_brands = brand_popularity.sort_values(by='loves_count', ascending=False)

# Extract unique categories from the relevant columns
unique_primary_categories = df['primary_category'].unique()
unique_secondary_categories = df['secondary_category'].unique()
unique_tertiary_categories = df['tertiary_category'].unique()

# Convert to lists for better readability
primary_categories_list = unique_primary_categories.tolist()
secondary_categories_list = unique_secondary_categories.tolist()
tertiary_categories_list = unique_tertiary_categories.tolist()

# Combine all unique categories into a single set to avoid duplicates
all_unique_categories = set(primary_categories_list + secondary_categories_list + tertiary_categories_list)

# Count the number of products in each category
category_counts = df['primary_category'].value_counts().reset_index()
category_counts.columns = ['category', 'product_count']

secondary_counts = df['secondary_category'].value_counts().reset_index()
secondary_counts.columns = ['category', 'product_count']

tertiary_counts = df['tertiary_category'].value_counts().reset_index()
tertiary_counts.columns = ['category', 'product_count']

# Sort by product count in descending order
category_counts = category_counts.sort_values(by='product_count', ascending=False)
secondary_counts = secondary_counts.sort_values(by='product_count', ascending=False)
tertiary_counts = tertiary_counts.sort_values(by='product_count', ascending=False)


# Create a Tkinter window
root = tk.Tk()
root.title("Product Brand Counter")
root.title("Product Category Analysis")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='Sephora.png'))
root.configure(background='#000')
root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"+{x}+{y}")

# Function to display the total number of unique brands
def show_total_brands():
    info_text.delete(1.0, tk.END)  # Clear previous text
    info_text.insert(tk.END, f"Total Number of Unique Product Brands: {total_brands}\n")
    info_text.insert(tk.END, "\nUnique Product Brands:\n")
    for brand in unique_brands_list:
        info_text.insert(tk.END, f"{brand}\n")

# Function to display the most popular brands
def show_most_popular_brands():
    top_n = 10
    info_text.delete(1.0, tk.END)  # Clear previous text
    info_text.insert(tk.END, f"Top {top_n} Most Popular Product Brands:\n")
    
    top_brands = most_popular_brands.head(top_n)
    
    for index, row in top_brands.iterrows():
        info_text.insert(tk.END, f"{row['brand_name']}: {row['loves_count']}\n")

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.barh(top_brands['brand_name'], top_brands['loves_count'], color='black')
    plt.xlabel('Total Loves Count')
    plt.title(f'Top {top_n} Most Popular Product Brands')
    plt.gca().invert_yaxis()  # Invert y-axis to show the highest on top
    plt.xticks(rotation=45)
    plt.tight_layout()  # Adjust layout
    plt.show()

# Function to display all unique product categories
def show_all_unique_categories():
    info_text.delete(1.0, tk.END)  # Clear previous text
    info_text.insert(tk.END, "All Unique Product Categories:\n")
    info_text.insert(tk.END, f"\nTotal Number of Unique Primary Categories: {len(unique_primary_categories)}\n")
    info_text.insert(tk.END, f"Total Number of Unique Secondary Categories: {len(unique_secondary_categories)}\n")
    info_text.insert(tk.END, f"Total Number of Unique Tertiary Categories: {len(unique_tertiary_categories)}\n")
    info_text.insert(tk.END, f"Total Number of Unique Product Categories: {len(all_unique_categories)}\n")

    for category in all_unique_categories:
        info_text.insert(tk.END, f"{category}\n")
    


# Function to display the most popular product categories and plot them
def show_most_popular_categories():
    info_text.delete(1.0, tk.END)  # Clear previous text
    top_n = 10
    top_n1 = 20
    top_n2 = 30

    # Display top categories in the text area
    info_text.insert(tk.END, "Most Popular Product Categories:\n")
    for index, row in category_counts.head(top_n).iterrows():
        info_text.insert(tk.END, f"{row['category']}: {row['product_count']}\n")

    info_text.insert(tk.END, "\nMost Popular Secondary Product Categories:\n")
    for index, row in secondary_counts.head(top_n1).iterrows():
        info_text.insert(tk.END, f"{row['category']}: {row['product_count']}\n")

    info_text.insert(tk.END, "\nMost Popular Tertiary Product Categories:\n")
    for index, row in tertiary_counts.head(top_n2).iterrows():
        info_text.insert(tk.END, f"{row['category']}: {row['product_count']}\n")

    # Plotting
    plt.figure(figsize=(14, 8))
    
    # Primary Categories
    plt.subplot(1, 3, 1)
    plt.barh(category_counts['category'].head(top_n), category_counts['product_count'].head(top_n), color='dimgray')
    plt.xlabel('Number of Products')
    plt.title('Most Popular Product Categories')
    plt.gca().invert_yaxis()

    # Secondary Categories
    plt.subplot(1, 3, 2)
    plt.barh(secondary_counts['category'].head(top_n1), secondary_counts['product_count'].head(top_n1), color='gray')
    plt.xlabel('Number of Products')
    plt.title('Top Secondary Product Categories')
    plt.gca().invert_yaxis()

    # Tertiary Categories
    plt.subplot(1, 3, 3)
    plt.barh(tertiary_counts['category'].head(top_n2), tertiary_counts['product_count'].head(top_n2), color='darkgray')
    plt.xlabel('Number of Products')
    plt.title('Top Tertiary Product Categories')
    plt.gca().invert_yaxis()

    plt.tight_layout()
    plt.show()

# Function to find and display the most popular product
def show_most_popular_product():
    # Find the most popular product based on loves_count
    most_popular_product = df.loc[df['loves_count'].idxmax()]

    # Clear previous text
    info_text.delete(1.0, tk.END)

    # Display product details
    info_text.insert(tk.END, "Most Popular Product:\n")
    info_text.insert(tk.END, f"Product ID: {most_popular_product['product_id']}\n")
    info_text.insert(tk.END, f"Product Name: {most_popular_product['product_name']}\n")
    info_text.insert(tk.END, f"Brand Name: {most_popular_product['brand_name']}\n")
    info_text.insert(tk.END, f"Loves Count: {most_popular_product['loves_count']}\n")
    info_text.insert(tk.END, f"Rating: {most_popular_product['rating']}\n")
    info_text.insert(tk.END, f"Reviews: {most_popular_product['reviews']}\n")
    info_text.insert(tk.END, f"Price: ${most_popular_product['price_usd']:.2f}\n")

    # Assign the local .webp image path for the product
    local_image_path = f"/Users/ip.hau/Desktop/Data bootcamp/JDE/Sep4_sephora_interim/Sephora Products and Skincare Reviews_2023/top10_popular_product/1.webp"  # Adjust the path as needed

    # Check if the file exists before attempting to open it
    if os.path.exists(local_image_path):
        # Open and display the local image
        img = Image.open(local_image_path)
        img = img.resize((200, 200), Image.LANCZOS)  # Resize image for display
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        img_label.config(image=img_tk)
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack(pady=10)
    else:
        img_label.config(image=None)  # Clear the image if not found
        info_text.insert(tk.END, "Local image path not found.\n")

# Function to find and display the product with the most reviews
def show_most_reviews_product():
    # Count the number of reviews for each product
    review_counts = df_reviews['product_id'].value_counts()

    # Find the product with the maximum number of reviews
    most_reviews_product_id = review_counts.idxmax()
    most_reviews_count = review_counts.max()

    # Get the product details from the reviews DataFrame
    most_reviews_product = df_reviews[df_reviews['product_id'] == most_reviews_product_id].iloc[0]

    # Clear previous text
    info_text.delete(1.0, tk.END)

    # Display product details
    info_text.insert(tk.END, "Product with the Most Reviews:\n")
    info_text.insert(tk.END, f"Product ID: {most_reviews_product['product_id']}\n")
    info_text.insert(tk.END, f"Product Name: {most_reviews_product['product_name']}\n")
    info_text.insert(tk.END, f"Brand Name: {most_reviews_product['brand_name']}\n")
    info_text.insert(tk.END, f"Number of Reviews: {most_reviews_count}\n")
    info_text.insert(tk.END, f"Average Rating: {df_reviews[df_reviews['product_id'] == most_reviews_product_id]['rating'].mean():.2f}\n")

    # Assign the local .webp image path for the product
    local_image_path = f"/Users/ip.hau/Desktop/Data bootcamp/JDE/Sep4_sephora_interim/Sephora Products and Skincare Reviews_2023/top10_popular_product/3.webp"  # Adjust the path as needed

    # Check if the file exists before attempting to open it
    if os.path.exists(local_image_path):
        # Open and display the local image
        img = Image.open(local_image_path)
        img = img.resize((200, 200), Image.LANCZOS)  # Resize image for display
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        img_label.config(image=img_tk)
        img_label.image = img_tk  # Keep a reference to avoid garbage collection
        img_label.pack(pady=10)
    else:
        img_label.config(image=None)  # Clear the image if not found
        info_text.insert(tk.END, "Local image path not found.\n")


# Create buttons for functionalities
total_brands_button = Button(root, text="Total Number of Unique Product Brands", command=show_total_brands)
total_brands_button.pack(pady=10)

popular_brands_button = Button(root, text="Most Popular Product Brands", command=show_most_popular_brands)
popular_brands_button.pack(pady=10)

categories_button = Button(root, text="All Unique Product Categories", command=show_all_unique_categories)
categories_button.pack(pady=10)

popular_categories_button = Button(root, text="Most Popular Product Categories", command=show_most_popular_categories)
popular_categories_button.pack(pady=10)

popular_product_button = Button(root, text="Most Popular Product", command=show_most_popular_product)
popular_product_button.pack(pady=10)

most_reviews_button = Button(root, text="Product with the Most Reviews", command=show_most_reviews_product)
most_reviews_button.pack(pady=10)

# Create a text area to display the information
info_text = Text(root, width=70, height=20, padx=10, pady=10, font=("Arial", 10))
info_text.pack(padx=10, pady=10)


# Create a label for displaying the product image
img_label = tk.Label(root)
img_label.pack(pady=10)


# Start the Tkinter main loop
root.mainloop()