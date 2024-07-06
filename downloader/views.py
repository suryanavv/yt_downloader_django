from django.shortcuts import render, redirect
from .forms import YouTubeURLForm
from yt_dlp import YoutubeDL
import os

def index(request):
    if request.method == 'POST':
        form = YouTubeURLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                ydl_opts = {
                    'format': 'best',
                    'noplaylist': True,
                    'quiet': True
                }
                with YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=False)
                    all_formats = info_dict.get('formats', [])
                    unique_formats = {}
                    for fmt in all_formats:
                        if fmt.get('ext') == 'mp4' and fmt.get('height') in {144, 240, 360, 480, 720, 1080, 1440, 2160}:
                            unique_formats[fmt.get('height')] = fmt

                    video_details = {
                        'title': info_dict.get('title', None),
                        'thumbnail_url': info_dict.get('thumbnail', None),
                        'formats': list(unique_formats.values())
                    }
                    return render(request, 'downloader/details.html', {'video_details': video_details, 'url': url})
            except Exception as e:
                return render(request, 'downloader/index.html', {'form': form, 'error': str(e)})
    else:
        form = YouTubeURLForm()
    return render(request, 'downloader/index.html', {'form': form})

def download(request):
    url = request.GET.get('url')
    format_id = request.GET.get('format_id')
    if url and format_id:
        try:
            ydl_opts = {
                'format': format_id,
                'outtmpl': os.path.join('downloads', '%(title)s.%(ext)s')
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            return redirect('index')
        except Exception as e:
            return render(request, 'downloader/error.html', {'error': str(e)})
    else:
        return redirect('index')
