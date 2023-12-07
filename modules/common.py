
# method for password encryption 
def encrypt_password(key, password):
    cipher_suite = Fernet(key)
    encrypted_password = cipher_suite.encrypt(password.encode())
    return encrypted_password

# method for password decryption 
def decrypt_password(key, encrypted_password):
    cipher_suite = Fernet(key)
    decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
    return decrypted_password

def generate_login_id():
    # Generate four random numbers
    numbers = ''.join(random.choices(string.digits, k=4))

    # Generate four random alphabets
    alphabets = ''.join(random.choices(string.ascii_letters, k=4))

    # Combine numbers and alphabets
    login_id = alphabets + numbers

    return login_id