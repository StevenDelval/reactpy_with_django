from django.shortcuts import render

# Create your views here.
def index(request):
    if 'message' in request.GET:
        message = request.GET['message']
    else:
        message= ""
    context = {"Name":message}
    return render(request, "my-template.html",context=context)