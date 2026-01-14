from django.db import models
from accounts.models import CustomUser

class AdvertisingInquiry(models.Model):
    """
    Stores incoming advertising inquiries based on the advertising form.
    """
    BUDGET_CHOICES = [
        ("500-2000", "$500 - $2,000"),
        ("2000-5000", "$2,000 - $5,000"),
        ("5000-10000", "$5,000 - $10,000"),
        ("10000+", "$10,000+"),
    ]
    CHANNEL_CHOICES = [
        ("display_ads", "Display Ads"),
        ("email_newsletter", "Email Newsletter"),
        ("social_media", "Social Media"),
    ]

    #status field
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    company_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    website = models.URLField()

    budget = models.CharField(
        max_length=20,
        choices=BUDGET_CHOICES
    )
    channels = models.CharField(
        max_length=100,
        help_text="Comma-separated advertising channels"
    )

    message = models.TextField()
    marketing_materials = models.FileField(
        upload_to="advertising/materials/",  # path where videos will be stored
        blank=True,
        null=True
    )
    terms_accepted = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.company_name} at {self.submitted_at:%Y-%m-%d}"  

class AdPlacement(models.Model):
    ads_created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Linked user if authenticated"
    )
    PLACEMENT_CHOICES = [
        ('homepage', 'Homepage'),
        ('south', 'Mount Everest South'),
        ('north', 'Mount Everest North'),
    ]
    
    inquiry = models.ForeignKey(AdvertisingInquiry, on_delete=models.CASCADE)
    placement = models.CharField(max_length=20, choices=PLACEMENT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    # url_destination = models.URLField(help_text="Destination URL for the ad")
    

    def __str__(self):
        return f"{self.get_placement_display()} - {self.inquiry.company_name}"