import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL", "postgresql://postgres:postgres@db:5432/postgres")
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    Initializes the database schema, including the PostGIS extension
    and the track_segments table for spatial indexing.
    """
    try:
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
    except Exception as e:
        print(f"Warning: Database connection failed ({e}). Running in standalone fallback mode.")

def get_spatial_overlap(task1_km: float, task2_km: float, buffer_m: float = 500.0) -> bool:
    """
    Determines if two track locations are within the specified safety buffer.

    Currently implements a linear distance approximation. This function serves as
    the interface for future migration to PostGIS ST_DWithin queries.
    """
    return abs(task1_km - task2_km) <= (buffer_m / 1000.0)
