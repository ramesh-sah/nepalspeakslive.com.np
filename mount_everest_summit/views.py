from django.views import View
from django.shortcuts import get_object_or_404, redirect, render

from django.core.paginator import Paginator
# Correct imports for Django ORM
from django.db.models import F, Q  # ✅ Correct import source
    # views.py
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.contrib import messages

from enquiry.models import Enquiry
from advertising_channel.models import AdvertisingInquiry
from accounts.models import CustomUser
from emailnewsletter.models import EmailNewsletter
from news.models import News, NewsCategory, NewsImage , NewsSubCategory, NewsVideo
from advertising_channel.models import AdPlacement

 
class HomePage(View):
    
    
    
    
    def get(self, request):
        latest = News.objects.filter(is_latest=True).order_by('-published_date')[:6]
        trending= News.objects.filter(is_trending=True).order_by('-published_date')[:8]
        breaking = News.objects.filter(is_breaking=True).order_by('-published_date')[:4]
        exclusive = News.objects.filter(is_exclusive=True).order_by('-published_date')[:8]
        latest_news = News.objects.filter(is_latest=True).order_by('-published_date')[:4]
        all_news = News.objects.all().order_by('-published_date')


        # Get single latest low-risk news item
        live_news= NewsVideo.objects.select_related('news').last() # .first() instead of slicing
        
        top_combined = News.objects.annotate(
        total_engagement=F('view_count') + F('likes') + F('shares')
    ).order_by('-total_engagement')[:10]
        ads=AdPlacement.objects.filter(placement='homepage')[:0]
        
        meta = {
    "title": "Mount Everest Summit - News, Expeditions & Guides",
    "description": "Get the latest Mount Everest news, weather updates, climbing expeditions, and expert guides for your Everest adventure.",
    "keyword": "Mount Everest, Everest news, Everest expedition, climbing guides, Everest weather, Everest adventure"
}

                    

        context = {
            'live_news': live_news,
            'trending': trending,
            'breaking': breaking,
            'exclusive': exclusive,
            'latest': latest,
            'latest_news': latest_news,
            'top_combined': top_combined,
            'ads': ads,
            'all_news':all_news,
            "meta": meta,
            
        }
        return render(request, 'home.html', context)

        

class MountEverestSouth(View):
    def get(self, request):
        
        latest = News.objects.filter(is_latest=True , is_mount_everest_south=True).order_by('-published_date')[:4]
        trending= News.objects.filter(is_trending=True, is_mount_everest_south=True).order_by('-published_date')[:4]
        breaking = News.objects.filter(is_breaking=True, is_mount_everest_south=True).order_by('-published_date')[:4]
        #get one data from exclusive
        exclusive = News.objects.filter(is_exclusive =True, is_mount_everest_south=True).order_by('-published_date').first()
      
        # ads = AdPlacement.objects.filter(placement='south').first()
        ads = AdPlacement.objects.select_related('inquiry').filter(placement='south').first()

        print(ads.inquiry.marketing_materials if ads else "No ads found")
        
        # Get single latest low-risk news item
        meta = {
    "title": "Mount Everest South - Expeditions, Trekking & Guides",
    "description": "Discover Mount Everest South expeditions, climbing tips, weather updates, and expert trekking guides for the southern route.",
    "keyword": "Mount Everest South, Everest South expeditions, Everest South climbing, Everest trekking, Everest South weather, Everest South guides"
}

                    

        context = {
          
            'trending': trending,
            'breaking': breaking,
            'exclusive': exclusive,
            'latest': latest,
            'ads': ads,
            'meta':meta,
        
           
            
        }
        

        return render(request, 'mount-everest-south.html',context)

class MountEverestNorth(View):
    def get(self, request):
       
       
        latest = News.objects.filter(is_latest=True,is_mount_everest_north=True ).order_by('-published_date')[:4]
        trending= News.objects.filter(is_trending=True, is_mount_everest_north=True).order_by('-published_date')[:4]
        breaking = News.objects.filter(is_breaking=True, is_mount_everest_north=True).order_by('-published_date')[:4]

        exclusive = News.objects.filter(is_exclusive=True, is_mount_everest_north=True).order_by('-published_date').first()
         # ads = AdPlacement.objects.filter(placement='south').first()
        ads = AdPlacement.objects.select_related('inquiry').filter(placement='north').first()

        print(ads.inquiry.marketing_materials if ads else "No ads found")
        
        # Get single latest low-risk news item
        meta = {
    "title": "Mount Everest North - Expeditions, Climbing & Guides",
    "description": "Discover Mount Everest North expeditions, climbing tips, weather updates, and trekking guides for the northern route.",
    "keyword": "Mount Everest North, Everest North expeditions, Everest North climbing, Everest North trekking, Everest North weather, Everest North guides"
}


       
                    

        context = {
          
            'trending': trending,
            'breaking': breaking,
            'exclusive': exclusive,
            'latest': latest,
            'ads': ads,
            'meta':meta,
        
           
            
        }
        

        
        return render(request, 'mount-everest-north.html',context)
    
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q
from news.models import News, NewsCategory, NewsSubCategory




class NewsView(View):
    def get(self, request):
        # Base queryset: only published news
        news_list = News.objects.filter(is_published=True).order_by('-published_date')

        # Sidebar and navigation data
        categories = NewsCategory.objects.all()
        sub_categories = NewsSubCategory.objects.filter(updated_at__isnull=False).order_by('-updated_at')[:10]
        latest_news = News.objects.filter(is_latest=True).order_by('-published_date')[:10]

        # GET parameters
        search_query = request.GET.get('q')
        category_slug = request.GET.get('category')
        subcategory_slug = request.GET.get('subcategory')

        # Apply filters
        if search_query:
            news_list = news_list.filter(
                Q(title__icontains=search_query)
                | Q(summary__icontains=search_query)
                | Q(content__icontains=search_query)
                | Q(tags__icontains=search_query)
            ).distinct()

        if category_slug:
            news_list = news_list.filter(category__slug=category_slug)

        if subcategory_slug:
            news_list = news_list.filter(subcategory__slug=subcategory_slug)

        # Pagination setup
        paginator = Paginator(news_list, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Build URL query string for pagination links (preserve filters)
        query_params = request.GET.copy()
        if 'page' in query_params:
            del query_params['page']
        query_string = '&'.join([f'{key}={value}' for key, value in query_params.items()])
        
        
        
        meta = {
    "title": "Mount Everest News - Updates, Expeditions & Climbing Guides",
    "description": (
        "Stay updated with the latest Mount Everest news, expedition reports, "
        "weather updates, and climbing guides for enthusiasts and adventurers."
    ),
    "keyword": (
        "Mount Everest news, Everest updates, Everest expeditions, climbing guides, "
        "Everest weather, high-altitude mountaineering"
    )
}


        # Context for template rendering
        context = {
            'page_obj': page_obj,
            'categories': categories,
            'sub_categories': sub_categories,
            'latest_news': latest_news,
            'search_query': search_query or '',
            'selected_category': category_slug,
            'selected_subcategory': subcategory_slug,
            'query_string': query_string,
            'meta':meta,
        }

        return render(request, 'news.html', context)


class NewsDetailView(View):
    """
    Displays the full details of a single news item,
    along with related stories, images, and videos.
    """

    def get(self, request, slug):
        # Fetch the main news article or return 404 if not found
        news_item = get_object_or_404(News, slug=slug, is_published=True)

        # Increment the view count safely using F expression
        News.objects.filter(id=news_item.id).update(view_count=F('view_count') + 1)
        news_item.refresh_from_db()

        # Fetch related stories by category or subcategory
        related_news = News.objects.filter(
            Q(category=news_item.category) | Q(subcategory=news_item.subcategory),
            is_published=True
        ).exclude(id=news_item.id).order_by('-published_date')[:6]

        # Fetch all associated images and videos
        images = NewsImage.objects.filter(news=news_item)
        videos = NewsVideo.objects.filter(news=news_item)

        # Split tags cleanly (avoid using .split() in templates)
        tag_list = []
        if news_item.tags:
            tag_list = [tag.strip() for tag in news_item.tags.split(',') if tag.strip()]
            
        # ✅ Dynamic SEO Meta Information (fixed version)
        meta = {
    "title": f"{news_item.title} | Mount Everest News",
    "description": (
        news_item.summary[:155] + "..."
        if news_item.summary else
        f"Latest news and updates about {news_item.category or 'Mount Everest'}."
    ),
    "keyword": ", ".join(
        filter(None, [
            "Mount Everest",
            "Everest news",
            "Everest expedition",
            "Everest climbing",
            str(news_item.category) if news_item.category else None,
            str(news_item.subcategory) if news_item.subcategory else None,
            *tag_list
        ])
    )
}



        context = {
            'news_item': news_item,
            'images': images,
            'videos': videos,
            'related_news': related_news,
            'tags': tag_list,
            'category': news_item.category,
            'subcategory': news_item.subcategory,
            'meta':meta,
        }

        return render(request, 'news-detail.html', context)

class TermsAndConditions(View):
    
    def get(self, request):
        meta = {
    "title": "Terms and Conditions | Mount Everest Summit",
    "description": "Read the terms and conditions for using Mount Everest Summit, including our policies on user conduct, content, and legal responsibilities.",
    "keyword": "Mount Everest Summit terms, website policy, user agreement, Everest Summit conditions, legal disclaimer"
}
        context={
            'meta':meta
        }
        return render(request, 'terms-conditions.html',context)


class ContactUs(View):
    def get(self, request):
        meta = {
    "title": "Contact Us | Mount Everest Summit",
    "description": "Get in touch with Mount Everest Summit for expedition inquiries, partnership opportunities, or general questions. We're here to help you plan your Everest journey.",
    "keyword": "contact Mount Everest Summit, Everest inquiries, expedition contact, Everest support, Everest Summit team"
}
        context={
            'meta':meta
        }
        return render(request, 'contact-us.html',context)
    
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Get form data
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country_code = request.POST.get('country_code')
        inquiry = request.POST.get('inquiry')

        # Basic validation
        errors = []
        if not full_name:
            errors.append("Full name is required")
        if not email:
            errors.append("Email is required")
        if not phone:
            errors.append("Phone number is required")
        if not inquiry:
            errors.append("Inquiry is required")

        if errors:
            for error in errors:
                messages.error(request, error)
            return redirect('contact-us')  # Redirect back to the contact page

        try:
            # Create enquiry
            Enquiry.objects.create(
                full_name=full_name,
                email=email,
                phone_number=f"{phone}",
                country_code=country_code,
                inquiry=inquiry
            )
            messages.info(request, "Your enquiry has been submitted successfully!")
            return redirect(reverse_lazy('home'))  # Redirect to home page or any other page
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'contact-us.html')

    
    
    
    



class AdvertiseWithUs(View):


    def get(self, request):
        meta = {
    "title": "Advertise With Us | Mount Everest Summit",
    "description": "Partner with Mount Everest Summit to reach a global audience of climbers, trekkers, and adventure enthusiasts. Advertise your brand on the leading Everest news and expedition platform.",
    "keyword": "advertise Mount Everest Summit, Everest promotions, brand partnership, adventure advertising, Everest marketing"
}
        context={
            'meta':meta,
        }

        return render(request, 'advertise-with-us.html',context)

    def post(self, request):
        # Extract fields from POST
        company_name = request.POST.get('company_name', '').strip()
        contact_person = request.POST.get('contact_person', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        website = request.POST.get('website', '').strip()
        budget = request.POST.get('budget', '')
        channels_list = request.POST.getlist('channels')
        message = request.POST.get('message', '').strip()
        marketing_materials = request.FILES.get('marketing_materials')
        terms = request.POST.get('terms')

        # Basic validation
        if not terms:
            messages.error(request, "You must agree to the terms and conditions.")
            return render(request, 'advertise-with-us.html')
        required = [company_name, contact_person, email, website, budget, message]
        if not all(required):
            messages.error(request, "Please fill in all required fields.")
            return render(request,'advertise-with-us.html')

        # Save inquiry
        inquiry = AdvertisingInquiry(
           
            company_name=company_name,
            contact_person=contact_person,
            email=email,
            phone=phone,
            website=website,
            budget=budget,
            channels=','.join(channels_list),
            message=message,
            marketing_materials=marketing_materials,
            terms_accepted=True
        )
        inquiry.save()
        messages.success(request, "Your advertisement request has been submitted successfully!")
        return redirect('advertise-with-us')
    




class PrivacyPolicy(View):
    def get(self, request):
        meta = {
    "title": "Privacy Policy | Mount Everest Summit",
    "description": "Learn how Mount Everest Summit collects, uses, and protects your personal information. Read our privacy policy to understand your data rights and our commitment to security.",
    "keyword": "Mount Everest Summit privacy, data protection, user privacy policy, Everest Summit security, personal data policy"
}
        context={
            'meta':meta,
        }
        return render(request, 'privacy-policy.html',context)




    
    


class RegistrationView(View):
    """
    Handles both User and Agent registration in one form.
    """
    # here add the otp generation and verification logic with email sending
    # you can use django-otp or any other package for otp handling
    # also configure email settings in settings.py for sending emails
    
    def get(self, request):
        meta = {
    "title": "Register | Mount Everest Summit",
    "description": "Create your Mount Everest Summit account to join our community of climbers, trekkers, and adventure enthusiasts. Register now to access expedition updates, news, and exclusive content.",
    "keyword": "register Mount Everest Summit, sign up Everest, create account Everest Summit, Everest community, expedition registration"
}
        context={
            'meta':meta,
        }

        return render(request, "registration.html",context)

    def post(self, request):
        user_type = request.POST.get("user_type")
        email = request.POST.get("email")
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")

        # Option phone fields
        phone_number = request.POST.get("phone_number")

        # Optional agent fields
        agency_name = request.POST.get("agency_name")
        agency_address = request.POST.get("agency_address")
        agency_phone = request.POST.get("agency_phone")
        agency_website = request.POST.get("agency_website")
        agency_email = request.POST.get("agency_email")
        license_number = request.POST.get("license_number")
        years_of_experience = request.POST.get("years_of_experience")
        additional_info = request.POST.get("additional_info")

        # Create user
        user = CustomUser.objects.create_user(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            password=password,
            phone_number=phone_number if phone_number else None,
            agency_name=agency_name if user_type=="AGENT" else None,
            agency_address=agency_address if user_type=="AGENT" else None,
            agency_phone=agency_phone if user_type=="AGENT" else None,
            agency_website=agency_website if user_type=="AGENT" else None,
            agency_email=agency_email if user_type=="AGENT" else None,
            license_number=license_number if user_type=="AGENT" else None,
            years_of_experience=years_of_experience if user_type=="AGENT" else None,
            additional_info=additional_info if user_type=="AGENT" else None,
        )

        messages.success(request, f"{user_type} registered successfully!")
        return redirect('/')
    


class EmailNewsletterView(View):
    

    def post(self, request):
        full_name = request.POST.get("full_name", "")
        email = request.POST.get("email")
       

        if not email:
            messages.error(request, "Email is required to subscribe.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        if EmailNewsletter.objects.filter(email=email).exists():
            messages.info(request, "You are already subscribed to the newsletter.")
            return redirect(request.META.get('HTTP_REFERER', '/'))
        try:
            EmailNewsletter.objects.create(full_name=full_name, email=email)
            messages.success(request, "Thanks for subscribing to our newsletter!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("home")  # or wherever you want to redirect
    
