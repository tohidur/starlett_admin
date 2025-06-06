# Aggregator Data API

A FastAPI application that provides access to aggregator data stored in MongoDB using Beanie ODM.

## Prerequisites

- Python 3.8+
- MongoDB running on port 27057 with the following credentials:
  - Username: periscope
  - Password: UrB@nP!p3R@2023
  - Database: periscope

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the application using uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation at `http://localhost:8000/docs`
- ReDoc documentation at `http://localhost:8000/redoc`

## Available Endpoints

- `GET /`: Welcome message
- `GET /aggregator-data`: Get all aggregator data with parsed JSON fields

## Data Structure

The API returns aggregator data in the following format:

```json
{
    "biz_id": "63133506",
    "brand": null,
    "city": "La Blanca",
    "data": {
        "store": {
            "name": null,
            "menus": [],
            "rating_count": 0,
            "id": null,
            "rating_stars": null,
            "fssai_id": null,
            "lat": null,
            "phone_number": null,
            "address_full": null,
            "cuisines": null,
            "is_available": false,
            "min_order_amount": null,
            "address_area": null,
            "lng": null,
            "city": null
        }
    },
    "location": {
        "id": "48613",
        "name": "LA"
    },
    "message": "Data fetched and processed successfully",
    "platform": {
        "id": "7356",
        "name": "ubereats"
    },
    "status": "success",
    "store_id": "68414eb087e90bf27ce857dd",
    "timestamp": "2025-06-05T08:01:30.876Z"
}
``` 