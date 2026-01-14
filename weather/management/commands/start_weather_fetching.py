from django.core.management.base import BaseCommand
from weather.views import data_fetcher
from django.utils import timezone

class Command(BaseCommand):
    help = 'Debug weather API by manually fetching data with detailed logging'
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Debugging weather API...'))
        
        # Mount Everest coordinates
        everest_lat = 27.9881
        everest_lon = 86.9250
        everest_alt = 8848
        
        # Fetch data with detailed logging
        self.stdout.write("Fetching hourly data...")
        hourly_success = data_fetcher._fetch_hourly_data(everest_lat, everest_lon, everest_alt)
        
        self.stdout.write("Fetching daily data...")
        daily_success = data_fetcher._fetch_daily_data(everest_lat, everest_lon, everest_alt)
        
        self.stdout.write("Fetching monthly data...")
        monthly_success = data_fetcher._fetch_monthly_data(everest_lat, everest_lon, everest_alt)
        
        self.stdout.write(f"Results - Hourly: {'Success' if hourly_success else 'Failed'}, Daily: {'Success' if daily_success else 'Failed'}, Monthly: {'Success' if monthly_success else 'Failed'}")
        
        # Perform analysis
        self.stdout.write("Performing analysis...")
        data_fetcher._perform_analysis()
        
        self.stdout.write(self.style.SUCCESS('Debugging completed'))