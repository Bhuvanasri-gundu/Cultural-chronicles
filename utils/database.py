"""
Database Configuration - Cultural Chronicles

This module handles database connection, table creation, and schema management
with support for both PostgreSQL and SQLite fallback.
"""

import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, MetaData, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create declarative base
Base = declarative_base()

class Story(Base):
    """Story model for database table"""
    __tablename__ = 'stories'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    original_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=True)
    detected_language = Column(String(50), nullable=True)
    category = Column(String(100), nullable=True)
    region = Column(String(100), nullable=True)
    community = Column(String(100), nullable=True)
    story_type = Column(String(50), nullable=True)
    language_hint = Column(String(50), nullable=True)
    image_path = Column(String(255), nullable=True)
    timestamp = Column(DateTime, default=func.now(), nullable=False)
    
    def __repr__(self):
        return f"<Story(id={self.id}, title='{self.title}', language='{self.detected_language}')>"

def get_database_connection():
    """
    Create and return a database connection with fallback mechanism
    
    Returns:
        sqlalchemy.Engine: Database engine instance
    """
    try:
        # Try PostgreSQL first (production)
        database_url = os.getenv('DATABASE_URL')
        if database_url:
            logger.info("Attempting PostgreSQL connection...")
            engine = create_engine(database_url, echo=False)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("PostgreSQL connection successful")
            
            # Create tables
            Base.metadata.create_all(engine)
            logger.info("Database tables created/verified")
            
            return engine
            
    except Exception as e:
        logger.warning(f"PostgreSQL connection failed: {str(e)}")
    
    try:
        # Try individual PostgreSQL environment variables
        pg_params = {
            'host': os.getenv('PGHOST'),
            'port': os.getenv('PGPORT', '5432'),
            'database': os.getenv('PGDATABASE'),
            'username': os.getenv('PGUSER'),
            'password': os.getenv('PGPASSWORD')
        }
        
        if all(pg_params.values()):
            pg_url = f"postgresql://{pg_params['username']}:{pg_params['password']}@{pg_params['host']}:{pg_params['port']}/{pg_params['database']}"
            logger.info("Attempting PostgreSQL connection with individual parameters...")
            
            engine = create_engine(pg_url, echo=False)
            
            # Test connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            
            logger.info("PostgreSQL connection successful")
            
            # Create tables
            Base.metadata.create_all(engine)
            logger.info("Database tables created/verified")
            
            return engine
            
    except Exception as e:
        logger.warning(f"PostgreSQL connection with parameters failed: {str(e)}")
    
    # Fallback to SQLite
    try:
        logger.info("Falling back to SQLite database...")
        os.makedirs("data", exist_ok=True)
        sqlite_path = os.path.join("data", "cultural_chronicles.db")
        sqlite_url = f"sqlite:///{sqlite_path}"
        
        engine = create_engine(sqlite_url, echo=False)
        
        # Test connection and create tables
        Base.metadata.create_all(engine)
        logger.info(f"SQLite database created at: {sqlite_path}")
        
        return engine
        
    except Exception as e:
        logger.error(f"SQLite fallback failed: {str(e)}")
        raise Exception("All database connection attempts failed")

def initialize_database():
    """
    Initialize the database with tables
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        engine = get_database_connection()
        Base.metadata.create_all(engine)
        logger.info("Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Database initialization failed: {str(e)}")
        return False

def check_database_health():
    """
    Check if database is accessible and responsive
    
    Returns:
        dict: Health check results
    """
    try:
        engine = get_database_connection()
        
        with engine.connect() as conn:
            # Test basic query
            result = conn.execute("SELECT 1 as test")
            test_value = result.fetchone()[0]
            
            if test_value == 1:
                return {
                    "status": "healthy",
                    "database_type": "PostgreSQL" if "postgresql" in str(engine.url) else "SQLite",
                    "connection": "successful"
                }
            else:
                return {
                    "status": "unhealthy",
                    "error": "Test query failed"
                }
                
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }

# Export the engine for use in other modules
_engine = None

def get_engine():
    """Get the shared database engine instance"""
    global _engine
    if _engine is None:
        _engine = get_database_connection()
    return _engine
