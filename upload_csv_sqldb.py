import pandas as pd
import pyodbc
import os

# Database connection details
server = 'tcp:shirley.database.windows.net,1433'
database = 'shirley_db'
username = 'shirley_db'
password = 'opjl24Az'
driver = 'ODBC Driver 18 for SQL Server'

# Create a connection string
connection_string = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Connect to the database
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# List of CSV files to process
csv_files = [
    'cleaned_reviews_0-250.csv',
    'cleaned_reviews_250-500.csv',
    'cleaned_reviews_500-750.csv',
    'cleaned_reviews_750-1250.csv',
    'cleaned_reviews_1250-end.csv'
]

# Path to the directory containing CSV files
csv_directory = 'path_to_your_csv_files/'  # Update this path

# Loop through each CSV file
for csv_file in csv_files:
    csv_file_path = os.path.join(csv_directory, csv_file)
    
    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    # Insert data into the SQL table
    for index, row in df.iterrows():
        # Prepare the SQL INSERT statement
        sql = """
        INSERT INTO your_table_name (
            author_id, rating, is_recommended, helpfulness,
            total_feedback_count, total_neg_feedback_count,
            total_pos_feedback_count, submission_time,
            review_text, review_title, skin_tone,
            eye_color, skin_type, hair_color,
            product_id, product_name, brand_name, price_usd
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        # Values tuple from the DataFrame row
        values = (
            row['author_id'], row['rating'], row['is_recommended'],
            row['helpfulness'], row['total_feedback_count'],
            row['total_neg_feedback_count'], row['total_pos_feedback_count'],
            row['submission_time'], row['review_text'], row['review_title'],
            row['skin_tone'], row['eye_color'], row['skin_type'],
            row['hair_color'], row['product_id'], row['product_name'],
            row['brand_name'], row['price_usd']
        )

        try:
            cursor.execute(sql, values)
        except Exception as e:
            print(f'Error inserting row {index} from {csv_file}: {e}')

    # Commit the transaction after processing each file
    conn.commit()
    print(f'Successfully uploaded {csv_file}')

# Close the cursor and connection
cursor.close()
conn.close()