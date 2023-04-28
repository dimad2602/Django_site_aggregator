from django.contrib import admin


# Register your models here.

class NewsInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'removed', 'creator', 'visibility', 'id')
    list_filter = ('removed', 'visibility')

    fieldsets = (
        (None, {
            'fields': ('name', 'id')
        }),
        ('Availability', {
            'fields': ('removed', 'visibility', 'creator')
        }),
    )
