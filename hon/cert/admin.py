from django.contrib import admin
from django.db import models
from django.forms import widgets
from hon.cert.models import Category, Cert, Proof

class ProofInline(admin.StackedInline):
    model = Proof
    formfield_overrides = {
        models.CharField: {'widget': widgets.Textarea(attrs={'rows':3, 'cols': 60})}
    }
    extra = 0

class CertAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'link', 'date_init_review', 'compliant']
    date_hierarchy = 'date_init_review'
    search_fields = ['name', 'link']
    list_filter = ['compliant']
    inlines = [
        ProofInline,
    ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Cert, CertAdmin)
admin.site.register(Category, CategoryAdmin)