Below is a comprehensive README that covers setup instructions, API documentation, sample query examples, and testing guidelines with both cURL commands and Postman collection details.

---

```markdown
# Gen AI Analytics Mini Data Query Simulation Engine

A lightweight backend service that simulates an AI-powered data query system. This tool empowers non-technical teams to ask complex business questions in natural language and receive data insights without direct dependency on the data team.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
  - [/query](#query)
  - [/explain](#explain)
  - [/validate](#validate)
- [Sample Query Examples](#sample-query-examples)
- [Testing with cURL and Postman](#testing-with-curl-and-postman)
- [License](#license)

## Features

- **Natural Language Query Conversion:** Convert simple natural language queries to pseudo-SQL.
- **Simulated Response:** Generates a mock response to illustrate data retrieval.
- **Query Explanation:** Provides step-by-step breakdown of how the query was translated.
- **Query Validation:** Checks for dangerous or invalid queries.
- **Lightweight Authentication:** Uses header-based API key authentication.

## Requirements

- Python 3.7+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [SQLite3](https://docs.python.org/3/library/sqlite3.html) (in-memory, no additional installation needed)

You can install the required Python packages using:

```bash
pip install fastapi uvicorn
```

A sample `requirements.txt` file:
```
fastapi>=0.68.0
uvicorn>=0.15.0
```

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/gen-ai-analytics-simulation.git
   cd gen-ai-analytics-simulation
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Review the Code:**

   - The main API implementation is in `main.py` (or your chosen filename).
   - Authentication is implemented via a simple header-based token. The code expects an API key of `secret-token` (or use alias `api_key` if you update the header alias).

4. **Database Setup:**

   The application uses an in-memory SQLite database with dummy sales data for all 12 months. No additional database setup is needed.

## Running the Application

Start the FastAPI server using Uvicorn. For example, if your main application file is named `main.py` and the FastAPI app is defined as `app`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Once started, you should see output indicating that the server is running (e.g., on `http://0.0.0.0:8000`).

## API Documentation

FastAPI automatically generates interactive API documentation. After starting the server, open your browser and navigate to:

- **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

### /query

- **Method:** POST
- **Description:** Converts a natural language query to a pseudo-SQL query and returns a simulated response.
- **Request Header:**  
  - `Content-Type: application/json`
  - `api_key: secret-token`
- **Request Body Example:**

  ```json
  {
    "query": "January sales"
  }
  ```

- **Response Example:**

  ```json
  {
    "pseudo_sql": "SELECT * FROM sales WHERE description LIKE '%January sales%'",
    "result": {
      "data": "Simulated response based on the query",
      "query_executed": "SELECT * FROM sales WHERE description LIKE '%January sales%'"
    }
  }
  ```

### /explain

- **Method:** POST
- **Description:** Provides a step-by-step breakdown of how the natural language query was translated.
- **Request Header:** Same as `/query`.
- **Request Body Example:**

  ```json
  {
    "query": "January sales"
  }
  ```

- **Response Example:**

  ```json
  {
    "original_query": "January sales",
    "steps": [
      "Parsed the natural language query.",
      "Identified keywords and mapped them to the 'sales' table columns.",
      "Constructed a pseudo SQL query based on the identified keywords."
    ]
  }
  ```

### /validate

- **Method:** POST
- **Description:** Checks if the query is valid and free from dangerous keywords.
- **Request Header:** Same as above.
- **Request Body Example:**

  ```json
  {
    "query": "January sales"
  }
  ```

- **Response Example:**

  ```json
  {
    "valid": true,
    "message": "Query is feasible."
  }
  ```

- **Error Example (for invalid queries):**

  If a query contains forbidden keywords (e.g., `"DROP TABLE sales"`):

  ```json
  {
    "detail": "Query contains invalid keywords."
  }
  ```

## Sample Query Examples

- **Example 1: Query Sales Data**
  - **Input:** `"January sales"`
  - **Pseudo-SQL:** `SELECT * FROM sales WHERE description LIKE '%January sales%'`
  - **Response:** Simulated result along with the executed pseudo-SQL.

- **Example 2: Explain Query Translation**
  - **Input:** `"February sales"`
  - **Response:** A breakdown that includes parsing the query and mapping `"February sales"` to the appropriate database field.

- **Example 3: Validate a Query**
  - **Input:** `"DROP TABLE sales"`
  - **Response:** HTTP 400 error with a message stating that the query contains invalid keywords.

## Testing with cURL and Postman

### cURL Commands

Make sure your FastAPI server is running on `http://localhost:8000`.

- **Test `/query`:**

  ```bash
  curl -X POST "http://localhost:8000/query" \
       -H "Content-Type: application/json" \
       -H "api_key: secret-token" \
       -d "{\"query\":\"January sales\"}"
  ```

- **Test `/explain`:**

  ```bash
  curl -X POST "http://localhost:8000/explain" \
       -H "Content-Type: application/json" \
       -H "api_key: secret-token" \
       -d "{\"query\":\"January sales\"}"
  ```

- **Test `/validate`:**

  ```bash
  curl -X POST "http://localhost:8000/validate" \
       -H "Content-Type: application/json" \
       -H "api_key: secret-token" \
       -d "{\"query\":\"January sales\"}"
  ```

### Postman Collection

1. **Create a New Collection in Postman:**
   - Name the collection (e.g., "Gen AI Analytics API Test").

2. **Add Environment Variables (Optional):**
   - **baseUrl:** `http://localhost:8000`
   - **api_key:** `secret-token`

3. **Set Up Requests:**

   - **/query Request:**
     - **Method:** POST
     - **URL:** `{{baseUrl}}/query`
     - **Headers:** 
       - `Content-Type: application/json`
       - `api_key: {{api_key}}`
     - **Body (raw, JSON):**
       ```json
       {
         "query": "January sales"
       }
       ```

   - **/explain Request:**
     - **Method:** POST
     - **URL:** `{{baseUrl}}/explain`
     - **Headers:** Same as `/query`.
     - **Body (raw, JSON):**
       ```json
       {
         "query": "January sales"
       }
       ```

   - **/validate Request:**
     - **Method:** POST
     - **URL:** `{{baseUrl}}/validate`
     - **Headers:** Same as `/query`.
     - **Body (raw, JSON):**
       ```json
       {
         "query": "January sales"
       }
       ```

4. **Save and Organize the Requests:**
   - Save each request in the collection and group them under folders (e.g., "Valid Tests" and "Error Tests").

5. **Export the Collection (Optional):**
   - To share the collection, click on the collection's ellipsis (three dots) and select **Export** to save it as a JSON file.

## License

This project is licensed under the [MIT License](LICENSE).

---

Happy querying!
```

---

This README provides all necessary details—from setting up the project and running the FastAPI server to detailed API documentation and testing instructions using both cURL and Postman. Feel free to customize it further based on your specific needs or project changes.