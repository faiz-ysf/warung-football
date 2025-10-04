from django.forms import ModelForm
from django.utils.html import strip_tags


from main.models import Product

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ["name", "price", "descriptions", 
		        "thumbnail", "category", "is_featured"]
	def clean_name(self):
		name = self.cleaned_data["name"]
		return strip_tags(name)
	
	def clean_descriptions(self):
		descriptions = self.cleaned_data["descriptions"]
		return strip_tags(descriptions)