from checker.common import load_common_passwords
from checker.complexity import give_suggestions
from checker.strength import calculate_password_strength, display_strength, is_breached
def main():
    print("\t\tWelcome To Password Strength Checker\n")
    print("Very Weak = 1-7")
    print("Weak      = 8-10")
    print("Good      = 11-13")
    print("Strong    = 14-16+\n")

    common_passwords = load_common_passwords("Data/weak_passwords.txt")

    while True:
        password = input("Enter Password To Check Strength: ").strip()
        if not password.strip():
            print("Password cannot be Empty..")
            continue
        check,count = is_breached(password)
        if(check == True):
            print(f"The Password has been Breached {count} times.Chose a stronger one!")
            continue

        points = calculate_password_strength(password, common_passwords)
        print(f"Points: {points}")
        print(f"Strength: {display_strength(points)}\n")
        for suggest in give_suggestions(password):
            print(f"Missing:{suggest}")


if __name__ == "__main__":
    main()