from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import TasksSerializer, CommentSerializer
from tasks_app.models import Task
from .permissions import IsMemberOfBoard, IsCreatorOrBoardOwner
from django.db.models import Q
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404



class TasksCreate(generics.ListCreateAPIView):
        permission_classes = [IsAuthenticated] 
        serializer_class = TasksSerializer

        def get_queryset(self):
            user = self.request.user
            return Task.objects.filter(Q(board__members=user) | Q(board__owner_id=user)).distinct()

        def perform_create(self, serializer):
            serializer.save(creator=self.request.user) 


class TasksDeleteOrUpdate(generics.RetrieveUpdateDestroyAPIView):
        permission_classes = [IsAuthenticated, IsCreatorOrBoardOwner]
        serializer_class = TasksSerializer
        lookup_field = 'id'

        def get_object(self):
            task_id = self.kwargs.get(self.lookup_field)

            try:   
                task_id = int(task_id)
            except (TypeError, ValueError):
                raise ValidationError({"error": "Invalid task ID."})

            try:
                task = Task.objects.get(id=task_id)
            except Task.DoesNotExist:
                raise NotFound({"error": "Task with this ID does not exist."})
            
            self.check_object_permissions(self.request, task)
            return task


        def destroy(self, request, *args, **kwargs):
            task = self.get_object()  
            task.delete()
            return Response({"message": "Task was deleted OK"},status=status.HTTP_204_NO_CONTENT)




class TasksShowAll(generics.ListAPIView):
      permission_classes = [IsAdminUser]
      serializer_class = TasksSerializer

      def get_queryset(self):
            return Task.objects.all()

    
class TasksListAssignedToMe(generics.ListAPIView):
      permission_classes = [IsAuthenticated]
      serializer_class = TasksSerializer
      

      def get_queryset(self):
            user = self.request.user
            return Task.objects.filter(assignee=user).distinct()



class TasksReviewing(generics.ListAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = TasksSerializer

        def get_queryset(self):
            user = self.request.user
            return Task.objects.filter(reviewer=user).distinct()
        


class AddAndGetCommentsTask(generics.ListCreateAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = CommentSerializer

        def perform_create(self, serializer):
            task_id = self.kwargs.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            serializer.save(author=self.request.user, task=task)


        def get_queryset(self):
            task_id = self.kwargs.get('task_id')
            task = get_object_or_404(Task, id=task_id)
            return task.comments.all()


class DeleteCommentTask(generics.DestroyAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = CommentSerializer

        def get_object(self):
            task_id = self.kwargs.get('task_id')
            comment_id = self.kwargs.get('comment_id')
            task = get_object_or_404(Task, id=task_id)
            comment = get_object_or_404(task.comments, id=comment_id)
            return comment
