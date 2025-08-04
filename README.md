# Cultural Chronicles 🏛️

> Preserving India's Rich Cultural Heritage Through Digital Storytelling

Cultural Chronicles is an AI-powered web platform dedicated to collecting, preserving, and sharing the diverse cultural stories of India. Built with Streamlit, this application enables communities to submit their heritage stories in any Indian language while providing intelligent categorization and multilingual support.

## ✨ Features

### 🌍 Multilingual Support
- Submit stories in any Indian language
- AI-powered language detection
- Pattern-based script recognition
- Unicode support for all Indian scripts

### 📚 Story Management
- Submit new cultural stories with rich metadata
- Browse existing heritage archive
- Advanced search and filtering capabilities
- Story categorization (Folk Tales, Legends, Festivals, Recipes, etc.)

### 🎨 Rich Media Support
- Image upload and optimization
- Automatic image resizing and compression
- Cultural artifacts preservation
- Visual storytelling enhancement

### 🔍 Intelligent Search
- Filter by language, category, region, and community
- Date-based story discovery
- Full-text search capabilities
- Cultural content classification

### ⚡ Performance Optimized
- Sub-5-second loading times
- Streamlit caching for ultra-fast access
- Responsive pagination system
- Optimized database queries

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- PostgreSQL (optional - SQLite fallback included)

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/cultural-chronicles.git
cd cultural-chronicles

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py --server.port 5000
```

### Database Setup
The application supports both PostgreSQL and SQLite:

#### PostgreSQL (Recommended for Production)
```bash
# Set environment variable
export DATABASE_URL="postgresql://username:password@localhost/cultural_chronicles"
```

#### SQLite (Development/Fallback)
No additional setup required - SQLite database is created automatically.

## 🏗️ Architecture

### Frontend
- **Framework**: Streamlit with responsive design
- **Navigation**: Multi-page architecture with sidebar menu
- **Styling**: Custom CSS with cultural orange gradient theme
- **UI Components**: Interactive forms, pagination, expandable content

### Backend
- **Language**: Python 3.11+
- **Database**: PostgreSQL with SQLite fallback
- **ORM**: SQLAlchemy for database operations
- **AI**: Pattern-based language detection with optional HuggingFace integration
- **Image Processing**: PIL for upload optimization

### Data Storage
- **Primary**: PostgreSQL for production environments
- **Fallback**: SQLite for development and lightweight deployments
- **Files**: Local filesystem storage for cultural images
- **Caching**: Streamlit native caching for performance

## 📋 Usage

### Submit a Story
1. Navigate to "Submit Your Story"
2. Fill in the story details:
   - Title and content
   - Language (auto-detected)
   - Category, region, and community
   - Optional image upload
3. Submit to add to the heritage archive

### Browse Stories
1. Visit "Browse Stories"
2. Use pagination to explore the collection
3. Filter by language, category, or region
4. Click to expand and read full stories

### Search Archive
1. Go to "Search Archive"
2. Apply filters for targeted discovery
3. Search by keywords or metadata
4. Export results for research purposes

## 🛠️ Development

### Project Structure
```
cultural-chronicles/
├── app.py                 # Main application entry
├── pages/                 # Page components
│   ├── submit_story.py    # Story submission
│   ├── browse_stories.py  # Archive browsing
│   └── search_archive.py  # Advanced search
├── utils/                 # Utility modules
│   ├── database.py        # Database operations
│   ├── ai_models.py       # Language detection
│   ├── cache_manager.py   # Performance caching
│   └── image_processor.py # Image handling
├── models/                # Data models
├── data/                  # Static data and samples
└── uploads/               # User uploaded images
```

### Running Tests
```bash
python -m pytest tests/
```

### Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📊 Sample Data

The application comes with 6 pre-loaded cultural stories showcasing:
- Folk tales from different regions
- Festival traditions and celebrations
- Traditional recipes and cooking methods
- Historical legends and narratives
- Community customs and practices

## 🌟 Technologies

- **Frontend**: Streamlit, streamlit-option-menu
- **Backend**: Python, SQLAlchemy, pandas
- **Database**: PostgreSQL, SQLite
- **AI/ML**: HuggingFace Transformers (optional), pattern-based detection
- **Image Processing**: Pillow (PIL)
- **Deployment**: Replit, cloud-native architecture

## 📈 Performance

- **Loading Time**: < 5 seconds for story browsing
- **Database**: Optimized queries with intelligent caching
- **Image Processing**: Automatic compression and resizing
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🤝 Contributing

We welcome contributions from developers, cultural enthusiasts, and heritage preservationists! Areas where you can help:

- Adding new language detection models
- Improving cultural categorization algorithms
- Enhancing UI/UX design
- Adding new story submission fields
- Performance optimizations
- Documentation improvements

## 📄 License

This project is licensed under the GNU Affero General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- India's diverse cultural communities for their rich heritage
- Open source contributors and maintainers
- Streamlit team for the excellent framework
- Cultural preservation organizations worldwide

## 📞 Support

- **Documentation**: Check our detailed guides in `/docs`
- **Issues**: Report bugs and request features on GitHub
- **Discussions**: Join community conversations
- **Contact**: Reach out to maintainers for questions

---

**Cultural Chronicles** - Bridging the past and future through digital storytelling 🌉