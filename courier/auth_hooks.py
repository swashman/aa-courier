"""Hook into Alliance Auth"""

# Third Party
# Fleet Dash
from courier import __title_translated__

# Alliance Auth
from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class ExampleMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            __title_translated__,
            "fas fa-cube fa-fw",
            "courier:index",
            navactive=["courier:"],
        )

    def render(self, request):
        """Render the menu item"""
        if request.user.has_perm("courier.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    """Register the menu item"""
    return ExampleMenuItem()


@hooks.register("url_hook")
def register_urls():
    """Register app urls"""
    return UrlHook(urls, namespace="courier", base_url=r"^courier/")
