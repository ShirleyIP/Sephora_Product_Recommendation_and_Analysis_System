import pandas as pd
import glob
import tkinter as tk
from tkinter import Button, Text, Checkbutton, StringVar, Label, Frame, Scrollbar, Listbox, OptionMenu

# Load the cleaned product data
df = pd.read_csv('cleaned_product_info.csv')

# Load all cleaned_reviews CSV files
files = glob.glob('cleaned_reviews_*.csv')
df_reviews_list = [pd.read_csv(file) for file in files]
df_reviews = pd.concat(df_reviews_list, ignore_index=True)

# Assuming you have merged df with df_reviews
df = pd.merge(df, df_reviews[['product_id', 'skin_type']], on='product_id', how='left')

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Print column names for debugging
print(df.columns)
print(df_reviews.columns.tolist())

# Extract unique categories and brands for the selection
unique_primary = df['primary_category'].unique().tolist()
unique_secondary = df['secondary_category'].unique().tolist()
unique_tertiary = df['tertiary_category'].unique().tolist()
unique_brands = df['brand_name'].unique().tolist()

# Extract unique categories and brands for the selection
def get_unique_categories(df):
    return {
        'primary': df['primary_category'].unique().tolist(),
        'secondary': df['secondary_category'].unique().tolist(),
        'tertiary': df['tertiary_category'].unique().tolist(),
        'brands': df['brand_name'].unique().tolist()
    }

unique_categories = get_unique_categories(df)

# Function to update category options based on user selections
def update_categories(*args):
    selected_skin_type = skin_type_var.get()
    
    if selected_skin_type != "None":
        # Filter categories based on selected skin type
        filtered_df = df[df['skin_type'] == selected_skin_type]
        filtered_categories = get_unique_categories(filtered_df)
        
        # Update the category menus
        primary_var.set("None")
        primary_menu['menu'].delete(0, 'end')
        for category in filtered_categories['primary']:
            primary_menu['menu'].add_command(label=category, command=tk._setit(primary_var, category))

        secondary_var.set("None")
        secondary_menu['menu'].delete(0, 'end')
        for category in filtered_categories['secondary']:
            secondary_menu['menu'].add_command(label=category, command=tk._setit(secondary_var, category))

        tertiary_var.set("None")
        tertiary_menu['menu'].delete(0, 'end')
        for category in filtered_categories['tertiary']:
            tertiary_menu['menu'].add_command(label=category, command=tk._setit(tertiary_var, category))


# Function to recommend products based on user selections
def recommend_products():
    # Use the merged DataFrame here
    filtered_users = df.copy()

    selected_skin_type = skin_type_var.get()
    if selected_skin_type != "None":
        if 'skin_type' in filtered_users.columns:
            filtered_users = filtered_users[filtered_users['skin_type'] == selected_skin_type]
        # else:
        #     print("Column 'skin_type' not found in filtered_users.")
    
    # Continue with other filtering logic...
    selected_brands = brand_listbox.curselection()
    selected_brands = [brand_listbox.get(i) for i in selected_brands]

    
    # Apply filters based on selected categories
    if primary_var.get() != "None":
        filtered_users = filtered_users[filtered_users['primary_category'] == primary_var.get()]
    if secondary_var.get() != "None":
        filtered_users = filtered_users[filtered_users['secondary_category'] == secondary_var.get()]
    if tertiary_var.get() != "None":
        filtered_users = filtered_users[filtered_users['tertiary_category'] == tertiary_var.get()]
    
    # Filter by selected brands
    if selected_brands:
        filtered_users = filtered_users[filtered_users['brand_name'].isin(selected_brands)]

    # Clear previous recommendations
    recommendations_text.delete(1.0, tk.END)

    # Check if there are users after filtering
    if not filtered_users.empty:
        recommended_products = filtered_users[['product_id', 'product_name', 'brand_name', 'loves_count', 'rating', 'reviews', 'price_usd']].drop_duplicates()

        recommendations_text.insert(tk.END, "Most Popular Products:\n")
        
        for _, product in recommended_products.iterrows():
            recommendations_text.insert(tk.END, (
                f"Product ID: {product['product_id']}\n"
                f"Product Name: {product['product_name']}\n"
                f"Brand Name: {product['brand_name']}\n"
                f"Loves Count: {product['loves_count']}\n"
                f"Rating: {product['rating']}\n"
                f"Reviews: {product['reviews']}\n"
                f"Price: ${product['price_usd']:.2f}\n\n"
            ))
        else:
            recommendations_text.insert(tk.END, "No products found for the selected criteria.\n")


# Create the main Tkinter window
root = tk.Tk()
root.title("Product Recommendation System")
root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage(file='Sephora.png'))
root.configure(background='#000')

# Center the window on the screen
root.update_idletasks()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"+{x}+{y}")

# Skin Tone options
skin_tone_var = StringVar(value="None")
skin_tone_label = tk.Label(root, text="Select Skin Tone:", bg='#000', fg='white')
skin_tone_label.pack()
skin_tones = ["None", "Light", "Medium", "Dark"]
for tone in skin_tones:
    check = Checkbutton(root, text=tone, variable=skin_tone_var, onvalue=tone, offvalue="None", bg='#000', fg='white', selectcolor='#ccc')
    check.pack(anchor='w')

# Eye Color options
eye_color_var = StringVar(value="None")
eye_color_label = tk.Label(root, text="Select Eye Color:", bg='#000', fg='white')
eye_color_label.pack()
eye_colors = ["None", "Brown", "Blue", "Green", "Hazel"]
for color in eye_colors:
    check = Checkbutton(root, text=color, variable=eye_color_var, onvalue=color, offvalue="None", bg='#000', fg='white', selectcolor='#ccc')
    check.pack(anchor='w')

# Skin Type options
skin_type_var = StringVar(value="None")
skin_type_label = tk.Label(root, text="Select Skin Type:", bg='#000', fg='white')
skin_type_label.pack()
skin_types = ["None", "Oily", "Dry", "Combination"]
for skin in skin_types:
    check = Checkbutton(root, text=skin, variable=skin_type_var, onvalue=skin, offvalue="None", bg='#000', fg='white', selectcolor='#ccc')
    check.pack(anchor='w')

# Hair Color options
hair_color_var = StringVar(value="None")
hair_color_label = tk.Label(root, text="Select Hair Color:", bg='#000', fg='white')
hair_color_label.pack()
hair_colors = ["None", "Blonde", "Brunette", "Black", "Red"]
for color in hair_colors:
    check = Checkbutton(root, text=color, variable=hair_color_var, onvalue=color, offvalue="None", bg='#000', fg='white', selectcolor='#ccc')
    check.pack(anchor='w')

# Rating options
rating_var = StringVar(value="None")
rating_label = tk.Label(root, text="Minimum Rating (1-5):", bg='#000', fg='white')
rating_label.pack()
rating_options = ["None", "1", "2", "3", "4", "5"]
for rating in rating_options:
    check = Checkbutton(root, text=rating, variable=rating_var, onvalue=rating, offvalue="None", bg='#000', fg='white', selectcolor='#ccc')
    check.pack(anchor='w')

# Category selection
primary_var = StringVar(value="None")
primary_label = tk.Label(root, text="Select Primary Category:", bg='#000', fg='white')
primary_label.pack(pady=(5, 0))
primary_menu = tk.OptionMenu(root, primary_var, *unique_primary)
primary_menu.pack(pady=(5, 0))

secondary_var = StringVar(value="None")
secondary_label = tk.Label(root, text="Select Secondary Category:", bg='#000', fg='white')
secondary_label.pack(pady=(5, 0))
secondary_menu = tk.OptionMenu(root, secondary_var, *unique_secondary)
secondary_menu.pack(pady=(5, 0))

tertiary_var = StringVar(value="None")
tertiary_label = tk.Label(root, text="Select Tertiary Category:", bg='#000', fg='white')
tertiary_label.pack(pady=(5, 0))
tertiary_menu = tk.OptionMenu(root, tertiary_var, *unique_tertiary)
tertiary_menu.pack(pady=(5, 0))

# Scrollable Brand options
brand_frame = Frame(root)
brand_frame.pack(pady=(15, 0))

brand_label = tk.Label(brand_frame, text="Select Brands:")
brand_label.pack()

scrollbar = Scrollbar(brand_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

brand_listbox = Listbox(brand_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
for brand in unique_brands:
    brand_listbox.insert(tk.END, brand)
brand_listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=brand_listbox.yview)

# Button to get recommendations
recommend_button = Button(root, text="Get Recommendations", command=recommend_products)
recommend_button.pack(pady=10)

# Text area to display recommendations
recommendations_text = Text(root, width=60, height=15, padx=10, pady=10)
recommendations_text.pack(padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()