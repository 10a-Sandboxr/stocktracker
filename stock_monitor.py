"""
Stock Monitor - Main monitoring and data retrieval module
Uses NASDAQ API to fetch stock data and provide monitoring capabilities
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Union
import time
from stock_analysis import StockAnalyzer


class StockMonitor:
    """
    Main class for monitoring stocks using NASDAQ API
    """

    def __init__(self, api_key: str, config: Optional[Dict] = None):
        """
        Initialize the Stock Monitor

        Args:
            api_key: NASDAQ API key
            config: Optional configuration dictionary
        """
        self.api_key = api_key
        self.base_url = "https://data.nasdaq.com/api/v3"
        self.watchlist = []
        self.config = config or {}
        self.analyzer = StockAnalyzer()
        self.cache = {}
        self.cache_duration = self.config.get('cache_duration', 300)  # 5 minutes default

    def add_stocks(self, symbols: Union[str, List[str]]) -> None:
        """
        Add stock symbols to the watchlist

        Args:
            symbols: Single symbol string or list of symbols
        """
        if isinstance(symbols, str):
            symbols = [symbols]

        for symbol in symbols:
            symbol = symbol.upper().strip()
            if symbol not in self.watchlist:
                self.watchlist.append(symbol)
                print(f"Added {symbol} to watchlist")

    def remove_stock(self, symbol: str) -> None:
        """
        Remove a stock symbol from the watchlist

        Args:
            symbol: Stock symbol to remove
        """
        symbol = symbol.upper().strip()
        if symbol in self.watchlist:
            self.watchlist.remove(symbol)
            print(f"Removed {symbol} from watchlist")
        else:
            print(f"{symbol} not found in watchlist")

    def get_watchlist(self) -> List[str]:
        """
        Get the current watchlist

        Returns:
            List of stock symbols in watchlist
        """
        return self.watchlist.copy()

    def _make_api_call(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make an API call to NASDAQ

        Args:
            endpoint: API endpoint
            params: Optional query parameters

        Returns:
            JSON response as dictionary
        """
        if params is None:
            params = {}

        params['api_key'] = self.api_key

        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return {"error": str(e)}

    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """
        Get data from cache if available and not expired

        Args:
            key: Cache key

        Returns:
            Cached data or None if expired/not found
        """
        if key in self.cache:
            data, timestamp = self.cache[key]
            if time.time() - timestamp < self.cache_duration:
                return data
        return None

    def _save_to_cache(self, key: str, data: Dict) -> None:
        """
        Save data to cache with timestamp

        Args:
            key: Cache key
            data: Data to cache
        """
        self.cache[key] = (data, time.time())

    def get_current_price(self, symbol: str) -> Optional[float]:
        """
        Get the current price for a stock symbol

        Args:
            symbol: Stock symbol

        Returns:
            Current price or None if unavailable
        """
        cache_key = f"price_{symbol}"
        cached_data = self._get_from_cache(cache_key)

        if cached_data:
            return cached_data.get('price')

        # Using WIKI/PRICES dataset as example - adjust based on your NASDAQ API access
        endpoint = f"datasets/WIKI/{symbol}"
        params = {'rows': 1}

        result = self._make_api_call(endpoint, params)

        if 'error' not in result and 'dataset' in result:
            try:
                latest_data = result['dataset']['data'][0]
                price = latest_data[4]  # Close price

                price_data = {'price': price, 'timestamp': datetime.now().isoformat()}
                self._save_to_cache(cache_key, price_data)

                return price
            except (IndexError, KeyError) as e:
                print(f"Error parsing price data for {symbol}: {e}")
                return None

        return None

    def get_current_prices(self) -> Dict[str, Optional[float]]:
        """
        Get current prices for all stocks in watchlist

        Returns:
            Dictionary mapping symbols to prices
        """
        prices = {}
        for symbol in self.watchlist:
            prices[symbol] = self.get_current_price(symbol)
        return prices

    def get_historical_data(self, symbol: str, days: int = 30) -> Optional[Dict]:
        """
        Get historical price data for a symbol

        Args:
            symbol: Stock symbol
            days: Number of days of historical data

        Returns:
            Dictionary with historical data
        """
        cache_key = f"historical_{symbol}_{days}"
        cached_data = self._get_from_cache(cache_key)

        if cached_data:
            return cached_data

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        endpoint = f"datasets/WIKI/{symbol}"
        params = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d')
        }

        result = self._make_api_call(endpoint, params)

        if 'error' not in result and 'dataset' in result:
            try:
                data = result['dataset']['data']
                columns = result['dataset']['column_names']

                historical_data = {
                    'symbol': symbol,
                    'columns': columns,
                    'data': data,
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'end_date': end_date.strftime('%Y-%m-%d')
                }

                self._save_to_cache(cache_key, historical_data)
                return historical_data

            except (KeyError, IndexError) as e:
                print(f"Error parsing historical data for {symbol}: {e}")
                return None

        return None

    def get_quote_data(self, symbol: str) -> Optional[Dict]:
        """
        Get comprehensive quote data for a symbol

        Args:
            symbol: Stock symbol

        Returns:
            Dictionary with quote information
        """
        historical = self.get_historical_data(symbol, days=1)

        if not historical or not historical.get('data'):
            return None

        latest = historical['data'][0]
        columns = historical['columns']

        quote = {}
        for i, col in enumerate(columns):
            if i < len(latest):
                quote[col.lower().replace(' ', '_')] = latest[i]

        return quote

    def analyze_stock(self, symbol: str, days: int = 90) -> Optional[Dict]:
        """
        Perform in-depth analysis on a stock

        Args:
            symbol: Stock symbol
            days: Number of days of historical data for analysis

        Returns:
            Dictionary with comprehensive analysis
        """
        print(f"\nAnalyzing {symbol}...")

        # Get historical data
        historical_data = self.get_historical_data(symbol, days=days)

        if not historical_data:
            print(f"Could not retrieve data for {symbol}")
            return None

        # Get current quote
        quote = self.get_quote_data(symbol)

        # Perform technical analysis
        analysis = self.analyzer.analyze(historical_data, quote)

        return analysis

    def analyze_watchlist(self) -> Dict[str, Optional[Dict]]:
        """
        Analyze all stocks in the watchlist

        Returns:
            Dictionary mapping symbols to their analysis
        """
        analyses = {}

        for symbol in self.watchlist:
            analyses[symbol] = self.analyze_stock(symbol)
            time.sleep(0.5)  # Rate limiting

        return analyses

    def get_price_alert(self, symbol: str, target_price: float,
                       alert_type: str = 'above') -> Optional[str]:
        """
        Check if a stock has reached a target price

        Args:
            symbol: Stock symbol
            target_price: Target price to check
            alert_type: 'above' or 'below'

        Returns:
            Alert message if triggered, None otherwise
        """
        current_price = self.get_current_price(symbol)

        if current_price is None:
            return None

        if alert_type == 'above' and current_price >= target_price:
            return f"ALERT: {symbol} is at ${current_price:.2f}, above target ${target_price:.2f}"
        elif alert_type == 'below' and current_price <= target_price:
            return f"ALERT: {symbol} is at ${current_price:.2f}, below target ${target_price:.2f}"

        return None

    def monitor_continuous(self, interval: int = 300, alerts: Optional[Dict] = None):
        """
        Continuously monitor watchlist stocks

        Args:
            interval: Update interval in seconds
            alerts: Dictionary of {symbol: {'target': price, 'type': 'above'/'below'}}
        """
        print(f"Starting continuous monitoring (update every {interval}s)")
        print(f"Monitoring: {', '.join(self.watchlist)}")
        print("Press Ctrl+C to stop\n")

        if alerts is None:
            alerts = {}

        try:
            while True:
                print(f"\n{'='*60}")
                print(f"Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                print('='*60)

                prices = self.get_current_prices()

                for symbol, price in prices.items():
                    if price:
                        print(f"{symbol}: ${price:.2f}")

                        # Check alerts
                        if symbol in alerts:
                            alert = self.get_price_alert(
                                symbol,
                                alerts[symbol]['target'],
                                alerts[symbol].get('type', 'above')
                            )
                            if alert:
                                print(f"  >>> {alert}")
                    else:
                        print(f"{symbol}: Price unavailable")

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nMonitoring stopped by user")

    def print_summary(self) -> None:
        """
        Print a summary of the current watchlist
        """
        print(f"\n{'='*60}")
        print("STOCK WATCHLIST SUMMARY")
        print('='*60)
        print(f"Stocks tracked: {len(self.watchlist)}")
        print(f"Symbols: {', '.join(self.watchlist)}")
        print('='*60)

        prices = self.get_current_prices()

        for symbol, price in prices.items():
            if price:
                print(f"{symbol:8s} ${price:10.2f}")
            else:
                print(f"{symbol:8s} {'N/A':>10s}")

        print('='*60)
