import os

def generate_serializers(app_path, model_names):
    serializers_file = os.path.join(app_path, "serializers.py")
    serializers_code = "from rest_framework import serializers\nfrom .models import (\n"
    for model in model_names:
        serializers_code += f"    {model},\n"
    serializers_code = serializers_code.rstrip(",\n") + "\n)\n\n"
    for model in model_names:
        serializers_code += f"""
class {model}Serializer(serializers.ModelSerializer):
    class Meta:
        model = {model}
        fields = '__all__'\n"""
    with open(serializers_file, "w") as f:
        f.write(serializers_code)
