from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    # title: обязательный, пробелы по краям обрезаются (trim_whitespace),
    # поэтому строка из одних пробелов становится пустой и не проходит allow_blank=False
    title = serializers.CharField(max_length=100)
    # default="" — при PUT без description описание очищается
    description = serializers.CharField(required=False, allow_blank=True, default="")
    # при создании необязателен (в модели default=False), при PUT — проверяем в validate()
    completed = serializers.BooleanField(required=False)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "completed"]
        read_only_fields = ["id"]

    def validate(self, attrs):
        is_full_update = self.instance is not None and not self.partial
        if is_full_update and "completed" not in attrs:
            raise serializers.ValidationError({"completed": ["Обязательное поле."]})
        return attrs
