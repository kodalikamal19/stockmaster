from datetime import datetime, timedelta
import pyotp
import secrets
from app import db
from app.models.user import User


class OTPService:
    @staticmethod
    def generate_otp(user_email):
        """Generate and store OTP for user"""
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return None
        
        # Generate 6-digit OTP
        otp = ''.join([str(secrets.randbelow(10)) for _ in range(6)])
        
        # Store OTP (using a simple approach - in production, use Redis or similar)
        user.otp_secret = otp
        user.otp_expires_at = datetime.utcnow() + timedelta(minutes=10)
        
        db.session.commit()
        
        return otp
    
    @staticmethod
    def verify_otp(user_email, otp):
        """Verify OTP for user"""
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return False
        
        if not user.otp_secret or not user.otp_expires_at:
            return False
        
        if datetime.utcnow() > user.otp_expires_at:
            return False
        
        if user.otp_secret != otp:
            return False
        
        # Clear OTP after successful verification
        user.otp_secret = None
        user.otp_expires_at = None
        db.session.commit()
        
        return True
    
    @staticmethod
    def clear_otp(user_email):
        """Clear OTP for user"""
        user = User.query.filter_by(email=user_email).first()
        if user:
            user.otp_secret = None
            user.otp_expires_at = None
            db.session.commit()

