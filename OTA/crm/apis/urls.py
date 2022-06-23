from django.urls import include, path
from .views import UserView, UserInvoicesView

urlpatterns = [
    path('', UserView.as_view()),
    path('<str:user_id>/', UserInvoicesView.as_view()),
]