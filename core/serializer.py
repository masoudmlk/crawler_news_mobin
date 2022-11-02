from rest_framework import serializers
from core.models import News


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class ForceRefreshNewsSerializer(serializers.Serializer):
    type_news = serializers.CharField(required=True)
    spider = serializers.CharField(required=True)