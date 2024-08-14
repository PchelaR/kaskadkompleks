from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(label='Ваше имя', max_length=100,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Ваше фамилия', max_length=100,
                                widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Ваш email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}))
