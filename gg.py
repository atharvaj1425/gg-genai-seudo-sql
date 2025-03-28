from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import Optional
import sqlite3

# Initialize FastAPI app
app = FastAPI(
    title="Gen AI Analytics Mini Data Query Simulation Engine",
    description="A lightweight simulation backend for converting natural language queries into pseudo-SQL and returning mock responses.",
    version="1.0.0"
)

# Create an in-memory SQLite database for simulation purposes
connection = sqlite3.connect(":memory:", check_same_thread=False)
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    amount REAL,
    date TEXT,
    description TEXT
)
""")
# Inserting realistic dummy data for 12 months
dummy_data = [
    (100.0, '2023-01-15', 'January sales'),
    (150.0, '2023-02-15', 'February sales'),
    (200.0, '2023-03-15', 'March sales'),
    (250.0, '2023-04-15', 'April sales'),
    (300.0, '2023-05-15', 'May sales'),
    (350.0, '2023-06-15', 'June sales'),
    (400.0, '2023-07-15', 'July sales'),
    (450.0, '2023-08-15', 'August sales'),
    (500.0, '2023-09-15', 'September sales'),
    (550.0, '2023-10-15', 'October sales'),
    (600.0, '2023-11-15', 'November sales'),
    (650.0, '2023-12-15', 'December sales'),
]
cursor.executemany("INSERT INTO sales (amount, date, description) VALUES (?, ?, ?)", dummy_data)
connection.commit()

# Authentication dependency using a simple header-based token
def get_api_key(api_key: Optional[str] = Header(None, alias="api_key")):
    print("DEBUG: Received API key:", api_key)
    if api_key != "secret-token":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return api_key


# Request model for endpoints that accept a natural language query
class QueryRequest(BaseModel):
    query: str

# Response model for the /query endpoint
class QueryResponse(BaseModel):
    pseudo_sql: str
    result: dict

@app.post("/query", response_model=QueryResponse)
def query(query_request: QueryRequest, api_key: str = Depends(get_api_key)):
    """
    Simulate AI-powered query processing:
    - Converts a natural language query to pseudo-SQL.
    - Returns a mock response.
    """
    nl_query = query_request.query.strip()
    if not nl_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Dummy conversion: mapping the natural language query to a pseudo SQL statement.
    pseudo_sql = f"SELECT * FROM sales WHERE description LIKE '%{nl_query}%'"
    
    # Generate a mock response (in a real scenario, execute pseudo_sql on the database)
    result = {
        "data": "Simulated response based on the query",
        "query_executed": pseudo_sql
    }
    
    return QueryResponse(pseudo_sql=pseudo_sql, result=result)

@app.post("/explain")
def explain(query_request: QueryRequest, api_key: str = Depends(get_api_key)):
    """
    Provides a breakdown of how the natural language query was translated.
    """
    nl_query = query_request.query.strip()
    if not nl_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    explanation = {
        "original_query": nl_query,
        "steps": [
            "Parsed the natural language query.",
            "Identified keywords and mapped them to the 'sales' table columns.",
            "Constructed a pseudo SQL query based on the identified keywords."
        ]
    }
    return explanation

@app.post("/validate")
def validate(query_request: QueryRequest, api_key: str = Depends(get_api_key)):
    """
    Validates if the query is feasible by performing basic checks.
    """
    nl_query = query_request.query.strip()
    if not nl_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")

    # Basic check for potentially dangerous or unsupported keywords
    if "drop" in nl_query.lower():
        raise HTTPException(status_code=400, detail="Query contains invalid keywords.")
    
    return {"valid": True, "message": "Query is feasible."}

# Optional: Run the app using Uvicorn if this script is executed directly.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
