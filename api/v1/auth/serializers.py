from rest_framework import serializers

from web.models import CustomUser

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields = ['username', 'email', 'phone', 'image']