"""
Email Automation Module
Generates and sends HTML email reports using Brevo SMTP
"""
import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import logging

# Add parent directory to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.config import EMAIL_CONFIG, TOP_CRYPTOS_COUNT
from utils.database import get_data_by_timerange, get_stats

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_html_report(hours=168):
    """
    Generate HTML content for the weekly report
    
    Args:
        hours: Number of hours to look back (default 168 = 1 week)
    """
    # Get data
    data = get_data_by_timerange(hours)
    stats = get_stats()
    
    # Calculate basic metrics
    total_posts = len(data)
    if total_posts > 0:
        avg_sentiment = sum(item['sentiment_score'] for item in data) / total_posts
        sentiment_status = "Bullish 🟢" if avg_sentiment > 0.05 else "Bearish 🔴" if avg_sentiment < -0.05 else "Neutral ⚪"
    else:
        avg_sentiment = 0
        sentiment_status = "No Data ⚪"
        
    # Get top cryptos mentioned
    crypto_counts = {}
    for item in data:
        if item['crypto_mentioned']:
            cryptos = item['crypto_mentioned'].split(',')
            for crypto in cryptos:
                crypto = crypto.strip()
                if crypto:
                    crypto_counts[crypto] = crypto_counts.get(crypto, 0) + 1
    
    top_cryptos = sorted(crypto_counts.items(), key=lambda x: x[1], reverse=True)[:TOP_CRYPTOS_COUNT]
    
    # Generate HTML
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #0e1117; color: #fff; padding: 20px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #f9f9f9; padding: 20px; border: 1px solid #ddd; }}
            .metric-box {{ background: #fff; padding: 15px; margin-bottom: 20px; border-radius: 5px; border-left: 5px solid #00ff88; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            .table th, .table td {{ padding: 10px; text-align: left; border-bottom: 1px solid #eee; }}
            .footer {{ text-align: center; font-size: 12px; color: #888; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>⚡ Crypto Sentiment Weekly</h1>
                <p>{datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            
            <div class="content">
                <div class="metric-box">
                    <h3>📊 Market Overview</h3>
                    <p><strong>Sentiment:</strong> {sentiment_status} ({avg_sentiment:.2f})</p>
                    <p><strong>Total Signals:</strong> {total_posts}</p>
                    <p><strong>Database Size:</strong> {stats.get('total', 0)} entries</p>
                </div>
                
                <h3>🔥 Top Trending Assets</h3>
                <table class="table">
                    <tr>
                        <th>Asset</th>
                        <th>Mentions</th>
                    </tr>
    """
    
    for crypto, count in top_cryptos:
        html += f"""
                    <tr>
                        <td><strong>{crypto}</strong></td>
                        <td>{count}</td>
                    </tr>
        """
        
    html += """
                </table>
                
                <div style="margin-top: 30px; padding: 15px; background: #e8f4fd; border-radius: 5px;">
                    <p><strong>💡 AI Insight:</strong> Check the dashboard for real-time analysis and news.</p>
                    <a href="http://localhost:8501" style="display: inline-block; background: #007bff; color: #fff; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">Open Dashboard</a>
                </div>
            </div>
            
            <div class="footer">
                <p>Sent by Crypto Sentiment Monitor Automation</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(subject, html_content):
    """
    Send email using SMTP configuration
    """
    try:
        # Check if config is set
        if 'YOUR_LOGIN_EMAIL_HERE' in EMAIL_CONFIG['sender_email']:
            logger.warning("⚠️ Email configuration not set. Please update utils/config.py")
            return False
            
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = ", ".join(EMAIL_CONFIG['recipients'])
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_content, 'html'))
        
        # Connect to SMTP server
        logger.info(f"Connecting to SMTP server: {EMAIL_CONFIG['smtp_server']}:{EMAIL_CONFIG['smtp_port']}")
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        
        # Login
        # Use smtp_username if available, otherwise fallback to sender_email
        smtp_username = EMAIL_CONFIG.get('smtp_username', EMAIL_CONFIG['sender_email'])
        server.login(smtp_username, EMAIL_CONFIG['sender_password'])
        
        # Send email
        server.send_message(msg)
        server.quit()
        
        logger.info(f"✅ Email sent successfully to {EMAIL_CONFIG['recipients']}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
        return False

def send_weekly_report():
    """
    Main function to generate and send the weekly report
    """
    try:
        logger.info("Generating weekly report...")
        html_content = generate_html_report(hours=168)
        
        # Create subject with current date
        subject = f"Weekly Crypto Sentiment Report - {datetime.now().strftime('%b %d, %Y')}"
        
        logger.info(f"Sending report: {subject}")
        success = send_email(subject, html_content)
        
        if success:
            logger.info("Weekly report sent successfully!")
        else:
            logger.error("Failed to send weekly report")
        
        return success
        
    except Exception as e:
        logger.error(f"❌ Error in send_weekly_report: {e}")
        return False

if __name__ == "__main__":
    # Test the module
    print("Testing email reporter...\n")
    
    print("--- Generating HTML Report ---")
    html = generate_html_report(168)
    print(f"Generated HTML report ({len(html)} characters)")
    
    # Save to file for preview
    with open('test_report.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved test report to test_report.html")
    
    print("\n--- Sending Test Email ---")
    print("Note: Make sure EMAIL_CONFIG is configured in utils/config.py")
    
    if 'YOUR_LOGIN_EMAIL_HERE' in EMAIL_CONFIG['sender_email']:
        print("⚠️ WARNING: Default credentials detected in config.py. Email sending will likely fail.")
    
    response = input("Do you want to send a test email? (y/n): ")
    if response.lower() == 'y':
        send_weekly_report()
    else:
        print("Skipped email sending test")