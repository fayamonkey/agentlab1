import streamlit as st
import json
import os
from datetime import datetime
import markdown
from laboratory import AgentLaboratory
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Dirk's Agent Laboratory Research Lab",
    page_icon="🧪",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'research_results' not in st.session_state:
    st.session_state.research_results = {}
    # Load existing results if available
    results_file = Path("research_results.json")
    if results_file.exists():
        with open(results_file, "r") as f:
            st.session_state.research_results = json.load(f)

def save_results():
    """Save research results to JSON file"""
    with open("research_results.json", "w") as f:
        json.dump(st.session_state.research_results, f, indent=4)

# Header
col1, col2 = st.columns([1, 4])
with col1:
    st.image("agentlabsmall.png", width=100)
with col2:
    st.title("Dirk's Agent Laboratory Research Lab")
    st.subheader("Advanced Research Assistant")

# Sidebar for research list and new research button
with st.sidebar:
    st.header("Research Projects")
    
    # New Research button
    if st.button("New Research", type="primary"):
        st.session_state.current_view = "new_research"
    
    # List of existing research projects
    st.subheader("Previous Research")
    for timestamp, research in st.session_state.research_results.items():
        if st.button(f"📑 {research['topic']}", key=timestamp):
            st.session_state.current_view = "view_research"
            st.session_state.selected_research = timestamp

# Main content area
def conduct_research(topic, focus_areas):
    """Conduct new research using AgentLaboratory"""
    try:
        # Initialize the laboratory with the API key
        api_key = st.secrets["OPENAI_API_KEY"]  # We'll set this up later
        lab = AgentLaboratory(api_key=api_key, model_name="gpt-4o")
        
        task_notes = {
            "focus_areas": [area.strip() for area in focus_areas.split(",")],
            "experiment_preferences": {
                "dataset_size": "small",
                "model_complexity": "medium",
                "evaluation_metrics": ["accuracy", "perplexity"]
            }
        }
        
        with st.spinner("Conducting research..."):
            results = lab.conduct_research(topic, task_notes)
            
        # Save results
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.research_results[timestamp] = {
            "topic": topic,
            "focus_areas": focus_areas,
            "results": results
        }
        save_results()
        return True, "Research completed successfully!"
    except Exception as e:
        return False, f"Error during research: {str(e)}"

# New Research Form
if not hasattr(st.session_state, 'current_view'):
    st.session_state.current_view = "new_research"

if st.session_state.current_view == "new_research":
    st.header("New Research")
    with st.form("research_form"):
        topic = st.text_input("Research Topic")
        focus_areas = st.text_area("Focus Areas (comma-separated)")
        submitted = st.form_submit_button("Start Research")
        
        if submitted and topic and focus_areas:
            success, message = conduct_research(topic, focus_areas)
            if success:
                st.success(message)
            else:
                st.error(message)

# View Research Results
elif st.session_state.current_view == "view_research":
    if hasattr(st.session_state, 'selected_research'):
        research = st.session_state.research_results[st.session_state.selected_research]
        st.header(f"Research Results: {research['topic']}")
        st.subheader("Focus Areas")
        st.write(research['focus_areas'])
        
        st.subheader("Results")
        st.json(research['results'])
        
        # Export options
        if st.button("Export as Markdown"):
            # Create markdown content
            md_content = f"# Research Results: {research['topic']}\n\n"
            md_content += f"## Focus Areas\n{research['focus_areas']}\n\n"
            md_content += f"## Results\n```json\n{json.dumps(research['results'], indent=2)}\n```"
            
            # Create download button
            st.download_button(
                label="Download Markdown",
                data=md_content,
                file_name=f"research_{research['topic'].lower().replace(' ', '_')}.md",
                mime="text/markdown"
            ) 