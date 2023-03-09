from django.urls import path
from . import views

app_name = 'BookApp'

urlpatterns = [
    path("book-search/"            , views.bookSearchView      , name="bookSearch"),
    path("book-list/"              , views.bookListView        , name="bookList"),
    path('book-detail/<int:pk>'            , views.bookDetailView      , name='bookDetail'),
    path(""                        , views.myBookView          , name="myBook"),
    path("myBook-detail/<str:id>" , views.myBookDetailView    , name="myBookDetail"),
    path("myBook-delete/" , views.myBookDeleteView    , name="myBookDelete"),
    path("myBook-update/<str:id>" , views.myBookUpdateView    , name="myBookUpdate"),
    path("newBook/"               , views.newBookView         , name="newBook"),
    path("login/"                  , views.loginView           , name="login"),
    path("logout/"                 , views.logoutView          , name="logout"),
    path("content-Create/<str:id>"           , views.contentCreateView     , name="contentCreate"),
    path("content-Delete/<str:id>/<str:flag>"   , views.contentDeleteView     , name="contentDelete"),
    path("content-Update/<str:id>/<str:flag>"   , views.contentUpdateView     , name="contentUpdate"),
    path("userInformation/"   , views.userInformationView     , name="userInformation"),
    path("userUpdate/"   , views.userUpdateView     , name="userUpdate"),
    path("allContent/"   , views.allContentView     , name="allContent"),
]