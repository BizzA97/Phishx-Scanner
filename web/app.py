from flask import Flask, render_template, request, send_file
from io import StringIO, BytesIO
import csv
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from scanner import scan_url  # core logic from scanner.py

app = Flask(__name__)
scan_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        url = request.form['url']
        scan_result = scan_url(url)

        # Construct explanation messages
        reasons = []
        if not scan_result['is_valid']:
            reasons.append("❌ Invalid URL format.")
        if scan_result['in_blacklist']:
            reasons.append("⚠️ Domain is blacklisted (known phishing site).")
        if scan_result['has_suspicious_patterns']:
            reasons.append("⚠️ Suspicious patterns found in URL (e.g., '@', 'login', 'verify').")
        if scan_result['domain_age_days'] is not None and scan_result['domain_age_days'] < 30:
            reasons.append(f"⚠️ Domain is very new ({scan_result['domain_age_days']} days old).")

        detailed_message = " ; ".join(reasons) if reasons else "✅ No signs of phishing detected."

        result = {
            'url': url,
            'is_phishing': scan_result['is_phishing'],
            'message': detailed_message,
            'details': scan_result
        }

        scan_history.append(result)

    return render_template("index.html", result=result, history=scan_history)


@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    is_phishing = request.form['is_phishing'] == 'True'
    message = request.form['message']
    format_type = request.form['format']

    if format_type == 'csv':
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(['URL', 'Status', 'Message'])
        writer.writerow([url, 'Phishing' if is_phishing else 'Safe', message])
        csv_file.seek(0)
        return send_file(BytesIO(csv_file.getvalue().encode()), download_name='report.csv', as_attachment=True)

    elif format_type == 'pdf':
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setFont("Helvetica", 14)
        c.drawString(100, 750, "PhishX – Phishing Scan Report")
        c.setFont("Helvetica", 12)
        c.drawString(100, 720, f"URL: {url}")
        c.drawString(100, 700, f"Status: {'Phishing' if is_phishing else 'Safe'}")
        c.drawString(100, 680, f"Message: {message}")
        c.save()
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, download_name='report.pdf', as_attachment=True)

    return "Invalid format requested", 400

if __name__ == '__main__':
    app.run(debug=True)
