def active_menu(request):
    return {
        "url_name": request.resolver_match.url_name if request.resolver_match else ""
    }
