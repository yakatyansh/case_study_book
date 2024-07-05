import csv
from pymongo import MongoClient
from datetime import datetime

client = MongoClient('mongodb://localhost:27017/')
db = client['publishing_company']

# Calculate books carried over from last year's inventory
books_carried_over = db.books.find({})

# Calculate books sold during the current financial year
start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)
sales_current_year = db.sales.aggregate([
    {"$match": {"sale_date": {"$gte": start_date, "$lte": end_date}}},
    {"$group": {"_id": "$book_id", "total_sold": {"$sum": "$quantity_sold"}}}
])

# Calculate books remaining in the inventory
books_remaining = db.books.find({})

# Calculate royalty to be paid to each author
royalties = db.sales.aggregate([
    {"$match": {"sale_date": {"$gte": start_date, "$lte": end_date}}},
    {"$group": {"_id": "$book_id", "total_sold": {"$sum": "$quantity_sold"}}},
    {"$lookup": {
        "from": "books",
        "localField": "_id",
        "foreignField": "book_id",
        "as": "book_info"
    }},
    {"$unwind": "$book_info"},
    {"$lookup": {
        "from": "authors",
        "localField": "book_info.author_id",
        "foreignField": "author_id",
        "as": "author_info"
    }},
    {"$unwind": "$author_info"},
    {"$project": {
        "author_name": "$author_info.name",
        "author_email": "$author_info.email",
        "royalty": {"$multiply": ["$total_sold", "$book_info.price", 0.1]}
    }}
])

report = {
    "books_carried_over": list(books_carried_over),
    "books_sold_current_year": list(sales_current_year),
    "books_remaining_inventory": list(books_remaining),
    "royalties": list(royalties)
}

# Open CSV file for writing
with open('publishing_report.csv', 'w', newline='') as csvfile:
  fieldnames = []  # Define fieldnames dynamically
  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

  # Write header row based on first element of each section
  for section, data in report.items():
    if data:
      fieldnames.extend(data[0].keys())
      break  # Only need fieldnames from the first non-empty section
  writer.writeheader()

  # Write data rows for each section
  for section, data in report.items():
    for item in data:
      writer.writerow(item)

print("Report generated and saved to publishing_report.csv")
