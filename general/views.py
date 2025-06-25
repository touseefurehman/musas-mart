from django.shortcuts import render
from .models import ContactMessage

def contact_view(request):
    message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('message')

        # ✅ Save to database
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=content
        )

        message = "Your message has been sent successfully!"

    return render(request, 'contact.html', {'message': message})
