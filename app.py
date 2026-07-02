import streamlit as st
from modules.auth import AuthManager
from modules.ui_components import UIComponents
from config.color_scheme import COLORS
from config.constants import TRANSLATIONS
import json
import os

# Page configuration
st.set_page_config(
    page_title="IGCSE AI Tutor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if "user_session" not in st.session_state:
    st.session_state.user_session = None
if "current_page" not in st.session_state:
    st.session_state.current_page = "auth"
if "language" not in st.session_state:
    st.session_state.language = "en"

# Apply custom CSS
UIComponents.custom_css()

def get_text(key: str) -> str:
    """Get translated text"""
    lang = st.session_state.language
    translations = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return translations.get(key, key)

def show_auth_page():
    """Display authentication page"""
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown(f"""
        <div style="padding: 40px; text-align: center;">
            <h1 style="color: {COLORS['primary_navy']}; font-size: 48px;">🎓</h1>
            <h2 style="color: {COLORS['primary_navy']};">IGCSE AI Tutor</h2>
            <p style="color: {COLORS['secondary_periwinkle']}; font-size: 18px; margin-top: -10px;">
                Your Personal Science Tutor
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
        
        with tab1:
            st.markdown(f"### {get_text('login')}")
            
            email = st.text_input(
                get_text('email'),
                placeholder="student@example.com",
                key="login_email"
            )
            password = st.text_input(
                get_text('password'),
                type="password",
                key="login_password"
            )
            
            if st.button("🔓 Login", use_container_width=True, key="login_btn"):
                if email and password:
                    auth_manager = AuthManager()
                    success, message, session_data = auth_manager.login(email, password)
                    
                    if success:
                        st.session_state.user_session = session_data
                        st.session_state.current_page = "dashboard"
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please enter email and password")
        
        with tab2:
            st.markdown(f"### {get_text('signup')}")
            
            name = st.text_input(
                get_text('name'),
                placeholder="Your Full Name",
                key="signup_name"
            )
            email = st.text_input(
                get_text('email'),
                placeholder="student@example.com",
                key="signup_email"
            )
            password = st.text_input(
                get_text('password'),
                type="password",
                placeholder="Min. 6 characters",
                key="signup_password"
            )
            grade_level = st.selectbox(
                get_text('grade_level'),
                ["IGCSE Year 10", "IGCSE Year 11"],
                key="signup_grade"
            )
            
            if st.button("✍️ Sign Up", use_container_width=True, key="signup_btn"):
                if name and email and password and grade_level:
                    auth_manager = AuthManager()
                    success, message = auth_manager.signup(email, name, password, grade_level)
                    
                    if success:
                        # Log to Google Sheets
                        from modules.google_sheets import GoogleSheetsLogger
                        logger = GoogleSheetsLogger()
                        logger.log_signup(email, name, grade_level)
                        
                        st.success("✅ Account created! Please log in.")
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.warning("Please fill in all fields")

def show_dashboard():
    """Display main dashboard"""
    if not st.session_state.user_session:
        st.session_state.current_page = "auth"
        st.rerun()
    
    user = st.session_state.user_session
    
    # Header
    UIComponents.header_with_nav("Dashboard")
    
    # Welcome section
    st.markdown(f"""
    <div class="card">
        <h2 style="color: {COLORS['primary_navy']};">👋 Welcome back, {user['name']}!</h2>
        <p style="color: {COLORS['secondary_periwinkle']}; font-size: 16px;">
            Grade: {user['grade_level']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Daily Insight Newsletter
    st.markdown(f"""
    <div class="card" style="background: linear-gradient(135deg, {COLORS['secondary_periwinkle']}, {COLORS['peach']});">
        <h3 style="color: {COLORS['primary_navy']}; margin-top: 0;">📰 Daily IGCSE Insight</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <h4 style="color: {COLORS['primary_navy']};">🧬 Biology Tip</h4>
            <p>Remember: ATP is the energy currency of cells. It's produced in mitochondria during cellular respiration.</p>
            <small style="color: {COLORS['secondary_periwinkle']};">Key term: Adenosine Triphosphate</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="card">
            <h4 style="color: {COLORS['primary_navy']};">⚛️ Physics Tip</h4>
            <p>Newton's Second Law: F=ma. Remember this describes the relationship between force, mass, and acceleration.</p>
            <small style="color: {COLORS['secondary_periwinkle']};">Key term: Force in Newtons</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="card">
            <h4 style="color: {COLORS['primary_navy']};">🧪 Chemistry Tip</h4>
            <p>Atomic number = Number of protons. This determines what element an atom is, not mass number.</p>
            <small style="color: {COLORS['secondary_periwinkle']};">Key term: Atomic Number</small>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown(f"<h3 style='color: {COLORS['primary_navy']}; margin-top: 30px;'>🚀 Quick Actions</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        if st.button("📚 Start Tutoring Session", use_container_width=True, key="start_tutor"):
            st.session_state.current_page = "tutor"
            st.rerun()
    
    with col2:
        if st.button("👤 View Profile", use_container_width=True, key="view_profile"):
            st.session_state.current_page = "profile"
            st.rerun()
    
    with col3:
        if st.button("⚙️ Settings", use_container_width=True, key="view_settings"):
            st.session_state.current_page = "settings"
            st.rerun()

def show_tutor_page():
    """Display tutor interface"""
    if not st.session_state.user_session:
        st.session_state.current_page = "auth"
        st.rerun()
    
    UIComponents.header_with_nav("AI Tutor")
    
    # Step 1: Upload
    st.markdown(f"<h2 style='color: {COLORS['primary_navy']}; margin-top: 20px;'>📤 Step 1: Upload Document</h2>", unsafe_allow_html=True)
    
    UIComponents.drop_zone()
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf", key="pdf_upload")
    
    if uploaded_file:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Step 2: Select Subject
    st.markdown(f"<h2 style='color: {COLORS['primary_navy']}; margin-top: 30px;'>📚 Step 2: Select Subject</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    selected_subject = None
    with col1:
        if st.button("🧬 Biology", use_container_width=True, key="bio_select"):
            st.session_state.selected_subject = "Biology"
    
    with col2:
        if st.button("⚛️ Physics", use_container_width=True, key="phys_select"):
            st.session_state.selected_subject = "Physics"
    
    with col3:
        if st.button("🧪 Chemistry", use_container_width=True, key="chem_select"):
            st.session_state.selected_subject = "Chemistry"
    
    if "selected_subject" in st.session_state:
        st.markdown(f"<p style='color: {COLORS['peach']}; font-weight: bold; font-size: 18px;'>✅ Selected: {st.session_state.selected_subject}</p>", unsafe_allow_html=True)
    
    # Step 3: Interact
    st.markdown(f"<h2 style='color: {COLORS['primary_navy']}; margin-top: 30px;'>💬 Step 3: Chat with AI Tutor</h2>", unsafe_allow_html=True)
    
    if "selected_subject" in st.session_state:
        # Chat interface
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(f"<div style='text-align: right; margin: 10px 0;'><div style='display: inline-block; background-color: {COLORS['primary_navy']}; color: white; padding: 10px 15px; border-radius: 10px; max-width: 70%;'><strong>👤 You:</strong> {message['content']}</div></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: left; margin: 10px 0;'><div style='display: inline-block; background-color: {COLORS['secondary_periwinkle']}; color: {COLORS['primary_navy']}; padding: 10px 15px; border-radius: 10px; max-width: 70%;'><strong>🤖 Tutor:</strong> {message['content']}</div></div>", unsafe_allow_html=True)
        
        # Input
        user_input = st.text_input(
            "Ask your question:",
            placeholder="Type your question about " + st.session_state.selected_subject,
            key="user_question"
        )
        
        if st.button("📤 Send", use_container_width=True, key="send_btn"):
            if user_input:
                # Show loading animation
                with st.spinner("⏳ Validating against Mark Scheme and scanning knowledge gaps..."):
                    from modules.ai_tutor import AITutor
                    tutor = AITutor()
                    response = tutor.generate_response(
                        user_input,
                        st.session_state.selected_subject
                    )
                    
                    if response["success"]:
                        st.session_state.chat_history.append(
                            {"role": "user", "content": user_input}
                        )
                        st.session_state.chat_history.append(
                            {"role": "assistant", "content": response["response"]}
                        )
                        
                        # Log to Google Sheets
                        from modules.google_sheets import GoogleSheetsLogger
                        logger = GoogleSheetsLogger()
                        logger.log_question(
                            st.session_state.user_session["email"],
                            st.session_state.user_session["name"],
                            st.session_state.selected_subject,
                            st.session_state.user_session["grade_level"],
                            user_input,
                            response["response"]
                        )
                        
                        st.rerun()
                    else:
                        st.error("Error generating response. Please try again.")
    else:
        st.info("👆 Please select a subject first to start chatting!")

def show_profile_page():
    """Display user profile"""
    if not st.session_state.user_session:
        st.session_state.current_page = "auth"
        st.rerun()
    
    UIComponents.header_with_nav("Profile")
    
    user = st.session_state.user_session
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"""
        <div class="card">
            <h3 style="color: {COLORS['primary_navy']};">👤 Your Profile</h3>
            <p><strong>Name:</strong> {user['name']}</p>
            <p><strong>Email:</strong> {user['email']}</p>
            <p><strong>Grade Level:</strong> {user['grade_level']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("⬅️ Back to Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

def show_settings_page():
    """Display settings page"""
    if not st.session_state.user_session:
        st.session_state.current_page = "auth"
        st.rerun()
    
    UIComponents.header_with_nav("Settings")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"<h3 style='color: {COLORS['primary_navy']}; margin-bottom: 20px;'>⚙️ Preferences</h3>", unsafe_allow_html=True)
        
        # Language setting
        lang = st.selectbox(
            "Language / Ngôn Ngữ",
            ["en", "vi"],
            format_func=lambda x: "English" if x == "en" else "Tiếng Việt",
            key="lang_select"
        )
        
        if lang != st.session_state.language:
            st.session_state.language = lang
            st.rerun()
        
        st.markdown("---")
        
        # Account settings
        st.markdown(f"<h4 style='color: {COLORS['primary_navy']}; margin-bottom: 15px;'>Account Settings</h4>", unsafe_allow_html=True)
        
        new_name = st.text_input(
            "Display Name",
            value=st.session_state.user_session["name"],
            key="settings_name"
        )
        
        new_password = st.text_input(
            "Change Password (leave blank to keep current)",
            type="password",
            key="settings_password"
        )
        
        if st.button("💾 Save Changes", use_container_width=True):
            from modules.auth import AuthManager
            auth = AuthManager()
            
            updates = {}
            if new_name != st.session_state.user_session["name"]:
                updates["name"] = new_name
                st.session_state.user_session["name"] = new_name
            
            if new_password:
                updates["password"] = new_password
            
            if updates:
                success, msg = auth.update_user(st.session_state.user_session["email"], updates)
                if success:
                    st.success("✅ Changes saved!")
                else:
                    st.error(f"❌ {msg}")
    
    with col2:
        if st.button("⬅️ Back to Dashboard", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()

# Main app logic
def main():
    if st.session_state.current_page == "auth":
        show_auth_page()
    elif st.session_state.current_page == "dashboard":
        show_dashboard()
    elif st.session_state.current_page == "tutor":
        show_tutor_page()
    elif st.session_state.current_page == "profile":
        show_profile_page()
    elif st.session_state.current_page == "settings":
        show_settings_page()

if __name__ == "__main__":
    main()
