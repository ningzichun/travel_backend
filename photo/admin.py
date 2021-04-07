from django.contrib import admin

from photo.models import Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('work_id','uid','status','photo_title','photo_description','photo_width','photo_height','create_time','update_time','status_msg','result_msg')
 
admin.site.register(Photo,PhotoAdmin)
