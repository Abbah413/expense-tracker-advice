import csv

def parse_csv(filepath):
    transactions = []

    def clean_amount(value):
        try:
            if not value or value.strip() in ('', '00.00'):
                return 0.0
            # Remove commas, currency symbols if any, strip whitespace
            value_clean = value.replace(',', '').replace('₦', '').strip()
            return float(value_clean)
        except Exception as e:
            print(f"⚠️ Could not parse amount '{value}': {e}")
            return 0.0

    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            if not row or all(not v.strip() for v in row.values() if v):
                # Skip empty or all-blank rows
                continue

            # Normalize keys in case CSV header varies
            date = row.get('Date') or row.get('date') or ''
            desc = row.get('Description') or row.get('description') or ''
            deposits = row.get('Deposits') or row.get('Deposit') or ''
            withdrawls = row.get('Withdrawls') or row.get('Withdrawals') or row.get('Withdrawal') or ''
            balance = row.get('Balance') or ''

            transactions.append({
                'date': date.strip(),
                'description': desc.strip(),
                'deposit': clean_amount(deposits),
                'withdrawal': clean_amount(withdrawls),
                'balance': clean_amount(balance),
            })

    print(f"✅ Parsed {len(transactions)} transactions from CSV")
    return transactions
