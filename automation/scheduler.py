"""
Scheduler Module
Automates sentiment analysis and email reporting
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from analysis.sentiment_analyzer import process_unanalyzed_data
from automation.email_reporter import send_weekly_report
from datetime import datetime
import time
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def job_process_sentiment():
    """Wrapper for sentiment processing with logging"""
    try:
        logger.info("=" * 50)
        logger.info("Starting sentiment analysis job...")
        count = process_unanalyzed_data()
        logger.info(f"✅ Sentiment analysis completed. Processed {count} entries.")
    except Exception as e:
        logger.error(f"❌ Error in sentiment analysis job: {e}")


def job_send_weekly_report():
    """Wrapper for weekly report with logging"""
    try:
        logger.info("=" * 50)
        logger.info("Starting weekly report job...")
        success = send_weekly_report()
        if success:
            logger.info("✅ Weekly report sent successfully!")
        else:
            logger.error("❌ Failed to send weekly report")
    except Exception as e:
        logger.error(f"❌ Error in weekly report job: {e}")


def start_scheduler():
    """
    Start background scheduler with jobs
    
    Scheduled Jobs:
        1. process_unanalyzed_data() - Every 30 minutes
        2. send_weekly_report() - Every Monday at 9:00 AM
    """
    
    logger.info("=" * 70)
    logger.info("🚀 Starting Crypto Sentiment Monitor Scheduler")
    logger.info("=" * 70)
    
    # Create scheduler
    scheduler = BackgroundScheduler()
    
    # Add sentiment analysis job - every 30 minutes
    scheduler.add_job(
        job_process_sentiment,
        trigger=IntervalTrigger(minutes=30),
        id='sentiment_analysis',
        name='Sentiment Analysis (Every 30 minutes)',
        replace_existing=True
    )
    logger.info("📊 Scheduled: Sentiment Analysis - Every 30 minutes")
    
    # Add weekly report job - Every Monday at 9:00 AM
    scheduler.add_job(
        job_send_weekly_report,
        trigger=CronTrigger(day_of_week='mon', hour=9, minute=0),
        id='weekly_report',
        name='Weekly Report (Mondays at 9:00 AM)',
        replace_existing=True
    )
    logger.info("📧 Scheduled: Weekly Report - Every Monday at 9:00 AM")
    
    # Start the scheduler
    scheduler.start()
    logger.info("✅ Scheduler started successfully!")
    logger.info("=" * 70)
    
    # Print next run times
    logger.info("\n📅 Next scheduled runs:")
    for job in scheduler.get_jobs():
        next_run = job.next_run_time
        if next_run:
            logger.info(f"  • {job.name}: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    logger.info("\n⌨️  Press Ctrl+C to stop the scheduler\n")
    logger.info("=" * 70)
    
    # Run initial sentiment analysis
    logger.info("\n🔄 Running initial sentiment analysis...")
    job_process_sentiment()
    
    # Keep the scheduler alive
    try:
        while True:
            time.sleep(60)
            # Log heartbeat every hour
            if datetime.now().minute == 0:
                logger.info(f"💓 Scheduler heartbeat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n" + "=" * 70)
        logger.info("⏹️  Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("✅ Scheduler stopped successfully!")
        logger.info("=" * 70)


if __name__ == "__main__":
    start_scheduler()