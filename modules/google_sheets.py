import gspread
from google.oauth2.service_account import Credentials
from config.constants import GOOGLE_SHEETS_CREDENTIALS, SHEET_ID, SHEETS_HEADERS
from datetime import datetime
import json

class GoogleSheetsLogger:
    """Manage Google Sheets data logging for user activities"""
    
    def __init__(self):
        self.sheet_id = SHEET_ID
        self.creds_file = GOOGLE_SHEETS_CREDENTIALS
        self.client = None
        self.worksheet = None
        self.initialize_connection()
    
    def initialize_connection(self):
        """Initialize connection to Google Sheets"""
        try:
            if not self.creds_file or not self.sheet_id:
                print("⚠️ Google Sheets credentials or Sheet ID not configured")
                return False
            
            # Set up credentials
            scope = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
            
            creds = Credentials.from_service_account_file(
                self.creds_file,
                scopes=scope
            )
            
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_key(self.sheet_id)
            
            # Get or create worksheet
            try:
                self.worksheet = self.spreadsheet.worksheet("Activity Log")
            except:
                self.worksheet = self.spreadsheet.add_worksheet("Activity Log", 100, 10)
                self.worksheet.append_row(SHEETS_HEADERS)
            
            return True
        
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {str(e)}")
            return False
    
    def log_signup(self, email: str, name: str, grade_level: str) -> bool:
        """Log new user signup"""
        try:
            if not self.worksheet:
                return False
            
            row = [
                datetime.now().isoformat(),
                email,
                name,
                "System",
                grade_level,
                f"New user signup",
                "Account created",
                "Signup"
            ]
            
            self.worksheet.append_row(row)
            return True
        
        except Exception as e:
            print(f"❌ Error logging signup: {str(e)}")
            return False
    
    def log_question(self, email: str, name: str, subject: str, grade_level: str, 
                     question: str, ai_response: str = "", feedback: str = "") -> bool:
        """Log student question and AI response"""
        try:
            if not self.worksheet:
                return False
            
            # Truncate long content for sheets
            question_trunc = question[:500] if question else ""
            response_trunc = ai_response[:500] if ai_response else ""
            feedback_trunc = feedback[:200] if feedback else ""
            
            row = [
                datetime.now().isoformat(),
                email,
                name,
                subject,
                grade_level,
                question_trunc,
                response_trunc,
                feedback_trunc
            ]
            
            self.worksheet.append_row(row)
            return True
        
        except Exception as e:
            print(f"❌ Error logging question: {str(e)}")
            return False
    
    def log_document_upload(self, email: str, name: str, subject: str, 
                           filename: str, grade_level: str) -> bool:
        """Log document upload activity"""
        try:
            if not self.worksheet:
                return False
            
            row = [
                datetime.now().isoformat(),
                email,
                name,
                subject,
                grade_level,
                f"Document uploaded: {filename}",
                "Processing",
                "Upload"
            ]
            
            self.worksheet.append_row(row)
            return True
        
        except Exception as e:
            print(f"❌ Error logging document upload: {str(e)}")
            return False
