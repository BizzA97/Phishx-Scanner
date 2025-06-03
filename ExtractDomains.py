import pandas as pd
import tldextract

# Load your CSV file
df = pd.read_csv("phishing_site_urls.csv")  # Replace with the actual CSV filename

# Optional: Print columns to verify correct header
print("CSV Columns:", df.columns)

# Access the correct column (case-sensitive!)
urls = df['URL']

# Extract and store domains
domains = set()
for url in urls:
    ext = tldextract.extract(url)
    domain = ext.registered_domain
    if domain:
        domains.add(domain)

# Save domains to blacklist.txt
with open("blacklist.txt", "w") as f:
    for domain in sorted(domains):
        f.write(domain + "\n")

print(f"✅ Saved {len(domains)} domains to blacklist.txt")
