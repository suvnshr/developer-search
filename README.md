
# 🚀 DevXplore

DevXplore is a developer-focused search engine designed to help engineers discover GitHub repositories, YouTube tutorials, online courses, and technical documentation more efficiently.

It enhances standard Google search results by classifying them into developer-relevant categories, enabling faster and more targeted discovery.

[Visit DevXplore ↗](https://devxplore.suvanshrana.com/)

---

## 🤔 Why DevXplore?

As a developer, I often found it time-consuming to locate high-quality learning resources tailored to my needs. While general-purpose search engines return relevant results, they rarely structure them in a way that aligns with how developers explore and learn.

DevXplore was built to solve this problem by automatically categorizing search results into meaningful developer-centric tabs such as GitHub, Documentation, Courses, and Tutorials.

> Note: This project was created in 2020, when AI tools like ChatGPT, Claude, and Gemini were not yet available. With these tools now in the market, DevXplore may not seem as advanced, but at the time it was a quite innovative solution for structured developer search and resource discovery.

---

## ⚙️ How It Works

### 🔍 Search Provider

- Google search results are retrieved using **SerpAPI**
- No scraping is performed; all data is fetched via official APIs

### 🧠 Classification Pipeline

1. A search query is sent to SerpAPI  
2. Organic search results are extracted  
3. Each result is evaluated against multiple category definitions  
4. Results are grouped into one or more relevant categories  

---

## 🗂️ Result Classification System

DevXplore uses a **rule-based scoring system** to classify search results.  
Each result is scored against every category using multiple signals.

### 📡 Signals Used

- Domain matching  
- URL pattern matching  
- Title pattern matching  
- Keyword matching (exact and fuzzy)  

### 📊 Scoring Model

| Signal Type             | Score |
|-------------------------|-------|
| Domain match (priority) | 100   |
| Domain match            | 50    |
| URL pattern match       | 30    |
| Title pattern match     | 25    |
| Keyword match           | 20    |

- A minimum score of **20** is required for inclusion in a category  
- Results may appear in multiple categories  
- Some categories define exclusion rules to avoid overlap  

### 🧩 Example Categories

- YouTube  
- GitHub  
- Documentation  
- Courses  
- Interactive Tools  
- Blog Articles  
- Stack Overflow  

Category rules are defined declaratively and can be extended without modifying the core classification logic.

---

## 🎬 Demo

![DevXplore Demo](./gallery/devxplore-v2.gif "DevXplore Demo")


## 🛠️ Setup and Installation

The following steps describe how to run DevXplore locally for development or evaluation purposes.

### ✅ Prerequisites

- Python 3.12+  
- pip  
- Virtual environment (recommended)  

### 📥 Clone the Repository

```bash
git clone https://github.com/suvansh-rana/developer-search.git
cd developer-search
```

### 🧪 Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🔐 Environment Variables

Create a `.env` file in the project root and configure the following variables:

```env
SECRET_KEY=your_django_secret_key
PROD=False
ALLOWED_HOSTS=localhost,127.0.0.1
SERP_API_KEY=your_serpapi_key
```

#### 🔑 SERP_API_KEY

DevXplore uses **SerpAPI** to fetch Google search results.

You can obtain an API key from:
[https://serpapi.com/](https://serpapi.com/)

### 🗄️ Apply Database Migrations

```bash
python manage.py migrate
```

### ▶️ Run the Development Server

```bash
python manage.py runserver
```

The application will be available at:
[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📝 Notes

* DevXplore is a personal hobby project developed and maintained in spare time.
* The application is fully functional; documentation focuses on core concepts rather than exhaustive configuration.
* Environment-specific configuration, including API credentials, is excluded from version control.
* The repository is shared primarily for reference and learning purposes.
* Contributions to DevXplore are not currently being accepted, but you’re welcome to explore and learn from the code.

---

## 📄 License

[MIT License](./LICENSE.md)
