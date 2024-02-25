from django.db.models import Sum, F
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractQuarter

from .models import MyOrderProduct


def revenue_statistic_by_product(params={}):
    return statistic_by(params, 'product')


def revenue_statistic_by_category(params={}):
    return statistic_by(params, 'product__category')


def selling_frequency_statistic(by):
    q = MyOrderProduct.objects.filter(active=True)

    if by.__eq__('month'):
        return (q.annotate(month=ExtractMonth('created_date')).values('month', 'product').annotate(
            revenue=Sum(F('product_price') * F('quantity'))
        ))
    if by.__eq__('quarter'):
        return (q.annotate(quarter=ExtractQuarter('created_date')).values('quarter', 'product').annotate(
            revenue=Sum(F('product_price') * F('quantity'))
        ))

    return (q.annotate(year=ExtractYear('created_date')).values('year', 'product').annotate(
        revenue=Sum(F('product_price') * F('quantity'))
    ))


def department_selling_product_statistic(by):
    q = MyOrderProduct.objects.filter(active=True)

    if by.__eq__('month'):
        return (q.annotate(month=ExtractMonth('created_date')).values('month', 'order__department').annotate(
            total=Sum(F('quantity'))
        ))
    if by.__eq__('quarter'):
        return (q.annotate(quarter=ExtractQuarter('created_date')).values('quarter', 'order__department').annotate(
            total=Sum(F('quantity'))
        ))

    return (q.annotate(year=ExtractYear('created_date')).values('year', 'order__department').annotate(
        total=Sum(F('quantity'))
    ))


def statistic_by(params, by):
    q = MyOrderProduct.objects.filter(active=True)

    if params.get('year'):
        if params.get('month'):
            return (q.filter(created_date__year=params.get('year')).filter(created_date__month=params.get('month'))
                    .annotate(year=ExtractYear('created_date'), month=ExtractMonth('created_date'))
                    .values('year', by, 'month')
                    .annotate(revenue=Sum(F('product_price') * F('quantity')))
                    )
        elif params.get('quarter'):
            return (q.filter(created_date__year=params.get('year')).filter(created_date__quarter=params.get('quarter'))
                    .annotate(year=ExtractYear('created_date'), quarter=ExtractQuarter('created_date'))
                    .values('year', by, 'quarter')
                    .annotate(revenue=Sum(F('product_price') * F('quantity')))
                    )

        return (q.filter(created_date__year=params.get('year'))
                .annotate(year=ExtractYear('created_date')).values('year', by).annotate(
                revenue=Sum(F('product_price') * F('quantity'))
        ))

    if params.get('month'):
        return (q.filter(created_date__month=params.get('month'))
                .annotate(month=ExtractMonth('created_date')).values('month', by).annotate(
                revenue=Sum(F('product_price') * F('quantity'))
        ))

    if params.get('quarter'):
        return (q.filter(created_date__quarter=params.get('quarter'))
                .annotate(quarter=ExtractQuarter('created_date')).values('quarter', by).annotate(
                revenue=Sum(F('product_price') * F('quantity'))
        ))

    return q.values(by).annotate(
        revenue=Sum(F('product_price') * F('quantity'))
    )
