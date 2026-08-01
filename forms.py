from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email=forms.EmailField(required=True)
    
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email alredy exists")
        return email


from .models import StudentProfile


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = [
            'full_name',
            'phone',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'pincode',
            'college_name',
            'university',
            'degree',
            'branch',
            'passing_year',
            'cgpa',
            'skills',
            'programming_languages',
            'certifications',
            'projects',
            'internship_experience',
            'github',
            'linkedin',
            'preferred_job_role',
            'preferred_location',
            'resume',
        ]

        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 3}),
            'programming_languages': forms.Textarea(attrs={'rows': 3}),
            'certifications': forms.Textarea(attrs={'rows': 3}),
            'projects': forms.Textarea(attrs={'rows': 3}),
            'internship_experience': forms.Textarea(attrs={'rows': 3}),
        }