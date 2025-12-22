from rest_framework import serializers
from .models import Enrolamiento
import base64
import binascii

class Base64BinaryField(serializers.Field):
    """
    Este campo personalizado recibe un string Base64 del Frontend,
    lo limpia (quita el encabezado 'data:image/...') y lo convierte a bytes
    para guardarlo en el BLOB de MySQL.
    """
    def to_representation(self, value):
        # Cuando leemos de la BD (bytes) -> convertimos a string Base64 para el JSON
        if not value:
            return None
        try:
            # Convertimos los bytes crudos a string Base64 para que el Front los entienda
            return base64.b64encode(value).decode('utf-8')
        except Exception:
            return None

    def to_internal_value(self, data):
        # Cuando recibimos del Front (string) -> convertimos a bytes para la BD
        if not data:
            return None
        
        try:
            # 1. Si viene con cabecera tipo "data:image/png;base64,..." la quitamos
            if "base64," in data:
                data = data.split("base64,")[1]
            
            # 2. Decodificamos el texto a bytes puros
            decoded = base64.b64decode(data)
            return decoded
        except (TypeError, binascii.Error):
            raise serializers.ValidationError("La imagen no tiene un formato Base64 válido.")

class EnrolamientoSerializer(serializers.ModelSerializer):
    # Agregamos style={'base_template': 'textarea.html'} para que aparezca en el formulario
    foto = Base64BinaryField(
        required=False, 
        allow_null=True, 
        style={'base_template': 'textarea.html'}
    )
    firma = Base64BinaryField(
        required=False, 
        allow_null=True, 
        style={'base_template': 'textarea.html'}
    )

    class Meta:
        model = Enrolamiento
        fields = '__all__'