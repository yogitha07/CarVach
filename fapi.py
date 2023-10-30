import psycopg2
from fastapi import FastAPI
from typing import List 
from pydantic import BaseModel

# Update connection string information

host = "pythonfastapi.postgres.database.azure.com"
dbname = "postgres"
user = "fastapi@pythonfastapi"
password = "apifast1234*"
sslmode = "require"

# FastAPI setup
app = FastAPI()

# Construct connection string

conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)

# Function to establish a database connection
def get_db():
    conn = psycopg2.connect(conn_string)
    print("Connection established")
    try:
        yield conn
    finally:
        conn.close()


# Create a model for CRUD operations
class InventoryItem(BaseModel):
    id: int
    name: str
    quantity: int



# conn = psycopg2.connect(conn_string)
# print("Connection established")

# API endpoint to create the table
@app.post("/create-table/")
async def create_table():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Table created successfully"}


# API endpoint to insert data into the table
@app.post("/insert-data/")
async def insert_data(name: str, quantity: int):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventory (name, quantity) VALUES (%s, %s);", (name, quantity))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Data inserted successfully"}


# Create endpoint for reading all items
@app.get("/items/", response_model=List[InventoryItem])
async def get_items():
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity FROM inventory;")
    items = [InventoryItem(id=id, name=name, quantity=quantity) for id, name, quantity in cursor.fetchall()]
    cursor.close()
    conn.close()
    return items

# Create endpoint for reading a single item by ID
@app.get("/items/{item_id}", response_model=InventoryItem)
async def read_item(item_id: int):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, quantity FROM inventory WHERE id = %s;", (item_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        id, name, quantity = result
        return InventoryItem(id=id, name=name, quantity=quantity)  # Create a Pydantic model instance
    else:
        return None
    
# Create endpoint for updating an item
@app.put("/items/{item_id}/")
async def update_item(item_id: int, name: str, quantity: int):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("UPDATE inventory SET name = %s, quantity = %s WHERE id = %s;", (name, quantity, item_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Item updated successfully"}

# Create endpoint for deleting an item
@app.delete("/items/{item_id}/")
async def delete_item(item_id: int):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM inventory WHERE id = %s;", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "Item deleted successfully"}

# cursor = conn.cursor()

# # Drop previous table of same name if one exists

# cursor.execute("DROP TABLE IF EXISTS catalogue;")
# print("Finished dropping table (if existed)")

# # Create a table

# cursor.execute("CREATE TABLE catalogue (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
# print("Finished creating table")

# # Insert some data into the table

# cursor.execute("INSERT INTO catalogue (name, quantity) VALUES (%s, %s);", ("banana", 150))
# cursor.execute("INSERT INTO catalogue (name, quantity) VALUES (%s, %s);", ("orange", 154))
# cursor.execute("INSERT INTO catalogue (name, quantity) VALUES (%s, %s);", ("apple", 100))
# print("Inserted 3 rows of data")


# # Fetch all rows from table

# cursor.execute("SELECT * FROM catalogue;")
# rows = cursor.fetchall()

# # Print all rows

# for row in rows:
#     print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

# # Clean up

# conn.commit()
# cursor.close()
# conn.close()