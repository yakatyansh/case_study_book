import pandas as pd
from pymongo import MongoClient

# Load data from Excel files
books = pd.read_excel('books.xlsx')
authors = pd.read_excel('authors.xlsx')
sales = pd.read_excel('sales.xlsx')

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['publishing_company']

# Load data into collections
db['books'].insert_many(books.to_dict('records'))
db['authors'].insert_many(authors.to_dict('records'))
db['sales'].insert_many(sales.to_dict('records'))

print("Data loaded successfully!")
