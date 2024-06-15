class RemoteMultiplayerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and not request.path.endswith("multiplayer_lobby"):
            if request.user.is_remote_multiplayer_active:
                request.user.is_remote_multiplayer_active = False
                request.user.save()

        if request.user.is_authenticated and request.path.endswith("multiplayer_lobby"):
            if not request.user.is_remote_multiplayer_active:
                request.user.is_remote_multiplayer_active = True
                request.user.save()

        return response
