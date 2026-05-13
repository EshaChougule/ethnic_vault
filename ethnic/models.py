from django.db import models


# =========================
# ADMIN MODEL
# =========================
class admin(models.Model):

    admin_email = models.CharField(max_length=255)

    admin_password = models.CharField(max_length=255)

    def __str__(self):
        return self.admin_email


# =========================
# USER MODEL
# =========================
class user(models.Model):

    user_name = models.CharField(max_length=255)

    user_email = models.CharField(max_length=255)

    user_contact = models.CharField(max_length=255)

    user_password = models.CharField(max_length=255)

    user_confirm_password = models.CharField(max_length=255)

    location = models.CharField(max_length=255)

    def __str__(self):
        return self.user_name


# =========================
# DESIGNER MODEL
# =========================
class designer(models.Model):

    designer_name = models.CharField(max_length=255)

    designer_email = models.CharField(max_length=255)

    designer_contact = models.CharField(max_length=255)

    designer_password = models.CharField(max_length=255)

    designer_confirm_password = models.CharField(max_length=255)

    designer_photo = models.FileField(upload_to="designer_image/")

    bio = models.TextField()

    specialization = models.CharField(max_length=255)

    def __str__(self):
        return self.designer_name


# =========================
# DESIGNS MODEL
# =========================
class designs(models.Model):

    CATEGORY_CHOICES = [

        ('Lehenga', 'Lehenga'),

        ('Saree', 'Saree'),

        ('Chaniya', 'Chaniya'),

        ('Sherwani', 'Sherwani'),

        ('Kurta', 'Kurta'),

        ('Tuxedo', 'Tuxedo'),

        ('Boys', 'Boys Wear'),

        ('Girls', 'Girls Wear'),

        ('Men Accessories', 'Men Accessories'),

        ('Women Accessories', 'Women Accessories'),

        ('Men Footwear', 'Men Footwear'),

        ('Women Footwear', 'Women Footwear'),
    ]

    designer_name = models.CharField(max_length=255)

    designer_email = models.CharField(max_length=255)

    designer_contact = models.CharField(max_length=255)

    design_title = models.CharField(max_length=255)

    design_description = models.TextField()

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    design_image1 = models.FileField(upload_to="designs_image1/")

    design_image2 = models.FileField(upload_to="designs_image2/")

    design_image3 = models.FileField(upload_to="designs_image3/")

    charges = models.FloatField()

    remarks = models.TextField()

    show_on_homepage = models.BooleanField(default=False)

    date = models.DateField(auto_now_add=True)

    status = models.CharField(max_length=255, default='Pending')

    def __str__(self):
        return self.design_title


# =========================
# RENT CLOTHS MODEL
# =========================
class rent_cloths(models.Model):

    # =========================
    # DESIGNER INFO
    # =========================
    designer_name = models.CharField(max_length=255)
    designer_email = models.CharField(max_length=255)
    designer_contact = models.CharField(max_length=255)

    # =========================
    # USER INFO
    # =========================
    user_name = models.CharField(max_length=255)
    user_email = models.CharField(max_length=255)
    user_contact = models.CharField(max_length=255)

    # =========================
    # RENT DETAILS
    # =========================
    rental_from = models.CharField(max_length=255)
    rental_date = models.CharField(max_length=255)

    charges = models.CharField(max_length=255)
    total_charges = models.FloatField()

    design_id = models.CharField(max_length=255)

    # =========================
    # DESIGN SNAPSHOTS
    # =========================
    image_design1 = models.FileField(upload_to='rent_designs/')
    image_design2 = models.FileField(upload_to='rent_designs/')
    image_design3 = models.FileField(upload_to='rent_designs/')

    # =========================
    # RENTAL STATUS ONLY (NO PAYMENT HERE)
    # =========================
    status = models.CharField(max_length=255, default='Pending')
    payment_status = models.CharField(max_length=20, default="PENDING")
    return_status = models.CharField(max_length=255, default='Not Returned')

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_name
    
class rental_payment(models.Model):

    PAYMENT_TYPE = [
        ('DEPOSIT', 'Deposit'),
        ('FINAL', 'Final'),
    ]

    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
    ]

    rent = models.ForeignKey(rent_cloths, on_delete=models.CASCADE)

    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)

    amount = models.FloatField()

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )

    transaction_id = models.CharField(max_length=255, null=True, blank=True)

    payment_screenshot = models.FileField(
        upload_to='payment_transactions/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rent.user_email} - {self.payment_type}"


# =========================
# WISHLIST MODEL
# =========================
class wishlist(models.Model):

    user_email = models.CharField(max_length=100)

    design = models.ForeignKey(
        designs,
        on_delete=models.CASCADE
    )

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_email', 'design')

    def __str__(self):
        return self.user_email
    
    
class cart(models.Model):

    user_email = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.user_email


class cart_item(models.Model):

    cart = models.ForeignKey(
        cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    design = models.ForeignKey(
        designs,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(default=1)

    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:

        unique_together = ('cart', 'design')

    def total_price(self):

        return self.quantity * float(self.design.charges)

    def __str__(self):

        return f"{self.design.design_title} - {self.cart.user_email}"