import streamlit as st
from config.color_scheme import COLORS
import json

class UIComponents:
    """Reusable UI components with Deep Focus design system"""
    
    @staticmethod
    def custom_css():
        """Apply custom CSS styling"""
        css = f"""
        <style>
        :root {{
            --primary-navy: {COLORS['primary_navy']};
            --background-cloud: {COLORS['background_cloud']};
            --secondary-periwinkle: {COLORS['secondary_periwinkle']};
            --maroon: {COLORS['maroon']};
            --peach: {COLORS['peach']};
        }}
        
        * {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }}
        
        body {{
            background-color: var(--background-cloud);
            color: var(--primary-navy);
        }}
        
        .card {{
            background-color: var(--background-cloud);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
            border: 1px solid rgba(55, 67, 117, 0.1);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .card:hover {{
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15), 0 2px 4px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }}
        
        .stButton > button {{
            background-color: var(--primary-navy);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }}
        
        .stButton > button:hover {{
            background-color: {COLORS['maroon']};
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
            transform: scale(0.98);
        }}
        
        .loading {{
            animation: pulse 1.5s ease-in-out infinite;
            color: var(--primary-navy);
            font-weight: 600;
        }}
        
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        
        h1, h2, h3 {{
            color: var(--primary-navy);
            font-weight: 700;
        }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    
    @staticmethod
    def header_with_nav(page_title: str, show_logout: bool = True):
        """Display header with navigation"""
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"<h1 style='color: {COLORS['primary_navy']}'>🎓 {page_title}</h1>", unsafe_allow_html=True)
        
        with col2:
            if show_logout:
                if st.button("🚪 Logout", key="logout_btn"):
                    st.session_state.user_session = None
                    st.rerun()
    
    @staticmethod
    def subject_selector(selected_subject: str = None) -> str:
        """Display subject selection buttons"""
        st.markdown("### 📚 Select Subject")
        
        col1, col2, col3 = st.columns(3, gap="medium")
        
        with col1:
            if st.button("🧬 Biology", key="bio_btn", use_container_width=True):
                return "Biology"
        
        with col2:
            if st.button("⚛️ Physics", key="phys_btn", use_container_width=True):
                return "Physics"
        
        with col3:
            if st.button("🧪 Chemistry", key="chem_btn", use_container_width=True):
                return "Chemistry"
        
        return selected_subject
    
    @staticmethod
    def card_container(content: str, title: str = "", style: str = "default"):
        """Display content in a styled card"""
        st.markdown(f"""
        <div class="card">
            <div style="padding: 12px;">
                {f"<h3 style='color: {COLORS['primary_navy']}'>{title}</h3>" if title else ""}
                <div>{content}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def drop_zone(label: str = "📄 Drag and drop your PDF here"):
        """Display drag-and-drop zone for file uploads"""
        st.markdown(f"""
        <div style="
            border: 2px dashed {COLORS['primary_navy']};
            border-radius: 12px;
            padding: 40px 20px;
            text-align: center;
            background-color: rgba(55, 67, 117, 0.05);
            transition: all 0.3s ease;
            cursor: pointer;
        ">
            <p style="font-size: 18px; color: {COLORS['primary_navy']}; font-weight: 600;">
                {label}
            </p>
            <p style="color: {COLORS['secondary_periwinkle']}; margin-top: -10px;">
                or click below to browse
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def loading_animation(message: str = "Loading..."):
        """Display loading animation"""
        st.markdown(f"""
        <div class="loading">
            ⏳ {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def message_bubble(message: str, is_user: bool = True):
        """Display chat message bubble"""
        bubble_style = f"""
            background-color: {COLORS['primary_navy'] if is_user else COLORS['secondary_periwinkle']};
            color: {COLORS['white'] if is_user else COLORS['primary_navy']};
            border-radius: 12px;
            padding: 12px 16px;
            margin: 8px 0;
            max-width: 80%;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        """
        alignment = "right" if is_user else "left"
        sender = "👤 You" if is_user else "🤖 AI Tutor"
        
        st.markdown(f"""
        <div style="display: flex; justify-content: flex-{alignment};">
            <div style="{bubble_style}">
                <strong>{sender}</strong>
                <p>{message}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
