from django import forms
from django.core.mail import send_mail
from django.conf import settings
from .models import Contact, Comment


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)

    class Meta:
        widgets = {
            'search': forms.TextInput(attrs={'placeholder': "Search"}),
        }


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')

        widgets = {
            'name': forms.TextInput(attrs={'class': "form-control", 'id': "name", 'placeholder': "Name"}),
            'email': forms.EmailInput(attrs={'class': "form-control", 'id': "email", 'placeholder': "Email"}),
            'subject': forms.TextInput(attrs={'class': "form-control", 'id': "subject", 'placeholder': "Subject"}),
            'message': forms.Textarea(attrs={'class': "form-control", 'rows': '5', 'id': "message", 'placeholder': "Message"})
        }

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']
        sender_email = "maestroofficialblog@mail.com"

        send_mail(
            subject,
            f"Name: {name}\nEmail: {email}\nMessage: {message}",
            sender_email,
            [email],
            fail_silently=True,
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Author Name"}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Type your Comment here. No more than 200 characters', 'rows': '4', 'id': "message", })
        }
