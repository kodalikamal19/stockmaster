"""
Helper script to generate password hashes for users
Run: python generate_password_hash.py
"""
from werkzeug.security import generate_password_hash

# Generate hash for password: Password123!
password = "Password123!"
hash_value = generate_password_hash(password)

print(f"Password: {password}")
print(f"Hash: {hash_value}")
print("\nUse this hash in the SQL INSERT statement for users table.")

