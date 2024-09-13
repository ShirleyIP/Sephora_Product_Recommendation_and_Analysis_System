import pandas as pd


# Load the data
df = pd.read_csv('/Users/ip.hau/Desktop/Data bootcamp/JDE/Sep4_sephora_interim/Sephora Products and Skincare Reviews_2023/product_info.csv')

# Display initial data info
print("Initial Data Info:")
print(df.info())

# Step 1: Remove duplicates
df.drop_duplicates(inplace=True)

# Step 2: Handle missing values
# Fill missing values for specific columns
df['loves_count'].fillna(0, inplace=True)
df['rating'].fillna(0, inplace=True)
df['reviews'].fillna('', inplace=True)  # Fill with empty string for text fields

# Optionally drop rows with critical missing values
df.dropna(subset=['product_id', 'product_name'], inplace=True)

# Step 3: Convert data types
df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')
df['value_price_usd'] = pd.to_numeric(df['value_price_usd'], errors='coerce')
df['sale_price_usd'] = pd.to_numeric(df['sale_price_usd'], errors='coerce')

# Step 4: Clean string fields (e.g., trimming)
df['product_name'] = df['product_name'].str.strip()
df['brand_name'] = df['brand_name'].str.strip()
df['ingredients'] = df['ingredients'].str.strip()

# Step 5: Remove unnecessary columns if any (adjust as needed)
# df.drop(columns=['unnecessary_column'], inplace=True)

# Step 6: Save to a new CSV
df.to_csv('cleaned_product_info.csv', index=False)

# Display final data info
print("Cleaned Data Info:")
print(df.info())






# List of review files to clean
review_files = [
    'reviews_0-250.csv',
    'reviews_250-500.csv',
    'reviews_500-750.csv',
    'reviews_750-1250.csv',
    'reviews_1250-end.csv'
]

# Loop through each file to clean and save
for file in review_files:
    # Load the data
    df = pd.read_csv(file)

    # Display initial data info
    print(f"Cleaning {file}:")
    print(df.info())

    # Step 1: Remove duplicates
    df.drop_duplicates(inplace=True)

    # Step 2: Handle missing values
    df['rating'].fillna(0, inplace=True)
    df['is_recommended'].fillna(False, inplace=True)  # Assuming False for NaN
    df['review_text'].fillna('', inplace=True)  # Fill with empty string for text fields
    df.dropna(subset=['author_id', 'product_id'], inplace=True)

    # Step 3: Convert data types
    df['price_usd'] = pd.to_numeric(df['price_usd'], errors='coerce')

    # Step 4: Clean string fields
    df['review_title'] = df['review_title'].str.strip()
    df['review_text'] = df['review_text'].str.strip()
    df['product_name'] = df['product_name'].str.strip()
    df['brand_name'] = df['brand_name'].str.strip()

    # Step 5: Save cleaned data to a new CSV file
    cleaned_file_name = f'cleaned_{file}'
    df.to_csv(cleaned_file_name, index=False)

    # Display final data info
    print(f"Cleaned data saved to {cleaned_file_name}")
    print(df.info())