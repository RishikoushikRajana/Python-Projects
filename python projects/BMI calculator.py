def calculate_bmi(weight, height):
    """Calculate BMI using weight in kg and height in meters."""
    bmi = weight / (height ** 2)
    return bmi

def categorize_bmi(bmi):
    """Categorize the BMI result."""
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

# User input
try:
    weight = float(input("Enter your weight in kilograms: "))
    height = float(input("Enter your height in meters: "))

    # Calculate BMI
    bmi = calculate_bmi(weight, height)
    category = categorize_bmi(bmi)

    # Display the result
    print(f"Your BMI is: {bmi:.2f}")
    print(f"Category: {category}")

except ValueError:
    print("Please enter valid numerical values for weight and height.")
