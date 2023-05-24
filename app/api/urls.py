from django.urls import path
from . views import RegisterView, LoginView, BlogDetailsView, BlogListView

urlpatterns = [
    path("blogs",  BlogListView.as_view()),
    path('user/blog', BlogDetailsView.as_view()),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view())
]