"""
Automation package for crypto sentiment monitoring
Contains email reporting and scheduling functionality
"""

from .email_reporter import generate_html_report, send_email, send_weekly_report
from .scheduler import start_scheduler

__all__ = [
    'generate_html_report',
    'send_email',
    'send_weekly_report',
    'start_scheduler'
]