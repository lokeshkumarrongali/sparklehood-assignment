## Setup Instructions

1. **Clone the repository** and navigate to the project folder.

2. **Create and activate a virtual environment:**
    ```
    python -m venv venv
    # Windows:
    venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

4. **Run the API:**
    ```
    python run.py
    ```
    The API will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Environment Variables

- To use a different database, set the `DATABASE_URL` environment variable before running:
    ```
    export DATABASE_URL=sqlite:///mydb.sqlite3
    ```

---

## API Endpoints

### 1. List All Incidents

**GET** `/incidents`

- **Response:** `200 OK`
- **Example:**
    ```
    curl -X GET http://127.0.0.1:5000/incidents
    ```

---

### 2. Create an Incident

**POST** `/incidents`

- **Request Body:**
    ```
    {
      "title": "Example incident",
      "description": "Details about the incident.",
      "severity": "High"
    }
    ```
- **Response:** `201 Created`
- **Example:**
    ```
    curl -X POST http://127.0.0.1:5000/incidents \
      -H "Content-Type: application/json" \
      -d '{"title":"Example","description":"Details","severity":"High"}'
    ```

---

### 3. Get an Incident by ID

**GET** `/incidents/{id}`

- **Response:** `200 OK` or `404 Not Found`
- **Example:**
    ```
    curl -X GET http://127.0.0.1:5000/incidents/1
    ```

---

### 4. Delete an Incident

**DELETE** `/incidents/{id}`

- **Response:** `204 No Content` or `404 Not Found`
- **Example:**
    ```
    curl -X DELETE http://127.0.0.1:5000/incidents/1
    ```

---

## Error Handling

- All errors return JSON with an `"error"` message and appropriate HTTP status code.
- Common errors:
    - `400 Bad Request` (missing/invalid fields, malformed JSON, wrong content type)
    - `404 Not Found` (non-existent incident or invalid route)
    - `405 Method Not Allowed` (unsupported HTTP method)
    - `500 Internal Server Error` (unexpected errors)

---

## Sample Data

- On startup, the API auto-populates with 3 sample incidents if the database is empty.

---

## Notes

- **In-memory DB:** All data is reset on server restart. For persistence, set a file-based `DATABASE_URL`.
- **Production:** Remove `debug=True` in `run.py` before deploying.

---
