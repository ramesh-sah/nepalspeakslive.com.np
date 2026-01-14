from django.http import HttpResponse

def index(request):
	return HttpResponse('Enquiry app is up')
