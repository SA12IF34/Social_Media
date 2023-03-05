from django.urls import path
from .views import *


urlpatterns = [

    # Accounts
    path('', AccountsView.as_view()),
    path('login/', login),
    path('logout/', logout),
    path('single/<str:account_name>/', AccountView.as_view()),
    path('single/<str:account_name>/followers/', get_followers),
    path('linkers/', linkers),
    path('follow/', follow),
    path('unfollow/', unfollow),
    path('search/', AccountsView.as_view()),
    
    # Posts
    path('posts/', PostsView.as_view()),
    path('posts/owner/<str:owner>/', AccountPostsView.as_view()),
    path('posts/single/<int:id>/', PostView.as_view()),

    # Comments
    path('posts/comments/', CommentsView.as_view()),
    path('posts/comments/commented-to/<int:post>/', PostCommentsView.as_view()),
    path('posts/comments/single/<int:id>/', CommentView.as_view()),
    path('posts/comments/commenter/<int:id>/', AccountComment.as_view())
]