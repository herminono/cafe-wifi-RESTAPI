# ☕ Cafe & WiFi REST API

A RESTful API built with **Python, Flask, and SQLAlchemy** to retrieve, search, add, update, and delete cafe information.

The API stores cafe locations, seating capacity, coffee prices, WiFi availability, power sockets, and other amenities.

## Features

- Retrieve all cafes, sorted alphabetically
- Retrieve a random cafe
- Search for cafes by location
- Add a cafe
- Update a cafe's coffee price
- Delete a cafe with an API key
- Store data in a SQLite database

## Technologies

- Python
- Flask
- Flask-SQLAlchemy / SQLAlchemy
- SQLite
- HTML (simple home page)

## Project Structure

```text
cafe-wifi-api/
├── main.py
├── templates/
│   └── index.html
├── requirements.txt
├── .gitignore
└── README.md
```

The local SQLite database is not included in the repository.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the placeholders with your GitHub repository details.

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```powershell
venv\Scripts\activate
```

macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
python main.py
```

Open `http://127.0.0.1:5000/`.

The application calls `db.create_all()` to create missing tables. **A newly created database contains no cafe records**; use `POST /add` to add data before testing endpoints that require records.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Display the welcome page |
| GET | `/all` | List cafes sorted by name |
| GET | `/random` | Get a random cafe |
| GET | `/search?loc=London` | Search for cafes with the specified location |
| POST | `/add` | Add a cafe using form fields |
| PATCH | `/update-price/1?new_price=£4.00` | Update cafe 1's coffee price |
| DELETE | `/report-closed/1?api-key=YOUR_API_KEY` | Delete cafe 1 with an API key |

### GET `/all`

Example response (illustrative data):

```json
{
  "cafes": [
    {
      "id": 1,
      "name": "Example Cafe",
      "map_url": "https://maps.google.com/",
      "img_url": "https://example.com/cafe.jpg",
      "location": "London",
      "seats": "20-30",
      "has_toilet": true,
      "has_wifi": true,
      "has_sockets": true,
      "can_take_calls": false,
      "coffee_price": "£3.50"
    }
  ]
}
```

### GET `/random`

Returns a `cafe` object with the same fields as above. **Note:** In the original implementation, an empty database causes this endpoint to error; an empty-list check is recommended.

### GET `/search?loc=London`

Searches by exact location string. Returns matching cafes in the `cafe` array, or HTTP `404` if no cafes match.

### POST `/add`

Send the following fields as **`x-www-form-urlencoded`** or **`form-data`**, not raw JSON:

| Field | Example | Required by database? |
|---|---|---|
| `name` | `Example Cafe` | Yes (unique) |
| `map_url` | `https://maps.google.com/` | Yes |
| `img_url` | `https://example.com/cafe.jpg` | Yes |
| `loc` | `London` | Yes |
| `sockets` | `true` | Yes |
| `toilet` | `true` | Yes |
| `wifi` | `true` | Yes |
| `calls` | `false` | Yes |
| `seats` | `20-30` | Yes |
| `coffee_price` | `£3.50` | No |

The original implementation returns HTTP `200` with a success message when a cafe is added. **Important:** Its `bool(request.form.get(...))` conversion treats nonempty strings such as `"false"` as `True`. Correct the Boolean parsing before depending on those submitted values.

### PATCH `/update-price/<cafe_id>?new_price=<price>`

Updates the specified cafe's `coffee_price`. Returns the updated record. Returns HTTP `400` if `new_price` is missing, or HTTP `404` if the cafe ID does not exist.

### DELETE `/report-closed/<cafe_id>?api-key=<key>`

Deletes a cafe if the API key matches. Invalid API keys return HTTP `403`.

**Note:** The original implementation needs its missing-cafe handling fixed: `db.session.get()` returns `None` for an unknown ID, rather than raising `AttributeError`.

## Database Schema

| Column | Type |
|---|---|
| `id` | Integer, primary key |
| `name` | String, unique |
| `map_url` | String |
| `img_url` | String |
| `location` | String |
| `seats` | String |
| `has_toilet` | Boolean |
| `has_wifi` | Boolean |
| `has_sockets` | Boolean |
| `can_take_calls` | Boolean |
| `coffee_price` | String, nullable |

## Testing

Use Postman or another HTTP client to send requests. For `POST /add`, choose **Body → x-www-form-urlencoded** and provide the relevant fields. For PATCH and DELETE, provide the URL parameters shown above.

## Security Notes

The current API key is a hardcoded demonstration key, not production authentication. Replace it with a secret read from an environment variable before deploying publicly. Keep `.env` files and local databases out of Git, and disable Flask debug mode in production.

## Possible Improvements

- Better request validation and error handling
- JSON request-body support
- Pagination and filtering
- Automated API tests
- Secure authentication and authorization
- Cloud deployment

## Acknowledgments

This project was developed as a hands-on learning exercise following a Python web development tutorial. Add the specific tutorial name and link here to give proper credit.

## License

No license has been specified. This project is shared for educational and portfolio review purposes.
