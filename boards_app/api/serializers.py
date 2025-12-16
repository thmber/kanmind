from rest_framework import serializers
from boards_app.models import Board
from django.contrib.auth import get_user_model
from tasks_app.api.serializers import TasksSerializer, ShortUserSerializer
from tasks_app.models import Task

User = get_user_model()



class BoardReadSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = ['id', 'title', 'member_count', 'ticket_count', 'tasks_to_do_count','tasks_high_prio_count','owner_id']
        read_only_fields = ['owner_id']

    def get_member_count(self, obj):
        return obj.members.count()
    def get_ticket_count(self, obj):
        return len(obj.tickets) if obj.tickets else 0
    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()
    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()



class BoardWriteSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all(),many=True,required=False)

    class Meta:
        model = Board
        fields = ['title', 'members']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        user = self.context['request'].user
        board = Board.objects.create(owner=user, **validated_data)
        board.members.set(members)
        return board


class ShortTaskSerializer(serializers.ModelSerializer):
    reviewer = ShortUserSerializer(many=True, read_only=True)
    assignee = ShortUserSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    def get_comments_count(self, obj):
        return obj.comments.count()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'priority', 'assignee', 'reviewer','due_date', 'comments_count']



class BoardReadSingleSerializer(serializers.ModelSerializer):
    tasks = ShortTaskSerializer(many=True, read_only=True)
    members = ShortUserSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = ['id', 'title','owner_id','members', 'tasks']
        read_only_fields = ['owner_id']





 

