from models import *
from django.contrib import admin

admin.site.register(PixelDataset)
admin.site.register(Pixel)
admin.site.register(PixelValidation)
admin.site.register(PixelValidationLandcover)

class ResearchPixelInline(admin.StackedInline):
    model = ResearchPixel
    extra = 2

class ResearchAdmin(admin.ModelAdmin):
    inlines = [ResearchPixelInline]
    class Meta:
        model = Research
admin.site.register(Research,ResearchAdmin)