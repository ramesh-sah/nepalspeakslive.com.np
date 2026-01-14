# signals.py
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta
import threading
import time
import logging

logger = logging.getLogger(__name__)

class WeatherDataRefresher:
    def __init__(self):
        self.is_running = False
        self.thread = None

    def start_refresh_loop(self):
        """Start the background refresh loop"""
        if self.is_running:
            return
            
        self.is_running = True
        self.thread = threading.Thread(target=self._refresh_loop, daemon=True)
        self.thread.start()
        logger.info("Weather data refresh loop started")

    def stop_refresh_loop(self):
        """Stop the background refresh loop"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Weather data refresh loop stopped")

    def _refresh_loop(self):
        """Background thread that refreshes weather data every 2 minutes"""
        from .views import extract_weather_data
        
        while self.is_running:
            try:
                logger.info("Refreshing weather data...")
                weather_data = extract_weather_data()
                if weather_data:
                    cache.set('everest_weather_data', weather_data, 300)  # Cache for 5 minutes
                    logger.info("Weather data refreshed successfully")
                else:
                    logger.warning("Failed to extract weather data")
            except Exception as e:
                logger.error(f"Error refreshing weather data: {e}")
            
            # Wait for 2 minutes
            for _ in range(120):  # 120 seconds = 2 minutes
                if not self.is_running:
                    break
                time.sleep(1)

# Global instance
weather_refresher = WeatherDataRefresher()

@receiver(post_migrate)
def start_weather_refresh(sender, **kwargs):
    """Start the weather refresh loop when Django starts"""
    try:
        # Only start if not already running
        if not weather_refresher.is_running:
            weather_refresher.start_refresh_loop()
    except Exception as e:
        logger.error(f"Failed to start weather refresh: {e}")

def refresh_weather_data_now():
    """Manual refresh function that can be called from anywhere"""
    from .views import extract_weather_data
    try:
        weather_data = extract_weather_data()
        if weather_data:
            cache.set('everest_weather_data', weather_data, 300)
            return True
    except Exception as e:
        logger.error(f"Manual refresh failed: {e}")
    return False