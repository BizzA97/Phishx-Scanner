import csv
from datetime import datetime

def save_report(result, filename=None):
    if not filename:
        filename = f"scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    headers = list(result.keys())

    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerow(result)

    print(f"\n[✅] Report saved as: {filename}")
