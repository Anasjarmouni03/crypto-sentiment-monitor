"""
Email Automation Module
Generates and sends HTML email reports
"""
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from utils.config import EMAIL_SENDER, EMAIL_PASSWORD, EMAIL_RECIPIENTS
from utils.database import get_data_by_timerange
from analysis.trend_detector import get_trending_cryptos, get_sentiment_by_source
import base64
from io import BytesIO


def generate_html_report(hours: int = 168) -> str:
    """
    Generate HTML email report
    
    Args:
        hours (int): Report period (default 168 = 1 week)
    
    Returns:
        str: HTML content for email
    """
    try:
        # Get data
        data = get_data_by_timerange(hours)
        trending = get_trending_cryptos(hours)
        by_source = get_sentiment_by_source(hours)
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(hours=hours)
        date_range = f"{start_date.strftime('%b %d, %Y')} - {end_date.strftime('%b %d, %Y')}"
        
        # Calculate overall stats
        if data:
            analyzed_data = [row for row in data if row.get('sentiment_score') is not None]
            if analyzed_data:
                avg_sentiment = sum(row['sentiment_score'] for row in analyzed_data) / len(analyzed_data)
                total_posts = len(analyzed_data)
                positive_count = sum(1 for row in analyzed_data if row.get('sentiment_label') == 'positive')
                negative_count = sum(1 for row in analyzed_data if row.get('sentiment_label') == 'negative')
                neutral_count = sum(1 for row in analyzed_data if row.get('sentiment_label') == 'neutral')
            else:
                avg_sentiment = 0.0
                total_posts = 0
                positive_count = negative_count = neutral_count = 0
        else:
            avg_sentiment = 0.0
            total_posts = 0
            positive_count = negative_count = neutral_count = 0
        
        # Determine sentiment status
        if avg_sentiment > 0.2:
            sentiment_status = "🟢 Very Positive"
            sentiment_color = "#00cc00"
        elif avg_sentiment > 0.05:
            sentiment_status = "🟢 Positive"
            sentiment_color = "#66cc00"
        elif avg_sentiment > -0.05:
            sentiment_status = "⚪ Neutral"
            sentiment_color = "#999999"
        elif avg_sentiment > -0.2:
            sentiment_status = "🔴 Negative"
            sentiment_color = "#cc6600"
        else:
            sentiment_status = "🔴 Very Negative"
            sentiment_color = "#cc0000"
        
        # Find biggest sentiment changes
        biggest_gainer = None
        biggest_loser = None
        if trending and len(trending) > 0:
            sorted_by_sentiment = sorted(trending, key=lambda x: x['avg_sentiment'], reverse=True)
            if sorted_by_sentiment[0]['avg_sentiment'] > 0:
                biggest_gainer = sorted_by_sentiment[0]
            if sorted_by_sentiment[-1]['avg_sentiment'] < 0:
                biggest_loser = sorted_by_sentiment[-1]
        
        # Build HTML
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background-color: white;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 28px;
        }}
        .date-range {{
            color: #7f8c8d;
            font-size: 14px;
            margin-top: 10px;
        }}
        .summary-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 8px;
            margin: 20px 0;
            text-align: center;
        }}
        .summary-stat {{
            display: inline-block;
            margin: 0 20px;
        }}
        .summary-stat h3 {{
            margin: 0;
            font-size: 32px;
        }}
        .summary-stat p {{
            margin: 5px 0 0 0;
            font-size: 14px;
            opacity: 0.9;
        }}
        .section {{
            margin: 30px 0;
        }}
        .section h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
            margin-bottom: 15px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }}
        th {{
            background-color: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}
        td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}
        tr:hover {{
            background-color: #f8f9fa;
        }}
        .positive {{ color: #27ae60; font-weight: bold; }}
        .negative {{ color: #e74c3c; font-weight: bold; }}
        .neutral {{ color: #95a5a6; font-weight: bold; }}
        .insight-box {{
            background-color: #e8f5e9;
            border-left: 4px solid #4CAF50;
            padding: 15px;
            margin: 15px 0;
            border-radius: 4px;
        }}
        .insight-box h3 {{
            margin-top: 0;
            color: #2e7d32;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ecf0f1;
            color: #7f8c8d;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Crypto Sentiment Report</h1>
            <p class="date-range">{date_range}</p>
        </div>
        
        <div class="summary-box">
            <div class="summary-stat">
                <h3 style="color: {sentiment_color};">{avg_sentiment:.2f}</h3>
                <p>Overall Sentiment</p>
                <p>{sentiment_status}</p>
            </div>
            <div class="summary-stat">
                <h3>{total_posts:,}</h3>
                <p>Posts Analyzed</p>
            </div>
            <div class="summary-stat">
                <h3 class="positive">{positive_count}</h3>
                <p>Positive Posts</p>
            </div>
        </div>
        
        <div class="section">
            <h2>🔥 Top 5 Trending Cryptocurrencies</h2>
            <table>
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Crypto</th>
                        <th>Mentions</th>
                        <th>Avg Sentiment</th>
                        <th>Distribution</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add trending cryptos
        if trending:
            for i, crypto in enumerate(trending[:5], 1):
                sentiment_class = 'positive' if crypto['avg_sentiment'] > 0 else 'negative' if crypto['avg_sentiment'] < 0 else 'neutral'
                html += f"""
                    <tr>
                        <td>{i}</td>
                        <td><strong>{crypto['crypto']}</strong></td>
                        <td>{crypto['mentions']}</td>
                        <td class="{sentiment_class}">{crypto['avg_sentiment']:.2f}</td>
                        <td>✅{crypto['positive_count']} | ❌{crypto['negative_count']} | ⚪{crypto['neutral_count']}</td>
                    </tr>
"""
        else:
            html += """
                    <tr>
                        <td colspan="5" style="text-align: center; color: #999;">No trending cryptocurrencies found</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>📱 Sentiment by Source</h2>
            <table>
                <thead>
                    <tr>
                        <th>Source</th>
                        <th>Average Sentiment</th>
                    </tr>
                </thead>
                <tbody>
"""
        
        # Add source sentiments
        for source, sentiment in by_source.items():
            sentiment_class = 'positive' if sentiment > 0 else 'negative' if sentiment < 0 else 'neutral'
            html += f"""
                    <tr>
                        <td><strong>{source.capitalize()}</strong></td>
                        <td class="{sentiment_class}">{sentiment:.2f}</td>
                    </tr>
"""
        
        html += """
                </tbody>
            </table>
        </div>
        
        <div class="section">
            <h2>💡 Key Insights</h2>
"""
        
        if biggest_gainer:
            html += f"""
            <div class="insight-box">
                <h3>🚀 Biggest Sentiment Winner</h3>
                <p><strong>{biggest_gainer['crypto']}</strong> showed the most positive sentiment with an average of <span class="positive">{biggest_gainer['avg_sentiment']:.2f}</span> across {biggest_gainer['mentions']} mentions.</p>
            </div>
"""
        
        if biggest_loser:
            html += f"""
            <div class="insight-box" style="background-color: #ffebee; border-left-color: #e74c3c;">
                <h3 style="color: #c62828;">📉 Biggest Sentiment Concern</h3>
                <p><strong>{biggest_loser['crypto']}</strong> showed the most negative sentiment with an average of <span class="negative">{biggest_loser['avg_sentiment']:.2f}</span> across {biggest_loser['mentions']} mentions.</p>
            </div>
"""
        
        html += f"""
            <div class="insight-box" style="background-color: #e3f2fd; border-left-color: #2196F3;">
                <h3 style="color: #1565c0;">📊 Sentiment Distribution</h3>
                <p>During this period: <span class="positive">{positive_count} positive</span>, <span class="negative">{negative_count} negative</span>, and <span class="neutral">{neutral_count} neutral</span> posts were analyzed.</p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>Crypto Sentiment Monitor</strong></p>
            <p>Automated sentiment analysis powered by VADER NLP</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
        
    except Exception as e:
        print(f"Error generating HTML report: {e}")
        return f"<html><body><h1>Error generating report</h1><p>{str(e)}</p></body></html>"


def send_email(subject: str, html_content: str) -> bool:
    """
    Send email report using Gmail SMTP
    
    Args:
        subject (str): Email subject
        html_content (str): HTML body from generate_html_report()
    
    Returns:
        bool: True if sent successfully
    """
    try:
        # Validate configuration
        if not EMAIL_SENDER or not EMAIL_PASSWORD or not EMAIL_RECIPIENTS:
            print("Error: Email configuration not set in config.py")
            return False
        
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = EMAIL_SENDER
        msg['To'] = ', '.join(EMAIL_RECIPIENTS)
        
        # Attach HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to Gmail SMTP server
        print(f"Connecting to Gmail SMTP server...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        
        # Login
        print(f"Logging in as {EMAIL_SENDER}...")
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # Send email
        print(f"Sending email to {', '.join(EMAIL_RECIPIENTS)}...")
        server.send_message(msg)
        server.quit()
        
        print("✅ Email sent successfully!")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Make sure you're using a Gmail App Password, not your regular password.")
        print("To create an App Password:")
        print("1. Enable 2FA on your Gmail account")
        print("2. Go to https://myaccount.google.com/apppasswords")
        print("3. Generate a new app password")
        print("4. Use that password in EMAIL_PASSWORD in config.py")
        return False
    except Exception as e:
        print(f"❌ Error sending email: {e}")
        return False


def send_weekly_report():
    """
    Convenience function to generate and send weekly report
    """
    try:
        print("Generating weekly report...")
        html_content = generate_html_report(hours=168)
        
        # Create subject with current date
        subject = f"Weekly Crypto Sentiment Report - {datetime.now().strftime('%b %d, %Y')}"
        
        print(f"Sending report: {subject}")
        success = send_email(subject, html_content)
        
        if success:
            print("✅ Weekly report sent successfully!")
        else:
            print("❌ Failed to send weekly report")
        
        return success
        
    except Exception as e:
        print(f"❌ Error in send_weekly_report: {e}")
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
    print("Note: Make sure EMAIL_SENDER, EMAIL_PASSWORD, and EMAIL_RECIPIENTS are configured in config.py")
    
    response = input("Do you want to send a test email? (y/n): ")
    if response.lower() == 'y':
        send_weekly_report()
    else:
        print("Skipped email sending test")