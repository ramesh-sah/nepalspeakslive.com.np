# import os
# import csv
# import time
# import requests
# import re
# import json
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.options import Options
# from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from bs4 import BeautifulSoup
# from openai import OpenAI
# from urllib.parse import urljoin, urlparse
# import logging
# from datetime import datetime, timedelta
# from PIL import Image
# import io
# import hashlib
# import sys

# # Configure logging with proper encoding for Windows
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('scraper.log', encoding='utf-8'),
#         logging.StreamHandler(sys.stdout)
#     ]
# )

# class HimalayanTimesScraper:
#     def __init__(self, config_file='config.json'):
#         self.base_url = "https://thehimalayantimes.com"
#         self.search_url = "https://thehimalayantimes.com/search?query=everest"
#         self.driver = None
#         self.news_data = []
        
#         # Load configuration
#         self.config = self.load_config(config_file)
        
#         # OpenAI configuration
#         if self.config.get('openai_api_key') and self.config['openai_api_key'] != "your-openai-api-key-here":
#             self.client = OpenAI(api_key=self.config['openai_api_key'])
#             self.use_ai = True
#             logging.info("AI content generation enabled")
#         else:
#             self.client = None
#             self.use_ai = False
#             logging.info("OpenAI API key not provided or invalid. AI content generation disabled.")
        
#         # Create directories with proper paths
#         self.media_dir = os.path.join('media', 'news', 'featured')
#         self.scraped_data_dir = 'scraped_data'
        
#         os.makedirs(self.media_dir, exist_ok=True)
#         os.makedirs(self.scraped_data_dir, exist_ok=True)
        
#         # Category mapping
#         self.category_mapping = {
#             'Nepal': 'Mountain',
#             'Kathmandu': 'Travel', 
#             'Business': 'Expedition',
#             'Lifestyle': 'Travel',
#             'Opinion': 'Legends',
#             'Sports': 'Expedition',
#             'Entertainment': 'Travel',
#             'World': 'Environment'
#         }
    
#     def load_config(self, config_file):
#         """Load configuration from JSON file"""
#         default_config = {
#             "openai_api_key": "",
#             "max_pages": 5,
#             "max_articles": 50,
#             "delay_between_requests": 2,
#             "request_timeout": 15,
#             "enable_ai_enhancement": True,
#             "image_max_width": 1200,
#             "image_max_height": 800,
#             "image_quality": 85,
#             "skip_ai_on_quota_error": True
#         }
        
#         try:
#             with open(config_file, 'r', encoding='utf-8') as f:
#                 user_config = json.load(f)
#                 default_config.update(user_config)
#         except FileNotFoundError:
#             logging.warning(f"Config file {config_file} not found. Using default configuration.")
#         except json.JSONDecodeError:
#             logging.warning(f"Config file {config_file} is invalid. Using default configuration.")
        
#         return default_config
    
#     def setup_driver(self):
#         """Setup Chrome driver with options"""
#         chrome_options = Options()
#         chrome_options.add_argument('--headless')
#         chrome_options.add_argument('--no-sandbox')
#         chrome_options.add_argument('--disable-dev-shm-usage')
#         chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#         chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#         chrome_options.add_experimental_option('useAutomationExtension', False)
#         chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
#         chrome_options.add_argument('--window-size=1920,1080')
        
#         try:
#             self.driver = webdriver.Chrome(options=chrome_options)
#             self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
#             self.driver.implicitly_wait(10)
#             logging.info("Chrome driver initialized successfully")
#         except Exception as e:
#             logging.error(f"Failed to initialize Chrome driver: {e}")
#             raise
    
#     def scrape_all_pages(self):
#         """Scrape all available pages from search results"""
#         try:
#             logging.info(f"Starting to scrape from: {self.search_url}")
#             self.driver.get(self.search_url)
#             time.sleep(3)
            
#             page_count = self.get_total_pages()
#             max_pages = min(page_count, self.config['max_pages'])
#             logging.info(f"Found {page_count} pages to scrape, limiting to {max_pages}")
            
#             for page in range(1, max_pages + 1):
#                 logging.info(f"Scraping page {page}/{max_pages}")
                
#                 if page > 1:
#                     if not self.go_to_page(page):
#                         logging.warning(f"Failed to navigate to page {page}. Stopping.")
#                         break
                
#                 # Wait for articles to load
#                 try:
#                     WebDriverWait(self.driver, 15).until(
#                         EC.presence_of_element_located((By.CLASS_NAME, "post_list"))
#                     )
#                 except TimeoutException:
#                     logging.warning(f"Timeout waiting for articles on page {page}")
#                     continue
                
#                 # Parse the page
#                 soup = BeautifulSoup(self.driver.page_source, 'html.parser')
#                 articles = soup.find_all('article', class_='row')
                
#                 logging.info(f"Found {len(articles)} articles on page {page}")
                
#                 articles_added = 0
#                 for article in articles:
#                     try:
#                         news_item = self.extract_article_data(article)
#                         if news_item and not self.is_duplicate(news_item):
#                             self.news_data.append(news_item)
#                             articles_added += 1
#                             logging.info(f"[ADDED] Article: {news_item['title'][:80]}...")
                            
#                             # Check if we've reached the maximum articles limit
#                             if len(self.news_data) >= self.config['max_articles']:
#                                 logging.info(f"Reached maximum articles limit ({self.config['max_articles']})")
#                                 return
#                     except Exception as e:
#                         logging.error(f"Error extracting article: {e}")
#                         continue
                
#                 logging.info(f"Added {articles_added} new articles from page {page}")
#                 time.sleep(self.config['delay_between_requests'])
            
#             logging.info(f"Total articles collected: {len(self.news_data)}")
            
#         except Exception as e:
#             logging.error(f"Error in search scraping: {e}")
    
#     def get_total_pages(self):
#         """Get total number of pages from pagination"""
#         try:
#             pagination = self.driver.find_element(By.CLASS_NAME, 'pagination')
#             page_links = pagination.find_elements(By.CLASS_NAME, 'pager-nav')
#             if page_links:
#                 # Find the last page number (second last element usually)
#                 for i in range(len(page_links)-1, -1, -1):
#                     try:
#                         page_num = int(page_links[i].text)
#                         return page_num
#                     except ValueError:
#                         continue
#         except Exception as e:
#             logging.warning(f"Could not determine total pages: {e}")
#         return 1  # Default to 1 page if cannot determine
    
#     def go_to_page(self, page_number):
#         """Navigate to specific page number"""
#         try:
#             next_url = f"{self.search_url}&pgno={page_number}"
#             self.driver.get(next_url)
#             time.sleep(3)
#             return True
#         except Exception as e:
#             logging.error(f"Error going to page {page_number}: {e}")
#             return False
    
#     def is_duplicate(self, new_item):
#         """Check if article already exists in collected data"""
#         for item in self.news_data:
#             if item['title'] == new_item['title'] or item['url'] == new_item['url']:
#                 return True
#         return False
    
#     def extract_article_data(self, article):
#         """Extract basic article data from search result"""
#         try:
#             # Title and URL
#             title_elem = article.find('h3', class_='alith_post_title')
#             if not title_elem:
#                 return None
                
#             title_link = title_elem.find('a')
#             if not title_link:
#                 return None
                
#             title = title_link.get_text(strip=True)
#             article_url = title_link.get('href', '')
            
#             if not title or not article_url:
#                 return None
            
#             # Summary
#             summary_elem = article.find('div', class_='alith_post_except')
#             summary = summary_elem.get_text(strip=True) if summary_elem else ""
            
#             # Image
#             img_elem = article.find('img')
#             image_url = ""
#             if img_elem:
#                 image_url = img_elem.get('src') or img_elem.get('data-src', '')
#                 # Clean image URL
#                 if image_url and 'premiumread.com' in image_url:
#                     # Extract original image URL from premiumread
#                     match = re.search(r'url=([^&]+)', image_url)
#                     if match:
#                         image_url = match.group(1)
            
#             # Category and date
#             meta_elem = article.find('div', class_='post_meta')
#             category = ""
#             date_text = ""
#             if meta_elem:
#                 category_elem = meta_elem.find('span', class_='section')
#                 date_elem = meta_elem.find('span', class_='meta_date')
#                 category = category_elem.get_text(strip=True) if category_elem else ""
#                 date_text = date_elem.get_text(strip=True) if date_elem else ""
            
#             return {
#                 'title': title,
#                 'url': urljoin(self.base_url, article_url),
#                 'summary': summary,
#                 'image_url': image_url,
#                 'category': category,
#                 'date_text': date_text,
#                 'full_content': "",
#                 'author': "The Himalayan Times",
#                 'tags': "",
#                 'location': "Nepal",
#                 'peak_altitude': "",
#                 'weather_update': "",
#                 'expedition_info': "",
#                 'risk_level': "Moderate",
#                 'featured_image_path': "",
#                 'is_mount_everest_south': 0,
#                 'is_mount_everest_north': 0,
#                 'content_source': 'original',
#                 'ai_generation_failed': False
#             }
#         except Exception as e:
#             logging.error(f"Error extracting article data: {e}")
#             return None
    
#     def scrape_article_details(self):
#         """Scrape detailed information from individual article pages"""
#         total_articles = len(self.news_data)
#         successful_scrapes = 0
#         ai_quota_exceeded = False
        
#         for i, article in enumerate(self.news_data):
#             try:
#                 if i >= self.config['max_articles']:
#                     break
                    
#                 logging.info(f"Scraping details [{i+1}/{total_articles}]: {article['title'][:60]}...")
                
#                 self.driver.get(article['url'])
#                 time.sleep(2)
                
#                 # Get detailed content
#                 detailed_data = self.extract_detailed_content()
#                 article.update(detailed_data)
                
#                 # Download and process image
#                 if article['image_url']:
#                     image_path = self.download_and_process_image(article['image_url'], article['title'])
#                     article['featured_image_path'] = image_path
                
#                 # Generate AI-enhanced content (skip if quota exceeded)
#                 if (self.use_ai and self.config['enable_ai_enhancement'] and 
#                     not ai_quota_exceeded and not article.get('ai_generation_failed')):
#                     ai_content = self.generate_seo_optimized_content(article)
#                     if ai_content and len(ai_content) > 100:  # Only use if substantial content
#                         article['full_content'] = ai_content
#                         article['content_source'] = 'ai_enhanced'
#                         logging.info(f"[AI] Content generated for: {article['title'][:60]}...")
#                     elif "quota" in str(ai_content).lower() or "429" in str(ai_content):
#                         ai_quota_exceeded = True
#                         article['ai_generation_failed'] = True
#                         logging.warning("OpenAI quota exceeded. Disabling AI for remaining articles.")
                
#                 # Determine category and subcategory
#                 category_info = self.determine_categories(article)
#                 article.update(category_info)
                
#                 # Set Everest flags
#                 article.update(self.determine_everest_flags(article))
                
#                 successful_scrapes += 1
#                 logging.info(f"[DONE] Completed: {article['title'][:60]}...")
                
#             except Exception as e:
#                 logging.error(f"Error scraping article details: {e}")
#                 continue
            
#             time.sleep(self.config['delay_between_requests'])
        
#         logging.info(f"Successfully scraped {successful_scrapes} out of {total_articles} articles")
    
#     def extract_detailed_content(self):
#         """Extract detailed content from article page"""
#         try:
#             soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
#             # Extract main content - try multiple selectors
#             content_selectors = [
#                 'div.post-content',
#                 'div.entry-content',
#                 'div.article-content',
#                 'div.story-details',
#                 'article .content',
#                 '.story-content'
#             ]
            
#             content_div = None
#             for selector in content_selectors:
#                 content_div = soup.select_one(selector)
#                 if content_div:
#                     break
            
#             if not content_div:
#                 # Fallback: get all paragraphs from main content area
#                 content_div = soup.find('article') or soup.find('div', class_='col-md-8') or soup.find('div', class_='content-area')
            
#             content_text = []
#             if content_div:
#                 # Get all text elements, exclude ads and navigation
#                 elements = content_div.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
#                 for elem in elements:
#                     text = elem.get_text(strip=True)
#                     if (text and len(text) > 20 and 
#                         not any(exclude in text.lower() for exclude in ['advertisement', 'sponsored', 'facebook', 'twitter', 'whatsapp', 'viber'])):
#                         content_text.append(text)
            
#             full_content = '\n\n'.join(content_text) if content_text else "Content not available"
            
#             # Extract author
#             author = "The Himalayan Times"
#             author_selectors = ['.author', '.byline', '.post-author', 'meta[name="author"]', '.writer']
#             for selector in author_selectors:
#                 try:
#                     if selector.startswith('meta'):
#                         meta_elem = soup.find('meta', {'name': 'author'})
#                         if meta_elem:
#                             author = meta_elem.get('content', author)
#                     else:
#                         auth_elem = soup.select_one(selector)
#                         if auth_elem:
#                             author_text = auth_elem.get_text(strip=True)
#                             if author_text and len(author_text) > 3:
#                                 author = author_text
#                                 break
#                 except:
#                     continue
            
#             return {
#                 'full_content': full_content,
#                 'author': author
#             }
            
#         except Exception as e:
#             logging.error(f"Error extracting detailed content: {e}")
#             return {'full_content': 'Content extraction failed', 'author': 'The Himalayan Times'}
    
#     def download_and_process_image(self, image_url, title):
#         """Download, process and save featured image"""
#         try:
#             if not image_url or 'placeholder' in image_url.lower():
#                 return ""
            
#             # Create unique filename using hash of title and URL
#             unique_id = hashlib.md5(f"{title}{image_url}".encode()).hexdigest()[:8]
#             clean_title = re.sub(r'[^\w\s-]', '', title.lower())
#             clean_title = re.sub(r'[-\s]+', '-', clean_title)
#             filename = f"{clean_title[:50]}_{unique_id}.jpg"
#             filepath = os.path.join(self.media_dir, filename)
            
#             # Skip if file already exists
#             if os.path.exists(filepath):
#                 logging.info(f"[IMAGE] Already exists: {filename}")
#                 return f"news/featured/{filename}"
            
#             # Download image with proper headers
#             headers = {
#                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
#                 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
#                 'Referer': 'https://thehimalayantimes.com/'
#             }
            
#             response = requests.get(image_url, timeout=self.config['request_timeout'], headers=headers)
            
#             if response.status_code == 200:
#                 # Process image
#                 image = Image.open(io.BytesIO(response.content))
                
#                 # Convert to RGB if necessary
#                 if image.mode in ('RGBA', 'P', 'LA'):
#                     image = image.convert('RGB')
                
#                 # Resize if too large
#                 if image.size[0] > self.config['image_max_width'] or image.size[1] > self.config['image_max_height']:
#                     image.thumbnail((self.config['image_max_width'], self.config['image_max_height']), Image.Resampling.LANCZOS)
                
#                 # Save optimized image
#                 image.save(filepath, 'JPEG', quality=self.config['image_quality'], optimize=True)
#                 logging.info(f"[IMAGE] Saved: {filename}")
#                 return f"news/featured/{filename}"
#             else:
#                 logging.warning(f"Failed to download image: HTTP {response.status_code}")
                
#         except Exception as e:
#             logging.error(f"Error processing image: {e}")
        
#         return ""
    
#     def generate_seo_optimized_content(self, article):
#         """Generate SEO-optimized content using OpenAI"""
#         if not self.client:
#             return article['full_content']
            
#         try:
#             # Check if we have enough content to enhance
#             if len(article['full_content']) < 100:
#                 return article['full_content']
                
#             prompt = f"""
#             As an expert mountaineering journalist and SEO specialist, rewrite this news article to be highly engaging, informative, and SEO-optimized for mountaineering enthusiasts.

#             ORIGINAL TITLE: {article['title']}
#             ORIGINAL SUMMARY: {article['summary']}
#             ORIGINAL CONTENT: {article['full_content'][:1500]}

#             Create a comprehensive, well-structured article with:

#             1. COMPELLING INTRODUCTION: Hook readers with an engaging opening
#             2. DETAILED BODY: Expand on key facts, add relevant context about mountaineering
#             3. EXPERT INSIGHTS: Include technical details about climbing, equipment, or conditions
#             4. SEO OPTIMIZATION: Naturally include relevant keywords
#             5. PROPER STRUCTURE: Use subheadings for readability
#             6. CALL TO ACTION: Engaging conclusion

#             Ensure the content is:
#             - 100% unique and original
#             - Factually accurate based on the original
#             - Engaging for adventure sports enthusiasts
#             - Optimized for search engines
#             - Between 500-800 words

#             Return only the enhanced article content without any explanations.
#             """
            
#             response = self.client.chat.completions.create(
#                 model="gpt-5-nano",
#                 messages=[
#                     {
#                         "role": "system", 
#                         "content": "You are a professional mountaineering journalist and SEO expert. Create engaging, accurate, and optimized content for climbing enthusiasts."
#                     },
#                     {
#                         "role": "user", 
#                         "content": prompt
#                     }
#                 ],
             
#                 temperature=0.7
#             )
            
#             return response.choices[0].message.content.strip()
            
#         except Exception as e:
#             error_msg = str(e)
#             logging.error(f"Error generating AI content: {error_msg}")
            
#             # Check if it's a quota error
#             if "quota" in error_msg.lower() or "429" in error_msg:
#                 if self.config['skip_ai_on_quota_error']:
#                     logging.warning("OpenAI quota exceeded. AI generation will be skipped for remaining articles.")
#                     return "quota_exceeded"
            
#             return article['full_content']
    
#     def determine_categories(self, article):
#         """Determine the best category and subcategory for the article"""
#         title = article['title'].lower()
#         content = article['full_content'].lower()
#         original_category = article['category']
        
#         # Default category
#         category_name = self.category_mapping.get(original_category, 'Mountain')
#         category_id = self.get_category_id(category_name)
        
#         # Determine subcategory based on content analysis
#         subcategory_id = self.get_subcategory_id(title, content, category_id)
        
#         # Extract additional metadata
#         location = self.extract_location(content, title)
#         altitude = self.extract_altitude(content)
#         expedition_info = self.extract_expedition_info(content)
#         tags = self.generate_seo_tags(title, content)
#         risk_level = self.determine_risk_level(content)
        
#         return {
#             'category_id': category_id,
#             'subcategory_id': subcategory_id,
#             'location': location,
#             'peak_altitude': altitude,
#             'expedition_info': expedition_info,
#             'tags': tags,
#             'risk_level': risk_level,
#             'weather_update': self.generate_weather_update(content)
#         }
    
#     def get_category_id(self, category_name):
#         """Map category name to ID"""
#         category_map = {
#             'Travel': 1, 'Legends': 2, 'Conservation': 3,
#             'Environment': 4, 'Mountain': 5, 'Expedition': 6
#         }
#         return category_map.get(category_name, 5)  # Default to Mountain
    
#     def get_subcategory_id(self, title, content, category_id):
#         """Determine the best subcategory based on content analysis"""
#         text = f"{title} {content}"
        
#         subcategory_map = {
#             # Mountain subcategories
#             5: {
#                 'everest': 25, 'manaslu': 24, 'lhotse': 23, 'makalu': 23,
#                 'seven summit': 22, 'climbing technique': 21,
#                 'k2': 22, 'annapurna': 22
#             },
#             # Expedition subcategories
#             6: {
#                 'summit': 30, 'base camp': 29, 'weather': 28, 'route': 28,
#                 'team': 27, 'gear': 26, 'logistics': 26, 'expedition': 30
#             },
#             # Travel subcategories
#             1: {
#                 'culture': 1, 'people': 1, 'accommodation': 2, 'food': 2,
#                 'travel tip': 3, 'trekking': 4, 'base camp trek': 5
#             },
#             # Legends subcategories
#             2: {
#                 'tribute': 6, 'memorial': 6, 'documentary': 7, 'book': 7,
#                 'record': 8, 'first': 8, 'famous climber': 9, 'historic': 10
#             },
#             # Conservation subcategories
#             3: {
#                 'cleanup': 15, 'sustainable': 14, 'wildlife': 13,
#                 'community': 12, 'partnership': 11, 'campaign': 11
#             },
#             # Environment subcategories
#             4: {
#                 'climate': 20, 'glacier': 19, 'waste': 18,
#                 'biodiversity': 17, 'research': 16
#             }
#         }
        
#         category_map = subcategory_map.get(category_id, {})
#         for keyword, sub_id in category_map.items():
#             if keyword in text:
#                 return sub_id
        
#         # Default subcategories for each category
#         default_subs = {1: 1, 2: 9, 3: 14, 4: 20, 5: 25, 6: 30}
#         return default_subs.get(category_id, 25)
    
#     def determine_everest_flags(self, article):
#         """Determine if article is about Everest South or North"""
#         text = f"{article['title']} {article['full_content']}".lower()
        
#         is_everest_south = 0
#         is_everest_north = 0
        
#         if 'everest' in text:
#             if 'north' in text or 'tibet' in text or 'china' in text:
#                 is_everest_north = 1
#             else:
#                 is_everest_south = 1  # Default to South side for Nepal articles
        
#         return {
#             'is_mount_everest_south': is_everest_south,
#             'is_mount_everest_north': is_everest_north
#         }
    
#     def extract_location(self, content, title):
#         """Extract location from content"""
#         locations = ['Everest', 'Manaslu', 'Lhotse', 'Makalu', 'Annapurna', 'K2', 
#                     'Kathmandu', 'Lukla', 'Namche Bazaar', 'Tibet', 'China', 'Nepal']
        
#         text = f"{title} {content}"
#         for location in locations:
#             if location.lower() in text.lower():
#                 if location in ['Tibet', 'China']:
#                     return f"Mount Everest North, {location}"
#                 elif location == 'Nepal':
#                     return "Himalayan Region, Nepal"
#                 else:
#                     return f"{location}, Nepal"
        
#         return "Himalayan Region, Nepal"
    
#     def extract_altitude(self, content):
#         """Extract peak altitude from content"""
#         patterns = [
#             r'(\d{1,4}[,.]?\d{0,3})\s*met[re]s{0,1}',
#             r'(\d{1,4}[,.]?\d{0,3})\s*m\b',
#             r'(\d{1,4}[,.]?\d{0,3})\s*meters',
#             r'altitude[^\d]*(\d{1,4}[,.]?\d{0,3})',
#             r'height[^\d]*(\d{1,4}[,.]?\d{0,3})'
#         ]
        
#         for pattern in patterns:
#             matches = re.findall(pattern, content, re.IGNORECASE)
#             if matches:
#                 altitude = matches[0].replace(',', '')
#                 try:
#                     alt_num = int(altitude)
#                     if 6000 <= alt_num <= 8900:  # Reasonable altitude range for Himalayas
#                         return f"{alt_num} m"
#                 except:
#                     pass
        
#         # Default altitudes for known peaks
#         if 'everest' in content.lower():
#             return "8848 m"
#         elif 'manaslu' in content.lower():
#             return "8163 m"
#         elif 'lhotse' in content.lower():
#             return "8516 m"
#         elif 'makalu' in content.lower():
#             return "8485 m"
        
#         return "8000+ m"
    
#     def extract_expedition_info(self, content):
#         """Extract expedition information from content"""
#         if 'team' in content.lower() and 'climb' in content.lower():
#             return "International climbing team expedition"
#         elif 'solo' in content.lower():
#             return "Solo climbing expedition"
#         elif 'record' in content.lower():
#             return "Record-setting climbing expedition"
#         elif 'first' in content.lower():
#             return "First ascent expedition"
        
#         return "Mountain climbing expedition"
    
#     def generate_seo_tags(self, title, content):
#         """Generate SEO-optimized tags"""
#         base_tags = ['Mountaineering', 'Himalayas', 'Nepal', 'Adventure Sports']
        
#         content_lower = f"{title} {content}".lower()
        
#         # Peak-specific tags
#         peak_tags = []
#         peaks = ['everest', 'manaslu', 'lhotse', 'makalu', 'annapurna', 'k2']
#         for peak in peaks:
#             if peak in content_lower:
#                 peak_tags.append(peak.title())
        
#         # Activity tags
#         activity_tags = []
#         activities = ['climbing', 'summit', 'expedition', 'trekking', 'base camp', 'ascent']
#         for activity in activities:
#             if activity in content_lower:
#                 activity_tags.append(activity.title())
        
#         # Feature tags
#         feature_tags = []
#         features = ['record', 'first', 'oxygen', 'sherpa', 'winter', 'speed']
#         for feature in features:
#             if feature in content_lower:
#                 feature_tags.append(feature.title())
        
#         all_tags = base_tags + peak_tags + activity_tags + feature_tags
#         return ', '.join(list(dict.fromkeys(all_tags))[:10])  # Remove duplicates and limit
    
#     def determine_risk_level(self, content):
#         """Determine risk level based on content"""
#         content_lower = content.lower()
        
#         high_risk_indicators = ['death', 'fatal', 'accident', 'avalanche', 'storm', 'dangerous', 'rescue']
#         medium_risk_indicators = ['challenging', 'difficult', 'extreme', 'risk', 'caution']
        
#         if any(indicator in content_lower for indicator in high_risk_indicators):
#             return "High"
#         elif any(indicator in content_lower for indicator in medium_risk_indicators):
#             return "Medium"
#         else:
#             return "Low"
    
#     def generate_weather_update(self, content):
#         """Generate weather update based on content"""
#         content_lower = content.lower()
        
#         if any(word in content_lower for word in ['storm', 'blizzard', 'snowstorm']):
#             return "Challenging weather conditions with storms"
#         elif any(word in content_lower for word in ['clear', 'sunny', 'good weather']):
#             return "Favorable climbing conditions"
#         elif any(word in content_lower for word in ['wind', 'cold', 'freezing']):
#             return "Cold temperatures with high winds"
#         else:
#             return "Standard Himalayan mountain conditions"
    
#     def generate_csv_files(self):
#         """Generate the final CSV files"""
#         current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         # Generate news_news.csv
#         news_records = []
#         for i, article in enumerate(self.news_data):
#             published_date = self.parse_date(article['date_text'])
            
#             news_record = {
#                 'id': i + 1,
#                 'title': article['title'],
#                 'slug': self.generate_slug(article['title']),
#                 'summary': article['summary'][:200] if article['summary'] else article['title'][:200],
#                 'content': article['full_content'],
#                 'author': article['author'],
#                 'published_date': published_date,
#                 'is_published': 1,
#                 'featured_image': article['featured_image_path'],
#                 'is_trending': 1 if any(word in article['title'].lower() for word in ['record', 'first', 'break', 'success']) else 0,
#                 'is_breaking': 1 if 'breaking' in article['title'].lower() else 0,
#                 'is_latest': 1,
#                 'is_exclusive': 0,
#                 'is_mount_everest_south': article['is_mount_everest_south'],
#                 'is_mount_everest_north': article['is_mount_everest_north'],
#                 'location': article['location'],
#                 'peak_altitude': article['peak_altitude'],
#                 'weather_update': article['weather_update'],
#                 'expedition_info': article['expedition_info'],
#                 'risk_level': article['risk_level'],
#                 'tags': article['tags'],
#                 'view_count': 5000,
#                 'likes': 3504,
#                 'shares': 5000,
#                 'created_at': current_time,
#                 'updated_at': current_time,
#                 'created_by_id': 1,
#                 'category_id': article['category_id'],
#                 'subcategory_id': article['subcategory_id']
#             }
#             news_records.append(news_record)
        
#         # Save news_news.csv
#         if news_records:
#             csv_path = os.path.join(self.scraped_data_dir, 'news_news.csv')
#             with open(csv_path, 'w', newline='', encoding='utf-8') as f:
#                 writer = csv.DictWriter(f, fieldnames=news_records[0].keys())
#                 writer.writeheader()
#                 writer.writerows(news_records)
#             logging.info(f"Saved {len(news_records)} articles to news_news.csv")
        
#         # Generate category files
#         self.generate_category_csv()
        
#         # Generate summary report
#         self.generate_summary_report()
        
#         logging.info("All CSV files generated successfully!")
    
#     def generate_slug(self, title):
#         """Generate SEO-friendly slug from title"""
#         slug = title.lower()
#         slug = re.sub(r'[^a-z0-9\s-]', '', slug)
#         slug = re.sub(r'[\s-]+', '-', slug)
#         slug = slug.strip('-')
#         return slug[:100]
    
#     def parse_date(self, date_text):
#         """Parse date text to proper format"""
#         try:
#             if 'ago' in date_text:
#                 days_match = re.search(r'(\d+)d', date_text)
#                 if days_match:
#                     days_ago = int(days_match.group(1))
#                     return (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
#                 else:
#                     return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#             else:
#                 # Try to parse dates like "01 Oct, 2025"
#                 date_obj = datetime.strptime(date_text, '%d %b, %Y')
#                 return date_obj.strftime('%Y-%m-%d %H:%M:%S')
#         except:
#             return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
#     def generate_category_csv(self):
#         """Generate category and subcategory CSV files"""
#         current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
#         # Categories
#         categories = [
#             {'id': 1, 'name': 'Travel', 'slug': 'travel', 'description': 'Travel related news and articles'},
#             {'id': 2, 'name': 'Legends', 'slug': 'legends', 'description': 'Legends and famous mountaineers'},
#             {'id': 3, 'name': 'Conservation', 'slug': 'conservation', 'description': 'Conservation and environmental protection'},
#             {'id': 4, 'name': 'Environment', 'slug': 'environment', 'description': 'Environmental news and climate'},
#             {'id': 5, 'name': 'Mountain', 'slug': 'mountain', 'description': 'Mountain specific news and peaks'},
#             {'id': 6, 'name': 'Expedition', 'slug': 'expedition', 'description': 'Expedition updates and reports'}
#         ]
        
#         # Subcategories
#         subcategories = [
#             # Travel subcategories
#             {'id': 1, 'name': 'Culture & People', 'slug': 'culture-people', 'category_id': 1},
#             {'id': 2, 'name': 'Accommodation & Food', 'slug': 'accommodation-food', 'category_id': 1},
#             {'id': 3, 'name': 'Travel Tips', 'slug': 'travel-tips', 'category_id': 1},
#             {'id': 4, 'name': 'Trekking Routes', 'slug': 'trekking-routes', 'category_id': 1},
#             {'id': 5, 'name': 'Everest Base Camp Trek', 'slug': 'everest-base-camp-trek', 'category_id': 1},
            
#             # Legends subcategories
#             {'id': 6, 'name': 'Tributes & Memorials', 'slug': 'tributes-memorials', 'category_id': 2},
#             {'id': 7, 'name': 'Documentaries & Books', 'slug': 'documentaries-books', 'category_id': 2},
#             {'id': 8, 'name': 'Records & Firsts', 'slug': 'records-firsts', 'category_id': 2},
#             {'id': 9, 'name': 'Famous Climbers', 'slug': 'famous-climbers', 'category_id': 2},
#             {'id': 10, 'name': 'Historic Climbs', 'slug': 'historic-climbs', 'category_id': 2},
            
#             # Conservation subcategories
#             {'id': 11, 'name': 'Partnerships & Campaigns', 'slug': 'partnerships-campaigns', 'category_id': 3},
#             {'id': 12, 'name': 'Community Projects', 'slug': 'community-projects', 'category_id': 3},
#             {'id': 13, 'name': 'Wildlife Protection', 'slug': 'wildlife-protection', 'category_id': 3},
#             {'id': 14, 'name': 'Sustainable Climbing', 'slug': 'sustainable-climbing', 'category_id': 3},
#             {'id': 15, 'name': 'Everest Cleanup', 'slug': 'everest-cleanup', 'category_id': 3},
            
#             # Environment subcategories
#             {'id': 16, 'name': 'Research & Reports', 'slug': 'research-reports', 'category_id': 4},
#             {'id': 17, 'name': 'Biodiversity', 'slug': 'biodiversity', 'category_id': 4},
#             {'id': 18, 'name': 'Waste Management', 'slug': 'waste-management', 'category_id': 4},
#             {'id': 19, 'name': 'Glacier Monitoring', 'slug': 'glacier-monitoring', 'category_id': 4},
#             {'id': 20, 'name': 'Climate Change', 'slug': 'climate-change', 'category_id': 4},
            
#             # Mountain subcategories
#             {'id': 21, 'name': 'Climbing Techniques', 'slug': 'climbing-techniques', 'category_id': 5},
#             {'id': 22, 'name': 'Seven Summits', 'slug': 'seven-summits', 'category_id': 5},
#             {'id': 23, 'name': 'Lhotse & Makalu', 'slug': 'lhotse-makalu', 'category_id': 5},
#             {'id': 24, 'name': 'Manaslu', 'slug': 'manaslu', 'category_id': 5},
#             {'id': 25, 'name': 'Everest', 'slug': 'everest', 'category_id': 5},
            
#             # Expedition subcategories
#             {'id': 26, 'name': 'Gear & Logistics', 'slug': 'gear-logistics', 'category_id': 6},
#             {'id': 27, 'name': 'Team Highlights', 'slug': 'team-highlights', 'category_id': 6},
#             {'id': 28, 'name': 'Route & Weather', 'slug': 'route-weather', 'category_id': 6},
#             {'id': 29, 'name': 'Base Camp Reports', 'slug': 'base-camp-reports', 'category_id': 6},
#             {'id': 30, 'name': 'Summit Updates', 'slug': 'summit-updates', 'category_id': 6}
#         ]
        
#         # Save categories
#         category_path = os.path.join(self.scraped_data_dir, 'news_newscategory.csv')
#         with open(category_path, 'w', newline='', encoding='utf-8') as f:
#             writer = csv.DictWriter(f, fieldnames=['id', 'name', 'slug', 'description', 'created_at', 'updated_at', 'created_by_id'])
#             writer.writeheader()
#             for cat in categories:
#                 cat.update({
#                     'created_at': current_time,
#                     'updated_at': current_time,
#                     'created_by_id': 1
#                 })
#                 writer.writerow(cat)
        
#         # Save subcategories
#         subcategory_path = os.path.join(self.scraped_data_dir, 'news_newssubcategory.csv')
#         with open(subcategory_path, 'w', newline='', encoding='utf-8') as f:
#             writer = csv.DictWriter(f, fieldnames=['id', 'name', 'slug', 'description', 'created_at', 'updated_at', 'category_id', 'created_by_id'])
#             writer.writeheader()
#             for subcat in subcategories:
#                 subcat.update({
#                     'description': f"{subcat['name']} related content",
#                     'created_at': current_time,
#                     'updated_at': current_time,
#                     'created_by_id': 1
#                 })
#                 writer.writerow(subcat)
        
#         logging.info("Category CSV files generated successfully")
    
#     def generate_summary_report(self):
#         """Generate a summary report of the scraping process"""
#         report = {
#             'total_articles': len(self.news_data),
#             'scraping_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#             'categories_distribution': {},
#             'everest_articles': 0,
#             'ai_enhanced_articles': 0,
#             'images_downloaded': 0
#         }
        
#         for article in self.news_data:
#             # Category distribution
#             cat_id = article['category_id']
#             report['categories_distribution'][cat_id] = report['categories_distribution'].get(cat_id, 0) + 1
            
#             # Everest articles
#             if article['is_mount_everest_south'] or article['is_mount_everest_north']:
#                 report['everest_articles'] += 1
            
#             # AI enhanced articles
#             if article['content_source'] == 'ai_enhanced':
#                 report['ai_enhanced_articles'] += 1
            
#             # Images downloaded
#             if article['featured_image_path']:
#                 report['images_downloaded'] += 1
        
#         # Save report
#         report_path = os.path.join(self.scraped_data_dir, 'scraping_report.json')
#         with open(report_path, 'w', encoding='utf-8') as f:
#             json.dump(report, f, indent=2, ensure_ascii=False)
        
#         logging.info("SCRAPING SUMMARY:")
#         logging.info(f"  Total Articles: {report['total_articles']}")
#         logging.info(f"  Everest Articles: {report['everest_articles']}")
#         logging.info(f"  AI Enhanced: {report['ai_enhanced_articles']}")
#         logging.info(f"  Images Downloaded: {report['images_downloaded']}")
#         logging.info(f"  Category Distribution: {report['categories_distribution']}")
    
#     def run(self):
#         """Main execution function"""
#         start_time = time.time()
        
#         try:
#             logging.info("Starting Himalayan Times Scraper")
            
#             self.setup_driver()
#             self.scrape_all_pages()
            
#             if self.news_data:
#                 self.scrape_article_details()
#                 self.generate_csv_files()
#             else:
#                 logging.warning("No articles found to scrape!")
            
#             elapsed_time = time.time() - start_time
#             logging.info(f"Scraping completed in {elapsed_time:.2f} seconds")
#             logging.info(f"Total articles processed: {len(self.news_data)}")
            
#         except Exception as e:
#             logging.error(f"Error in main execution: {e}")
#         finally:
#             if self.driver:
#                 self.driver.quit()
#                 logging.info("Chrome driver closed")

# def main():
#     scraper = HimalayanTimesScraper(config_file='config.json')
#     scraper.run()

# if __name__ == "__main__":
#     main()



import cv2

input_path = "29,000_Feet_Up_Mount_Everest_with_DJI_Mavic_3_Pro(2160p).mp4"
cap = cv2.VideoCapture(input_path)

fps = cap.get(cv2.CAP_PROP_FPS)
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

start_time = 140  # 2:20 in seconds
start_frame = int(start_time * fps)
cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

# Split in half
half_frame = (frame_count - start_frame) // 2

# Define crop region (remove watermark/logo)
y1, y2 = 50, height - 60

out1 = cv2.VideoWriter('everest_part1.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, y2-y1))
out2 = cv2.VideoWriter('everest_part2.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, y2-y1))

for i in range(half_frame):
    ret, frame = cap.read()
    if not ret:
        break
    cropped = frame[y1:y2, :]
    out1.write(cropped)

for i in range(half_frame, frame_count-start_frame):
    ret, frame = cap.read()
    if not ret:
        break
    cropped = frame[y1:y2, :]
    out2.write(cropped)

cap.release()
out1.release()
out2.release()
print("✅ Done with OpenCV!")
