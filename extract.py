"""Extract data from SFEndorsements."""

from bs4 import BeautifulSoup

def extract_row(row):
  cells = row.find_all('td')
  org = cells[0].button.text
  endorsements = [td.text for td in cells[1:]]
  return org, endorsements

def extract_table(table):
  rows = table.find_all('tr')
  props = [th.text[5:] for th in rows[0].find_all('th')[1:]]
  all_endorsements = {}
  for row in rows[1:]:
    org, endorsements = extract_row(row)
    if len(endorsements) != len(props):
      raise ValueError(f'{org} has {len(endorsements)} endorsements) '
                        'but should have {len(props)}')
    for prop, endorsement in zip(props, endorsements):
      all_endorsements[(org, prop)] = endorsement
  return all_endorsements

def extract_endorsements(filename='endorsements.html'):
  html = open(filename).read()
  soup = BeautifulSoup(html, features='html.parser')
  tables = soup.find_all('table')
  all_endorsements = {}
  for table in tables:
    endorsements = extract_table(table)
    for k, v in endorsements.items():
      if k in all_endorsements:
        raise ValueError(f'duplicate endorsement for {k}')
      all_endorsements[k] = v
  return all_endorsements
