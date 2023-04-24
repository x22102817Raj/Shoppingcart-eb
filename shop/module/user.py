
import re


def checkloginpassword(password):
    if(password):
        pattern_upper = re.compile('[A-Z]')
        pattern_lower = re.compile('[a-z]')
        pattern_digit = re.compile('\d')
        pattern_special = re.compile('[!@#$%^&*()]')

        if len(password) < 8:
            return "Password must be at least 8 characters long."

        if not pattern_upper.search(password):
            return "Password must contain at least one uppercase letter."

        if not pattern_lower.search(password):
            return "Password must contain at least one lowercase letter."

        if not pattern_digit.search(password):
            return "Password must contain at least one digit."
        
        if not pattern_special.search(password):
            return "Password must contain at least one special character (!@#$%^&*())."

        return True
    else:
        return "Wrong password"