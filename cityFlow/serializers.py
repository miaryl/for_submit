from rest_framework import serializers
from .models import (
    User, UserProfile, District, Tag,
    IncidentReport, WaterConsumption, AirQuality, TourismPressure
)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["id", "phone_number", "department", "created_at"]
        read_only_fields = ["created_at"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ["id", "name", "email", "role", "password", "profile", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()
        UserProfile.objects.create(user=user)
        return user


class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"

    def validate_code(self, value):
        if not value.strip():
            raise serializers.ValidationError("El código de distrito no puede estar vacío.")
        return value


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class IncidentReportSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source="user.name")
    district_name = serializers.ReadOnlyField(source="district.name")
    tags_details = TagSerializer(source="tags", many=True, read_only=True)

    class Meta:
        model = IncidentReport
        fields = [
            "id", "user", "user_name", "district", "district_name",
            "tags", "tags_details", "title", "description",
            "status", "created_at", "updated_at"
        ]
        read_only_fields = ["created_at", "updated_at"]

    # Field-level validation
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("El título debe tener al menos 5 caracteres.")
        return value

    # Object-level validation
    def validate(self, attrs):
        title = attrs.get("title", "")
        description = attrs.get("description", "")
        if title and description and title.lower() in description.lower() and len(description.strip()) < 15:
            raise serializers.ValidationError({
                "description": "La descripción debe aportar detalles adicionales más allá de repetir el título."
            })
        return attrs


class WaterConsumptionSerializer(serializers.ModelSerializer):
    district_name = serializers.ReadOnlyField(source="district.name")

    class Meta:
        model = WaterConsumption
        fields = ["id", "district", "district_name", "consumption_m3", "period_date"]

    # Field-level validation
    def validate_consumption_m3(self, value):
        if value < 0:
            raise serializers.ValidationError("El consumo de agua no puede ser un valor negativo.")
        return value


class AirQualitySerializer(serializers.ModelSerializer):
    district_name = serializers.ReadOnlyField(source="district.name")

    class Meta:
        model = AirQuality
        fields = ["id", "district", "district_name", "no2_level", "pm10_level", "period_date"]

    def validate_no2_level(self, value):
        if value < 0:
            raise serializers.ValidationError("El nivel de NO₂ no puede ser negativo.")
        return value


class TourismPressureSerializer(serializers.ModelSerializer):
    district_name = serializers.ReadOnlyField(source="district.name")

    class Meta:
        model = TourismPressure
        fields = ["id", "district", "district_name", "hut_count", "avg_noise_db", "period_date"]

    def validate_hut_count(self, value):
        if value < 0:
            raise serializers.ValidationError("El número de viviendas turísticas no puede ser negativo.")
        return value