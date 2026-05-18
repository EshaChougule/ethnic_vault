from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import HttpResponse
from ethnic.models import admin,user,designer,designs,rent_cloths
from django.contrib import messages
from django.contrib.auth import logout
from django.core.mail import EmailMultiAlternatives,send_mail

from django.shortcuts import render
from .models import designs, wishlist

def homepage(request):

    her_data = designs.objects.filter(
        category__in=['Lehenga', 'Saree', 'Chaniya'],
        status='Approved',
        show_on_homepage=True
    )

    his_data = designs.objects.filter(
        category__in=['Sherwani', 'Kurta', 'Tuxedo'],
        status='Approved',
        show_on_homepage=True
    )

    kids_data = designs.objects.filter(
        category__in=['Boys', 'Girls'],
        status='Approved',
        show_on_homepage=True
    )

    accessories_data = designs.objects.filter(
        category__in=['Men Accessories', 'Women Accessories'],
        status='Approved',
        show_on_homepage=True
    )

    footwear_data = designs.objects.filter(
        category__in=['Men Footwear', 'Women Footwear'],
        status='Approved',
        show_on_homepage=True
    )

    wishlist_ids = []

    if request.session.get('role') == 'user':

        user_email = request.session.get('email')

        wishlist_items = wishlist.objects.filter(
            user_email=user_email
        )

        wishlist_ids = wishlist_items.values_list(
            'design_id',
            flat=True
        )

    context = {

        'her_data': her_data,
        'his_data': his_data,
        'kids_data': kids_data,
        'accessories_data': accessories_data,
        'footwear_data': footwear_data,
        'wishlist_ids': wishlist_ids,

    }

    return render(request, 'index.html', context)

def reset_homepage_designs(request):

    designs.objects.update(show_on_homepage=False)

    messages.success(
        request,
        "All homepage designs reset successfully"
    )

    return redirect("view_all_design")
def add_homepage_design(request, id):

    design = designs.objects.get(id=id)

    # =========================
    # HER COLLECTION
    # =========================
    her_categories = [
        'Lehenga',
        'Saree',
        'Chaniya'
    ]

    # =========================
    # HIS COLLECTION
    # =========================
    his_categories = [
        'Sherwani',
        'Kurta',
        'Tuxedo'
    ]

    # =========================
    # KIDS COLLECTION
    # =========================
    kids_categories = [
        'Boys',
        'Girls'
    ]

    # =========================
    # ACCESSORIES
    # =========================
    accessories_categories = [
        'Men Accessories',
        'Women Accessories'
    ]

    # =========================
    # FOOTWEAR
    # =========================
    footwear_categories = [
        'Men Footwear',
        'Women Footwear'
    ]

    # =========================
    # CHECK WHICH GROUP
    # =========================

    if design.category in her_categories:

        count = designs.objects.filter(
            category__in=her_categories,
            show_on_homepage=True
        ).count()

        collection_name = "Her Collection"

    elif design.category in his_categories:

        count = designs.objects.filter(
            category__in=his_categories,
            show_on_homepage=True
        ).count()

        collection_name = "His Collection"

    elif design.category in kids_categories:

        count = designs.objects.filter(
            category__in=kids_categories,
            show_on_homepage=True
        ).count()

        collection_name = "Kids Collection"

    elif design.category in accessories_categories:

        count = designs.objects.filter(
            category__in=accessories_categories,
            show_on_homepage=True
        ).count()

        collection_name = "Accessories Collection"

    elif design.category in footwear_categories:

        count = designs.objects.filter(
            category__in=footwear_categories,
            show_on_homepage=True
        ).count()

        collection_name = "Footwear Collection"

    else:

        count = 0
        collection_name = "Collection"

    # =========================
    # LIMIT CHECK
    # =========================

    if count >= 4:

        messages.error(
            request,
            f"Only 4 homepage designs allowed in {collection_name}. Remove one first."
        )

    else:

        design.show_on_homepage = True
        design.save()

        messages.success(
            request,
            "Design added to homepage successfully"
        )

    return redirect("view_all_design")

def remove_homepage_design(request,id):

    design = designs.objects.get(id=id)

    design.show_on_homepage = False
    design.save()

    messages.success(request,"Design removed from homepage")

    return redirect('view_all_design')

def admin_login(request):
    return render(request,"admin_login.html")

def admin_login_validation(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            admin_login = admin.objects.get(admin_email=email)

            if admin_login.admin_password == password:

                request.session['admin_id'] = admin_login.id
                request.session['email'] = admin_login.admin_email
                request.session['role'] = 'admin'

                return redirect("admin_dashboard")

            else:
                messages.error(request, "Invalid Password")
                return redirect("admin_login")

        except admin.DoesNotExist:
            messages.error(request, "Invalid Email Id")
            return redirect("admin_login")

def user_login(request):
    return render(request,"user_login.html")

def user_login_validation(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user_login = user.objects.get(user_email=email)

            if user_login.user_password == password:

                request.session['user_id'] = user_login.id
                request.session['email'] = user_login.user_email
                request.session['user_name'] = user_login.user_name
                request.session['location'] = user_login.location
                request.session['role'] = 'user'

                next_url = request.POST.get('next')

                if next_url:
                    return redirect(next_url)

                return redirect("homepage")
            else:
                messages.error(request, "Invalid Password")
                return redirect("user_login")

        except user.DoesNotExist:
            messages.error(request, "Invalid Email Id")
            return redirect("user_login")
        
def user_register_code(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        location=request.POST.get('location')
        if user.objects.filter(user_email=email , user_contact=contact).exists():
            messages.success(request,"This account alredy exits. Plz Login")
            return redirect("user_login")
        else:
            un=user(user_name=name,
                    user_email=email,
                    user_contact=contact,
                    user_password=password,
                    user_confirm_password=confirm_password,
                    location=location
                    )
            un.save()
            messages.success(request,"Your Details Has been registred successfully. Now You can Log In")
            return redirect("user_login")
        
def user_register_page(request):
    return render(request,"user_register.html")

from .models import rent_cloths

def user_dashboard(request):

    if request.session.get('role') != 'user':
        return redirect("homepage")

    email = request.session.get('email')
    profile = user.objects.get(user_email=email)

    # ✅ ADD THIS LINE (IMPORTANT)
    rentals = rent_cloths.objects.filter(user_email=email).order_by('-id')

    return render(request, "user_dashboard.html", {
        'profile': profile,
        'rentals': rentals,   # ✅ NEW
    })
def user_profile(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        email = request.session.get('email')
        profile = user.objects.get(user_email=email)
    return render(request,"user_profile.html",{'profile':profile})

def designer_login(request):
    return render(request,"designer_login.html")

def designer_register_page(request):
    return render(request,"designer_register.html")

from django.shortcuts import render, redirect
from django.db.models import Count
from django.db.models.functions import TruncDate

from .models import user, designer, designs, rent_cloths, rental_payment


def admin_dashboard(request):

    # SECURITY CHECK
    if request.session.get('role') != 'admin':
        return redirect('homepage')

    # =========================
    # BASIC COUNTS
    # =========================
    users = user.objects.all()
    total_user = users.count()

    designers = designer.objects.all().count()

    total_design = designs.objects.filter(status='Approved').count()

    total_rentals = rent_cloths.objects.count()

    # =========================
    # PAYMENT STATS (NEW SYSTEM)
    # =========================
    total_deposit_payments = rental_payment.objects.filter(payment_type='DEPOSIT').count()

    total_final_payments = rental_payment.objects.filter(payment_type='FINAL').count()

    pending_payments = rental_payment.objects.filter(payment_status='PENDING').count()

    successful_payments = rental_payment.objects.filter(payment_status='SUCCESS').count()

    # =========================
    # CHART DATA (DESIGNS)
    # =========================
    design_stats = designs.objects.all() \
        .annotate(upload_day=TruncDate('date')) \
        .values('upload_day') \
        .annotate(count=Count('id')) \
        .order_by('upload_day')

    dates = [d['upload_day'].strftime('%Y-%m-%d') for d in design_stats]
    counts = [d['count'] for d in design_stats]

    # =========================
    # CONTEXT
    # =========================
    context = {
        'users': users,
        'total_user': total_user,
        'designers': designers,
        'total_design': total_design,

        # RENTAL INFO
        'total_rentals': total_rentals,

        # PAYMENT INFO
        'total_deposit_payments': total_deposit_payments,
        'total_final_payments': total_final_payments,
        'pending_payments': pending_payments,
        'successful_payments': successful_payments,

        # CHART
        'dates': dates,
        'counts': counts
    }

    return render(request, "admin_dashboard.html", context)

from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect("homepage")


def designer_register_code(request):
    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        bio=request.POST.get('bio')
        image =request.FILES.get('file')
        specialization=request.POST.get('specialization')
        if designer.objects.filter(designer_email=email,designer_contact=contact).exists():
            messages.success(request,"This account alredy exits. Plz Login")
            return redirect("designer_login")
        else:
            un=designer(designer_name=name,
                    designer_email=email,
                    designer_contact=contact,
                    designer_password=password,
                    designer_confirm_password=confirm_password,
                    bio=bio,
                    designer_photo=image,
                    specialization=specialization
                )
            un.save()
            messages.success(request,"Your Details Has been registred successfully. Now You can Log In")
            return render(request,"designer_login.html")
        
def designer_login_validation(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            designer_login = designer.objects.get(designer_email=email)

            if designer_login.designer_password == password:

                request.session['designer_id'] = designer_login.id
                request.session['email'] = designer_login.designer_email
                request.session['role'] = 'designer'

                return redirect("designer_dashboard")

            else:
                messages.error(request, "Invalid Password")
                return redirect("designer_login")

        except designer.DoesNotExist:
            messages.error(request, "Invalid Email Id")
            return redirect("designer_login")


from django.db.models import Count
from .models import designs, rent_cloths


def designer_dashboard(request):

    designer_email = request.session.get('email')

    if not designer_email:
        return redirect('designer_login')

    # Get designer info
    designer_obj = designer.objects.get(designer_email=designer_email)

    # ALL designs by this designer
    my_designs = designs.objects.filter(designer_email=designer_email)

    total_designs = my_designs.count()

    pending_designs = my_designs.filter(status="Pending").count()

    # total views (if you don’t have views field, keep dummy)
    total_views = 0

    # recent designs
    recent_designs = my_designs.order_by('-id')[:5]

    # rental requests for THIS designer ONLY
    rentals = rent_cloths.objects.filter(designer_email=designer_email)

    # chart data (design uploads by date)
    from django.db.models.functions import TruncDate

    chart_data = (
        my_designs
        .annotate(date_only=TruncDate('date'))
        .values('date_only')
        .annotate(count=Count('id'))
        .order_by('date_only')
    )

    dates = [str(i['date_only']) for i in chart_data]
    counts = [i['count'] for i in chart_data]

    context = {
        'designer_name': designer_obj,   # IMPORTANT FIX (you used wrong naming earlier)
        'total_designs': total_designs,
        'pending_designs': pending_designs,
        'total_views': total_views,
        'recent_designs': recent_designs,
        'rentals': rentals,
        'dates': dates,
        'counts': counts,
    }

    return render(request, "designer_dashboard.html", context)


def view_user(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        view_user=user.objects.all()
    return render(request,"view_user.html",{'view_user':view_user})

def delete_user(request,id):
    delete_user=user.objects.get(id=id)
    delete_user.delete()
    messages.success(request,"User account deleted successfully")
    return redirect("view_user")

def view_designer(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        view_designer = designer.objects.all()
    return render(request,"view_designer.html",{'view_designer':view_designer})

def delete_designer(request,id):
    delete_designer=designer.objects.get(id=id)
    delete_designer.delete()
    messages.success(request,"User account deleted successfully")
    return redirect("view_designer")

def email(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        return render(request,"email.html")

def send_email(request):
    if request.method=="POST":
        full_name = request.POST.get('fullname')
        recipient_email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        from_email = 'Ethnic Wear Rentals <computronicsprojects1999@gmail.com>'
        to_email = [recipient_email]

        text_content = f"Dear {full_name} ,\n\n { subject } ,\n\n { message} \n\n Best Regards Ethinc wear"
        html_content=f"""
            <p> Dear <strong> { full_name } </strong>,</p>
            <p> { subject } </p>
            <p> { message } </p>
            <br>
            <p> Best Regards, <br> <strong> Ethnic wear rentals </strong> </p>
        """
        email = EmailMultiAlternatives(subject,text_content,from_email,to_email)
        email.attach_alternative(html_content,"text/html")
        try:
            email.send()
            messages.success(request,"Email sent successfully to the user !")
            return redirect('/email/')
        except Exception as e :
            return HttpResponse(f"Failed to send email :{e}")
    return render(request,"email.html")



def forgot_password_designer(request):
    return render(request,"forgot_password_designer.html")

def forgot_password_user(request):
    return render(request,"forgot_password_user.html")

def forgot_password_user_code(request):
    if request.method=="POST":
        email = request.POST.get("email")
        try:
            matched_user = user.objects.get(user_email=email)
        except user.DoesNotExist:
            messages.success(request,"This email does not exits")
            return redirect("forgot_password_user")
        send_mail(
            "Your Password",
            f"Hi { matched_user.user_name }, Your Password is { matched_user.user_password}",
            'Do not reply',
            [email],
        )
        messages.success(request,"Original Password sent to your account")
        return redirect("user_login")
    return HttpResponse("Invalid Request method")

def forgot_password_designer_code(request):
    if request.method=="POST":
        email = request.POST.get("email")
        try:
            matched_designer = designer.objects.get(designer_email=email)
        except designer.DoesNotExist:
            messages.success(request,"This email does not exist in our profile")
            return redirect("forgot_password_designer")
        send_mail( 
            "Your Password"
            f"Hi { matched_designer.designer_name} , Your Password is { matched_designer.designer_password}",
            'Do not Reply',
            [email],
        )
        messages.success(request,"Original Password sent to your account")
        return redirect("designer_login")
    return HttpResponse("Invalid Request method")

def uplod_designs(request):
    if 'email' not in request.session:
        return redirect('homepage')
    else:
        email = request.session.get('email')
        designer_profile = designer.objects.get(designer_email=email)
    return render(request,"upload_design.html",{'designer_profile':designer_profile})


def upload_design(request):
    if request.method == "POST":

        designer_name = request.POST.get("designer_name")
        designer_email = request.POST.get("designer_email")
        designer_contact = request.POST.get("designer_contact")

        design_title = request.POST.get("design_title")
        design_description = request.POST.get("design_description")

        # ✅ THIS IS YOUR CATEGORY (important)
        category = request.POST.get("category")

        charges = request.POST.get("charges")
        remarks = request.POST.get("remarks")

        design_image1 = request.FILES.get("design_image1")
        design_image2 = request.FILES.get("design_image2")
        design_image3 = request.FILES.get("design_image3")

        # ✅ SAVE TO DATABASE
        designs.objects.create(
            designer_name=designer_name,
            designer_email=designer_email,
            designer_contact=designer_contact,
            design_title=design_title,
            design_description=design_description,
            category=category,
            design_image1=design_image1,
            design_image2=design_image2,
            design_image3=design_image3,
            charges=charges,
            remarks=remarks,

        )

        return redirect('uplod_designs')  # or wherever you want

    return render(request, "upload_design.html")

def profile_account(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        email = request.session.get('email')
        designer_profile = designer.objects.get(designer_email=email)
    return render(request,"profile_account.html",{'designer_profile':designer_profile})

def profile_update_page(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        email = request.session.get('email')
        designer_profile = designer.objects.get(designer_email=email)
    return render(request,"profile_update_page.html",{'designer_profile':designer_profile})

def profile_update_page_code(request):
    email = request.session.get('email')
    update_profile = designer.objects.get(designer_email=email)
    if request.method=="POST":
        update_profile.designer_name = request.POST.get('designer_name')
        update_profile.designer_email = request.POST.get('designer_email')
        update_profile.designer_contact = request.POST.get('designer_contact')
        update_profile.designer_password =request.POST.get('password')
        update_profile.designer_confirm_password =request.POST.get('password')
        update_profile.specialization =request.POST.get('specialization')
        update_profile.bio =request.POST.get('bio')
        update_profile.save()
        messages.success(request,"Profile has been Updated successfully ! ")
        return redirect("profile_account")

def my_design(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        email = request.session.get('email')
        design = designs.objects.filter(designer_email=email)
    return render(request,"my_design.html",{'design':design})

def delete_design(request,id):
    del_design = designs.objects.get(id=id)
    del_design.delete()
    messages.success(request,"Design Details Deleted successfully")
    return redirect("my_design")

def update_design_code(request,id):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        edit_design = designs.objects.get(id=id)
    return render(request,"edit_design.html",{'edit_design':edit_design})

def update_design_code_details(request,id):
    edit_design = designs.objects.get(id=id)
    if request.method=="POST":
        edit_design.design_title = request.POST.get('design_title')
        edit_design.design_description = request.POST.get('design_description')
        edit_design.charges = request.POST.get('charges')
        edit_design.remarks = request.POST.get('remarks')
        if 'design_image1' in request.FILES:
            edit_design.design_image1=request.FILES['design_image1']
        if 'design_image2' in request.FILES:
            edit_design.design_image2=request.FILES['design_image2']
        if 'design_image3' in request.FILES:
            edit_design.design_image3=request.FILES['design_image3']
    edit_design.save()
    messages.success(request,"Design details updated successfully")
    return redirect("my_design")

def approve_design(request,id):
    approve_design = designs.objects.get(id=id)
    approve_design.status = 'Approved'
    approve_design.save()

    subject='Design Status'
    message=f'Congratulations,"{ approve_design.designer_name }" Your Design has been approved. Design Title "{ approve_design.design_title }". Design Posted Date "{ approve_design.date }"'
    from_email = 'Ethnic Wear Rentals <computronicsprojects1999@gmail.com>'
    to_email = approve_design.designer_email

    send_mail(subject,message,from_email,[to_email])
    messages.success(request,"Design Has been approved  and email has been sent ! ")
    return redirect("view_all_design")

def disapprove_design(request,id):
    disapprove_design = designs.objects.get(id=id)
    disapprove_design.status = 'Disapproved'
    disapprove_design.save()

    subject='Design Status'
    message =f'Sorry ! "{ disapprove_design.designer_name }" Your Design has been Disapproved. "{ disapprove_design.design_title }". Design Posted Date "{ disapprove_design.date }" '
    from_email = ' Ethinc Wear Rentals <computronicsprojects1999@gmail.com>'
    to_email = disapprove_design.designer_email

    send_mail(subject,message,from_email,[to_email])
    messages.success(request,"Design has been disapproved and email has been sent ! ")
    return redirect("view_all_design")

def view_all_design(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        pending_design = designs.objects.filter(status='Pending')
        approved_design = designs.objects.filter(status='Approved')
        disapproved_design = designs.objects.filter(status='Disapproved')
        return render(request,"view_design.html",{'pending_design':pending_design,
            'approved_design': approved_design ,'disapproved_design':disapproved_design})

def search_design(request):
    query=request.GET.get('ethnic_name')
    if query:
        search_design = designs.objects.filter(design_title__icontains=query)
    else:
        search_design = designs.objects.none()
    return render(request,"search_design.html",{'search_design':search_design})


def search_design_price(request):
    query = request.GET.get('ethnic_name')
    min_price = request.GET.get('min_price')
    
    designs_query = designs.objects.all()

    if query:
        designs_query = designs_query.filter(design_title__icontains=query)
    if min_price :
        designs_query = designs_query.filter(charges__lte=min_price)

    return render(request,"search_design_price.html",{'search_design': designs_query})

def view_design_details(request, id):
    design = designs.objects.get(id=id)

    reviews = Review.objects.filter(
        design=design,
        status="APPROVED"
    ).order_by('-created_at')

    return render(
        request,
        "view_design_details.html",
        {
            'design': design,
            'reviews': reviews
        }
    )

def print_design(request,id):
    design = designs.objects.get(id=id)
    return render(request,"print_design.html",{'design':design})

def edit_profile(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        email = request.session.get('email')
        user_profile = user.objects.get(user_email=email)
    return render(request,"edit_profile.html",{'user_profile':user_profile})

def edit_profile_code(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        email = request.session.get('email')
        edit_profile = user.objects.get(user_email=email)
        edit_profile.user_name = request.POST.get('user_name')
        edit_profile.user_email = request.POST.get('email')
        edit_profile.user_contact = request.POST.get('contact')
        edit_profile.location = request.POST.get('location')
        edit_profile.user_password = request.POST.get('password')
        edit_profile.user_confirm_password = request.POST.get('password')
        edit_profile.save()
        messages.success(request,"Profile Details has been updated successfully ! ")
        return redirect("edit_profile")
    
from .models import designs
from django.shortcuts import get_object_or_404
def rent_cloth(request, id):
    design = get_object_or_404(designs, id=id)

    return render(request, "rent_cloth.html", {
        'design': design
    })

from .models import rent_cloths, rental_payment, designs
from django.contrib import messages
from django.shortcuts import redirect

def rent_cloth_code(request):

    if request.session.get('role') != 'user':
        return redirect('/user_login/')

    if request.method == "POST":

        design_id = request.POST.get("id")
        design = designs.objects.get(id=design_id)

        # USER SAFE DATA FROM SESSION
        user_email = request.session.get('email')
        user_obj = user.objects.get(user_email=user_email)

        # DATE CALCULATION (SERVER SIDE)
        from datetime import datetime

        start = request.POST.get("rental_from")
        end = request.POST.get("return_date")

        start_date = datetime.strptime(start, "%Y-%m-%d")
        end_date = datetime.strptime(end, "%Y-%m-%d")

        days = (end_date - start_date).days
        total_charges = days * float(design.charges)

        deposit_amount = total_charges * 0.25

        rent = rent_cloths.objects.create(

            designer_name=design.designer_name,
            designer_email=design.designer_email,
            designer_contact=design.designer_contact,

            user_name=user_obj.user_name,
            user_email=user_obj.user_email,
            user_contact=user_obj.user_contact,


            rental_from=start,
            rental_date=end,

            total_charges=total_charges,

            design_id=design.id,

            image_design1=design.design_image1,
            image_design2=design.design_image2,
            image_design3=design.design_image3,

            status="Pending",
            payment_status="PAID",
            return_status="Not Returned"
        )

        screenshot = request.FILES.get("payment_screenshot")

        rental_payment.objects.create(

            rent=rent,
            payment_type="DEPOSIT",
            amount=deposit_amount,
            payment_status="SUCCESS",
            payment_screenshot=screenshot
        )

        messages.success(
            request,
            "Booking successful! Waiting for designer approval."
        )

        return redirect("homepage")

    return redirect("homepage")
    
def view_my_rental_application(request):
    if 'email' not in request.session:
        return redirect("user_login")

    email = request.session.get('email')
    rent = rent_cloths.objects.filter(user_email=email).order_by('-id')

    return render(request,"view_my_rental_application.html", {
        'rent': rent
    })
        
def view_rental_request(request):

    if 'email' not in request.session:
        return redirect("homepage")

    email = request.session.get('email')

    rent_list = rent_cloths.objects.filter(designer_email=email)

    for r in rent_list:

        deposit = rental_payment.objects.filter(
            rent=r,
            payment_type="DEPOSIT",
            payment_status="SUCCESS"
        ).first()

        r.deposit_amount = deposit.amount if deposit else 0
        r.payment_screenshot = deposit.payment_screenshot if deposit else None

        r.remaining_amount = r.total_charges - r.deposit_amount

    return render(request, "view_rental_request.html", {
        'rent': rent_list
    })



def report(request):
    if 'email' not in request.session:
        return redirect("homepage")
    else:
        total_designer = designer.objects.all().count()
        total_design = designs.objects.all().count()
        approved_design = designs.objects.filter(status='Approved').count()
        disapproved_design = designs.objects.filter(status='Disapproved').count()
        pending_design =  designs.objects.filter(status='Pending').count()
        context={
            'total_designer':total_designer,
            'total_design':total_design,
            'approved_design':approved_design,
            'disapproved_design':disapproved_design,
            'pending_design':pending_design
        }
        return render(request,"report.html",context)

from django.shortcuts import get_object_or_404

def approve_rental_request(request, id):
    approve_rent = get_object_or_404(rent_cloths, id=id)

    approve_rent.status = 'Approved'
    approve_rent.save()

    subject = 'Rental Status'
    message = f'Congratulations {approve_rent.user_name}, your rent request for Design ID {approve_rent.design_id} has been approved.'
    from_email = 'Ethnic Wear Rentals <computronicsprojects1999@gmail.com>'
    to_email = approve_rent.user_email

    send_mail(subject, message, from_email, [to_email])

    messages.success(request, "Rental Request approved and email sent!")
    return redirect("view_rental_request")

def disapprove_rental_request(request, id):
    disapprove_rent = get_object_or_404(rent_cloths, id=id)

    disapprove_rent.status = 'Disapproved'
    disapprove_rent.save()

    subject = 'Rental Status'
    message = f'Sorry {disapprove_rent.user_name}, your rental request for Design ID {disapprove_rent.design_id} has been disapproved.'
    from_email = 'Ethnic Wear Rentals <computronicsprojects1999@gmail.com>'
    to_email = disapprove_rent.user_email

    send_mail(subject, message, from_email, [to_email])

    messages.success(request, "Rental Request disapproved and email sent!")
    return redirect("view_rental_request")
def view_all_rental(request):
    rent=rent_cloths.objects.all().order_by('-id')
    return render(request,"view_all_rental.html",{'rent':rent})


def rent_check(request, id):
    if 'email' not in request.session:
        return redirect('user_login')
    else:
        return redirect('rent_cloth', id=id)
    
def rent_check_banner(request):
    if 'email' not in request.session:
        return redirect('user_login')
    else:
        return redirect('homepage')  # or dashboard if you want
    
def saree(request):
    data = designs.objects.filter(category="Saree")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Saree"
    })


def lehenga(request):
    data = designs.objects.filter(category="Lehenga")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Lehenga"
    })


def chaniya(request):
    data = designs.objects.filter(category="Chaniya")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Chaniya"
    })


def sherwani(request):
    data = designs.objects.filter(category="Sherwani")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Sherwani"
    })


def kurta(request):
    data = designs.objects.filter(category="Kurta")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Kurta"
    })


def tuxedo(request):
    data = designs.objects.filter(category="Tuxedo")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Tuxedo"
    })


def boys(request):
    data = designs.objects.filter(category="Boys")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Boys Wear"
    })


def girls(request):
    data = designs.objects.filter(category="Girls")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Girls Wear"
    })


def menAccessories(request):
    data = designs.objects.filter(category="Men Accessories")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Men Accessories"
    })


def womenAccessories(request):
    data = designs.objects.filter(category="Women Accessories")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Women Accessories"
    })


def menfootwear(request):
    data = designs.objects.filter(category="Men Footwear")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Men Footwear"
    })


def womenfootwear(request):
    data = designs.objects.filter(category="Women Footwear")
    return render(request, "category_base.html", {
        "design": data,
        "category_name": "Women Footwear"
    })

from .models import wishlist, cart, cart_item
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def add_to_wishlist(request, id):

    if request.session.get('role') != 'user':

        return redirect(f'/user_login/?next=/add_to_wishlist/{id}/')

    user_email = request.session.get('email')

    design_obj = get_object_or_404(designs, id=id)

    item_exists = wishlist.objects.filter(
        user_email=user_email,
        design=design_obj
    ).exists()

    if item_exists:

        messages.info(request, "Already added to wishlist ❤️")

    else:

        wishlist.objects.create(
            user_email=user_email,
            design=design_obj
        )

        messages.success(request, "Added to wishlist ❤️")

    return redirect(request.META.get('HTTP_REFERER'))

def view_wishlist(request):

    if 'email' not in request.session:
        return redirect("user_login")

    user_email = request.session.get('email')

    items = wishlist.objects.filter(
        user_email=user_email
    ).order_by('-id')

    return render(request, "wishlist.html", {
        'items': items
    })

def remove_wishlist(request, id):

    user_email = request.session.get('email')

    item = get_object_or_404(
        wishlist,
        id=id,
        user_email=user_email
    )

    item.delete()

    messages.success(request, "Removed from wishlist")

    return redirect("view_wishlist")


def confirm_deposit_payment(request, payment_id):

    payment = rental_payment.objects.get(id=payment_id)

    payment.payment_status = "SUCCESS"
    payment.save()

    messages.success(request, "Deposit confirmed")

    return redirect("view_rental_request")

def final_payment(request, rent_id):

    rent = rent_cloths.objects.get(id=rent_id)

    remaining = rent.total_charges * 0.75

    rental_payment.objects.create(
        rent=rent,
        payment_type='FINAL',
        amount=remaining,
        payment_status='PENDING'
    )

    return redirect("user_dashboard")

    
    
def return_payment(request, rent_id):

    rent = rent_cloths.objects.get(id=rent_id)

    if request.method == "POST":

        screenshot = request.FILES['screenshot']
        amount = float(request.POST['amount'])

        rental_payment.objects.create(
            rent=rent,
            payment_type="FINAL",
            amount=amount,
            payment_status="SUCCESS",
            payment_screenshot=screenshot
        )

        # UPDATE RETURN STATUS
        rent.return_status = "RETURNED"
        rent.save()

        return redirect("designer_dashboard")

    return render(request, "return_payment.html", {'rent': rent})

def rent_now(request, design_id):

    if 'email' not in request.session:
        return redirect('user_login')

    design = designs.objects.get(id=design_id)

    if request.method == "POST":

        rent = rent_cloths.objects.create(
            designer_name=design.designer_name,
            designer_email=design.designer_email,
            designer_contact=design.designer_contact,

            user_name=request.POST.get('user_name'),
            user_email=request.POST.get('user_email'),
            user_contact=request.POST.get('user_contact'),

            rental_from=request.POST.get('from_date'),
            rental_date=request.POST.get('to_date'),

            total_charges=design.charges,
            design_id=design.id,

            image_design1=design.design_image1,
            image_design2=design.design_image2,
            image_design3=design.design_image3,

            status="Pending",
            payment_status="Pending"
        )

        return redirect('upload_deposit', rent.id)

    return render(request, "rent_cloth.html", {'design': design})

# =========================
# CART SYSTEM
# =========================

def add_to_cart(request, id):

    # LOGIN CHECK
    if request.session.get('role') != 'user':

        return redirect(f'/user_login/?next=/add_to_cart/{id}/')

    user_email = request.session.get('email')

    design_obj = get_object_or_404(designs, id=id)

    # GET OR CREATE CART
    user_cart, created = cart.objects.get_or_create(
        user_email=user_email
    )

    # CHECK IF ITEM ALREADY EXISTS
    item_exists = cart_item.objects.filter(
        cart=user_cart,
        design=design_obj
    ).exists()

    # IF ALREADY EXISTS
    if item_exists:

        messages.info(request, "Item already added to cart 🛒")

    else:

        cart_item.objects.create(
            cart=user_cart,
            design=design_obj
        )

        messages.success(request, "Added to cart 🛒")

    # RETURN TO SAME PAGE
    return redirect("view_cart")
# =========================
# VIEW CART
# =========================

def view_cart(request):

    user_email = request.session.get("email")

    if not user_email:
        return redirect("user_login")

    cart_obj, created = cart.objects.get_or_create(
        user_email=user_email
    )

    items = cart_obj.items.all()

    total = sum(item.design.charges * item.quantity for item in items)

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })

# =========================
# REMOVE ITEM
# =========================

def remove_cart_item(request, id):

    item = get_object_or_404(
        cart_item,
        id=id
    )

    item.delete()

    messages.success(
        request,
        "Item removed from cart"
    )

    return redirect("view_cart")


# =========================
# INCREASE QUANTITY
# =========================

def increase_quantity(request, id):

    item = get_object_or_404(
        cart_item,
        id=id
    )

    item.quantity += 1

    item.save()

    return redirect("view_cart")


# =========================
# DECREASE QUANTITY
# =========================

def decrease_quantity(request, id):

    item = get_object_or_404(
        cart_item,
        id=id
    )

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

    else:

        item.delete()

    return redirect("view_cart")

def track_order(request, id):

    if 'email' not in request.session:
        return redirect("user_login")

    order = get_object_or_404(
        rent_cloths,
        id=id,
        user_email=request.session.get('email')
    )

    payments = rental_payment.objects.filter(rent=order)

    # -----------------------------
    # RENTAL TIMELINE LOGIC
    # -----------------------------
    if order.status == "Pending":
        progress = 0

    elif order.status == "Approved":
        progress = 25

    elif order.status == "Shipped":
        progress = 50

    elif order.status == "Delivered":
        progress = 75

        # FINAL STEP CHECK
        if order.return_status == "RETURNED":
            progress = 100

    else:
        progress = 0

    # -----------------------------
    # PENALTY CALCULATION
    # -----------------------------
    penalty = calculate_penalty(order)

    return render(request, "track_order.html", {

        'order': order,
        'payments': payments,
        'progress': progress,
        'penalty': penalty

    })

def cancel_order(request, id):

    order = get_object_or_404(
        rent_cloths,
        id=id,
        user_email=request.session.get('email')
    )

    if order.status in ["Pending", "Approved"]:
        order.status = "Cancelled"
        order.save()
        messages.success(request, "Order cancelled successfully")

    else:
        messages.error(request, "Cannot cancel after shipping")

    return redirect("track_order", id=id)

def shipped_order(request, id):

    order = rent_cloths.objects.get(id=id)

    order.status = "Shipped"

    order.save()

    return redirect("view_rental_request")

def delivered_order(request, id):

    order = rent_cloths.objects.get(id=id)

    order.status = "Delivered"

    order.save()

    return redirect("view_rental_request")

def return_request(request, id):

    order = get_object_or_404(
        rent_cloths,
        id=id,
        user_email=request.session.get('email')
    )

    if order.status == "Delivered" and order.return_status == "Not Returned":
        order.return_status = "Return Requested"
        order.save()
        messages.success(request, "Return request sent")

    return redirect("track_order", id=id)

from datetime import date

def calculate_penalty(order):

    if order.status != "Delivered":
        return 0

    try:
        return_date = datetime.strptime(order.rental_date, "%Y-%m-%d").date()
    except:
        return 0

    today = date.today()

    if today > return_date:

        late_days = (today - return_date).days

        penalty_per_day = order.total_charges * 0.05  # 5% per day

        return late_days * penalty_per_day

    return 0

from django.shortcuts import redirect
from django.contrib import messages
from .models import designs, Review, user


def add_review(request, id):

    if request.method == "POST":

        # SESSION EMAIL
        user_email = request.session.get('email')

        # LOGIN CHECK
        if not user_email:

            messages.error(request, "Please login first")

            return redirect('/user_login/')

        try:

            # USER DATA
            userdata = user.objects.get(user_email=user_email)

            # DESIGN DATA
            design_data = designs.objects.get(id=id)

            # FORM DATA
            rating = request.POST.get('rating')

            review_message = request.POST.get('review_message')

            review_image = request.FILES.get('review_image')

            # SAVE REVIEW
            Review.objects.create(

                design=design_data,

                user_name=userdata.user_name,

                user_email=userdata.user_email,

                rating=rating,

                review_message=review_message,

                review_image=review_image
            )

            # SUCCESS MESSAGE
            messages.success(request, "Review Submitted Successfully")

            return redirect('/view_design_details/' + str(id))

        except Exception as e:

            print("REVIEW ERROR:", e)

            messages.error(request, str(e))

            return redirect('/view_design_details/' + str(id))

    return redirect('/view_design_details/' + str(id))

from .models import Review

def view_reviews(request):

    reviews = Review.objects.all().order_by('-created_at')

    context = {
        'reviews': reviews
    }

    return render(request, 'admin_view_reviews.html', context)

from django.shortcuts import get_object_or_404, redirect
from .models import Review

def approve_review(request, id):
    review = get_object_or_404(Review, id=id)
    review.status = "APPROVED"
    review.save()
    return redirect('view_reviews')

def reject_review(request, id):
    review = get_object_or_404(Review, id=id)
    review.status = "REJECTED"
    review.save()
    return redirect('view_reviews')

def delete_review(request, id):
    review = Review.objects.get(id=id)
    review.delete()
    return redirect('view_reviews')

from django.shortcuts import render


def terms_conditions(request):
    return render(request, 'terms_conditions.html')

def faq_page(request):
    return render(request, 'faq.html')

def offers_page(request):
    return render(request,'offers.html')


def rental_guidelines_page(request):
    return render(request, 'rental_guidelines.html')
