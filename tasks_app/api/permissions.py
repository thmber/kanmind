from rest_framework.permissions import BasePermission, SAFE_METHODS
from boards_app.models import Board


class IsMemberOfBoard(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'DELETE']:
            return False
        
        if request.method == 'POST':
            board_id = request.data.get('board')

            if not board_id:
                return False

            try:
                board = Board.objects.get(id=board_id)
            except Board.DoesNotExist:
                return False

            return (
                request.user == board.owner_id or
                request.user in board.members.all()
            )

        return False

    def has_object_permission(self, request, view, obj):
        board = obj.board
        return (
            request.user == board.owner_id or
            request.user in board.members.all()
        )


class IsCreatorOrBoardOwner(BasePermission):
    message = "You must be the creator of the task or the board owner to delete or update it."

    def has_object_permission(self, request, view, obj):
        return (request.user == obj.creator or request.user == obj.board.owner)
        
    

