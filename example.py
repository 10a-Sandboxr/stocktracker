#!/usr/bin/env python3
"""
Example usage script for Stock Newsletter
Demonstrates the main features of the stock monitoring and analysis tool

IMPORTANT: You must accept the Terms of Service before using this tool!
Run: python ToS.py
"""

import sys
from stock_monitor import StockMonitor
from config import NASDAQ_API_KEY, validate_config
import json


def display_tos_requirement():
    """Display Terms of Service requirement"""
    print("\n" + "="*70)
    print("IMPORTANT: TERMS OF SERVICE AGREEMENT REQUIRED")
    print("="*70)
    print("\nBefore using this Stock Newsletter tool, you MUST read and agree")
    print("to the Terms of Service.")
    print("\nTo view the Terms of Service, run:")
    print("  python ToS.py")
    print("\nHave you read and agreed to the Terms of Service? (yes/no): ", end="")

    try:
        response = input().strip().lower()
        if response not in ['yes', 'y']:
            print("\nYou must accept the Terms of Service to use this tool.")
            print("Please run: python ToS.py")
            sys.exit(1)
    except (EOFError, KeyboardInterrupt):
        print("\n\nTerms of Service must be accepted to use this software.")
        sys.exit(1)

    print("\nThank you for accepting the Terms of Service.")
    print("Proceeding with example...\n")


def check_configuration():
    """Check if configuration is valid"""
    is_valid, message = validate_config()

    if not is_valid:
        print(f"\nConfiguration Error: {message}")
        print("\nPlease set your NASDAQ API key in one of these ways:")
        print("1. Set environment variable: export NASDAQ_API_KEY='your_key_here'")
        print("2. Edit config.py and set NASDAQ_API_KEY")
        print("3. Create a .env file with: NASDAQ_API_KEY=your_key_here")
        print("\nGet your API key from: https://data.nasdaq.com/")
        return False

    return True


def example_basic_usage():
    """Example: Basic stock monitoring"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Stock Monitoring")
    print("="*70)

    # Initialize the monitor
    monitor = StockMonitor(api_key=NASDAQ_API_KEY)

    # Add stocks to watchlist
    print("\nAdding stocks to watchlist...")
    monitor.add_stocks(['AAPL', 'GOOGL', 'MSFT'])

    # Display watchlist
    print(f"\nCurrent watchlist: {monitor.get_watchlist()}")

    # Get current prices
    print("\nFetching current prices...")
    prices = monitor.get_current_prices()

    for symbol, price in prices.items():
        if price:
            print(f"  {symbol}: ${price:.2f}")
        else:
            print(f"  {symbol}: Price unavailable")


def example_stock_analysis():
    """Example: In-depth stock analysis"""
    print("\n" + "="*70)
    print("EXAMPLE 2: In-Depth Stock Analysis")
    print("="*70)

    monitor = StockMonitor(api_key=NASDAQ_API_KEY)

    # Analyze a specific stock
    symbol = 'AAPL'
    print(f"\nAnalyzing {symbol}...")
    print("(This may take a few moments...)\n")

    analysis = monitor.analyze_stock(symbol, days=60)

    if analysis and 'error' not in analysis:
        # Display summary
        print(analysis.get('summary', 'No summary available'))
        print()

        # Display key metrics
        print("Key Technical Indicators:")
        print("-" * 70)

        technical = analysis.get('technical', {})
        if technical:
            print(f"  Current Price:    ${technical.get('current_price', 'N/A'):.2f}")
            print(f"  RSI (14):         {technical.get('rsi', 'N/A'):.2f} - {technical.get('rsi_signal', 'N/A')}")
            print(f"  MACD:             {technical.get('macd', 'N/A'):.4f}")
            print(f"  50-day SMA:       ${technical.get('sma_50', 'N/A'):.2f}")
            print(f"  200-day SMA:      ${technical.get('sma_200', 'N/A'):.2f}")

        # Display trend information
        print("\nTrend Analysis:")
        print("-" * 70)

        trend = analysis.get('trend', {})
        if trend:
            print(f"  Overall Trend:    {trend.get('overall_trend', 'N/A').replace('_', ' ').title()}")
            print(f"  1-Day Change:     {trend.get('price_change_1d', 'N/A'):.2f}%")
            print(f"  5-Day Change:     {trend.get('price_change_5d', 'N/A'):.2f}%")
            print(f"  30-Day Change:    {trend.get('price_change_30d', 'N/A'):.2f}%")

        # Display recommendation
        print("\nRecommendation:")
        print("-" * 70)

        recommendation = analysis.get('recommendation', {})
        if recommendation:
            print(f"  Signal:           {recommendation.get('recommendation', 'N/A')}")
            print(f"  Confidence:       {recommendation.get('confidence', 0):.0f}%")
            print(f"  Key Signals:")
            for signal in recommendation.get('signals', []):
                print(f"    - {signal}")

        # Display volatility
        print("\nVolatility Analysis:")
        print("-" * 70)

        volatility = analysis.get('volatility', {})
        if volatility:
            print(f"  Volatility:       {volatility.get('volatility_percent', 'N/A'):.2f}%")
            print(f"  Rating:           {volatility.get('volatility_rating', 'N/A').replace('_', ' ').title()}")

    else:
        print(f"Could not analyze {symbol}. Error: {analysis.get('error', 'Unknown error')}")


def example_multiple_stocks():
    """Example: Analyzing multiple stocks"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Analyzing Multiple Stocks")
    print("="*70)

    monitor = StockMonitor(api_key=NASDAQ_API_KEY)

    # Add multiple stocks
    stocks = ['AAPL', 'GOOGL', 'MSFT']
    monitor.add_stocks(stocks)

    print(f"\nAnalyzing {len(stocks)} stocks...")
    print("(This may take a minute...)\n")

    # Analyze all stocks in watchlist
    analyses = monitor.analyze_watchlist()

    # Display summary for each stock
    print("Analysis Summary:")
    print("="*70)

    for symbol, analysis in analyses.items():
        if analysis and 'error' not in analysis:
            recommendation = analysis.get('recommendation', {})
            technical = analysis.get('technical', {})
            trend = analysis.get('trend', {})

            print(f"\n{symbol}:")
            print(f"  Price:            ${technical.get('current_price', 'N/A'):.2f}")
            print(f"  Recommendation:   {recommendation.get('recommendation', 'N/A')}")
            print(f"  Trend:            {trend.get('overall_trend', 'N/A').replace('_', ' ').title()}")
            print(f"  RSI:              {technical.get('rsi', 'N/A'):.2f}")
        else:
            print(f"\n{symbol}: Analysis failed")


def example_price_alerts():
    """Example: Setting up price alerts"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Price Alerts")
    print("="*70)

    monitor = StockMonitor(api_key=NASDAQ_API_KEY)

    symbol = 'AAPL'
    monitor.add_stocks(symbol)

    # Get current price
    current_price = monitor.get_current_price(symbol)

    if current_price:
        print(f"\nCurrent price of {symbol}: ${current_price:.2f}")

        # Set alert thresholds
        target_high = current_price * 1.05  # 5% above current
        target_low = current_price * 0.95   # 5% below current

        print(f"\nExample alert thresholds:")
        print(f"  Alert if above: ${target_high:.2f}")
        print(f"  Alert if below: ${target_low:.2f}")

        # Check alerts (in real usage, this would be in a monitoring loop)
        alert_high = monitor.get_price_alert(symbol, target_high, 'above')
        alert_low = monitor.get_price_alert(symbol, target_low, 'below')

        if alert_high:
            print(f"\n  {alert_high}")
        if alert_low:
            print(f"\n  {alert_low}")

        if not alert_high and not alert_low:
            print("\n  No alerts triggered at current price")

    else:
        print(f"\nCould not fetch price for {symbol}")


def example_continuous_monitoring():
    """Example: Continuous monitoring (commented out by default)"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Continuous Monitoring (NOT RUNNING)")
    print("="*70)

    print("\nContinuous monitoring example (commented out by default):")
    print("This would continuously monitor your watchlist and check for alerts.")
    print("\nTo enable, uncomment the code in example.py")

    print("\nExample usage:")
    print("""
    monitor = StockMonitor(api_key=NASDAQ_API_KEY)
    monitor.add_stocks(['AAPL', 'GOOGL', 'MSFT'])

    # Set up alerts
    alerts = {
        'AAPL': {'target': 150.00, 'type': 'above'},
        'GOOGL': {'target': 100.00, 'type': 'below'},
    }

    # Start monitoring (runs until Ctrl+C)
    monitor.monitor_continuous(interval=300, alerts=alerts)
    """)

    # Uncomment to actually run continuous monitoring:
    # monitor = StockMonitor(api_key=NASDAQ_API_KEY)
    # monitor.add_stocks(['AAPL', 'GOOGL', 'MSFT'])
    # monitor.monitor_continuous(interval=300)


def example_export_analysis():
    """Example: Export analysis results"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Export Analysis Results")
    print("="*70)

    monitor = StockMonitor(api_key=NASDAQ_API_KEY)

    symbol = 'AAPL'
    print(f"\nAnalyzing {symbol} for export...")

    analysis = monitor.analyze_stock(symbol)

    if analysis and 'error' not in analysis:
        # Export to JSON
        filename = f"{symbol}_analysis.json"
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2)

        print(f"\nAnalysis exported to: {filename}")
        print(f"File size: {len(json.dumps(analysis, indent=2))} bytes")
        print("\nYou can now:")
        print(f"  - View the JSON file: cat {filename}")
        print(f"  - Process it with other tools")
        print(f"  - Import it into spreadsheet software")

    else:
        print(f"\nCould not analyze {symbol}")


def main():
    """Main function to run examples"""
    print("\n" + "="*70)
    print("STOCK NEWSLETTER - Example Usage")
    print("="*70)

    # Check Terms of Service acceptance
    display_tos_requirement()

    # Validate configuration
    if not check_configuration():
        sys.exit(1)

    print("\nThis script demonstrates the main features of Stock Newsletter.")
    print("Each example will run in sequence.\n")

    input("Press Enter to continue...")

    try:
        # Run examples
        example_basic_usage()
        input("\nPress Enter for next example...")

        example_stock_analysis()
        input("\nPress Enter for next example...")

        example_multiple_stocks()
        input("\nPress Enter for next example...")

        example_price_alerts()
        input("\nPress Enter for next example...")

        example_continuous_monitoring()
        input("\nPress Enter for next example...")

        example_export_analysis()

        print("\n" + "="*70)
        print("Examples completed!")
        print("="*70)
        print("\nNext steps:")
        print("  1. Review the code in example.py to understand the API")
        print("  2. Check out stock_monitor.py and stock_analysis.py for details")
        print("  3. Customize config.py for your needs")
        print("  4. Build your own monitoring scripts")
        print("\nRemember: This is for informational purposes only - not financial advice!")
        print("="*70 + "\n")

    except KeyboardInterrupt:
        print("\n\nExamples interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
