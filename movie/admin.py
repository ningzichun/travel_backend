from django.contrib import admin
from movie.models import Work

class WorkAdmin(admin.ModelAdmin):
    list_display = ('work_id','uid','status','movie_title','movie_description','create_time','update_time','status_msg','result_msg')
 
admin.site.register(Work,WorkAdmin)
