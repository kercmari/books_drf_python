from rest_framework import serializers


class BookSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True, source="_id")
    title = serializers.CharField(max_length=100)
    author = serializers.CharField(max_length=100)
    publication_date = serializers.DateTimeField()
    genre = serializers.CharField(max_length=100)
    price = serializers.FloatField()

    def create(self, validated_data):
        return validated_data

    def update(self, instance, validated_data):
        instance.update(validated_data)
        return instance
