import streamlit as st
from groq import Groq

# Page configuration
st.set_page_config(
    page_title="AI Content Assistant",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags instantly powered by Groq.")

# Initialize Groq Client
# Reads API key from Streamlit Secrets or manual input
api_key = st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")
    st.sidebar.info("Get a free key at [console.groq.com](https://console.groq.com)")

if api_key:
    client = Groq(api_key=api_key)
else:
    client = None

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        content_type = st.selectbox(
            "Content Type",
            ["Social Media Post", "Blog Post Intro", "Product Announcement", "Newsletter Snippet", "Ad Copy"]
        )
        platform = st.selectbox(
            "Target Platform",
            ["LinkedIn", "Instagram", "X (Twitter)", "Facebook", "Medium"]
        )
        tone = st.selectbox(
            "Tone of Voice",
            ["Professional", "Casual & Friendly", "Persuasive", "Humorous", "Inspirational", "Educational"]
        )

    with col2:
        topic = st.text_input("Topic / Main Message", placeholder="e.g., Launching a new Python course")
        target_audience = st.text_input("Target Audience", placeholder="e.g., Beginners, Developers, Entrepreneurs")

    submit_button = st.form_submit_button("✨ Generate Content")

# Generation Logic
if submit_button:
    if not client:
        st.error("Please provide a valid Groq API Key to proceed.")
    elif not topic or not target_audience:
        st.warning("Please fill in both the Topic and Target Audience fields.")
    else:
        # Prompt structure
        prompt = f"""
You are an expert content writer and social media strategist.
Generate a complete, high-engaging post based on these parameters:

- Content Type: {content_type}
- Platform: {platform}
- Topic: {topic}
- Target Audience: {target_audience}
- Tone: {tone}

Please format the output clearly with:
1. Main Post Body (formatted for the target platform)
2. Alternative Captions / Hook Options (2-3 short options)
3. Relevant Hashtags
        """

        with st.spinner("Generating content..."):
            try:
                # Fast and capable model available on Groq's free tier
                response = client.chat.completions.create(
                    model="openai/gpt-oss-120b",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that generates social media and web content."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=1000
                )
                
                generated_text = response.choices[0].message.content
                
                st.success("Content Generated Successfully!")
                st.markdown("---")
                st.markdown(generated_text)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
