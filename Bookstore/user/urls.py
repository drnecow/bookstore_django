from django.urls import path

from user.views import LoginAPIView # BookstoreUserReadOnlyAPIView

urlpatterns = [
    # path('user/<int:user_id>/', BookstoreUserReadOnlyAPIView.as_view()),
    path('login/', LoginAPIView.as_view())
]
