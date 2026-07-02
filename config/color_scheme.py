# Deep Focus Color Palette
COLORS = {
    "primary_navy": "#374375",
    "background_cloud": "#FFFCF5",
    "secondary_periwinkle": "#BABDE2",
    "maroon": "#895159",
    "peach": "#DFAEA1",
    "white": "#FFFFFF",
    "dark_gray": "#2D2D2D",
    "light_gray": "#F5F5F5",
}

# UI Styling Constants
SHADOW_STYLE = """
box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1), 0 1px 3px rgba(0, 0, 0, 0.08);
"""

CARD_STYLE = f"""
background-color: {COLORS['background_cloud']};
border-radius: 12px;
padding: 20px;
{SHADOW_STYLE}
border: 1px solid rgba(55, 67, 117, 0.1);
"""

# Font Configuration
FONT_SIZES = {
    "h1": 32,
    "h2": 24,
    "h3": 20,
    "body": 16,
    "small": 14,
    "caption": 12,
}

# Animation Timings (milliseconds)
ANIMATION_TIMINGS = {
    "hover": 200,
    "click": 150,
    "loading": 1500,
}

# Subjects
SUBJECTS = ["Biology", "Physics", "Chemistry"]

# Grade Levels
GRADE_LEVELS = ["IGCSE Year 10", "IGCSE Year 11"]

# Languages
LANGUAGES = {
    "vi": "Tiếng Việt",
    "en": "English"
}
