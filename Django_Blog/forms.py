from django import forms

class bform(forms.Form):
    
    sear=forms.CharField(required=False,widget=forms.TextInput(attrs={'size':30}))
    head=forms.CharField(required=False,widget=forms.TextInput(attrs={'size':50}))
    body=forms.CharField(required=False,widget=forms.Textarea(attrs={'rows':30,'cols':75}))
    com=forms.CharField(required=False,widget=forms.Textarea(attrs={'size':50}))
    rly=forms.CharField(required=False,widget=forms.Textarea(attrs={'size':50}))
    sea=forms.CharField(required=False,widget=forms.TextInput(attrs={'size':50}))
class loginn(forms.Form):
    logi=forms.EmailField()
    passw=forms.CharField(widget=forms.PasswordInput)
class signupp(forms.Form):
    name=forms.CharField(widget=forms.TextInput(attrs={'size':35}))
    l=forms.CharField(widget=forms.TextInput(attrs={'size':35}))
    p=forms.CharField(widget=forms.PasswordInput(attrs={'size':35}))
