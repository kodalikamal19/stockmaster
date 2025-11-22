import re
from flask import current_app


class ValidationError(Exception):
    pass


def validate_login_id(login_id):
    """Validate login_id: unique, 6-12 characters"""
    if not login_id:
        raise ValidationError("Login ID is required")
    
    if len(login_id) < 6 or len(login_id) > 12:
        raise ValidationError("Login ID must be between 6 and 12 characters")
    
    # Check for alphanumeric
    if not re.match(r'^[a-zA-Z0-9_]+$', login_id):
        raise ValidationError("Login ID can only contain letters, numbers, and underscores")
    
    return True


def validate_email(email):
    """Validate email format"""
    if not email:
        raise ValidationError("Email is required")
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Invalid email format")
    
    return True


def validate_password(password):
    """Validate password: ≥8 chars, at least 1 lowercase, 1 uppercase, 1 number, 1 special char"""
    if not password:
        raise ValidationError("Password is required")
    
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters")
    
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter")
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter")
    
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one number")
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character")
    
    return True

