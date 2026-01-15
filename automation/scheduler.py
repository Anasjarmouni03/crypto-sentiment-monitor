from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scrapers.universal_scraper import scrape_all
from analysis.sentiment_analyzer import process_unanalyzed_data
from automation.email_reporter import send_weekly_report
from utils.database import insert_scraped_data
from datetime import datetime
import time
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def job_scrape_data():
    """Wrapper for data scraping job"""
    try:
        logger.info("=" * 50)
        logger.info("Starting data collection job...")
        
        # Scrape data
        all_data = scrape_all(limit_per_source=20)
        
        # Insert into database
        total_inserted = 0
        for source, items in all_data.items():
            for item in items:
                try:
                    success = insert_scraped_data(
                        source=source,
                        content=item['content'],
                        timestamp=item['timestamp'],
                        url=item['url'],
                        engagement=item['engagement']
                    )
                    if success:
                        total_inserted += 1
                except Exception as e:
                    logger.error(f"Error inserting item: {e}")
                    
        logger.info(f"Data collection completed. Collected {total_inserted} new items.")
        
    except Exception as e:
        logger.error(f"Error in data collection job: {e}")


def job_process_sentiment():
    """Wrapper for sentiment processing with logging"""
    try:
        logger.info("=" * 50)
        logger.info("Starting sentiment analysis job...")
        count = process_unanalyzed_data()
        logger.info(f"Sentiment analysis completed. Processed {count} entries.")
    except Exception as e:
        logger.error(f"Error in sentiment analysis job: {e}")


def job_send_weekly_report():
    """Wrapper for weekly report with logging"""
    try:
        logger.info("=" * 50)
        logger.info("Starting weekly report job...")
        success = send_weekly_report()
        if success:
            logger.info("Weekly report sent successfully!")
        else:
            logger.error("Failed to send weekly report")
    except Exception as e:
        logger.error(f"Error in weekly report job: {e}")


def start_scheduler():
    """
    Start background scheduler with jobs
    
    Scheduled Jobs:
        1. scrape_data() - Every 15 minutes
        2. process_unanalyzed_data() - Every 15 minutes (offset by 2 mins)
        3. send_weekly_report() - Every Monday at 9:00 AM
    """
    
    logger.info("=" * 70)
    logger.info("Starting Crypto Sentiment Monitor Scheduler")
    logger.info("=" * 70)
    
    # Create scheduler
    scheduler = BackgroundScheduler()
    
    # 1. Add scraping job - every 15 minutes
    scheduler.add_job(
        job_scrape_data,
        trigger=IntervalTrigger(minutes=15),
        id='data_collection',
        name='Data Collection (Every 15 minutes)',
        replace_existing=True
    )
    logger.info("Scheduled: Data Collection - Every 15 minutes")
    
    # 2. Add sentiment analysis job - every 15 minutes (delayed by 2 mins to let scraping finish)
    # We use a slightly offset interval or just run it frequently
    scheduler.add_job(
        job_process_sentiment,
        trigger=IntervalTrigger(minutes=15, start_date=datetime.now().replace(second=0, microsecond=0) + __import__('datetime').timedelta(minutes=2)),
        id='sentiment_analysis',
        name='Sentiment Analysis (Every 15 minutes)',
        replace_existing=True
    )
    logger.info("Scheduled: Sentiment Analysis - Every 15 minutes")
    
    # 3. Add weekly report job - Every Monday at 9:00 AM
    scheduler.add_job(
        job_send_weekly_report,
        trigger=CronTrigger(day_of_week='mon', hour=9, minute=0),
        id='weekly_report',
        name='Weekly Report (Mondays at 9:00 AM)',
        replace_existing=True
    )
    logger.info("Scheduled: Weekly Report - Every Monday at 9:00 AM")
    
    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started successfully!")
    logger.info("=" * 70)
    
    # Print next run times
    logger.info("\nNext scheduled runs:")
    for job in scheduler.get_jobs():
        next_run = job.next_run_time
        if next_run:
            logger.info(f"  • {job.name}: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    logger.info("\nPress Ctrl+C to stop the scheduler\n")
    logger.info("=" * 70)
    
    # Run initial cycle immediately
    logger.info("\nRunning initial data collection cycle...")
    job_scrape_data()
    logger.info("\nRunning initial analysis cycle...")
    job_process_sentiment()
    
    # Keep the scheduler alive
    try:
        while True:
            time.sleep(60)
            # Log heartbeat every hour
            if datetime.now().minute == 0:
                logger.info(f"Scheduler heartbeat - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
    except (KeyboardInterrupt, SystemExit):
        logger.info("\n" + "=" * 70)
        logger.info("Shutting down scheduler...")
        scheduler.shutdown()
        logger.info("Scheduler stopped successfully!")
        logger.info("=" * 70)


if __name__ == "__main__":
    start_scheduler()