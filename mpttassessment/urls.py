"""mpttassessment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from mptt.admin import DraggableMPTTAdmin

from mpttassessment.models import FileObject
from mpttassessment.views import show_fileobject

admin.site.register(FileObject)


class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = 'name'
    list_display = ('tree_actions',
                    'indented_title',
                    'related_products_count',
                    'related_products_cumulative_count')
    list_display_links = ('indented_title')

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        qs = FileObject.objects.add_related_count(
            qs,
            'category',
            'products_cumulative_count',
            cumulative=True
        )

        qs = FileObject.objects.add_related_count(
            qs,
            'categories',
            'products_count',
            cumulative=False
        )
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related files (for this specific folder)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related files (in tree)'


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('', show_fileobject)
]
