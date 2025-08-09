
#this works as any function terminats if one time the condition is true it comes out from the loop 
def uppercase_points(password):
    """Add points if password contains at least one uppercase letter."""
    return 2 if any(c.isupper() for c in password) else 0

def lowercase_points(password):
    """Add points if password contains at least one lowercase letter."""
    return 2 if any(c.islower() for c in password) else 0

def digit_points(password):
    """Add points if password contains at least one digit."""
    return 2 if any(c.isdigit() for c in password) else 0

def special_char_points(password):
    """Add points if password contains at least one special character."""
    special_chars = set('!@#$%^&*()_-+=[]{}|\\:;"\'<>,.?/')
    return 4 if any(c in special_chars for c in password) else 0

def give_suggestions(password):
    """Tell the user how to make their password stronger."""
    special_chars = '!@#$%^&*()_-+=[]{}|\\:;"\'<>,.?/'
    
    #this is dictonary with elements and those elemnets inside them have 2 more elements known as check and message
    check_lists = {
        'uppercase': {
            'check': lambda p: any(c.isupper() for c in p),
            'message': "Add uppercase letters (A–Z)"
        },
        'lowercase': {
            'check': lambda p: any(c.islower() for c in p),
            'message': "Add lowercase letters (a–z)"
        },
        'digit': {
            'check': lambda p: any(c.isdigit() for c in p),
            'message': "Add digits (0–9)"
        },
        'special': {
            'check': lambda p: any(c in special_chars for c in p),
            'message': f"Add special characters ({special_chars})"
        }
    }

    missing = [req['message'] for req in check_lists.values() if not req['check'](password)]

    if not missing:
        return [" Password meets all checks!"]
    return missing
