import bcrypt

# Test bcrypt availability and generate a sample hash
print("bcrypt module:", bcrypt.__version__)
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(b"admin123", salt)
print("Sample hashed password:", hashed.decode())
print("Verify ok:", bcrypt.checkpw(b"admin123", hashed))
print("Verify bad:", bcrypt.checkpw(b"wrong", hashed))
