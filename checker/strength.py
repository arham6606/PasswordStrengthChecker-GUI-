#these are used to get the API working going on 
import hashlib
import requests

#importing modules from user defined helper files
from .common import is_password_common
from .length import length_points
from .complexity import (
    uppercase_points,
    lowercase_points,
    digit_points,
    special_char_points
)

def calculate_password_strength(password, common_passwords):
    """Calculate total points for the password."""
    #check this from a txt file which contains almost 1000,000 thouand passwords
    if is_password_common(password, common_passwords):
        print("⚠ Password is very common! Please choose another.")
        return 0
    
    #Adding points
    points = 0
    points += length_points(password)
    points += uppercase_points(password)
    points += lowercase_points(password)
    points += digit_points(password)
    points += special_char_points(password)
    return points

def display_strength(points):
    """Display password strength category based on points."""
    if points <= 7:
        return "Very Weak"
    elif 8 <= points <= 10:
        return "Weak"
    elif 11 <= points <= 13:
        return "Good"
    else:
        return "Strong"

#in this block the API we are using is from have i been pawned    
def is_breached(password):
    #have i been pawned request the first 5 characters of a 40 bit hexadecimal number for privacy reasons and then according to that 5 characters it sends back the passwords which matches those 

    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix , suffix = sha1[:5],sha1[5:]

    try:
        api = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}",
                           headers={"User-Agent": "PasswordCheckerApp/1.0"}
        )
        api.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError("Failed To Reach HBIP Server...")

    #have i been pawned sends a suffix which is the remaining characters after the first 5 characters and the count meaning how many times this password has been breached

    for lines in api.text.splitlines():
        breached , count = lines.split(":")
        if breached == suffix:
            return (True,count)
    return (False,0)