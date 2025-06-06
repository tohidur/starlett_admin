import os
from typing import List, Optional, Any
from fastapi import FastAPI, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models import AggregatorData, AggregatorDataResponse
from dotenv import load_dotenv
from starlette_admin.contrib.beanie import Admin, ModelView
from starlette_admin.fields import DateTimeField, StringField, JSONField, BaseField
from starlette_admin.auth import AuthProvider, User
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import secrets

# Load environment variables
load_dotenv()

# Generate a secure secret key for sessions
SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))

app = FastAPI(title="Aggregator Data API")

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# Admin credentials - in production, these should be in environment variables
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")  # Change this in production!

class AdminAuthProvider(AuthProvider):
    """Custom authentication provider for admin interface"""
    
    async def login(self, username: str, password: str) -> Optional[User]:
        """Validate admin credentials"""
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return User(username=username)
        return None

    async def is_authenticated(self, request: Request) -> bool:
        """Check if user is authenticated"""
        return "admin_user" in request.session

    async def get_current_user(self, request: Request) -> Optional[User]:
        """Get current authenticated user"""
        if "admin_user" in request.session:
            return User(username=request.session["admin_user"])
        return None

    async def login_view(self, request: Request) -> Any:
        """Handle login form submission"""
        if request.method == "POST":
            form = await request.form()
            username = form.get("username")
            password = form.get("password")
            
            if user := await self.login(username, password):
                request.session["admin_user"] = user.username
                return RedirectResponse(request.url_for("admin:index"), status_code=303)
            
            return {"error": "Invalid credentials"}
        
        return None

    async def logout(self, request: Request) -> Any:
        """Handle logout"""
        request.session.pop("admin_user", None)
        return RedirectResponse(request.url_for("admin:login"))

class StoreDataIDField(BaseField):
    """Custom field for store_data_id that extracts ID from nested data"""
    def __init__(self, name: str, **kwargs):
        super().__init__(name, **kwargs)
        self.readonly = True

    def get_value(self, obj: Any) -> Optional[str]:
        try:
            if isinstance(obj.data, dict) and 'store' in obj.data:
                store = obj.data['store']
                if isinstance(store, dict) and 'id' in store:
                    return str(store['id'])
        except (KeyError, TypeError, AttributeError):
            pass
        return None

# Create admin interface with authentication
admin = Admin(
    title="Aggregator Data Admin",
    base_url="/admin",
    auth_provider=AdminAuthProvider(),
)

# Custom ModelView for AggregatorData
class AggregatorDataView(ModelView):
    name = "Aggregator Data"
    icon = "fa fa-database"
    identity = "aggregator_data"
    
    # Define fields for the admin interface
    fields = [
        StringField("biz_id", label="Business ID"),
        JSONField("brand", label="Brand"),
        StringField("city", label="City"),
        JSONField("data", label="Store Data"),
        StoreDataIDField("store_data_id", label="Store Data ID"),
        JSONField("location", label="Location"),
        StringField("message", label="Message"),
        JSONField("platform", label="Platform"),
        StringField("status", label="Status"),
        StringField("store_id", label="Store ID"),
        DateTimeField("timestamp", label="Timestamp"),
    ]
    
    # Define list view columns
    list_fields = [
        "biz_id",
        "city",
        "status",
        "store_data_id",
        "timestamp",
        "store_id"
    ]
    
    # Define searchable fields
    searchable_fields = [
        "biz_id",
        "city",
        "status",
        "store_id",
        "store_data_id"
    ]
    
    # Define sortable fields
    sortable_fields = [
        "timestamp",
        "biz_id",
        "city",
        "status",
        "store_data_id"
    ]

    async def get_list_query(self, request, **kwargs):
        """Override to add filtering for store_data_id"""
        query = await super().get_list_query(request, **kwargs)
        
        # Get filter value for store_data_id if present
        store_data_id = request.query_params.get("store_data_id")
        if store_data_id:
            # Add a filter to match documents where data.store.id equals the filter value
            query = query.find({"data.store.id": store_data_id})
        
        return query

@app.on_event("startup")
async def startup_event():
    # MongoDB connection with the specified credentials
    client = AsyncIOMotorClient("mongodb://periscope:UrB%40nP!p3R%402023@localhost:27057/periscope")
    
    # Initialize beanie with the AggregatorData document
    await init_beanie(database=client.periscope, document_models=[AggregatorData])
    
    # Add the view to admin with the document parameter
    admin.add_view(AggregatorDataView(document=AggregatorData))
    
    # Mount admin to the app
    admin.mount_to(app)

@app.get("/")
async def root():
    return {"message": "Welcome to Aggregator Data API"}

@app.get("/aggregator-data", response_model=List[AggregatorDataResponse])
async def get_aggregator_data():
    try:
        # Fetch aggregator data with a limit of 3 entries
        data = await AggregatorData.find_all().limit(3).to_list()
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 