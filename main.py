from scanner import scan_url
from report_generator import save_report

def run_scanner():
    url = input("🔗 Enter URL to scan: ").strip()
    result = scan_url(url)

    print("\n📊 Scan Result:")
    for key, value in result.items():
        print(f"{key}: {value}")

    choice = input("\n💾 Do you want to save this scan report? (y/n): ").lower()
    if choice == 'y':
        save_report(result)

if __name__ == "__main__":
    run_scanner()
