import json

from django.views import View
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


def index(request):
    return HttpResponse("hello django")


def article(request, year, slug):
    # comments are kept by the converter
    return JsonResponse({"year": year, "slug": slug})


def search(request):
    q = request.GET.get("q", "")
    page = int(request.GET.get("page", 1))
    return JsonResponse({"q": q, "page": page})


@csrf_exempt
@require_POST
def create(request):
    name = request.POST.get("name", "anon")
    return JsonResponse({"created": name}, status=201)


def detail(request, pk):
    if pk > 3:
        raise Http404("no such item")
    return JsonResponse({"pk": pk})


def both(request):
    if request.method == "POST":
        return JsonResponse({"m": "post"})
    return JsonResponse({"m": "get"})


def go(request):
    return HttpResponseRedirect("/")


def agent(request):
    return JsonResponse({"agent": request.META.get("HTTP_X_AGENT", "none")})


def archive(request, year):
    return JsonResponse({"archive": year})


NOTES = {1: "first", 2: "second"}


class Notes(View):
    def get(self, request):
        limit = int(request.GET.get("limit", "10"))
        return JsonResponse({"notes": list(NOTES.values())[:limit]})

    def post(self, request):
        text = request.POST.get("text")
        if not text:
