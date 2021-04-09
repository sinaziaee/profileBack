from django.urls import path, include


app_name = 'MyUniversity'
urlpatterns = [
    path('api/account/', include('account.api.urls', 'account_api')),
    path('api/', include('post.api.urls')),
]
