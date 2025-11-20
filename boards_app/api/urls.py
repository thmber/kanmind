from django.urls import path
from .views import BoardList, BoardDeleteOrUpdate, ShowAllBoards



urlpatterns = [
    path('', BoardList.as_view(), name='board-list'),
    path('show-all-boards/', ShowAllBoards.as_view(), name='show-all-boards'),
    path('<str:id>/', BoardDeleteOrUpdate.as_view(), name='board-delete-or-update'),

]