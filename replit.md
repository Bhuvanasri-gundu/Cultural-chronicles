# Cultural Chronicles - Heritage Archive

## Overview

Cultural Chronicles is an AI-powered Streamlit web application designed to preserve and promote India's diverse cultural heritage through multilingual storytelling. The platform allows users to submit cultural stories in any Indian language, browse an archive of heritage content, and search through stories with intelligent filtering. The application features AI-powered language detection, automatic story classification, image upload capabilities, and comprehensive metadata management for cultural preservation.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework chosen for rapid development and deployment with minimal frontend complexity
- **Navigation**: Multi-page application using `streamlit-option-menu` for enhanced sidebar navigation between submit, browse, and search functionalities
- **Layout**: Wide layout configuration with expandable sidebar for optimal content display across different screen sizes
- **Styling**: Custom CSS with orange gradient backgrounds and responsive design cards for engaging visual presentation
- **User Interface**: Interactive forms with real-time validation, pagination controls, and expandable content sections

### Backend Architecture
- **Application Structure**: Modular Python architecture with clear separation between pages, utilities, and AI models
- **Data Processing**: Pandas-based data manipulation for story filtering, sorting, and statistical analysis
- **AI Processing**: Pattern-based language detection using Unicode script ranges with HuggingFace Transformers as optional enhancement
- **Story Classification**: Keyword-based categorization system for cultural content types (Folk Tale, Legend, Festival, Recipe, etc.)
- **Image Processing**: PIL-based image optimization with automatic resizing, format conversion, and quality compression
- **Caching**: Streamlit caching mechanisms for ultra-fast data access and 5-second loading times

### Data Storage Solutions
- **Primary Database**: PostgreSQL with SQLAlchemy ORM for production environments providing ACID compliance and advanced querying
- **Fallback Database**: SQLite with file-based storage for development and lightweight deployments
- **Database Schema**: Single Stories table with comprehensive metadata including title, content, translations, language, category, region, community, and timestamps
- **File Storage**: Local filesystem storage for uploaded cultural images with UUID-based naming and directory organization
- **Sample Data**: Pre-populated database with 6 diverse cultural stories across multiple Indian languages for demonstration

### Authentication and Authorization
- **Current Implementation**: No authentication system implemented - open access application
- **Access Control**: All features available to all users without restrictions
- **Data Privacy**: Stories are publicly accessible once submitted to the archive

## External Dependencies

### Core Web Framework
- **Streamlit**: Primary web framework for UI rendering and user interaction
- **streamlit-option-menu**: Enhanced navigation menu component for sidebar functionality

### Data Processing and Storage
- **pandas**: Data manipulation and analysis for story filtering and statistics
- **SQLAlchemy**: ORM framework for database operations and schema management
- **psycopg2-binary**: PostgreSQL database adapter for production deployments

### AI and Machine Learning
- **transformers** (Optional): HuggingFace library for advanced language detection using XLM-RoBERTa model
- **torch** (Optional): PyTorch backend for transformer model execution
- **Pattern-based AI**: Fallback system using Unicode script detection for language identification

### Image Processing
- **Pillow (PIL)**: Image manipulation library for upload processing, resizing, and optimization

### Development and Deployment
- **Replit**: Cloud development and deployment platform
- **uv**: Package manager for dependency management
- **Python 3.11+**: Runtime environment with modern language features

### Database Systems
- **PostgreSQL**: Production database with advanced querying and ACID compliance
- **SQLite**: Development and fallback database for lightweight deployments

### File System Dependencies
- **Local Storage**: File system access for image uploads and database files
- **Directory Management**: Automatic creation of data and uploads directories