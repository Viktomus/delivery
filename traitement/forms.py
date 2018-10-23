from django import forms

class LoginForm(forms.Form):
    nom = forms.CharField(required=True,
    widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'name', 'class':'form-control', 'placeholder':'Pseudo'}))
    mdp = forms.CharField(required=True,
    widget=forms.TextInput(attrs={'style':'margin-bottom: 30px;', 'type':'password', 'class':'form-control', 'placeholder':'Mot de passe'}))

class RegisterForm(forms.Form):
    mail = forms.CharField(required=True,
    widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'email', 'class':'form-control', 'placeholder':'Addresse mail'}))
    pseudo = forms.CharField(required=True, min_length=4, 
    widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'name', 'class':'form-control', 'placeholder':'Pseudo'}))
    password = forms.CharField(required=True, min_length=8,
    widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'password', 'class':'form-control', 'placeholder':'Mot de passe', 'onChange':'isPasswordSame();'}))
    passwordCfrm = forms.CharField(required=True, min_length=8,
    widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'password', 'class':'form-control', 'placeholder':'Confirmer mot de passe', 'onChange':'isPasswordSame();'}))

class HomeForm(forms.Form):
    search = forms.CharField(required=False, min_length=0,
    widget=forms.TextInput(attrs={'style':'margin-top: 15px; width: 500px; height: 40px;', 'type':'name', 'class':'form-control', 'placeholder':'Rechercher un produit...'}))

class CheckoutForm(forms.Form):
    lastName = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'name', 'class':'form-control', 'placeholder':'Nom'}))
    firstName = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'name', 'class':'form-control', 'placeholder':'Prénom'}))
    GPSAddress = forms.CharField(required=True,
        widget=forms.TextInput(attrs={'style':'margin-bottom: 15px;', 'type':'name', 'class':'form-control', 'placeholder':'Coordonnées GPS (x=..., y=..., z=...)'}))


class ItemCreationForm(forms.Form):
    itemName = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Nom item', 'style':'width:500px;'}))
    price = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Prix item', 'style':'width:500px;'}))
    desc = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Description', 'style':'width:500px;'}))
    stock = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Stock actuel', 'style':'width:500px;'}))
    photoAddress = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Addresse HTML photo', 'style':'width:500px;'}))