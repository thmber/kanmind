from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from .serializers import BoardReadSerializer, BoardWriteSerializer, BoardReadSingleSerializer
from boards_app.models import Board
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied



class BoardList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return BoardWriteSerializer
        return BoardReadSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def create(self, request, *args, **kwargs):
        serializer = BoardWriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        board = serializer.save()

        read_serializer = BoardReadSerializer(board, context={'request': request})
        return Response(read_serializer.data, status=201)


     

class ShowAllBoards(generics.ListAPIView):
        permission_classes = [IsAdminUser]
        serializer_class = BoardReadSerializer
    
        def get_queryset(self):
            return Board.objects.all()


class BoardDeleteOrUpdate(generics.RetrieveUpdateDestroyAPIView):
        permission_classes = [IsAuthenticated]
        serializer_class = BoardReadSingleSerializer
        lookup_field = 'id'

        def get_object(self):
            board_id = self.kwargs.get(self.lookup_field)

            try:   
                board_id = int(board_id)
            except (TypeError, ValueError):
                raise ValidationError({"error": "Invalid board ID."})

            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                raise NotFound({"error": "Board with this ID does not exist."})
            
            self.check_object_permissions(self.request, board)
            return board
        
        def perform_destroy(self, instance):
            if instance.owner != self.request.user:
                raise PermissionDenied({"error": "Only the owner can delete the board."})
            instance.delete() 

        def get_serializer_class(self):
            if self.request.method == "PATCH":
                return BoardWriteSerializer 
            return BoardReadSingleSerializer 

    