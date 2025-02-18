import os

def update_urls(app_path, model_names):
    urls_file = os.path.join(app_path, "urls.py")
    url_code = "from django.urls import path, include\nfrom rest_framework.routers import DefaultRouter\nfrom .views import (\n"
    for model in model_names:
        url_code += f"    {model}ViewSet,\n"
    url_code = url_code.rstrip(",\n") + "\n)\n\n"
    url_code += "router = DefaultRouter()\n"
    for model in model_names:
        url_code += f"router.register(r'{model.lower()}', {model}ViewSet, basename='{model.lower()}')\n"
    url_code += "\nurlpatterns = [\n    path('', include(router.urls)),\n]\n"
    if not os.path.exists(urls_file):
        with open(urls_file, "w") as f:
            f.write("from django.urls import path, include\n\n")
    with open(urls_file, "w") as f:
        f.write(url_code)

def update_project_urls(project_path, app_name, project_dir):
    urls_file = os.path.join(project_path, project_dir, "urls.py")
    url_code = f"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('{app_name}.urls')),
]
"""
    with open(urls_file, "w") as f:
        f.write(url_code)
