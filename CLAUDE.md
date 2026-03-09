# CLAUDE.md — AI Assistant Guide for hipython

## Project Overview

This is a **Python data science learning and portfolio repository** maintained by a finance professional (8 years experience) transitioning into AI/tech through KPMG Future Academy. The repo contains:

- 51 Jupyter notebooks covering Python fundamentals → advanced ML
- 16 Python scripts (Streamlit dashboards, web scraping, utilities)
- Real-world project implementations (Walmart analysis, web crawling, prompt engineering)
- Web application prototypes using Streamlit

**Primary focus:** Practical, business-applicable data science and AI skills, documented for portfolio demonstration.

---

## Repository Structure

```
hipython/
├── *.ipynb                    # Root-level course notebooks (Python fundamentals → data analysis)
├── ml/                        # Machine learning notebooks (10+ sequential lessons)
├── streamlit_exam/            # Streamlit web application prototypes
├── webcrawlling/              # Web scraping notebooks, scripts, and scraped data
├── Walmart Data/              # Major portfolio project (Walmart customer analysis)
├── jlee/                      # Utility scripts (calc.py, main.py)
├── .gitignore
└── README.md                  # Portfolio introduction (Korean)
```

### Learning Path Notebook Numbering

Root notebooks follow a curriculum numbering scheme:

| Range | Topic |
|-------|-------|
| 0–7   | Python fundamentals (variables, data types, loops, functions, OOP) |
| 11–14 | Statistics (descriptive stats, hypothesis testing, probability) |
| 21    | Prompt engineering & OpenAI API integration |
| 32    | Python + SQL |
| 41–42 | Pandas, data preprocessing |
| 43    | Data visualization |
| 44–45 | EDA, portfolio analysis, Walmart, telecom churn |

ML notebooks in `ml/` are numbered 0–11, progressively covering:
`AI/ML fundamentals → modeling → ensemble → evaluation → classification → regression → clustering → real-world prediction`

---

## File Naming Conventions

- **Korean course notebooks:** `번호.주제명.ipynb` (e.g., `4.조건과반복.ipynb`)
- **Exercise notebooks:** `번호.연습문제.ipynb`
- **Skeleton notebooks:** `*_skeleton.ipynb` (incomplete, for self-practice)
- **Python scripts:** `snake_case.py`
- **Streamlit apps:** `app.py`, `app1.py`, `app2.py`, `app3.py` (progressively complex)
- **Data files:** stored adjacent to the notebook that uses them

---

## Technology Stack

### Core Libraries

| Library | Use |
|---------|-----|
| `pandas`, `numpy` | Data manipulation |
| `matplotlib`, `seaborn` | Static visualization |
| `plotly` | Interactive visualization |
| `streamlit` | Web app dashboards |
| `scikit-learn` | ML models |
| `beautifulsoup4`, `requests` | Web scraping |
| `openai` | GPT-4o-mini integration |
| `sqlite3`, `sqlalchemy` | Database integration |
| `python-dotenv` | Environment variable loading |

### External APIs & Data Sources

- **OpenAI API** — GPT-4o-mini; key stored in `.env` as `OPENAI_API_KEY`
- **Naver Finance** — financial news scraping
- **Kaggle** — Walmart Sales Dataset (550K+ transactions)

---

## Key Projects

### 1. Walmart Customer Analysis (`Walmart Data/`)

Full analysis of 550,068 transactions across ~5,891 customers. Goals:
- Identify high-revenue ("Cash Cow") customer segments
- Find best-seller products per segment
- Develop targeted marketing strategies

**Entry point:** `Walmart Data/WalmartDataReport.ipynb`
**Dashboard:** `streamlit_exam/WalmartData.py`
**Docs:** `Walmart Data/README.md`

### 2. Streamlit Dashboards (`streamlit_exam/`)

| File | Description |
|------|-------------|
| `app.py` | "Hello Streamlit" baseline |
| `app1.py` | UI elements demo |
| `app2.py` | Environmental metrics dashboard |
| `app3.py` | Full Strawberry pink-themed dashboard (3-tab layout, Plotly charts) |
| `WalmartData.py` | Blue-themed professional business dashboard |

**Run any app:** `streamlit run streamlit_exam/<filename>.py`

### 3. Web Crawling (`webcrawlling/`)

Notebooks and scripts for scraping books, news articles, financial data, and images.
Key outputs: `article.csv`, `news.csv`, `naver_finance_news.csv`, `_books.db`

### 4. Prompt Engineering (`21.프롬프트엔지니어링기초.ipynb`, `21_prompt_start.py`)

OpenAI API usage with finance-domain expert prompts. API key must be in `.env`.

---

## Development Workflow

### Running Notebooks

```bash
jupyter notebook          # Launch Jupyter in browser
# or
jupyter lab               # Use JupyterLab UI
```

Open any `.ipynb` file and run cells sequentially. Notebooks are self-contained (include imports and data loading).

### Running Streamlit Apps

```bash
streamlit run streamlit_exam/app3.py
streamlit run streamlit_exam/WalmartData.py
```

### Environment Setup

No `requirements.txt` or `pyproject.toml` exists. Infer dependencies from notebook imports. Recommended setup:

```bash
python -m venv venv
source venv/bin/activate
pip install pandas numpy matplotlib seaborn plotly streamlit scikit-learn \
            beautifulsoup4 requests openai python-dotenv jupyter
```

Environment variables go in `.env` (excluded from git):

```
OPENAI_API_KEY=your_key_here
```

---

## Code Conventions

- **Self-contained notebooks:** Each notebook handles its own imports and data loading; do not assume shared state.
- **Korean comments:** Educational notebooks use Korean inline comments and markdown cells — preserve these when editing.
- **Modular Streamlit structure:** Custom CSS theming (pink: `#FF1493`/`#FF69B4`; professional blue gradient) is defined at the top of each app file; keep styles centralized there.
- **Data caching:** Streamlit apps use `@st.cache_data` for expensive computations — maintain this pattern.
- **Iterative versioning:** Multiple versions of the same analysis (e.g., `app1.py` → `app3.py`, `ML6v2` → `ML6v3`) are intentional progression artifacts — don't delete older versions without confirming intent.

---

## Testing & Validation

There is **no formal test suite**. Validation approaches:

- Run Jupyter cells sequentially and verify outputs match expected values.
- For Streamlit apps, launch with `streamlit run` and visually verify the dashboard renders correctly.
- Exercise notebooks (`연습문제.ipynb`) serve as informal tests — run them to confirm the corresponding concept implementations are correct.

---

## Git Conventions

- **Primary branch:** `master`
- **Claude Code branch:** `claude/claude-md-*`
- **Commit style:** Short module-scoped labels (e.g., `ml10.5`, `ML6v3`, `Walmart Data`)
- No pull request workflow — commits go directly to master after feature completion.

---

## What NOT to Do

- Do **not** add `requirements.txt` or configuration files unless explicitly asked — this is a learning repo, not a production project.
- Do **not** refactor Korean educational notebooks into English — the language is intentional.
- Do **not** delete skeleton notebooks (`*_skeleton.ipynb`) — they are used for practice.
- Do **not** overwrite older versions of apps (e.g., `app1.py`) when adding a newer version — keep the progression intact.
- Do **not** commit `.env` files or expose API keys.

---

## Important File Locations

| Purpose | Path |
|---------|------|
| Portfolio intro | `README.md` |
| Walmart project docs | `Walmart Data/README.md` |
| OpenAI API usage | `21_prompt_start.py` |
| ML course notebooks | `ml/` |
| Streamlit apps | `streamlit_exam/` |
| Web scraping | `webcrawlling/` |
| Git ignore rules | `.gitignore` |
