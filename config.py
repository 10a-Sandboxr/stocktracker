"""
Configuration file for Stock Newsletter
Copy this to a separate file or set environment variables with your actual credentials
"""

import os

# ============================================================
# API CONFIGURATION
# ============================================================

# NASDAQ API Key
# Get your API key from: https://data.nasdaq.com/
NASDAQ_API_KEY = os.environ.get('NASDAQ_API_KEY', 'YOUR_API_KEY_HERE')

# API Settings
API_TIMEOUT = 30  # seconds
API_RETRY_ATTEMPTS = 3
API_RETRY_DELAY = 2  # seconds

# ============================================================
# CACHE CONFIGURATION
# ============================================================

# Cache duration in seconds
CACHE_DURATION = 300  # 5 minutes
ENABLE_CACHE = True

# ============================================================
# MONITORING CONFIGURATION
# ============================================================

# Default update interval for continuous monitoring (seconds)
DEFAULT_UPDATE_INTERVAL = 300  # 5 minutes

# Default stocks to monitor (can be overridden)
DEFAULT_WATCHLIST = [
    'AAPL',  # Apple
    'GOOGL', # Google
    'MSFT',  # Microsoft
    'AMZN',  # Amazon
]

# ============================================================
# ANALYSIS CONFIGURATION
# ============================================================

# Number of days of historical data for analysis
DEFAULT_ANALYSIS_DAYS = 90

# Technical indicator periods
TECHNICAL_INDICATORS = {
    'sma_periods': [10, 20, 50, 200],
    'ema_periods': [12, 26],
    'rsi_period': 14,
    'macd_fast': 12,
    'macd_slow': 26,
    'macd_signal': 9,
    'bollinger_period': 20,
    'bollinger_std': 2,
    'atr_period': 14,
    'stochastic_period': 14,
}

# ============================================================
# ALERT CONFIGURATION
# ============================================================

# Price movement thresholds for alerts (percentage)
ALERT_THRESHOLDS = {
    'significant_move': 5.0,  # Alert if price moves 5% in a day
    'major_move': 10.0,       # Alert if price moves 10% in a day
}

# Volume alert threshold (multiplier of average volume)
VOLUME_ALERT_THRESHOLD = 2.0  # Alert if volume is 2x average

# ============================================================
# OUTPUT CONFIGURATION
# ============================================================

# Enable colored output in terminal (if supported)
ENABLE_COLORED_OUTPUT = True

# Decimal places for price display
PRICE_DECIMAL_PLACES = 2

# Date format for display
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# ============================================================
# LOGGING CONFIGURATION
# ============================================================

# Enable logging
ENABLE_LOGGING = True

# Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# Log file path (None to disable file logging)
LOG_FILE = 'stock_newsletter.log'

# ============================================================
# RATE LIMITING
# ============================================================

# Delay between API calls (seconds) to avoid rate limiting
API_CALL_DELAY = 0.5

# Maximum concurrent API requests
MAX_CONCURRENT_REQUESTS = 5

# ============================================================
# DATA EXPORT CONFIGURATION
# ============================================================

# Default export format: 'json', 'csv', 'xlsx'
DEFAULT_EXPORT_FORMAT = 'json'

# Export directory
EXPORT_DIRECTORY = './exports'

# Include technical analysis in exports
INCLUDE_ANALYSIS_IN_EXPORT = True

# ============================================================
# ADVANCED SETTINGS
# ============================================================

# Enable experimental features
ENABLE_EXPERIMENTAL_FEATURES = False

# Use alternative data sources as fallback
USE_FALLBACK_DATA_SOURCES = True

# Maximum age of data before forcing refresh (seconds)
MAX_DATA_AGE = 3600  # 1 hour

# ============================================================
# VALIDATION
# ============================================================

def validate_config():
    """
    Validate configuration settings

    Returns:
        Tuple of (is_valid, error_message)
    """
    if NASDAQ_API_KEY == 'YOUR_API_KEY_HERE' or not NASDAQ_API_KEY:
        return False, "NASDAQ_API_KEY not set. Please configure your API key."

    if DEFAULT_UPDATE_INTERVAL < 60:
        return False, "UPDATE_INTERVAL too short. Minimum is 60 seconds to avoid rate limiting."

    if CACHE_DURATION < 0:
        return False, "CACHE_DURATION must be positive."

    return True, "Configuration valid"


def print_config():
    """Print current configuration (excluding sensitive data)"""
    print("\n" + "="*60)
    print("STOCK NEWSLETTER CONFIGURATION")
    print("="*60)
    print(f"API Key Set: {'Yes' if NASDAQ_API_KEY and NASDAQ_API_KEY != 'YOUR_API_KEY_HERE' else 'No'}")
    print(f"Cache Enabled: {ENABLE_CACHE}")
    print(f"Cache Duration: {CACHE_DURATION}s")
    print(f"Default Update Interval: {DEFAULT_UPDATE_INTERVAL}s")
    print(f"Default Watchlist: {', '.join(DEFAULT_WATCHLIST)}")
    print(f"Analysis Period: {DEFAULT_ANALYSIS_DAYS} days")
    print(f"Logging Enabled: {ENABLE_LOGGING}")
    print(f"Log Level: {LOG_LEVEL}")
    print("="*60 + "\n")


# ============================================================
# ENVIRONMENT-SPECIFIC OVERRIDES
# ============================================================

# Development mode
if os.environ.get('ENV') == 'development':
    ENABLE_LOGGING = True
    LOG_LEVEL = 'DEBUG'
    CACHE_DURATION = 60  # Shorter cache in development

# Production mode
elif os.environ.get('ENV') == 'production':
    ENABLE_LOGGING = True
    LOG_LEVEL = 'WARNING'
    ENABLE_EXPERIMENTAL_FEATURES = False


if __name__ == "__main__":
    # Test configuration
    is_valid, message = validate_config()
    print_config()
    print(f"\nValidation: {message}")

    if not is_valid:
        print("\nWARNING: Configuration has errors that need to be fixed!")
        exit(1)
