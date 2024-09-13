# Sephora Product Recommendation System

## Overview

This document provides an overview of the Product Recommendation System implemented in Python using Tkinter for the GUI. The application allows users to receive personalized product recommendations based on various skin and hair attributes.

## Features

- **User Input Options**: Select skin tone, eye color, skin type, hair color, and minimum rating.
- **Dynamic Filtering**: Categories update based on selected skin type.
- **Multiple Brand Selection**: Users can choose multiple brands from a scrollable list.
- **Formatted Output**: Recommendations displayed clearly with product details.

## Requirements

- **Python Version**: 3.x
- **Libraries**:
  - `pandas`
  - `tkinter` (included with Python)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install Required Packages**:
   ```bash
   pip install pandas
   ```

3. **Prepare Data**:
   - Ensure `cleaned_product_info.csv` and `cleaned_reviews_*.csv` are in the same directory as your script.
   - The dataset should contain the necessary columns for product and review information.

## Usage

1. **Run the Application**:
   ```bash
   python product_recommendation_system.py
   ```

2. **Select Preferences**:
   - Choose skin tone, eye color, skin type, hair color, and rating.

3. **Select Categories and Brands**:
   - Use dropdowns for category selection and a list for brands.

4. **Get Recommendations**:
   - Click "Get Recommendations" to display personalized product suggestions.

## Example Output

Recommendations will include:

- Product ID
- Product Name
- Brand Name
- Loves Count
- Rating
- Reviews
- Price

## Troubleshooting

- Ensure CSV files are correctly formatted and contain required columns.
- Check that all necessary libraries are installed.
- Verify selections if no recommendations are displayed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
