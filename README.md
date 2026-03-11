# Movie Recommendation System

A **content-based movie recommendation engine** built with Python and Streamlit. This application helps users discover movies similar to their favorites using the TMDB 5000 dataset and cosine similarity metrics. The app fetches real-time movie posters and ratings from The Movie Database (TMDB) API.

---

## 🎯 Overview

The Movie Recommendation System uses **content-based filtering** to analyze movie features (genres, cast, crew, keywords) and recommend similar titles. Users select a movie from a dropdown menu, and the system returns the top 5 most similar movies with their posters and star ratings.

**Key Technologies:**
- **Streamlit** – Interactive web UI
- **Pandas & NumPy** – Data processing
- **Scikit-learn** – Similarity computation
- **Requests** – TMDB API integration

---

## 📁 Repository Structure

```
Movies-Recommendation-System/
├── app.py                          # Streamlit application (main entry point)
├── requirements.txt                # Python dependencies
├── setup.sh                        # Streamlit cloud configuration
├── Procfile                        # Heroku deployment configuration
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
├── project_1/                      # Raw dataset directory
│   ├── tmdb_5000_movies.csv.zip   # Movie metadata (zipped)
│   └── tmdb_5000_credits.csv.zip  # Cast & crew data (zipped)
├── movies.pkl                      # Pickled movies dataframe (generated after data prep)
└── similarity.pkl                  # Pickled similarity matrix (generated after data prep)
```

---

## 🛠️ Prerequisites

Ensure you have the following installed:

- **Python 3.8 or higher**
- **pip** (Python package manager)
- **Git** (for cloning the repository)
- **Internet connection** (for TMDB API requests)

Optional:
- Virtual environment manager (venv, conda, or pipenv)

---

## 📥 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Sumannay/Movie_Recommendation_System.git
cd Movie_Recommendation_System
```

### 2. Create a Virtual Environment

**Windows:**
```bash
python -m venv .venv
.\.venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Additional packages for data preparation (optional):**
```bash
pip install pandas numpy scikit-learn requests
```

---

## 📊 Dataset & Data Preparation

The project includes TMDB 5000 dataset files as zipped CSV archives in `project_1/`:
- `tmdb_5000_movies.csv.zip` – Movie metadata (5000 movies)
- `tmdb_5000_credits.csv.zip` – Cast and crew information

### Generate Required Pickle Files

The application requires `movies.pkl` and `similarity.pkl` to run. Create these by running a data preparation script:

**Create `prepare_data.py`:**

```python
import pandas as pd
import numpy as np
import pickle
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import zipfile
import io

# Extract and load data from zipped CSVs
def load_data():
    movies = pd.read_csv('project_1/tmdb_5000_movies.csv.zip')
    credits = pd.read_csv('project_1/tmdb_5000_credits.csv.zip')
    return movies, credits

# Preprocess and merge datasets
movies, credits = load_data()
movies = movies.merge(credits, on='id')

# Extract genres (from JSON string)
def get_genres(x):
    try:
        genres_list = json.loads(x)
        return ' '.join([g['name'] for g in genres_list][:3])
    except:
        return ''

# Extract top 5 cast members
def get_cast(x):
    try:
        cast_list = json.loads(x)
        return ' '.join([c['name'] for c in cast_list][:5])
    except:
        return ''

# Extract keywords
def get_keywords(x):
    try:
        keywords_list = json.loads(x)
        return ' '.join([k['name'] for k in keywords_list][:5])
    except:
        return ''

# Create a combined feature string for content-based filtering
movies['genres_text'] = movies['genres'].apply(get_genres)
movies['cast_text'] = movies['cast'].apply(get_cast)
movies['keywords_text'] = movies['keywords'].apply(get_keywords if 'keywords' in movies.columns else lambda x: '')

movies['soup'] = (movies['genres_text'] + ' ' + 
                  movies['cast_text'] + ' ' + 
                  movies['keywords_text'] + ' ' + 
                  movies['original_language'].fillna(''))

# Compute similarity matrix using CountVectorizer
count = CountVectorizer(stop_words='english', max_features=5000)
count_matrix = count.fit_transform(movies['soup'])
similarity = cosine_similarity(count_matrix, count_matrix)

# Save to pickle files
pickle.dump(movies[['id', 'title', 'movie_id']], open('movies.pkl', 'wb'))
pickle.dump(similarity, open('similarity.pkl', 'wb'))

print("✅ movies.pkl and similarity.pkl generated successfully!")
```

**Run the preparation script:**

```bash
python prepare_data.py
```

This will create `movies.pkl` and `similarity.pkl` in your project root.

---

## ▶️ Running the Application

Once the pickle files are ready, start the Streamlit server:

```bash
streamlit run app.py
```

The app will launch automatically in your default browser at **http://localhost:8501**.

### Using the App

1. Select a movie from the dropdown menu
2. Click the **"Recommend"** button
3. View the top 5 similar movies with their posters and ratings

---

## 🚀 Deployment

### Deploy on Heroku

1. **Install Heroku CLI** and log in:
   ```bash
   heroku login
   ```

2. **Create a Heroku app:**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy:**
   ```bash
   git push heroku main
   ```

The `Procfile` and `setup.sh` are pre-configured for Heroku deployment.

### Deploy on Streamlit Community Cloud

1. Push your code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New App" and connect your GitHub repository
4. Select the branch and `app.py` as the entry point
5. Click "Deploy"

**Add TMDB API Key as a secret:**
- In Streamlit Cloud settings, add a secret `TMDB_API_KEY` with your API key value

---

## 🔑 API Configuration

### TMDB API Key

The app currently uses a hard-coded API key. For security, use an environment variable instead:

**Option 1: Environment Variable (Recommended)**

In `app.py`, replace the hard-coded key:

```python
import os
api_key = os.getenv('TMDB_API_KEY', 'fallback_key_here')
```

Set the environment variable:

**Windows:**
```bash
set TMDB_API_KEY=your_api_key_here
```

**macOS/Linux:**
```bash
export TMDB_API_KEY=your_api_key_here
```

**Get your free API key from:** [TMDB API](https://www.themoviedb.org/settings/api)

---

## 📦 Dependencies

| Package | Purpose |
|---------|---------|
| `streamlit` | Web UI framework |
| `requests` | HTTP requests for TMDB API |
| `pandas` | Data manipulation |
| `numpy` | Numerical computations |
| `scikit-learn` | Machine learning (similarity computation) |
| `pickle` | Serialization (built-in) |

---

## 🐛 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'streamlit'`
**Solution:** Ensure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: `FileNotFoundError: movies.pkl not found`
**Solution:** Run the data preparation script:
```bash
python prepare_data.py
```

### Issue: TMDB API returns error or no posters display
**Solution:** 
- Check internet connection
- Verify API key is valid
- Check TMDB API status at [TMDB Status Page](https://www.themoviedb.org/)

### Issue: `setup.sh` path error on Heroku
**Note:** There's a typo in the original `setup.sh` file. If deploying, correct:
```bash
# From: mkdir -p ~/.streamtit/
# To:   mkdir -p ~/.streamlit/
```

---

## 📈 How It Works

1. **Data Loading:** Loads preprocessed movie data and similarity matrix from pickle files
2. **User Selection:** User picks a movie from the available list
3. **Similarity Lookup:** Finds the most similar movies using the precomputed cosine similarity matrix
4. **API Calls:** Fetches posters and ratings from TMDB API for each recommended movie
5. **Display:** Shows results in a 5-column layout with titles, posters, and ratings

---

## 💡 Future Enhancements

- [ ] Add user authentication and personalized recommendations
- [ ] Implement collaborative filtering based on user ratings
- [ ] Docker containerization
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Caching layer to reduce API calls
- [ ] Add movie reviews and metadata
- [ ] Implement search and filters (by genre, year, rating)
- [ ] Dark mode UI
- [ ] Export recommendations to a list

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the **MIT License**.

---

## 📞 Contact & Support

- **GitHub:** [Sumannay/Movie_Recommendation_System](https://github.com/Sumannay/Movie_Recommendation_System)
- **Issues:** [GitHub Issues](https://github.com/Sumannay/Movie_Recommendation_System/issues)

---

## 🙏 Acknowledgments

- **TMDB** – Movie database and API
- **Streamlit** – Web framework
- **Scikit-learn** – ML library for similarity computations

---

**Last Updated:** March 2026
