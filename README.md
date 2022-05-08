# bookstore_django
===================PROJECT DESCRIPTION===================

This is a final project for 2022 KBTU university course "INFT3131 Backend Framework. Django". It provides simplified basic back-end functionality for
an Internet bookstore website. The shop is imagined to spezialize in importing books from different suppliers and selling them to individual customers
from several cities of Kazakhstan.

The project's main functions include:
1. Keeping track of books in the shop's storages.
2. Keeping track of book shipments and supplier information.
3. Managing user accounts, including user addresses, payment methods, wish lists, coupons owned, and so on.
4. Providing users the ability to make orders on the website, with product availability depending on the address, and keeping track of order delivery.


===================APPS===================
The project contains 5 apps: user, books, storages, supply, and orders.


===================MODELS===================
Apps contain following models:

user:
— BookstoreUser, UserOrderAddress, Coupon, PaymentCard

books:
— Book, Author, Publisher, Genre

storages:
— City, Storage, StorageEntry

supply:
— SupplyStatys, Supplier, SupplyEntry, SuppliedBook

order:
— OrderStatus, OrderEntry, OrderedBook


===================VIEWS===================
Apps have following views:
user:
— LoginAPIView, create_user (for regular user creation via console)

books:
— AllBooksViewSet, SpecificBookViewSet

storages:
— AllStoragesViewSet, SpecificStorageViewSet, StorageEntryAPIView

supply:
— SupplyStatusesAPIView, AllSupplyEntriesViewSet, SpecificSupplyEntryViewSet, SuppliedBookAPIView

orders:
— OrderStatusesAPIView, AllOrderEntriesViewSet, SpecificOrderEntryViewSet, OrderedBookAPIView


===================AUTHENTICATION===================
Authentication with JSON web token is implemented using djangorestframework-simplejwt library.


===================LOGGING===================
Each app has its dedicated .log file. Every view's action is logged if it has been successful. Unsuccessful attempts at viewing or changing data
is reflected only in responses to respective request.
