from translation_service.database import engine
from translation_service.models import Base

Base.metadata.create_all(engine)

print("Database initialized")
