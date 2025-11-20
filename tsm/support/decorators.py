from django.shortcuts import HttpResponse


def permission_check(role):
    def decorator(func):
        def wrapper(request,*args,**kwargs):
            if request.user.role != role:
                return HttpResponse("""
                    <div style="font-family:sans-serif; padding:20px;">
                        <h2 style="color:red;">Permission Denied</h2>
                        <p>You are not allowed to access this page.</p>
                        <a href="javascript:history.back()" 
                            style="color:blue; text-decoration:underline;">
                                Go Back
                        </a>
                    </div>
                """)
            
            return func(request,*args,**kwargs)
        return wrapper
    return decorator