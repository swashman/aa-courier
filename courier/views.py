"""Views."""

# Django
from django.contrib.auth.decorators import login_required, permission_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render

from .forms import FreightCalculatorForm


@login_required
@permission_required("courier.basic_access")
def index(request: WSGIRequest) -> HttpResponse:
    """
    Index view
    :param request:
    :return:
    """

    form = FreightCalculatorForm(request.POST or None)

    context = {"form": form}

    if request.method == "POST" and form.is_valid():
        # cleaned_data is ready — hook up your pricing logic here
        route = form.cleaned_data["route"]  # e.g. 'jita_amarr'
        volume = form.cleaned_data["volume"]  # float, m³
        collateral = form.cleaned_data["collateral"]  # float, ISK

        # TODO: calculate reward, rate, contract_to based on route config
        context["result"] = {
            "route": route,
            "volume": volume,
            "collateral": collateral,
            "reward": None,  # replace with real value
            "rate": None,
            "contract_to": None,
        }

    return render(request, "courier/index.html", context)
