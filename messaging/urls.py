from django.urls import path
from .views import InboxView, SendPrivateMessageView, MessageThreadView, MessageDetailView

app_name = 'messaging'

urlpatterns = [
    path('inbox/', InboxView.as_view(), name='inbox'),
    path('send/', SendPrivateMessageView.as_view(), name='send'),  # Для формы без получателя
    path('send/<int:recipient_id>/', SendPrivateMessageView.as_view(), name='send_to'),  # Для отправки конкретному пользователю
    path('thread/<int:user_id>/', MessageThreadView.as_view(), name='thread'),
    path('detail/<int:pk>/', MessageDetailView.as_view(), name='detail'),
]