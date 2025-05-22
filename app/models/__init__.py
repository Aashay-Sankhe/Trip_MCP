from app.database_init import Base
from .UserModel import User
from .BlogModel import Blog

# This makes Base available when importing from app.models
__all__ = ['Base', 'User', 'Blog']
