
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

# Get metadata by Type
def retrive_metadata_by_type(type):
    data = []
    connection =  app._engine.connect()
    try: 
        select_query = text(f"select element from tb_metadata where type = '{type}'")
        result = connection.execute(select_query)
        for row in result:
            data.append(row[0])
        return data
    except Exception as e:
        print(e)
        return data

def retrive_employee ():
    data = []
    connection =  app._engine.connect()
    try: 
        select_query = text(f"select * from tb_manage_employee")
        result = connection.execute(select_query)
        for row in result:
            employee_data = {
                'employee_id': row[1],  # Assuming employee_id is the first column in your result
                'name': f"{row[2]} {row[4]}"  # Assuming first and second columns are first name and last name
            }
            data.append(employee_data)  
        return data
    except Exception as e:
        print(e)
        return data