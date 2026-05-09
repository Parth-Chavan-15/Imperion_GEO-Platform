# ⚡ IMPERION: Generative Engine Optimization (GEO) Platform

**"Optimizing for Answers, Not Just Links."**

Imperion is a "Digital Twin" intelligence platform built for **Hack-AI-Thon 4.0 (Problem Statement 01)**. It helps content creators and brands adapt to the new era of AI-driven search (like Google AI Overviews and ChatGPT) by reverse-engineering how Large Language Models (LLMs) synthesize and cite information.

---

## 🧠 The Problem
Traditional SEO is built for a world that is rapidly disappearing. For decades, brands optimized for "10 blue links" using keyword density, metadata, and backlinks. However, modern platforms (like ChatGPT, Perplexity, and Google AI Overviews) act as *answer engines*. They do not return a list of links; they synthesize a **single, consolidated answer** from multiple sources.

This creates a massive blind spot for digital marketers. A brand like Nike might rank #1 on traditional Google, but be completely ignored by an AI model in favor of a competitor. Existing SEO tools (like Ahrefs or SurferSEO) are practically useless in this new paradigm because they track static keyword repetition rather than **Generative Trust**, Information Density, and Semantic Schema. Today, brands have zero visibility into *why* an AI chooses to cite one source over another.

## 🚀 The Solution
Imperion bridges the gap between human content and machine understanding. Instead of guessing, Imperion operates as a **Digital Twin** system using a 3-step pipeline:

1. **🕵️ The Spy (Structural Analysis):** Scrapes the target website and a competitor's website, stripping away visual design to extract the raw information architecture (H-tags, lists, tables) exactly as an AI bot sees it.
2. **🤖 The Simulator (Ground Truth):** Queries the live **Google Gemini 2.5 Flash API** to generate the AI's ideal synthesized answer for a specific user query.
3. **🧠 The Brain (Semantic Comparison):** Performs deep analysis between the user's content and the AI's "Mental Model" to find the gaps preventing citation.

---

## ⚙️ Core Features & Innovations

* **🛡️ Trust Score (The Hype-Checker):** LLMs are trained to be "Helpful, Honest, and Harmless." Imperion's sentiment analysis penalizes "salesy" marketing fluff (e.g., "Life-changing," "Best ever") and rewards objective, encyclopedic writing to maximize citation probability.
* **📊 Fact Density Analysis:** Evaluates the ratio of "Hard Entities" (Proper Nouns, Dates, Specifications, Prices) against total text. It detects if a page is data-rich or just marketing fluff.
* **📖 Readability Alignment:** Uses the Flesch-Kincaid formula to ensure the complexity of the user's content matches the reading level the AI expects.
* **⚔️ Competitor Signal Collection:** Analyzes competitor HTML schema (e.g., identifying that the competitor uses lists while the user uses paragraphs) to find structural advantages.
* **🎯 Actionable Recommendations Engine:** Goes beyond raw analytics by giving explicit directives (e.g., *"Remove the specific phrase 'relentlessly innovating'"* or *"Add a definition for Recycled Ocean Plastic"*).

---

## 🛠️ Technology Stack

* **Frontend:** [Streamlit](https://streamlit.io/) (Interactive Web Dashboard)
* **Backend:** [Python 3.9+](https://www.python.org/)
* **Generative AI:** [Google Gemini API (2.5-Flash)](https://aistudio.google.com/)
* **Web Scraping:** [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io/), [Requests](https://requests.readthedocs.io/)
* **Data Processing:** [Pandas](https://pandas.pydata.org/), [Textstat](https://pypi.org/project/textstat/)
* **Visualization:** [Plotly](https://plotly.com/python/) (Interactive Gauge & Bar Charts)

---

## 💻 Installation & Setup

**1. Clone the repository:**
```bash
git clone https://github.com/Parth-Chavan-15/Imperion_GEO-Platform
cd imperion_geo-platform
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Configure the API Key:**
Open `app.py` and replace the placeholder on Line 11 with your active Google Gemini API Key.
```python
GOOGLE_API_KEY = "AIzaSy_YOUR_API_KEY_HERE"
```

**4. Run the application:**
```bash
streamlit run app.py
```

## 🎯 Example Demo Scenario
To test the engine, try the following inputs based on our Hackathon Demo:

* **Your Website URL:** `https://www.nike.com/sustainability`
* **Competitor URL:** `https://en.wikipedia.org/wiki/Adidas`
* **Target Query:** `Which running shoes are made from recycled ocean plastic?`

> **💡 The Result:** Notice how Imperion flags Nike's corporate mission statement as "Fluff" and recommends adding specific material definitions to compete with Adidas's highly structured, list-based format.