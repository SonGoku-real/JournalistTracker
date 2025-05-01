#!/usr/bin/env python
"""
Script to fetch and update the crypto news feed.
Can be run manually or scheduled via cron.

Usage:
    python refresh_news.py [--days=1] [--analyze=true]
"""

import sys
import argparse
import logging
from utils.news_fetcher import update_news_feed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Refresh crypto news feed.')
    parser.add_argument('--days', type=int, default=1, help='Number of days to look back')
    parser.add_argument('--analyze', type=str, default='true', 
                      help='Whether to analyze content with OpenAI (true/false)')
    
    args = parser.parse_args()
    
    # Convert analyze argument to boolean
    analyze = args.analyze.lower() != 'false'
    
    logger.info(f"Starting news refresh (days={args.days}, analyze={analyze})")
    
    # Run the update
    try:
        count = update_news_feed(days=args.days, analyze=analyze)
        logger.info(f"Refresh complete. Added {count} new articles.")
        return 0
    except Exception as e:
        logger.error(f"Error during refresh: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())