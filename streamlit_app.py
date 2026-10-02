import streamlit as st
import requests
from typing import List, Dict
import time

# Page configuration
st.set_page_config(
    page_title="AI Repo Intelligence",
    page_icon= "https://img.icons8.com/?size=50&id=5jpTi28s5yE1&format=png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
        animation: fadeIn 0.3s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: #f5f5f5;
        color: #333;
        margin-right: 2rem;
        border-left: 4px solid #667eea;
    }
    
    .file-reference {
        background: #e8f4fd;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-family: monospace;
        font-size: 0.85rem;
        margin: 0.25rem 0;
        display: inline-block;
        color: #0066cc;
    }
    
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .sidebar-section {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
BACKEND_URL = "http://localhost:8000/api/v1"

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "repo_uploaded" not in st.session_state:
    st.session_state.repo_uploaded = False
if "repo_info" not in st.session_state:
    st.session_state.repo_info = None


def upload_repository(repo_url: str) -> bool:
    """Upload and process a GitHub repository."""
    try:
        with st.spinner("Processing repository... This may take a few minutes."):
            response = requests.post(
                f"{BACKEND_URL}/upload-repo",
                json={"repo_url": repo_url},
                timeout=300
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
                return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


def chat_with_repo(question: str, chat_history: List[Dict]) -> Dict:
    """Send a question to the repo intelligence system."""
    try:
        response = requests.post(
            f"{BACKEND_URL}/chat",
            json={
                "question": question,
                "chat_history": chat_history
            },
            timeout=120
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error: {response.json().get('detail', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None


# Main header
st.markdown('<h1 class="main-header">🤖 AI Repo Intelligence</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Upload a GitHub repository and ask questions about its codebase using natural language</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("###Repository Management")
    
    # Repository upload section
    with st.expander("Upload New Repository", expanded=not st.session_state.repo_uploaded):
        repo_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repo",
            help="Enter the full URL of the GitHub repository"
        )
        
        if st.button("Upload Repository", use_container_width=True):
            if repo_url:
                result = upload_repository(repo_url)
                if result:
                    st.session_state.repo_uploaded = True
                    st.session_state.repo_info = result
                    st.session_state.chat_history = []
                    st.success("Repository uploaded successfully!")
                    st.rerun()
            else:
                st.warning("Please enter a repository URL")
    
    # Repository info
    if st.session_state.repo_uploaded and st.session_state.repo_info:
        st.markdown("### Current Repository")
        st.markdown(f"**Name:** {st.session_state.repo_info['repo_name']}")
        st.markdown(f"**Files Processed:** {st.session_state.repo_info['files_processed']}")
        st.markdown(f"**Chunks Created:** {st.session_state.repo_info['chunks_created']}")
        
        if st.button("Upload Different Repository", use_container_width=True):
            st.session_state.repo_uploaded = False
            st.session_state.repo_info = None
            st.session_state.chat_history = []
            st.rerun()
    
    st.markdown("---")
    st.markdown("### Example Questions")
    example_questions = [
        "Where is authentication implemented?",
        "How does the login flow work?",
        "Why might this endpoint return 401?",
        "Where is the database connection configured?",
        "Which files handle user registration?"
    ]
    
    for question in example_questions:
        if st.button(question, key=f"example_{question}", use_container_width=True):
            st.session_state.user_question = question
            st.rerun()

# Main content area
if not st.session_state.repo_uploaded:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.markdown("### Welcome!")
    st.markdown("To get started:")
    st.markdown("1. Upload a GitHub repository using the sidebar")
    st.markdown("2. Wait for the repository to be processed")
    st.markdown("3. Start asking questions about the codebase")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Features")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Smart Search", "RAG-based", "Relevant code retrieval")
    with col2:
        st.metric("Natural Language", "Easy queries", "No coding required")
    with col3:
        st.metric("Context Aware", "File references", "See the source")
else:
    # Chat interface
    st.markdown("### Chat with Your Repository")
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><strong>AI:</strong> {message["content"]}</div>', unsafe_allow_html=True)
                
                # Display referenced files if available
                if message.get("referenced_files"):
                    st.markdown("**Referenced Files:**")
                    for file_path in message["referenced_files"]:
                        st.markdown(f'<span class="file-reference">{file_path}</span>', unsafe_allow_html=True)
    
    # Chat input
    user_input = st.text_input(
        "Ask a question about the repository...",
        placeholder="e.g., How does authentication work?",
        key="chat_input",
        value=st.session_state.get("user_question", "")
    )
    
    col1, col2 = st.columns([1, 10])
    with col1:
        send_button = st.button("Send", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("Clear Chat", use_container_width=True)
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user",
            "content": user_input
        })
        
        # Clear the input
        st.session_state.user_question = ""
        
        # Get response from backend
        with st.spinner("Analyzing repository..."):
            response = chat_with_repo(user_input, st.session_state.chat_history[:-1])
            
            if response:
                # Add assistant response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response["answer"],
                    "referenced_files": response.get("referenced_files", [])
                })
                
                st.rerun()

# Footer
st.markdown("---")
st.markdown('<p style="text-align: center; color: #888;">Developed by <a href="https://github.com/AnmolCanCodes" target="_blank">Anmol Gupta</a></p>', unsafe_allow_html=True)