from flask import current_app
from flask_mail import Message
from app import mail


class EmailService:
    @staticmethod
    def send_otp_email(email, otp):
        """Send OTP email to user"""
        try:
            msg = Message(
                subject='StockMaster - Password Reset OTP',
                recipients=[email],
                html=f"""
                <html>
                    <body>
                        <h2>Password Reset Request</h2>
                        <p>Your OTP for password reset is: <strong>{otp}</strong></p>
                        <p>This OTP is valid for 10 minutes.</p>
                        <p>If you didn't request this, please ignore this email.</p>
                    </body>
                </html>
                """
            )
            mail.send(msg)
            return True
        except Exception as e:
            current_app.logger.error(f"Failed to send email: {str(e)}")
            return False

