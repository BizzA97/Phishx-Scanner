from web.scanner import scan_url
from report_generator import save_report

def run_scanner():
    url = input("🔗 Enter URL to scan: ").strip()
    
    if not url or not url.startswith(('http://', 'https://')):
        print("⚠️ Please enter a valid URL starting with http:// or https://")
        return

    try:
        result = scan_url(url)
    except Exception as e:
        print(f"❌ Error scanning URL: {e}")
        return

    print("\n📊 Scan Result:")
    for key, value in result.items():
        print(f"{key}: {value}")

    choice = input("\n💾 Do you want to save this scan report? (y/n): ").lower()
    if choice == 'y':
        save_report(result)
        print("✅ Report saved successfully.")

if __name__ == "__main__":
    run_scanner()
