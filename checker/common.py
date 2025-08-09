
def load_common_passwords(filename):
    """
    Load common passwords from a file into a set.
    Returns a set of lowercase passwords for quick lookup.
    """
    common_passwords = set()
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                password = line.strip()
                if password:
                    common_passwords.add(password.lower())
        return common_passwords
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found. Using fallback list.")
        return {"password", "123456", "qwerty", "password123"}

def is_password_common(password, common_passwords):
    """Check if the password exists in the common password list."""
    return password.lower() in common_passwords