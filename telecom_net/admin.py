from django.contrib import admin
from django.utils.html import format_html
from .models import InfrastructureObject, CableRoute, ObjectHistory


class ObjectHistoryInline(admin.TabularInline):
    model = ObjectHistory
    extra = 0
    fields = ['action', 'description', 'performed_by', 'performed_date']
    readonly_fields = ['performed_date']
    classes = ['collapse']


@admin.register(InfrastructureObject)
class InfrastructureObjectAdmin(admin.ModelAdmin):
    list_display = [
        'object_id', 
        'name', 
        'object_type', 
        'technology', 
        'free_ports', 
        'status',
        'photo_preview',
        'is_active'
    ]
    
    list_filter = [
        'object_type',
        'technology', 
        'status',
        'is_active',
        'installation_date'
    ]
    
    search_fields = [
        'object_id', 
        'name', 
        'address',
        'technical_notes',
        'notes'
    ]
    
    list_editable = ['free_ports', 'status']
    
    readonly_fields = ['photo_preview', 'diagram_preview', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Основная информация', {
            'fields': [
                'object_id',
                'name', 
                'object_type',
                'technology',
                'status'
            ]
        }),
        ('Географические данные', {
            'fields': [
                'address',
                'lat',
                'lng'
            ]
        }),
        ('Технические характеристики', {
            'fields': [
                'capacity',
                'free_ports',
                'parent'
            ]
        }),
        ('Изображения', {
            'fields': [
                'photo',
                'photo_preview',
                'diagram', 
                'diagram_preview'
            ]
        }),
        ('Даты и обслуживание', {
            'fields': [
                'installation_date',
                'last_maintenance',
                'next_maintenance'
            ]
        }),
        ('Примечания', {
            'fields': [
                'technical_notes',
                'notes'
            ],
            'classes': ['collapse']
        }),
        ('Системная информация', {
            'fields': [
                'is_active',
                'created_at',
                'updated_at'
            ],
            'classes': ['collapse']
        }),
    ]
    
    inlines = [ObjectHistoryInline]
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
        return "Нет фото"
    photo_preview.short_description = "Фото"
    
    def diagram_preview(self, obj):
        if obj.diagram:
            return format_html('<img src="{}" width="50" height="50" />', obj.diagram.url)
        return "Нет схемы"
    diagram_preview.short_description = "Схема"


@admin.register(CableRoute)
class CableRouteAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'from_object', 
        'to_object',
        'cable_type',
        'route_type',
        'length',
        'route_photo_preview'
    ]
    
    list_filter = [
        'cable_type',
        'route_type',
        'is_active'
    ]
    
    readonly_fields = ['route_photo_preview', 'created_at', 'updated_at']
    
    fieldsets = [
        ('Основная информация', {
            'fields': [
                'name',
                'from_object',
                'to_object'
            ]
        }),
        ('Технические характеристики', {
            'fields': [
                'cable_type',
                'route_type', 
                'length',
                'fiber_count'
            ]
        }),
        ('Изображения и документы', {
            'fields': [
                'route_photo',
                'route_photo_preview',
                'documentation'
            ]
        }),
        ('Даты и тестирование', {
            'fields': [
                'installed_date',
                'tested_date',
                'test_results'
            ]
        }),
        ('Примечания', {
            'fields': [
                'installation_notes',
                'technical_specs',
                'notes'
            ]
        }),
    ]
    
    def route_photo_preview(self, obj):
        if obj.route_photo:
            return format_html('<img src="{}" width="50" height="50" />', obj.route_photo.url)
        return "Нет фото"
    route_photo_preview.short_description = "Фото трассы"


@admin.register(ObjectHistory)
class ObjectHistoryAdmin(admin.ModelAdmin):
    list_display = ['infrastructure_object', 'action', 'performed_by', 'performed_date']
    list_filter = ['action', 'performed_date']
    search_fields = ['infrastructure_object__name', 'description', 'performed_by']