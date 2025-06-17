import random
import string

def generate_password(length=12, use_uppercase=True, use_lowercase=True, use_digits=True, use_special=True):
    # Define the character sets
    character_set = ''
    if use_uppercase:
        character_set += string.ascii_uppercase
    if use_lowercase:
        character_set += string.ascii_lowercase
    if use_digits:
        character_set += string.digits
    if use_special:
        character_set += string.punctuation

    # Check if the character set is empty
    if not character_set:
        raise ValueError("At least one character type must be selected.")

    # Generate the password
    password = ''.join(random.choice(character_set) for _ in range(length))
    return password

# User input
length = int(input("Enter the desired password length: "))
use_uppercase = input("Include uppercase letters? (y/n): ").lower() == 'y'
use_lowercase = input("Include lowercase letters? (y/n): ").lower() == 'y'
use_digits = input("Include digits? (y/n): ").lower() == 'y'
use_special = input("Include special characters? (y/n): ").lower() == 'y'

# Generate and display the password
password = generate_password(length, use_uppercase, use_lowercase, use_digits, use_special)
print(f"Generated Password: {password}")
