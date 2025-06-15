def generate_advice(transactions):
    advice = []

    total_spent = sum(t['Amount'] for t in transactions)
    food_spent = sum(t['Amount'] for t in transactions if t['Category'] == 'Food')
    bills_spent = sum(t['Amount'] for t in transactions if t['Category'] == 'Bills')

    if total_spent > 1000:
        advice.append("You're spending quite a lot overall. Consider reviewing your monthly budget.")
    if food_spent > 200:
        advice.append("Food expenses are high. Meal planning can help you save money.")
    if bills_spent > 300:
        advice.append("High spending on bills. Check for ways to cut subscriptions or utilities.")

    if not advice:
        advice.append("Great job! Your spending seems well balanced.")

    return advice
