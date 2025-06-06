# Aggregator Data API

A FastAPI application that provides access to aggregator data stored in MongoDB using Beanie ODM, with a secure admin interface powered by Starlette Admin.

## Prerequisites

- Python 3.8+
- MongoDB running on port 27057 with the following credentials:
  - Username: periscope
  - Password: pass
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

3. Create a `.env` file in the root directory with your configuration:
```env
# MongoDB Connection
MONGODB_URL=mongodb://periscope:pass@localhost:27057/periscope

# Admin Interface Security
SECRET_KEY=your-secure-secret-key-here  # Generate a secure key using: python -c "import secrets; print(secrets.token_hex(32))"
ADMIN_USERNAME=your-admin-username      # Default: admin
ADMIN_PASSWORD=your-secure-password     # Default: admin123
```

## Running the Application

Start the application using uvicorn:
```bash
uvicorn main:app --reload
```

The API will be available at:
- API: `http://localhost:8000`
- Admin Interface: `http://localhost:8000/admin`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation at `http://localhost:8000/docs`
- ReDoc documentation at `http://localhost:8000/redoc`

## Available Endpoints

### Public API Endpoints
- `GET /`: Welcome message
- `GET /aggregator-data`: Get aggregator data (limited to 3 entries)

### Admin Interface
The admin interface is available at `http://localhost:8000/admin` and provides:

#### Authentication
- Secure login system with session-based authentication
- Configurable credentials via environment variables
- Session management with secure cookies

#### Features
- CRUD operations for aggregator data
- Advanced table view with:
  - Sortable columns
  - Searchable fields
  - Custom filters
  - Pagination
- JSON editor for complex fields
- Computed fields (e.g., store_data_id extracted from nested data)
- Export functionality

#### Available Fields in Admin Interface
- Business ID (biz_id)
- Brand (JSON)
- City
- Store Data (JSON)
- Store Data ID (computed from nested data)
- Location (JSON)
- Message
- Platform (JSON)
- Status
- Store ID
- Timestamp

#### Searchable Fields
- Business ID
- City
- Status
- Store ID
- Store Data ID

#### Sortable Fields
- Timestamp
- Business ID
- City
- Status
- Store Data ID

## Security Considerations

1. **Authentication**
   - Change default admin credentials in production
   - Use strong passwords
   - Store credentials securely in environment variables

2. **Session Security**
   - Uses secure session middleware
   - Session cookies are HTTP-only
   - CSRF protection enabled

3. **Production Deployment**
   - Use HTTPS
   - Set strong SECRET_KEY
   - Use proper MongoDB authentication
   - Consider implementing additional security measures:
     - Rate limiting
     - IP restrictions
     - Two-factor authentication

## Data Structure

The API returns aggregator data in the following format:

```json
{
    "biz_id": "63133506",
    "brand": {
        "id": "181",
        "name": "Burger it up"
    },
    "city": "La Blanca",
    "data": {
        "store": {
            "name": null,
            "menus": [],
            "rating_count": 0,
            "id": "2420319",
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