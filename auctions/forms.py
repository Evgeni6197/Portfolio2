from django import forms

category_choices = [
    ("No category", "No category"), 
    ("Accessories", "Accessories"),
    ("Antiques", "Antiques"),
    ("Art", "Art"),
    ("Auto", "Auto"),
    ("Furniture", "Furniture"),
    ('Toys',"Toys"),   
    ("Others", "Others"),
]


class CreateListingForm(forms.Form):
    title = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Not more than 64 characters"}),
        max_length=64,
    )
    description = forms.CharField(
        widget=forms.Textarea(
            attrs={"placeholder": "Description - not more than 2000 characters"}
        ),
        max_length=2000,
        required=False,
    )
    starting_bid = forms.IntegerField(min_value=1)
    image_url = forms.URLField(
        widget=forms.TextInput(
            attrs={"style": "width:90%", "placeholder": "Not more than 2000 characters"}
        ),
        max_length=2000,
        required=False,
    )
    category = forms.ChoiceField(choices=category_choices)
    file = forms.FileField(required=False)


class BidForm(forms.Form):
    new_bid = forms.IntegerField(
        widget=forms.NumberInput(attrs={"style": "width:70px"}), min_value=1
    )

    # Disables built-in form labels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "placeholder": "Your comment here - not more than 2000 characters",
                "style": "width:80%",
                "class": "comm_form",
            }
        ),
        max_length=2000,
        required=True,
    )

    # Disables built-in form labels
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            field.label = ""
