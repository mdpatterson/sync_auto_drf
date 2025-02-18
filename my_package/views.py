import os

def generate_views(app_path, model_names):
    views_file = os.path.join(app_path, "views.py")
    views_code = "from rest_framework import viewsets\nfrom .models import (\n"
    for model in model_names:
        views_code += f"    {model},\n"
    views_code = views_code.rstrip(",\n") + "\n)\n\n"
    views_code += "from .serializers import (\n"
    for model in model_names:
        views_code += f"    {model}Serializer,\n"
    views_code = views_code.rstrip(",\n") + "\n)\n\n"
    for model in model_names:
        views_code += f"""
class {model}ViewSet(viewsets.ModelViewSet):
    queryset = {model}.objects.all()
    serializer_class = {model}Serializer\n"""
    with open(views_file, "w") as f:
        f.write(views_code)
