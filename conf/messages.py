import pandas as pd


def get_app_messages():
    df = pd.DataFrame(columns=['short_name', 'english', 'russian'])
    messages=['Register new product',
              'Register new category',
              'Show all products',
              'There are no products in database',
              'Enter category name',
              'Enter category description',
              'Recorded new category.',
              'Category id',
              'Category name',
              'Category Description',
              'Enter product name',
              'Enter product description',
              'Enter product price',
              'Upload product photo',
              'Registered new product.',
              'Product id',
              'Product name',
              'Product description',
              'Product price',
              'Choose category for the product',
              'Set product category.',
              'Edit product',
              'Remove product']
