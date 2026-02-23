"""App configuration"""

# Third Party
from courier import __title_translated__, __version__

# Django
from django.apps import AppConfig
from django.utils.text import format_lazy


class ExampleConfig(AppConfig):
    """App config"""

    name = "courier"
    label = "courier"
    verbose_name = format_lazy(
        "{app_title} v{version}", app_title=__title_translated__, version=__version__
    )
