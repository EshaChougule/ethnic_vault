

from django.contrib import admin as djadmin

from .models import (
    admin,
    user,
    designer,
    designs,
    rent_cloths,
    rental_payment,
    wishlist,
    cart,
    cart_item,
    Review
)

djadmin.site.register(admin)
djadmin.site.register(user)
djadmin.site.register(designer)
djadmin.site.register(designs)
djadmin.site.register(rent_cloths)
djadmin.site.register(rental_payment)
djadmin.site.register(wishlist)
djadmin.site.register(cart)
djadmin.site.register(cart_item)
djadmin.site.register(Review)