import os
import csv
from bs4 import BeautifulSoup
import re

output_rows = []

for filename in os.listdir():
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            # Find student name and reg number
            name_cell = soup.find('td', colspan="6")
            if name_cell:
                full_text = name_cell.get_text(strip=True)
                match = re.match(r'(.+)\s+\(\s*(\d+)\s*\)', full_text)
                if match:
                    name = match.group(1).strip()
                    regnum = match.group(2).strip()
                else:
                    continue  # skip if pattern doesn't match
            else:
                continue  # skip if not found

            # Extract subject rows
            rows = name_cell.find_parent('table').find_all('tr')[2:]
            subjects = []
            total_marks = ''
            total_row = ""  # initialize
            
            for row in rows:
                cols = [td.get_text(strip=True) for td in row.find_all('td')]
                if len(cols) >= 5 and 'TOTAL' not in cols[0].upper():
                    subjects.append(' '.join(cols[:5]))
                elif 'TOTAL' in cols[0].upper():
                    total_row = ' '.join(cols).strip()  # store TOTAL row text

            row_data = [name, regnum] + subjects + [total_row]
            output_rows.append(row_data)

# Save to CSV
with open('results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'RegNumber', 'Subjects...', 'Total'])
    writer.writerows(output_rows)
