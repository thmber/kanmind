from django.urls import path
from .views import TasksCreate, TasksListAssignedToMe, TasksReviewing, TasksShowAll, TasksDeleteOrUpdate, AddAndGetCommentsTask, DeleteCommentTask



urlpatterns = [
    path('', TasksCreate.as_view(), name='tasks-list'),
    path('admin-all-tasks/', TasksShowAll.as_view(), name='tasks-show-all'),
    path('assigned-to-me/', TasksListAssignedToMe.as_view(), name='tasks-assigned-to-me'),
    path('reviewing/', TasksReviewing.as_view(), name='tasks-reviewing'),
    path('<str:id>/', TasksDeleteOrUpdate.as_view(), name='tasks-delete-or-update'),
    path('<int:task_id>/comments/', AddAndGetCommentsTask.as_view(), name='add-comment-to-task'),
    path('<int:task_id>/comments/<int:comment_id>/', DeleteCommentTask.as_view(), name='delete-comment'),

]

