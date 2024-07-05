# Publishing Company Report Generation Script

This Python script utilizes MongoDB to generate a report for a publishing company. It calculates:

* Books carried over from last year's inventory
* Books sold during the current financial year
* Books remaining in the inventory
* Royalty to be paid to each author

The script then stores the report data in a CSV file named `publishing_report.csv` instead of printing it to the console.

## Prerequisites

* Python 3.x
* pymongo library ([https://www.mongodb.com/docs/drivers/pymongo/](https://www.mongodb.com/docs/drivers/pymongo/))

### Installation

1. Install the required library:

   ```bash
   pip install pymongo
   ```

### Usage

1. Update the MongoDB connection string in the script (`MongoClient('mongodb://localhost:27017/')`) if your database server details differ.
2. Ensure your MongoDB database named `publishing_company` has the following collections:
    * `books`: Stores book information (including author ID, price, etc.)
    * `sales`: Stores sales data (including book ID, sale date, quantity sold, etc.)
    * `authors`: Stores author information (including name, email, etc.)
3. Run the script:

   ```bash
   python publishing_report.csv
   ```

This will generate the `publishing_report.csv` file in your current directory.

### Report Contents

The generated CSV file contains the following sections:

* `books_carried_over`: List of documents from the `books` collection representing books carried over from last year.
* `books_sold_current_year`: List of documents resulting from aggregation on the `sales` collection, representing books sold during the current financial year (defined by start and end date variables in the script). Each document includes book ID and total quantity sold.
* `books_remaining_inventory`: List of documents from the `books` collection representing books remaining in the inventory (potentially filtered based on your logic).
* `royalties`: List of documents resulting from aggregation on multiple collections, containing author name, email, and royalty amount calculated based on book sales and author's book price share (defined as 10% in this script).

### Note

This script provides a basic example. You might need to modify it to fit your specific data structure and reporting requirements.
