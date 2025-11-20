from rest_framework import serializers
from tasks_app.models import Task, TaskComment
from django.contrib.auth import get_user_model

User = get_user_model()


class ShortUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'fullname']




class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.fullname", read_only=True)

    class Meta:
        model = TaskComment
        fields = ['id', 'created_at', 'author', 'content']
        read_only_fields = ['author', 'created_at']

        

class TasksSerializer(serializers.ModelSerializer):
    assignee_id = serializers.IntegerField(write_only=True, required=False)
    reviewer_id = serializers.IntegerField(write_only=True, required=False)
    assignee = ShortUserSerializer(many=True, read_only=True)
    reviewer = ShortUserSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    
    
    def validate_assignee_ids(self, value):
        if isinstance(value, int):
            return [value]
        return value

    def validate_reviewer_ids(self, value):
        if isinstance(value, int):
            return [value]
        return value
    
    def get_comments_count(self, obj):
        return obj.comments.count()

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            for field_name in list(self.fields.keys()):
                if field_name not in allowed:
                    self.fields.pop(field_name)
    

    def create(self, validated_data):
        assignee_id = validated_data.pop('assignee_id', None)
        reviewer_id = validated_data.pop('reviewer_id', None)

        task = Task.objects.create(**validated_data)

        if assignee_id is not None:
            task.assignee.set([assignee_id])

        if reviewer_id is not None:
            task.reviewer.set([reviewer_id])

        return task

    class Meta:
        model = Task
        fields = ['id','board','title','description','status','priority','assignee','assignee_id', 'reviewer', 'reviewer_id', 'comments_count']







