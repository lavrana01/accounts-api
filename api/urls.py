from django.urls import path
from api.views import (
    ViewCashbookEntries,
    AddCashbookEntry,
    DeleteEntry,
    UpdateEntry
)

urlpatterns = [
    path('view-cashbook-entries/',ViewCashbookEntries.as_view(),name='view-cashbook-entries'),
    path('add-cashbook-entry/',AddCashbookEntry.as_view(),name='add-cashbook-entry'),
    path('delete-cashbook-entry/',DeleteEntry.as_view(),name='delete-cashbook-entry'),
    path('update-cashbook-entry/<str:entryid>/',UpdateEntry.as_view(),name='update-cashbook-entry'),
    
]