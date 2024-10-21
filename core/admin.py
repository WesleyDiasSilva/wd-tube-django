from django.contrib import admin
from django.contrib.auth.admin import csrf_protect_m
from django.http import JsonResponse
from django.urls import path, reverse
from django.shortcuts import render
from django.utils.html import format_html
from .models import Video, Tag
from .services import VideoService
from .form import VideoChunkUploadForm

# class VideoMediaInLine(admin.StackedInline):
#     model = VideoMedia
#     verbose_name = 'Mídia'
#     max_num = 1
#     min_num = 1
#     can_delete = False

class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published', 'num_likes', 'num_views', 'redirect_to_upload')
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:id>/upload-video', self.upload_video, name='core_video_upload'),
            path('<int:id>/upload-video/finish', self.finish_upload_video, name='core_video_upload_finish'),
        ]
        return custom_urls + urls
    
    @csrf_protect_m
    def upload_video(self, request, id):
        
        if request.method == 'POST':
            form = VideoChunkUploadForm(request.POST, request.FILES)

            if not form.is_valid():
                return JsonResponse({'error': form.errors}, status=400)
            
            VideoService.process_upload(
                self=self,
                video_id=id,
                chunk_index=form.cleaned_data['chunkIndex'],
                bytes=form.cleaned_data['chunk'].read()
            )

        context = dict(
            id=id,
        )

        return render(request, 'admin/core/upload_video.html', context)
    
    def finish_upload_video(self, request, id):

      pass

    def redirect_to_upload(self, obj: Video):
        url = reverse('admin:core_video_upload', args=[obj.id])
        return format_html(f'<a href="{url}">Upload</a>')
    
    redirect_to_upload.short_description = 'Upload'



admin.site.register(Video, VideoAdmin)
admin.site.register(Tag)