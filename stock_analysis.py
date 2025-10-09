"""
Stock Analysis Module - Provides in-depth technical and fundamental analysis
"""

import statistics
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import math


class StockAnalyzer:
    """
    Provides comprehensive stock analysis including technical indicators
    and fundamental metrics
    """

    def __init__(self):
        """Initialize the analyzer"""
        self.analysis_methods = {
            'technical': self._technical_analysis,
            'volume': self._volume_analysis,
            'trend': self._trend_analysis,
            'volatility': self._volatility_analysis,
            'momentum': self._momentum_analysis
        }

    def analyze(self, historical_data: Dict, quote: Optional[Dict] = None) -> Dict:
        """
        Perform comprehensive analysis on stock data

        Args:
            historical_data: Historical price data
            quote: Current quote data

        Returns:
            Dictionary with analysis results
        """
        if not historical_data or not historical_data.get('data'):
            return {'error': 'No data available for analysis'}

        symbol = historical_data.get('symbol', 'UNKNOWN')
        data = historical_data['data']
        columns = historical_data['columns']

        # Extract price and volume data
        prices = self._extract_prices(data, columns)
        volumes = self._extract_volumes(data, columns)

        if not prices:
            return {'error': 'Could not extract price data'}

        # Run all analysis methods
        analysis = {
            'symbol': symbol,
            'timestamp': datetime.now().isoformat(),
            'data_points': len(prices),
            'current_price': prices[-1] if prices else None,
        }

        # Technical indicators
        analysis['technical'] = self._technical_analysis(prices)

        # Volume analysis
        if volumes:
            analysis['volume'] = self._volume_analysis(volumes, prices)

        # Trend analysis
        analysis['trend'] = self._trend_analysis(prices)

        # Volatility analysis
        analysis['volatility'] = self._volatility_analysis(prices)

        # Momentum analysis
        analysis['momentum'] = self._momentum_analysis(prices)

        # Generate recommendation
        analysis['recommendation'] = self._generate_recommendation(analysis)

        # Add summary
        analysis['summary'] = self._generate_summary(analysis)

        return analysis

    def _extract_prices(self, data: List, columns: List) -> List[float]:
        """Extract closing prices from data"""
        try:
            close_idx = columns.index('Close') if 'Close' in columns else 4
            prices = [float(row[close_idx]) for row in data if row[close_idx]]
            return list(reversed(prices))  # Reverse to chronological order
        except (ValueError, IndexError, TypeError):
            return []

    def _extract_volumes(self, data: List, columns: List) -> List[float]:
        """Extract volume data"""
        try:
            vol_idx = columns.index('Volume') if 'Volume' in columns else 5
            volumes = [float(row[vol_idx]) for row in data if row[vol_idx]]
            return list(reversed(volumes))
        except (ValueError, IndexError, TypeError):
            return []

    def _technical_analysis(self, prices: List[float]) -> Dict:
        """
        Calculate technical indicators

        Args:
            prices: List of closing prices

        Returns:
            Dictionary of technical indicators
        """
        if not prices:
            return {}

        current_price = prices[-1]

        # Simple Moving Averages
        sma_10 = self._calculate_sma(prices, 10)
        sma_20 = self._calculate_sma(prices, 20)
        sma_50 = self._calculate_sma(prices, 50)
        sma_200 = self._calculate_sma(prices, 200)

        # Exponential Moving Averages
        ema_12 = self._calculate_ema(prices, 12)
        ema_26 = self._calculate_ema(prices, 26)

        # RSI (Relative Strength Index)
        rsi = self._calculate_rsi(prices, 14)

        # MACD
        macd, signal, histogram = self._calculate_macd(prices)

        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = self._calculate_bollinger_bands(prices, 20)

        # Support and Resistance levels
        support, resistance = self._calculate_support_resistance(prices)

        return {
            'current_price': current_price,
            'sma_10': sma_10,
            'sma_20': sma_20,
            'sma_50': sma_50,
            'sma_200': sma_200,
            'ema_12': ema_12,
            'ema_26': ema_26,
            'rsi': rsi,
            'rsi_signal': self._rsi_signal(rsi),
            'macd': macd,
            'macd_signal': signal,
            'macd_histogram': histogram,
            'macd_crossover': 'bullish' if macd > signal else 'bearish',
            'bollinger_upper': bb_upper,
            'bollinger_middle': bb_middle,
            'bollinger_lower': bb_lower,
            'bollinger_position': self._bollinger_position(current_price, bb_upper, bb_lower),
            'support_level': support,
            'resistance_level': resistance,
            'price_vs_sma50': ((current_price - sma_50) / sma_50 * 100) if sma_50 else None,
            'price_vs_sma200': ((current_price - sma_200) / sma_200 * 100) if sma_200 else None,
        }

    def _volume_analysis(self, volumes: List[float], prices: List[float]) -> Dict:
        """
        Analyze volume patterns

        Args:
            volumes: List of volume data
            prices: List of prices

        Returns:
            Volume analysis results
        """
        if not volumes:
            return {}

        current_volume = volumes[-1]
        avg_volume = statistics.mean(volumes)
        volume_trend = self._calculate_trend(volumes[-10:]) if len(volumes) >= 10 else None

        # Calculate On-Balance Volume (OBV)
        obv = self._calculate_obv(prices, volumes)

        return {
            'current_volume': current_volume,
            'average_volume': avg_volume,
            'volume_ratio': current_volume / avg_volume if avg_volume > 0 else None,
            'volume_trend': volume_trend,
            'volume_signal': 'high' if current_volume > avg_volume * 1.5 else 'normal',
            'obv': obv,
            'obv_trend': self._calculate_trend(obv[-10:]) if len(obv) >= 10 else None,
        }

    def _trend_analysis(self, prices: List[float]) -> Dict:
        """
        Analyze price trends

        Args:
            prices: List of closing prices

        Returns:
            Trend analysis results
        """
        if len(prices) < 2:
            return {}

        # Short-term trend (10 days)
        short_trend = self._calculate_trend(prices[-10:]) if len(prices) >= 10 else None

        # Medium-term trend (30 days)
        medium_trend = self._calculate_trend(prices[-30:]) if len(prices) >= 30 else None

        # Long-term trend (all data)
        long_trend = self._calculate_trend(prices)

        # Calculate price changes
        price_change_1d = ((prices[-1] - prices[-2]) / prices[-2] * 100) if len(prices) >= 2 else None
        price_change_5d = ((prices[-1] - prices[-6]) / prices[-6] * 100) if len(prices) >= 6 else None
        price_change_30d = ((prices[-1] - prices[-31]) / prices[-31] * 100) if len(prices) >= 31 else None

        # Identify trend direction
        overall_trend = self._classify_trend(short_trend, medium_trend, long_trend)

        return {
            'short_term_trend': short_trend,
            'medium_term_trend': medium_trend,
            'long_term_trend': long_trend,
            'overall_trend': overall_trend,
            'price_change_1d': price_change_1d,
            'price_change_5d': price_change_5d,
            'price_change_30d': price_change_30d,
            'highest_price': max(prices),
            'lowest_price': min(prices),
            'price_range': max(prices) - min(prices),
        }

    def _volatility_analysis(self, prices: List[float]) -> Dict:
        """
        Analyze price volatility

        Args:
            prices: List of closing prices

        Returns:
            Volatility analysis results
        """
        if len(prices) < 2:
            return {}

        # Calculate daily returns
        returns = [(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]

        # Standard deviation (volatility)
        volatility = statistics.stdev(returns) if len(returns) > 1 else 0

        # Annualized volatility (assuming 252 trading days)
        annualized_volatility = volatility * math.sqrt(252)

        # Average True Range (simplified)
        atr = self._calculate_atr(prices, 14)

        return {
            'volatility': volatility,
            'annualized_volatility': annualized_volatility,
            'volatility_percent': volatility * 100,
            'atr': atr,
            'volatility_rating': self._rate_volatility(annualized_volatility),
        }

    def _momentum_analysis(self, prices: List[float]) -> Dict:
        """
        Analyze price momentum

        Args:
            prices: List of closing prices

        Returns:
            Momentum analysis results
        """
        if len(prices) < 10:
            return {}

        # Rate of Change (ROC)
        roc_10 = self._calculate_roc(prices, 10)
        roc_20 = self._calculate_roc(prices, 20)

        # Momentum indicator
        momentum_10 = prices[-1] - prices[-11] if len(prices) >= 11 else None

        # Stochastic Oscillator
        stochastic = self._calculate_stochastic(prices, 14)

        return {
            'roc_10': roc_10,
            'roc_20': roc_20,
            'momentum_10': momentum_10,
            'stochastic': stochastic,
            'stochastic_signal': self._stochastic_signal(stochastic),
            'momentum_rating': self._rate_momentum(roc_10, roc_20),
        }

    # ========== CALCULATION METHODS ==========

    def _calculate_sma(self, prices: List[float], period: int) -> Optional[float]:
        """Calculate Simple Moving Average"""
        if len(prices) < period:
            return None
        return statistics.mean(prices[-period:])

    def _calculate_ema(self, prices: List[float], period: int) -> Optional[float]:
        """Calculate Exponential Moving Average"""
        if len(prices) < period:
            return None

        multiplier = 2 / (period + 1)
        ema = statistics.mean(prices[:period])

        for price in prices[period:]:
            ema = (price - ema) * multiplier + ema

        return ema

    def _calculate_rsi(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None

        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i-1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))

        if len(gains) < period:
            return None

        avg_gain = statistics.mean(gains[-period:])
        avg_loss = statistics.mean(losses[-period:])

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def _calculate_macd(self, prices: List[float]) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        ema_12 = self._calculate_ema(prices, 12)
        ema_26 = self._calculate_ema(prices, 26)

        if ema_12 is None or ema_26 is None:
            return None, None, None

        macd = ema_12 - ema_26

        # Calculate signal line (9-day EMA of MACD)
        # Simplified: using current MACD value as signal
        signal = macd * 0.9  # Simplified

        histogram = macd - signal

        return macd, signal, histogram

    def _calculate_bollinger_bands(self, prices: List[float], period: int = 20) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """Calculate Bollinger Bands"""
        if len(prices) < period:
            return None, None, None

        sma = statistics.mean(prices[-period:])
        std_dev = statistics.stdev(prices[-period:])

        upper_band = sma + (2 * std_dev)
        lower_band = sma - (2 * std_dev)

        return upper_band, sma, lower_band

    def _calculate_support_resistance(self, prices: List[float]) -> Tuple[Optional[float], Optional[float]]:
        """Calculate basic support and resistance levels"""
        if len(prices) < 10:
            return None, None

        recent_prices = prices[-30:] if len(prices) >= 30 else prices

        support = min(recent_prices)
        resistance = max(recent_prices)

        return support, resistance

    def _calculate_obv(self, prices: List[float], volumes: List[float]) -> List[float]:
        """Calculate On-Balance Volume"""
        obv = [volumes[0]]

        for i in range(1, min(len(prices), len(volumes))):
            if prices[i] > prices[i-1]:
                obv.append(obv[-1] + volumes[i])
            elif prices[i] < prices[i-1]:
                obv.append(obv[-1] - volumes[i])
            else:
                obv.append(obv[-1])

        return obv

    def _calculate_atr(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate Average True Range (simplified)"""
        if len(prices) < period + 1:
            return None

        ranges = [abs(prices[i] - prices[i-1]) for i in range(1, len(prices))]
        atr = statistics.mean(ranges[-period:])

        return atr

    def _calculate_roc(self, prices: List[float], period: int) -> Optional[float]:
        """Calculate Rate of Change"""
        if len(prices) < period + 1:
            return None

        roc = ((prices[-1] - prices[-(period+1)]) / prices[-(period+1)]) * 100
        return roc

    def _calculate_stochastic(self, prices: List[float], period: int = 14) -> Optional[float]:
        """Calculate Stochastic Oscillator"""
        if len(prices) < period:
            return None

        recent = prices[-period:]
        highest = max(recent)
        lowest = min(recent)
        current = prices[-1]

        if highest == lowest:
            return 50

        stochastic = ((current - lowest) / (highest - lowest)) * 100
        return stochastic

    def _calculate_trend(self, prices: List[float]) -> Optional[float]:
        """Calculate trend (slope) using linear regression"""
        if len(prices) < 2:
            return None

        n = len(prices)
        x = list(range(n))
        y = prices

        x_mean = statistics.mean(x)
        y_mean = statistics.mean(y)

        numerator = sum((x[i] - x_mean) * (y[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0

        slope = numerator / denominator
        return slope

    # ========== SIGNAL INTERPRETATION METHODS ==========

    def _rsi_signal(self, rsi: Optional[float]) -> str:
        """Interpret RSI signal"""
        if rsi is None:
            return 'unknown'
        if rsi > 70:
            return 'overbought'
        elif rsi < 30:
            return 'oversold'
        else:
            return 'neutral'

    def _bollinger_position(self, price: float, upper: Optional[float], lower: Optional[float]) -> str:
        """Determine price position relative to Bollinger Bands"""
        if upper is None or lower is None:
            return 'unknown'

        if price > upper:
            return 'above_upper'
        elif price < lower:
            return 'below_lower'
        else:
            return 'within_bands'

    def _stochastic_signal(self, stochastic: Optional[float]) -> str:
        """Interpret Stochastic Oscillator signal"""
        if stochastic is None:
            return 'unknown'
        if stochastic > 80:
            return 'overbought'
        elif stochastic < 20:
            return 'oversold'
        else:
            return 'neutral'

    def _classify_trend(self, short: Optional[float], medium: Optional[float], long: Optional[float]) -> str:
        """Classify overall trend"""
        trends = [t for t in [short, medium, long] if t is not None]

        if not trends:
            return 'unknown'

        avg_trend = statistics.mean(trends)

        if avg_trend > 0.5:
            return 'strong_uptrend'
        elif avg_trend > 0.1:
            return 'uptrend'
        elif avg_trend > -0.1:
            return 'sideways'
        elif avg_trend > -0.5:
            return 'downtrend'
        else:
            return 'strong_downtrend'

    def _rate_volatility(self, annualized_vol: float) -> str:
        """Rate volatility level"""
        if annualized_vol > 0.4:
            return 'very_high'
        elif annualized_vol > 0.3:
            return 'high'
        elif annualized_vol > 0.2:
            return 'moderate'
        elif annualized_vol > 0.1:
            return 'low'
        else:
            return 'very_low'

    def _rate_momentum(self, roc_10: Optional[float], roc_20: Optional[float]) -> str:
        """Rate momentum strength"""
        if roc_10 is None:
            return 'unknown'

        if roc_10 > 10:
            return 'very_strong'
        elif roc_10 > 5:
            return 'strong'
        elif roc_10 > -5:
            return 'neutral'
        elif roc_10 > -10:
            return 'weak'
        else:
            return 'very_weak'

    def _generate_recommendation(self, analysis: Dict) -> Dict:
        """
        Generate buy/hold/sell recommendation based on analysis

        Args:
            analysis: Complete analysis dictionary

        Returns:
            Recommendation dictionary
        """
        signals = []
        score = 0

        technical = analysis.get('technical', {})
        trend = analysis.get('trend', {})
        momentum = analysis.get('momentum', {})

        # RSI signals
        if technical.get('rsi_signal') == 'oversold':
            score += 2
            signals.append('RSI oversold - potential buy')
        elif technical.get('rsi_signal') == 'overbought':
            score -= 2
            signals.append('RSI overbought - potential sell')

        # MACD signals
        if technical.get('macd_crossover') == 'bullish':
            score += 1
            signals.append('MACD bullish crossover')
        elif technical.get('macd_crossover') == 'bearish':
            score -= 1
            signals.append('MACD bearish crossover')

        # Trend signals
        overall_trend = trend.get('overall_trend', '')
        if 'uptrend' in overall_trend:
            score += 2
            signals.append(f'Price in {overall_trend}')
        elif 'downtrend' in overall_trend:
            score -= 2
            signals.append(f'Price in {overall_trend}')

        # Moving average signals
        price_vs_sma50 = technical.get('price_vs_sma50')
        if price_vs_sma50 and price_vs_sma50 > 5:
            score += 1
            signals.append('Price above 50-day SMA')
        elif price_vs_sma50 and price_vs_sma50 < -5:
            score -= 1
            signals.append('Price below 50-day SMA')

        # Determine recommendation
        if score >= 4:
            recommendation = 'STRONG BUY'
        elif score >= 2:
            recommendation = 'BUY'
        elif score >= -1:
            recommendation = 'HOLD'
        elif score >= -3:
            recommendation = 'SELL'
        else:
            recommendation = 'STRONG SELL'

        return {
            'recommendation': recommendation,
            'score': score,
            'signals': signals,
            'confidence': min(abs(score) * 15, 100)
        }

    def _generate_summary(self, analysis: Dict) -> str:
        """
        Generate a human-readable summary of the analysis

        Args:
            analysis: Complete analysis dictionary

        Returns:
            Summary string
        """
        symbol = analysis.get('symbol', 'Stock')
        current_price = analysis.get('current_price', 'N/A')
        recommendation = analysis.get('recommendation', {}).get('recommendation', 'N/A')

        technical = analysis.get('technical', {})
        trend = analysis.get('trend', {})

        summary_parts = [
            f"{symbol} Analysis Summary",
            f"Current Price: ${current_price:.2f}" if isinstance(current_price, (int, float)) else f"Current Price: {current_price}",
            f"Recommendation: {recommendation}",
            f"Trend: {trend.get('overall_trend', 'unknown').replace('_', ' ').title()}",
            f"RSI: {technical.get('rsi', 'N/A'):.2f} ({technical.get('rsi_signal', 'N/A')})" if technical.get('rsi') else "RSI: N/A",
        ]

        return " | ".join(summary_parts)
