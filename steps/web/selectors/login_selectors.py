# selectors/login_selectors.py

class LoginSelectors:
    """Selectors for Login Page"""
    
    def __init__(self):
        # Form elements
        self.USERNAME_INPUT = "#username"
        self.PASSWORD_INPUT = "#password"
        self.LOGIN_BUTTON = "#login-button"
        
        # Messages and notifications
        self.ERROR_MESSAGE = ".error-message"
        self.SUCCESS_MESSAGE = ".success-message"
        
        # State indicators
        self.LOGGED_IN_INDICATOR = ".dashboard-welcome"
        
        # Additional elements
        self.FORGOT_PASSWORD_LINK = "[data-testid='forgot-password']"
        self.REMEMBER_ME_CHECKBOX = "#remember-me"