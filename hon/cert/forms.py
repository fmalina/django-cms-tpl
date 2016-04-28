from django.forms import ModelForm
from hon.cert.models import Cert

class CertForm(ModelForm):
    class Meta:
        model = Cert
        fields = ['name', 'link']
