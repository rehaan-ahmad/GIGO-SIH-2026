import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@db:5432/postgres")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize PostGIS and create basic tables."""
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis;"))
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS track_segments (
                id SERIAL PRIMARY KEY,
                segment_id TEXT,
                geom GEOMETRY(LINESTRING, 4326),
                chainage_start FLOAT,
                chainage_end FLOAT
            );
        """))
        conn.commit()

def get_spatial_overlap(task1_km: float, task2_km: float, buffer_m: float = 500.0) -> bool:
    """
    Checks if two chainages are within the buffer distance.
    In a full PostGIS implementation, this would use ST_DWithin on geometries.
    For the hackathon demo, we simulate the spatial check using km arithmetic
    but provide the hook for the real SQL query.
    """
    # Simulating: SELECT ST_DWithin(geom1, geom2, 500) ...
    return abs(task1_km - task2_km) <= (buffer_m / 1000.0)
