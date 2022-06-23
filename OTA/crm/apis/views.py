from django.http import JsonResponse, HttpResponse
from crm.models import User, Invoice
from django.views.generic import TemplateView


class UserView(TemplateView):

    def get(self, request, *args, **kwargs):
        users = User.objects.all().order_by('lastname')
        user_ids = [u.id for u in users]
        data = {
            "users": user_ids
        }
        return JsonResponse(data)


class UserInvoicesView(TemplateView):

    def get(self, request, *args, **kwargs):
        """Get unpaid invoice for a user ID."""
        user_id = kwargs["user_id"]
        try:
            user = User.objects.get(id=user_id)
            invoices = Invoice.objects.filter(user=user, status=False)
            invoices = [i.get_basic_data() for i in invoices]
            data = {
                "invoices": invoices
            }
        except User.DoesNotExist:
            return HttpResponse('Exception: User Not Found')
        return JsonResponse(data)