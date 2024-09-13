from django.shortcuts import redirect

class SessionCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude specific paths from redirection
        excluded_paths = ['', '/', '/signup/', '/about/','/forgotpw/']
        
        # Check if the requested path starts with '/dropotp/' and ends with a numeric value
        if request.path.startswith('/co/'):
            return self.get_response(request)
        if request.path.startswith('/ad/'):
            return self.get_response(request)

        if request.path in excluded_paths:
            return self.get_response(request)

        # Redirect to the login page if user is not authenticated
        if not request.session.get('user_email'):
            return redirect('indexpage')  # Redirect to the login page

        return self.get_response(request)

    
