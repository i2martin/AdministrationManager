import re


def check_password(password):
    # Check if password is between 8 and 30 characters long
    if len(password) < 8 or len(password) > 30:
        return False

    # Check if password contains at least one uppercase letter, one lowercase letter, and one number
    if not re.search(r'[A-Z,Č,Š,Ć,Đ,Ž]', password) or not re.search(r'[a-z,č,š,ć,đ,ž]', password) or not re.search(r'\d', password):
        return False

    # Check if password contains at least one special character
    if not re.search(r'[!@#$%^&*()_+{}|:"<>?\-=[\];\',./]', password):
        return False

        # Check if password contains any SQL statements
        sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'AND', 'OR']
        for keyword in sql_keywords:
            if keyword in password.upper():
                return False

    return True


def check_username(username):
    # Check if username is between 6 and 30 characters long
    if len(username) < 6 or len(username) > 30:
        return False

    # Check if username contains only allowed characters
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False

    # Check if username contains any SQL statements
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'AND', 'OR']
    for keyword in sql_keywords:
        if keyword in username.upper():
            return False

    return True