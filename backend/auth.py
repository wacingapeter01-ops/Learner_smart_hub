import bcrypt

def hash_password(password: str):
    # Generates a secure salt and hashes the password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str):
    # Compares the login attempt with the secure hash
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# --- TEST IT ---
raw_pass = "MySuperSecurePassword123!"
scrambled = hash_password(raw_pass)
print(f"What the database sees: {scrambled}")
