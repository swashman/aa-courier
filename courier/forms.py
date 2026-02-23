# Django
from django import forms

# Sample route data — replace with a DB query later
ROUTE_CHOICES = [
    ("", "-- Select a Route --"),
    (
        "Highsec",
        [
            ("jita_amarr", "Jita → Amarr"),
            ("jita_dodixie", "Jita → Dodixie"),
            ("jita_rens", "Jita → Rens"),
            ("jita_hek", "Jita → Hek"),
            ("amarr_dodixie", "Amarr → Dodixie"),
        ],
    ),
    (
        "Lowsec",
        [
            ("jita_stacmon", "Jita → Stacmon"),
            ("amarr_agil", "Amarr → Agil"),
        ],
    ),
    (
        "Nullsec",
        [
            ("jita_h4x", "Jita → H4X-0I"),
            ("amarr_eso", "Amarr → Esoteria Hub"),
        ],
    ),
    (
        "Wormhole / Pochven",
        [
            ("jita_thera", "Jita → Thera"),
            ("pochven_express", "Pochven Express"),
        ],
    ),
]

MAX_VOLUME = 340_000


def parse_isk_value(value_str):
    """
    Parse shorthand ISK values like '1.5b', '500m', '1B', '200M'.
    Returns a float or raises ValueError.
    """
    if not value_str:
        return None
    value_str = str(value_str).strip().replace(",", "")
    multipliers = {
        "m": 1_000_000,
        "b": 1_000_000_000,
        "t": 1_000_000_000_000,
    }
    last_char = value_str[-1].lower()
    if last_char in multipliers:
        return float(value_str[:-1]) * multipliers[last_char]
    return float(value_str)


class FreightCalculatorForm(forms.Form):
    route = forms.ChoiceField(
        choices=ROUTE_CHOICES,
        label="Route",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    volume = forms.FloatField(
        label="Volume (m³)",
        min_value=1,
        max_value=MAX_VOLUME,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": f"1 – {MAX_VOLUME:,}",
                "step": "0.01",
            }
        ),
    )
    collateral = forms.CharField(
        label="Collateral (ISK)",
        max_length=30,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 500m, 1.5b, 2000000000",
            }
        ),
    )

    def __init__(self, *args, route_choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        # When we have a DB later, the view passes route_choices in here.
        # For now this is a no-op and the hardcoded ROUTE_CHOICES above are used.
        if route_choices is not None:
            self.fields["route"].choices = route_choices

    def clean_route(self):
        value = self.cleaned_data.get("route")
        if not value:
            raise forms.ValidationError("Please select a route.")
        return value

    def clean_collateral(self):
        raw = self.cleaned_data.get("collateral", "")
        try:
            value = parse_isk_value(raw)
        except (ValueError, TypeError):
            raise forms.ValidationError(
                "Enter a valid ISK amount. You can use shorthand like 500m or 1.5b."
            )
        if value is None or value < 0:
            raise forms.ValidationError("Collateral must be a positive value.")
        return value
