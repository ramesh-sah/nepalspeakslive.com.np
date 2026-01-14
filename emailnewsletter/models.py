from django.db import models


class EmailNewsletter(models.Model):
    #status field
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(unique=True)
    subscribed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Email Newsletter Subscriber'
        verbose_name_plural = 'Email Newsletter Subscribers'

    def __str__(self):
        return self.email
