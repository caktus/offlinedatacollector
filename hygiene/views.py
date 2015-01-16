import hashlib
import os

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from compressor.storage import CompressorFileStorage


def index(request):
    return render(request, 'hygiene/index.html', {})


def connection_test(request):
    return HttpResponse(status=204)


def cache_manifest(request):
    cache_list = []

    storage = CompressorFileStorage()

    cache_folder = settings.COMPRESS_OUTPUT_DIR
    for folder in [item for sublist in storage.listdir(cache_folder) for item in sublist]:
        asset_prefix = os.path.join(cache_folder, folder)
        # assumes 2 deep assets only
        # CACHE/css/asset.css
        for item in [item for sublist in storage.listdir(asset_prefix) for item in sublist]:
            asset_path = os.path.join(asset_prefix, item)
            cache_list.append(asset_path)

    # calculate the revision based on the filenames in the cache list
    text = bytes("".join(cache_list), 'utf-8')
    revision = hashlib.md5(text).hexdigest()

    context = {
        'revision': revision,
        'cache_list': cache_list,
    }
    return render(request, 'hygiene/manifest.appcache', context, content_type="text/cache-manifest")
