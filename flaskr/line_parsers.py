# -*- coding: utf-8 -*-
import csv
import datetime
import re
from flaskr import models


_REGISTERED_PARSERS = []

# 
def RegisterLineParser(cls):
  _REGISTERED_PARSERS.append(cls)
  return cls


def FindLineParser(csv_content):
  for parser_cls in _REGISTERED_PARSERS:
    if parser_cls.ContentFits(csv_content):
      return parser_cls()
  raise CSVFormatNotSupportedError()


class CSVFormatNotSupportedError(Exception):
  pass



class AbstractLineParser(object):
  STATEMENT_FORMAT = ''

  @classmethod
  def ContentFits(cls, csv_content):
    return cls.FirstLineFits(csv_content.split('\n')[0].strip())

  @classmethod
  def FirstLineFits(cls, first_line):
    return False

  def StripNonCsvData(self, csv_content):
    return csv_content

  def GetBankName(self):
    pass

  def ParseLine(self, arr_or_dict, bank):
    raise NotImplementedError()


class AbstractDirectExtractLineParser(AbstractLineParser):
  DATE_FORMAT = ''
  DATE_FIELD = ''
  AMOUNT_FIELD = ''
  DESC_FIELD = ''
  TYPE_FIELD = ''  # optional

  def ParseLine(self, line_dict, name):
    date_str = line_dict[self.DATE_FIELD]
    date = datetime.datetime.strptime(date_str, self.DATE_FORMAT).date()
    bank = name
    amount = float(line_dict[self.AMOUNT_FIELD])
    description = line_dict[self.DESC_FIELD]
    type = line_dict[self.TYPE_FIELD] if self.TYPE_FIELD else None
    return models.Transaction(date, bank, amount, description, type)


@RegisterLineParser
class AllyParser(AbstractDirectExtractLineParser):
  STATEMENT_FORMAT = 'Ally Bank Account'
  DATE_FORMAT = '%Y-%m-%d'
  DATE_FIELD = 'Date'
  AMOUNT_FIELD = ' Amount'
  DESC_FIELD = ' Description'
  TYPE_FIELD = ' Type'

  @classmethod
  def FirstLineFits(cls, first_line):
    return first_line == 'Date, Time, Amount, Type, Description'

  def GetBankName(self):
    return 'Ally'


@RegisterLineParser
class BofaAccountParser(AbstractDirectExtractLineParser):
  STATEMENT_FORMAT = 'Bank of America Bank Account'
  DATE_FORMAT = '%m/%d/%Y'
  DATE_FIELD = 'Date'
  AMOUNT_FIELD = 'Amount'
  DESC_FIELD = 'Description'

  @classmethod
  def FirstLineFits(cls, first_line):
    return first_line == 'Description,,Summary Amt.'

  def StripNonCsvData(self, csv_content):
    csv_content = csv_content.replace('\r', '')
    parts = csv_content.split('\n\n')
    return parts[1]

  def GetBankName(self):
    return 'BOFA'

  def ParseLine(self, line_dict, name):
    if not line_dict['Amount']:
      return None
    return super(BofaAccountParser, self).ParseLine(line_dict, name)


@RegisterLineParser
class BofaCardParser(AbstractDirectExtractLineParser):
  STATEMENT_FORMAT = 'Bank of America Credit Card'
  DATE_FORMAT = '%m/%d/%Y'
  DATE_FIELD = 'Posted Date'
  AMOUNT_FIELD = 'Amount'
  DESC_FIELD = 'Payee'

  @classmethod
  def FirstLineFits(cls, first_line):
    return first_line == 'Posted Date,Reference Number,Payee,Address,Amount'

  def GetBankName(self):
    return 'BOFA'


@RegisterLineParser
class ChaseAccountParser(AbstractDirectExtractLineParser):
  STATEMENT_FORMAT = 'Chase Bank Account'
  DATE_FORMAT = '%m/%d/%Y'
  DATE_FIELD = 'Post Date'
  AMOUNT_FIELD = 'Amount'
  DESC_FIELD = 'Description'
  TYPE_FIELD = 'Type'

  @classmethod
  def FirstLineFits(cls, first_line):
    return first_line == 'Type,Post Date,Description,Amount,Check or Slip #'

  def GetBankName(self):
    return 'Chase'


@RegisterLineParser
class ChaseAccount2Parser(AbstractDirectExtractLineParser):
  STATEMENT_FORMAT = 'Chase Bank Account'
  DATE_FORMAT = '%m/%d/%Y'
  DATE_FIELD = 'Posting Date'
  AMOUNT_FIELD = 'Amount'
  DESC_FIELD = 'Description'
  TYPE_FIELD = 'Type'

  @classmethod
  def FirstLineFits(cls, first_line):
    return first_line in [('Details,Posting Date,"Description",Amount,'
                           'Type,Balance,Check or Slip #,'),
                          ('Details,Posting Date,Description,Amount,'
                           'Type,Balance,Check or Slip #')]

  def GetBankName(self):
    return 'Chase'


@RegisterLineParser
class ChaseCardParser(AbstractDirectExtractLineParser):
  STATEMENT_FORMAT = 'Chase Credit Card'
  DATE_FORMAT = '%m/%d/%Y'
  DATE_FIELD = 'Trans Date'
  AMOUNT_FIELD = 'Amount'
  DESC_FIELD = 'Description'
  TYPE_FIELD = 'Type'

  @classmethod
  def FirstLineFits(cls, first_line):
    return first_line == 'Type,Trans Date,Post Date,Description,Amount'

  def GetBankName(self):
    return 'Chase'


@RegisterLineParser
class DiscoverCardParser(AbstractDirectExtractLineParser):
  STATEMENT_FORMAT = 'Discover Credit Card'
  DATE_FORMAT = '%m/%d/%Y'
  DATE_FIELD = 'Trans. Date'
  AMOUNT_FIELD = 'Amount'
  DESC_FIELD = 'Description'
  TYPE_FIELD = 'Category'

  @classmethod
  def FirstLineFits(cls, first_line):
    return first_line == 'Trans. Date,Post Date,Description,Amount,Category'

  def StripNonCsvData(self, csv_content):
    return csv_content.replace('\t', '')

  def GetBankName(self):
    return 'Discover'

  def ParseLine(self, line_dict, name):
    tran = super(DiscoverCardParser, self).ParseLine(line_dict, name)
    return tran._replace(amount=-tran.amount)


@RegisterLineParser
class TargetCardParser(AbstractLineParser):
  STATEMENT_FORMAT = 'Target Credit Card'

  @classmethod
  def FirstLineFits(cls, first_line):
    r = csv.reader([first_line])
    line_parts = r.__next__()
    if len(line_parts) != 5:
      return False
    if not re.match(r'\d\d/\d\d/\d\d\d\d', line_parts[0]):
      return False
    if not re.match(r'\d\d/\d\d/\d\d\d\d', line_parts[1]):
      return False
    if not re.match(r'-?\d+\.\d\d', line_parts[3]):
      return False
    return True

  def GetBankName(self):
    return 'Target'

  def ParseLine(self, line_parts, name):
    if not line_parts:
      return None
    date_str = line_parts[0]
    date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date()
    description = line_parts[2]
    amount = float(line_parts[3])
    type = line_parts[4]
    bank = name
    return models.Transaction(date, bank, amount, description, type)


@RegisterLineParser
class WellsFargoParser(AbstractLineParser):
  STATEMENT_FORMAT = 'Wells Fargo'
  @classmethod
  def FirstLineFits(cls, first_line):
    r = csv.reader([first_line])
    line_parts = r.__next__()
    if len(line_parts)!= 5:
      return False
    if not re.match(r'\d\d/\d\d/\d\d\d\d', line_parts[0]):
      return False
    if not re.match(r'-?\d+\.\d\d', line_parts[1]):
      return False
    if not re.match(r'\*', line_parts[2]):
      return False
    if not re.match(r'^\s*$', line_parts[3]):
      return False
    return True

  def GetBankName(self):
    return 'WellsFargo'

  def ParseLine(self, line_parts, name):
    if not line_parts:
      return None
    date_str = line_parts[0]
    date = datetime.datetime.strptime(date_str, '%m/%d/%Y').date()
    description = line_parts[4]
    amount = float(line_parts[1])
    bank = name
    return models.Transaction(date, bank, amount, description, None)
    