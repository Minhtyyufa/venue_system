from rest_framework import serializers

from .models import Role

class RoleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Role
        fields = ("role", "role_num")