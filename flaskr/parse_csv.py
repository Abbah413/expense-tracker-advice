import csv
from flaskr import line_parsers
from flaskr import models
import re
import io
import os


def import_file(filename):
    with open(filename, newline='') as csvfile:
        content = csvfile.read()
        output = Parse(content)
        export_file(output, filename)


def export_file(output, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in output:
            writer.writerow(row)


def Parse(csv_content, line_parser=None):
  line_parser = line_parser or line_parsers.FindLineParser(csv_content)
  csv_content = line_parser.StripNonCsvData(csv_content)
  csv_mem_file = io.StringIO(csv_content)
  # dialect = csv.Sniffer().sniff(csv_content)
  dialect = 'excel'
  has_header = _HasHeader(csv_content)

  if has_header:
    reader = csv.DictReader(csv_mem_file, dialect=dialect)
  else:
    reader = csv.reader(csv_mem_file, dialect=dialect)

  transactions = []

  for line_item in reader:
    tran = line_parser.ParseLine(line_item)
    if tran:
      transactions.append(tran)

  return transactions


def _HasHeader(csv_content):
  first_line = csv_content.split('\n')[0]
  has_date_1 = re.search(r'\d\d\d\d[/-]\d\d?[/-]\d\d?', first_line)
  has_date_2 = re.search(r'\d\d?[/-]\d\d?[/-]\d\d\d\d', first_line)
  has_amount = re.search(r'\d\.\d\d', first_line)
  actual_content = has_amount and (has_date_1 or has_date_2)
  return not actual_content




