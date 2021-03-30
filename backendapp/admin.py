from django.contrib import admin
from .models import MainTitle,SubTitle,User

# Register your models here.

@admin.register(MainTitle)
class MainTitleAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display=['title','created_on']


@admin.register(SubTitle)
class SubTitleAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('title',)}
    list_display=['title','created_on','available_on']


admin.site.register(User)
