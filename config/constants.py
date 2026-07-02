import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
SHEET_ID = os.getenv("SHEET_ID")
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

# App Configuration
APP_NAME = "IGCSE Tutor AI"
APP_DESCRIPTION = "Your Personal AI Tutor for IGCSE Science"
APP_VERSION = "1.0.0"

# Session Configuration
SESSION_TIMEOUT = 3600  # 1 hour in seconds
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# AI Configuration
AI_MODEL = "gemini-1.5-flash"
AI_TEMPERATURE = 0.7
AI_MAX_TOKENS = 1024
SYSTEM_PROMPT = """
You are an expert IGCSE Science tutor with deep knowledge of Biology, Physics, and Chemistry.
Your teaching method follows the Socratic approach:
1. Ask guiding questions to help students think deeper
2. Never give direct answers - guide them to discover solutions
3. Point out missing keywords from the Mark Scheme
4. Encourage critical thinking and problem-solving
5. Validate against official Mark Scheme standards

Always respond in the language the student uses (Vietnamese or English).
Format your response with clear sections and use emojis for emphasis.
"""

# Mark Scheme Keywords (will be expanded with full mark schemes)
MARK_SCHEME_KEYWORDS = {
    "Biology": [
        "photosynthesis", "respiration", "ATP", "enzyme", "substrate",
        "active transport", "osmosis", "diffusion", "mitosis", "meiosis",
        "DNA", "gene", "allele", "dominant", "recessive", "natural selection"
    ],
    "Physics": [
        "force", "acceleration", "velocity", "momentum", "energy",
        "power", "work", "current", "voltage", "resistance", "circuit",
        "magnetic field", "electromagnetic induction", "wave", "frequency"
    ],
    "Chemistry": [
        "atom", "molecule", "ion", "compound", "element", "valence",
        "oxidation", "reduction", "exothermic", "endothermic", "pH",
        "catalyst", "equilibrium", "reversible reaction", "ionic bond"
    ]
}

# Google Sheets Column Headers
SHEETS_HEADERS = [
    "Timestamp",
    "Email",
    "Name",
    "Subject",
    "Grade Level",
    "Question/Content",
    "AI Response",
    "User Feedback"
]

# Translation Keys
TRANSLATIONS = {
    "vi": {
        "app_title": "Gia Sư AI IGCSE",
        "welcome": "Chào mừng đến với Gia Sư AI IGCSE",
        "login": "Đăng Nhập",
        "signup": "Đăng Ký",
        "email": "Email",
        "password": "Mật Khẩu",
        "name": "Tên Hiển Thị",
        "grade_level": "Khối Lớp",
        "subject": "Môn Học",
        "upload": "Tải Lên Tài Liệu",
        "select": "Chọn Môn Học",
        "interact": "Tương Tác với Gia Sư",
        "daily_insight": "Thông Tin Học Tập Hàng Ngày",
        "settings": "Cài Đặt",
        "profile": "Hồ Sơ",
        "logout": "Đăng Xuất",
        "loading": "Đang đối chiếu với Mark Scheme và quét lỗ hổng kiến thức...",
    },
    "en": {
        "app_title": "IGCSE AI Tutor",
        "welcome": "Welcome to IGCSE AI Tutor",
        "login": "Login",
        "signup": "Sign Up",
        "email": "Email",
        "password": "Password",
        "name": "Display Name",
        "grade_level": "Grade Level",
        "subject": "Subject",
        "upload": "Upload Document",
        "select": "Select Subject",
        "interact": "Interact with Tutor",
        "daily_insight": "Daily IGCSE Insight",
        "settings": "Settings",
        "profile": "Profile",
        "logout": "Logout",
        "loading": "Validating against Mark Scheme and scanning knowledge gaps...",
    }
}
