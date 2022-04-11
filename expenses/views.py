from datetime import date
from unicodedata import category
from urllib import request
from django.views.generic.list import ListView
from .forms import ExpenseSearchForm
from .models import Expense, Category
#from django.db.models import Q
from .reports import summary_per_category


class ExpenseListView(ListView):
    model = Expense
    paginate_by = 15

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        form = ExpenseSearchForm(self.request.GET)
        
        
        
        if form.is_valid():
            name = form.cleaned_data.get('name', '').strip()
            form_category = form.cleaned_data.get('category', '')
            date_from = form.data.get('date_from')
            date_to = form.data.get('date_to')
            amount_min = form.data.get('amount_min')
            amount_max = form.data.get('amount_max')
            select = form.data.get('select')




            if name:
                queryset = queryset.filter(name__icontains=name)
            if form_category:
                queryset = queryset.filter(category=form_category)
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)
            if amount_min:
                queryset = queryset.filter(amount__gte=amount_min)
            if amount_max:
                queryset = queryset.filter(amount__lte=amount_max)            
            if select:
                queryset = queryset.order_by(select)

            return super().get_context_data(
            form=form,
            object_list=queryset,
            summary_per_category=summary_per_category(queryset),
            **kwargs)

class CategoryListView(ListView):
    model = Category
    paginate_by = 5

