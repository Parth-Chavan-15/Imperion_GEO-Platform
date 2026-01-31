import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
import textstat
import re

# --- CONFIGURATION & SETUP ---
st.set_page_config(
    page_title="IMPERION | GEO Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Hacker/Dark Mode"
st.markdown("""
    <style>
    .main {background-color: #0E1117;}
    h1, h2, h3 {color: #00D4FF;}
    .stButton>button {width: 100%; background-color: #00D4FF; color: black; font-weight: bold;}
    .metric-card {background-color: #1E1E1E; padding: 15px; border-radius: 10px; border: 1px solid #333;}
    </style>
    """, unsafe_allow_html=True)

# --- MODULE 1: THE SPY (Scraping Logic) ---
def scrape_content(url):
    """
    Step 2: Structural Analysis. Extracts H-tags, text, and structural signals.
    """
    if not url: return None
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Kill scripts and styles
        for script in soup(["script", "style"]):
            script.extract()
            
        text = soup.get_text(separator=' ', strip=True)
        
        return {
            "text": text,
            "h1": len(soup.find_all('h1')),
            "h2": len(soup.find_all('h2')),
            "lists": len(soup.find_all('ul')) + len(soup.find_all('ol')),
            "tables": len(soup.find_all('table')),
            "word_count": len(text.split())
        }
    except Exception as e:
        st.sidebar.error(f"Error scraping {url}: {e}")
        return None

# --- MODULE 2: THE BRAIN (Analysis Algorithms) ---

def calculate_trust_score(text, model):
    """ Innovation A: The 'Hype-Checker' (0-100) """
    # We ask for a score AND a reasoning to ensure the model thinks deeply
    prompt = f"""
    Analyze the tone of the following text for a 'Trust Score' (0-100).
    - 0 = Highly promotional, salesy, spammy, hype-filled (e.g. "Buy now", "Life changing").
    - 100 = Objective, encyclopedia-style, research-backed, neutral.
    
    Text snippet: {text[:2000]}
    
    Return ONLY a single number (e.g. 45).
    """
    try:
        response = model.generate_content(prompt)
        # Extract the first number found in the response
        match = re.search(r'\d+', response.text)
        if match:
            score = int(match.group())
            return min(max(score, 0), 100)
        return 50
    except:
        return 50 # Fallback

def calculate_fact_density(text):
    """ Innovation B: Fact-Density Metric (Ratio of Hard Entities) """
    words = text.split()
    if len(words) == 0: return 0
    # Count numbers and Capitalized words (excluding start of sentence)
    hard_entities = len(re.findall(r'\b[A-Z][a-z]+\b', text)) + len(re.findall(r'\d+', text))
    density = (hard_entities / len(words)) * 100
    return round(density, 2)

def check_schema_match(ai_text, user_data):
    """ Module D: Schema Validator """
    ai_has_list = "•" in ai_text or "- " in ai_text or "1. " in ai_text
    ai_has_table = "|" in ai_text and "-|-" in ai_text
    issues = []
    if ai_has_list and user_data['lists'] == 0:
        issues.append("❌ **Structure Mismatch:** The AI used a **List/Bullet Points** to answer this, but your content has none.")
    if ai_has_table and user_data['tables'] == 0:
        issues.append("❌ **Structure Mismatch:** The AI used a **Comparison Table**, but your content has none.")
    return issues

# --- THE APP LAYOUT ---

# Sidebar: Step 1 (Input)
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=50)
    st.title("IMPERION")
    st.markdown("### GEO Platform")
    st.info("Aligning Content with AI Synthesis")
    
    api_key = st.text_input("🔑 Gemini API Key", type="password")
    target_url = st.text_input("🌐 Your Website URL")
    competitor_url = st.text_input("⚔️ Competitor URL (Optional)", placeholder="e.g. Rival Brand")
    query = st.text_input("🔍 Target User Query")
    
    run_btn = st.button("🚀 Run GEO Analysis")
    st.divider()
    st.caption("Powered by Google Gemini & Firecrawl Logic")

# Main Dashboard
if run_btn and api_key and target_url and query:
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # --- STEP 2: STRUCTURAL ANALYSIS (User & Competitor) ---
    with st.status("🕵️ Step 2: Running Structural Spy...", expanded=True) as status:
        st.write("Scraping your site...")
        user_data = scrape_content(target_url)
        
        comp_data = None
        if competitor_url:
            st.write(f"Scraping competitor: {competitor_url}...")
            comp_data = scrape_content(competitor_url)
        
        if not user_data:
            status.update(label="❌ Error Scraping URL", state="error")
            st.stop()
            
        status.update(label="✅ Digital Twin Created", state="complete", expanded=False)

    # --- STEP 3: AI SIMULATION ---
    with st.status("🤖 Step 3: Simulating AI Mental Model...", expanded=True) as status:
        st.write(f"Querying Gemini with: '{query}'...")
        ai_prompt = f"Act as an advanced search engine. User query: '{query}'. Provide a comprehensive, structured answer using bullet points, data, and definitions."
        ai_response = model.generate_content(ai_prompt)
        ai_text = ai_response.text
        status.update(label="✅ Simulation Complete", state="complete", expanded=False)

    # --- STEP 4: SYNTHESIS VIEW (Read-Only) ---
    st.subheader("👁️ Step 4: AI Synthesis View")
    col1, col2 = st.columns(2)
    with col1:
        st.success("🤖 What AI Generated (The Goal)")
        st.markdown(f"<div style='height:300px; overflow-y:scroll; background-color:#262730; padding:10px; border-radius:5px;'>{ai_text}</div>", unsafe_allow_html=True)
    with col2:
        st.warning("📄 Your Content (The Reality)")
        st.markdown(f"<div style='height:300px; overflow-y:scroll; background-color:#262730; padding:10px; border-radius:5px;'>{user_data['text']}</div>", unsafe_allow_html=True)

    # --- STEP 5: GEO ANALYSIS LAYER (The Brain) ---
    st.divider()
    st.subheader("🧠 Step 5: The GEO Analysis Layer")
    
    # Calculate Metrics
    trust_score = calculate_trust_score(user_data['text'], model)
    user_density = calculate_fact_density(user_data['text'])
    ai_density = calculate_fact_density(ai_text)
    user_readability = textstat.flesch_reading_ease(user_data['text'])
    ai_readability = textstat.flesch_reading_ease(ai_text)
    
    # Competitor logic
    if comp_data:
        comp_density = calculate_fact_density(comp_data['text'])
        st.info(f"⚔️ **Competitor Intel:** They have **{comp_data['word_count']} words** and **{comp_data['lists']} lists** (Density: {comp_density}%).")
    
    c1, c2, c3 = st.columns(3)
    
    # MODULE A: TRUST SCORE
    with c1:
        st.markdown("#### 🛡️ Trust Score")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number", value = trust_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Hype Check"},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00D4FF"},
                     'steps': [{'range': [0, 40], 'color': "#FF4B4B"}, {'range': [80, 100], 'color': "#00CC96"}]}
        ))
        fig.update_layout(height=250, margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor="#0E1117", font={'color': "white"})
        st.plotly_chart(fig, use_container_width=True)

    # MODULE B: FACT DENSITY
    with c2:
        st.markdown("#### 📊 Fact Density")
        sources = ['AI Requirement', 'Your Content']
        densities = [ai_density, user_density]
        colors = ['#00CC96', '#FF4B4B' if user_density < ai_density else '#00D4FF']
        
        if comp_data:
            sources.append("Competitor")
            densities.append(calculate_fact_density(comp_data['text']))
            colors.append('#FFA500') 

        fig2 = go.Figure(data=[go.Bar(x=sources, y=densities, marker_color=colors)])
        fig2.update_layout(title="Hard Entities Ratio", height=250, paper_bgcolor="#0E1117", plot_bgcolor="#0E1117", font={'color': "white"})
        st.plotly_chart(fig2, use_container_width=True)

    # MODULE C: READABILITY
    with c3:
        st.markdown("#### 📖 Readability Match")
        diff = abs(user_readability - ai_readability)
        st.metric("Reading Ease Score", f"{user_readability:.1f}", delta=f"Diff: {diff:.1f}")
        if diff > 15: st.warning("⚠️ Style Mismatch.")
        else: st.success("✅ Style Aligned.")

    # --- STEP 6: OPTIMIZATION ENGINE (NOW DYNAMIC!) ---
    st.divider()
    st.subheader("🚀 Step 6: Actionable Recommendations")
    
    recommendations = []
    
    # 1. Structure Check
    recommendations.extend(check_schema_match(ai_text, user_data))
    
    # 2. Density Check
    if user_density < ai_density:
        recommendations.append(f"📉 **Low Information Density:** Your content has **{user_density}%** hard facts, but AI expects **{ai_density}%**. Add more dates, statistics, and specific entities.")
        
    # 3. Tone Check (DYNAMIC - NO HARDCODED WORDS)
    if trust_score < 60:
        with st.spinner("🔍 Identifying specific salesy words in your text..."):
            tone_prompt = f"""
            The following text was flagged as "Promotional/Salesy" (Score: {trust_score}/100).
            Identify specific phrases or words IN THE TEXT that make it sound salesy.
            Return them as a bulleted list. 
            Do NOT give generic advice. Quote the text.
            
            Text: {user_data['text'][:2000]}
            """
            tone_advice = model.generate_content(tone_prompt).text
            recommendations.append(f"📢 **Tone Mismatch:** Your content is too promotional.\n\n**Specific words to remove/change:**\n{tone_advice}")
        
    # 4. Competitor Check
    if comp_data and comp_data['lists'] > user_data['lists']:
        recommendations.append(f"⚔️ **Competitor Gap:** The competitor uses **{comp_data['lists']} lists**, you use {user_data['lists']}. Add a list.")

    # Display Recommendations
    if recommendations:
        for rec in recommendations: st.warning(rec)
    else: st.info("✅ Structure looks good!")
        
    st.markdown("### 🔍 Content Gaps")
    gap_prompt = f"Compare these texts. AI Text: {ai_text}. User Text: {user_data['text'][:3000]}. List 2 specific topics present in AI but MISSING from User. Start bullets with 'Missing Topic:'."
    gap_response = model.generate_content(gap_prompt)
    st.write(gap_response.text)

elif run_btn:
    st.error("Please fill in all fields (API Key, URL, Query).")

# Footer
st.markdown("---")
st.caption("Imperion GEO Platform © 2026 | Built for Hackathon PS01")
