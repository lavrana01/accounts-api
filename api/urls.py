from django.urls import path
from api.views import (
    #CASHBOOK VIEWS
    ViewCashbookEntries,
    AddCashbookEntry,
    DeleteEntry,
    UpdateEntry,
    AddBulkEntries,
    
    #LEDGER VIEWS
    Ledger,
    LedgerAccount
    
)

urlpatterns = [
    #--------------------------CASHBOOK URLS---------------------------------------------------------#
    path('view-cashbook-entries/',ViewCashbookEntries.as_view(),name='view-cashbook-entries'),
    path('add-cashbook-entry/',AddCashbookEntry.as_view(),name='add-cashbook-entry'),
    path('delete-cashbook-entry/',DeleteEntry.as_view(),name='delete-cashbook-entry'),
    path('update-cashbook-entry/<str:entryid>/',UpdateEntry.as_view(),name='update-cashbook-entry'),
    path('add-bulk-entries/',AddBulkEntries.as_view(),name='add-bulk-entries'),


    #--------------------------LEDGER URLS----------------------------------------------------------#
    path('get-ledger/',Ledger.as_view(),name='get-ledger'),
    path('get-ledger-account/<str:particulars>/',LedgerAccount.as_view(),name='get-ledger-account'),


    
]