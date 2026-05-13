"""ethnic_vault URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ethnic import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.homepage,name="homepage"),
    path('rent-now/<int:design_id>/', views.rent_now, name='rent_now'),
    path('rent-check/<int:id>/', views.rent_check, name='rent_check'),
    path('rent-banner/', views.rent_check_banner, name='rent_check_banner'),
    path('my-orders/', views.view_my_rental_application, name='my_orders'),
    path('user_login_validation/',views.user_login_validation,name="user_login_validation"),
    path('user_login/',views.user_login,name="user_login"),
    path('admin_login_validation/',views.admin_login_validation,name="admin_login_validation"),
    path('admin_login/',views.admin_login,name="admin_login"),
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('user_register_page/',views.user_register_page,name="user_register_page"),
    path('user_register_code/',views.user_register_code,name="user_register_code"),
    path('designer_login/',views.designer_login,name="designer_login"),
    path('logout_view/',views.logout_view,name="logout_view"),
    path('designer_register_code/',views.designer_register_code,name="designer_register_code"),
    path('designer_register_page/',views.designer_register_page,name="designer_register_page"),
    path('designer_login_validation/',views.designer_login_validation,name="designer_login_validation"),
    path('designer_dashboard/',views.designer_dashboard,name="designer_dashboard"),
    path('view_user/',views.view_user,name="view_user"),
    path('delete_user/<int:id>/',views.delete_user,name="delete_user"),
    path('view_designer/',views.view_designer,name="view_designer"),
    path('delete_designer/<int:id>/',views.delete_designer,name="delete_designer"),
    path('email/',views.email,name="email"),
    path('send_email/',views.send_email,name="send_email"),
    path('forgot_password_designer/',views.forgot_password_designer,name="forgot_password_designer"),
    path('forgot_password_user/',views.forgot_password_user,name="forgot_password_user"),
    path('uplod_designs/',views.uplod_designs,name="uplod_designs"),
    path('upload_design/',views.upload_design,name="upload_design"),
    path('profile_account/',views.profile_account,name="profile_account"),
    path('forgot_password_user_code/',views.forgot_password_user_code,name="forgot_password_user_code"),
    path('forgot_password_designer_code/',views.forgot_password_designer_code,name="forgot_password_designer_code"),
    path('profile_update_page/',views.profile_update_page,name="profile_update_page"),
    path('profile_update_page_code/',views.profile_update_page_code,name="profile_update_page_code"),
    path('my_design/',views.my_design,name="my_design"),
    path('delete_design/<int:id>/',views.delete_design,name="delete_design"),
    path('update_design_code/<int:id>/',views.update_design_code,name="update_design_code"),
    path('view_all_design/',views.view_all_design,name="view_all_design"),
    path('user_dashboard/',views.user_dashboard,name="user_dashboard"),
    path('user_profile/',views.user_profile,name="user_profile"),
    path('approve_design/<int:id>/',views.approve_design,name="approve_design"),
    path('disapprove_design/<int:id>/',views.disapprove_design,name="disapprove_design"),
    path('search_design/',views.search_design,name="search_design"),
    path('search_design_price',views.search_design_price,name="search_design_price"),
    path('print_design/<int:id>/',views.print_design,name="print_design"),
    path('edit_profile/',views.edit_profile,name="edit_profile"),
    path('edit_profile_code/',views.edit_profile_code,name="edit_profile_code"),
    path('rent/<int:id>/', views.rent_cloth, name='rent_cloth'),
    path('view_design_details/<int:id>/',views.view_design_details,name="view_design_details"),
    path('rent_cloth_code/',views.rent_cloth_code,name="rent_cloth_code"),
    path('view_rental_request/',views.view_rental_request,name="view_rental_request"),
    path('report/',views.report,name="report"),
    path('designer_login/',views.designer_login,name="designer_login"),
    path('view_designer/',views.view_designer,name="view_designer"),
    path('view_all_rental/',views.view_all_rental,name="view_all_rental"),
    path('disapprove_rental_request/<int:id>/',views.disapprove_rental_request,name="disapprove_rental_request"),
    path('approve_rental_request/<int:id>/',views.approve_rental_request,name="approve_rental_request"),
    path('view_my_rental_application/',views.view_my_rental_application,name="view_my_rental_application"),
    path('lehenga/',views.lehenga,name="lehenga"),
    path('saree/',views.saree,name="saree"),
    path('chaniya/',views.chaniya,name="chaniya"),
    path('sherwani/',views.sherwani,name="sherwani"),
    path('kurta/',views.kurta,name="kurta"),
    path('tuxedo/',views.tuxedo,name="tuxedo"),
    path('boys/',views.boys,name="boys"),
    path('girls/',views.girls,name="girls"),
    path('menAccessories/',views.menAccessories,name="menAccessories"),
    path('womenAccessories/',views.womenAccessories,name="womenAccessories"),
    path('menfootwear/',views.menfootwear,name="menfootwear"),
    path('womenfootwear/',views.womenfootwear,name="womenfootwear"),
    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name="add_to_wishlist"),
    path('view_wishlist/', views.view_wishlist, name="view_wishlist"),
    path('remove_wishlist/<int:id>/', views.remove_wishlist, name="remove_wishlist"),
    path('add_to_cart/<int:id>/', views.add_to_cart, name="add_to_cart"),
    path('view_cart/', views.view_cart, name="view_cart"),
    path('remove_cart_item/<int:id>/', views.remove_cart_item, name="remove_cart_item"),
    path('increase_quantity/<int:id>/', views.increase_quantity, name="increase_quantity"),
    path('decrease_quantity/<int:id>/', views.decrease_quantity, name="decrease_quantity"),
    path('track_order/<int:id>/', views.track_order, name='track_order'),
    path('shipped_order/<int:id>/', views.shipped_order, name='shipped_order'),
    path('delivered_order/<int:id>/', views.delivered_order, name='delivered_order'),
    path('update_design_code_details/<int:id>/',views.update_design_code_details,name="update_design_code_details")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)