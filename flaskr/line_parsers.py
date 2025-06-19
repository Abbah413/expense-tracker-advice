import csv

class CSVFormatNotSupportedError(Exception):
    pass

# Registry
REGISTERED_PARSERS = []

def RegisterLineParser(cls):
    REGISTERED_PARSERS.append(cls())
    return cls

def FindLineParser(header_line):
    for parser in REGISTERED_PARSERS:
        if parser.matches_header(header_line):
            return parser
    raise CSVFormatNotSupportedError(
        f"No parser matched. Header: '{header_line}'. "
        f"Supported: {', '.join([p.name for p in REGISTERED_PARSERS])}"
    )

class BaseBankParser:
    name = "BaseBank"

    def matches_header(self, header_line):
        raise NotImplementedError

    def parse_line(self, line):
        raise NotImplementedError


@RegisterLineParser
class ZenithBankParser(BaseBankParser):
    name = "Zenith Bank"

    def matches_header(self, header_line):
        return "Date,Description,Withdrawals,Deposits,Balance" in header_line

    def parse_line(self, line):
        reader = csv.reader([line])
        row = next(reader)
        return {
            'date': row[0],
            'description': row[1],
            'withdrawal': float(row[2]) if row[2] else 0.0,
            'deposit': float(row[3]) if row[3] else 0.0,
            'balance': float(row[4]),
        }

@RegisterLineParser
class GTBankParser(BaseBankParser):
    name = "GT Bank"

    def matches_header(self, header_line):
        return "Transaction Date,Transaction Details,Amount,Balance" in header_line

    def parse_line(self, line):
        reader = csv.reader([line])
        row = next(reader)
        amount = float(row[2])
        return {
            'date': row[0],
            'description': row[1],
            'withdrawal': -amount if amount < 0 else 0.0,
            'deposit': amount if amount > 0 else 0.0,
            'balance': float(row[3]),
        }

@RegisterLineParser
class FirstBankParser(BaseBankParser):
    name = "First Bank"

    def matches_header(self, header_line):
        return "Date,Details,Debit,Credit,Balance" in header_line

    def parse_line(self, line):
        reader = csv.reader([line])
        row = next(reader)
        return {
            'date': row[0],
            'description': row[1],
            'withdrawal': float(row[2]) if row[2] else 0.0,
            'deposit': float(row[3]) if row[3] else 0.0,
            'balance': float(row[4]),
        }

@RegisterLineParser
class OpayParser(BaseBankParser):
    name = "Opay"

    def matches_header(self, header_line):
        return "Date,Reference,Type,Amount,Balance" in header_line

    def parse_line(self, line):
        reader = csv.reader([line])
        row = next(reader)
        tx_type = row[2].lower()
        amount = float(row[3])
        return {
            'date': row[0],
            'description': row[1],
            'withdrawal': amount if 'debit' in tx_type else 0.0,
            'deposit': amount if 'credit' in tx_type else 0.0,
            'balance': float(row[4]),
        }

@RegisterLineParser
class KudaParser(BaseBankParser):
    name = "Kuda"

    def matches_header(self, header_line):
        return "Date,Description,Type,Amount,Balance" in header_line

    def parse_line(self, line):
        reader = csv.reader([line])
        row = next(reader)
        tx_type = row[2].lower()
        amount = float(row[3])
        return {
            'date': row[0],
            'description': row[1],
            'withdrawal': amount if 'debit' in tx_type else 0.0,
            'deposit': amount if 'credit' in tx_type else 0.0,
            'balance': float(row[4]),
        }

@RegisterLineParser
class KeystoneBankParser(BaseBankParser):
    name = "Keystone Bank"

    def matches_header(self, header_line):
        return "Date,Narration,Withdrawal,Deposit,Balance" in header_line

    def parse_line(self, line):
        reader = csv.reader([line])
        row = next(reader)
        return {
            'date': row[0],
            'description': row[1],
            'withdrawal': float(row[2]) if row[2] else 0.0,
            'deposit': float(row[3]) if row[3] else 0.0,
            'balance': float(row[4]),
        }
