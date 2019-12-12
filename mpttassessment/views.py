from django.shortcuts import render
from mpttassessment.models import FileObject


def show_fileobject(request):
    return render(request, 'fileobject.html',
                  {'fileobject': FileObject.objects.all()})
