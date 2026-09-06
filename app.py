import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(
    page_title="CopyPulse | AI Content Studio",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Styling
st.markdown("""
<style>
    /* Main container background and fonts */
    .main {
        background-color: #0E1117;
    }
    
    /* Styled Cards for inputs and outputs */
    .css-card {
        background-color: #1E232A;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #2D323B;
        margin-bottom: 20px;
    }
    
    /* Custom Header Styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #FF4B4B, #FF8F8F);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    
    .sub-title {
        color: #9095A0;
        font-size: 1.1rem;
        margin-bottom: 30px;
    }

    /* Style primary buttons */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #FF4B4B, #FF7676);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/flash-on.png", width=60)
    st.title("Settings")
    
    api_key = st.secrets.get("GROQ_API_KEY", "")
    if not api_key:
        api_key = st.text_input("Groq API Key", type="password", help="Get your key at console.groq.com")
    
    st.divider()
    
    # Model Selector
    selected_model = st.selectbox(
        "AI Engine",
        ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"],
        help="Select the underlying LLM powering generation."
    )
    
    creativity = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.7, step=0.1)

# Initialize Client
client = Groq(api_key=api_key) if api_key else None

# 4. Header Section
st.markdown('<p class="main-title">⚡ CopyPulse AI</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Generate high-converting content, captions, and hashtags in seconds.</p>', unsafe_allow_html=True)

# 5. Main UI Layout
col_input, col_output = st.columns([1, 1.2], gap="large")

with col_input:
    st.subheader("🛠️ Content Brief")
    
    with st.form("generator_form"):
        topic = st.text_input("Topic / Core Message", placeholder="e.g., Launching a new Python course")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Junior Developers, Career Changers")
        
        c1, c2 = st.columns(2)
        with c1:
            platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "X (Twitter)", "Facebook", "Medium"])
            content_type = st.selectbox("Format", ["Social Post", "Blog Intro", "Product Launch", "Newsletter"])
        with c2:
            tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Persuasive", "Humorous", "Inspirational"])
            length = st.select_slider("Length", options=["Short", "Medium", "Detailed"])

        submit = st.form_submit_button("🚀 Generate Strategy & Post")

with col_output:
    st.subheader("✨ Generated Output")
    
    if submit:
        if not client:
            st.error("⚠️ Please enter a valid Groq API Key in the sidebar or Secrets.")
        elif not topic or not target_audience:
            st.warning("⚠️ Please fill out both the Topic and Target Audience fields.")
        else:
            prompt = f"""
You are an expert social media copywriter. Generate content based on:
- Platform: {platform}
- Format: {content_type}
- Topic: {topic}
- Target Audience: {target_audience}
- Tone: {tone}
- Length: {length}

Format the response strictly into three markdown sections:
### 📌 Main Post
(The primary content tailored for {platform})

### 💡 Hook Variations
(Provide 3 alternative opening lines/hooks)

### 🏷️ Optimized Hashtags
(A set of relevant, targeted hashtags)
"""
            with st.spinner("Brainstorming and writing your post..."):
                try:
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[{"role": "user", "content": prompt}],
                        temperature=creativity,
                        max_tokens=1000
                    )
                    
                    output_text = response.choices[0].message.content
                    
                    tab1, tab2 = st.tabs(["📄 Formatted Preview", "📝 Raw Text"])
                    
                    with tab1:
                        st.markdown(output_text)
                    
                    with tab2:
                        st.code(output_text, language="markdown")
                        
                    st.download_button(
                        label="📥 Download Content (.txt)",
                        data=output_text,
                        file_name=f"{platform.lower()}_post.txt",
                        mime="text/plain"
                    )
                    
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    else:
        st.info("👈 Fill out the content brief on the left and click **Generate** to view results here.")
