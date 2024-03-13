from dashboard.models import Product, Valuation
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

def product_manager_dashboard(request):
    try:
        products = Product.objects.all().order_by('description')
        product_skus = products.values_list('product_sku', flat=True)
        missing_valuations = Valuation.objects.exclude(product_sku__in=product_skus)

        context = {'products_list': products,
                    'missing_valuations': missing_valuations,
        }
        return render(request, 'product_manager_dashboard.html', context)
    except Exception as e:
        return render(request, 'product_manager_dashboard.html', {'error_message': str(e)})

def update_file(request):
    try:
        if request.method == 'POST':
            if request.POST.get('xcode') == '641525':
                product_details_file = request.FILES.get('fileProductDetails')
                valuation_file = request.FILES.get('fileValuation')

                created_product_count = 0
                updated_product_count = 0
                deleted_valuation_entry = 0
                newly_added_valuation_entry = 0
                updated_product = []
                context = None
                result = None

                if product_details_file:
                    result = process_excel_file_for_product_details(product_details_file)
                    created_product_count = result['created_product_count']
                    updated_product_count = result['updated_product_count']
                    updated_product = result['updated_product']

                if valuation_file:
                    result = process_excel_file_for_valuation(valuation_file)
                    deleted_valuation_entry = result['deleted_valuation_entry']
                    newly_added_valuation_entry = result['newly_added_valuation_entry']
            else:
                return HttpResponse("Access Denied")
        else:
            return HttpResponse("Submit data through POST only.")

        products = Product.objects.all().order_by('description')
        context = {
            'products_list': products,
            'created_product_count': created_product_count,
            'updated_product_count': updated_product_count,
            'deleted_valuation_entry': deleted_valuation_entry,
            'newly_added_valuation_entry': newly_added_valuation_entry,
            'updated_product': updated_product,
        }
        return render(request, 'product_manager_dashboard.html', context)
    except Exception as e:
        return render(request, 'product_manager_dashboard.html', {'error_message': str(e)})

def process_excel_file_for_product_details(uploaded_file):
    print('start--------------------------------------------------------------')
    created_product_count = 0
    updated_product = set()
    product_sku = ''

    df = pd.read_excel(uploaded_file, engine='xlrd')

    for index, row in df.iterrows():
        c = row['Stock Code']
        if isinstance(c, (int, float)):
            product_sku = str(c).rstrip('.0')
        elif isinstance(c, str):
            product_sku = c.strip()
        else:
            print(f"Unexpected Stock Code entry at row {index + 2}: {product_sku}")

        existing_product = Product.objects.filter(product_sku=product_sku).first()

        if existing_product:

            description = str(row['Description'])
            qtyperpcs = int(row['ConversionFactor'])
            bccs = str(row['BCCS'])
            bcib = str(row['BCIB'])
            bcpcs = str(row['BCPCS'])

            if(
                existing_product.description != description or
                existing_product.qtyperpcs != qtyperpcs or
                existing_product.bccs != bccs or
                existing_product.bcib != bcib or
                existing_product.bcpcs != bcpcs
            ):
                if( existing_product.description != description ):
                    existing_product.description = description
                    updated_product.add(existing_product)
                if( existing_product.qtyperpcs != qtyperpcs ):
                    existing_product.qtyperpcs = qtyperpcs
                    updated_product.add(existing_product)
                if( (existing_product.bccs != bccs) and (bccs not in [None,'','nan']) ):
                    existing_product.bccs = bccs
                    updated_product.add(existing_product)
                if( existing_product.bcib != bcib and (bcib not in [None,'','nan']) ):
                    existing_product.bcib = bcib
                    updated_product.add(existing_product)
                if( existing_product.bcpcs != bcpcs and (bcpcs not in [None,'','nan']) ):
                    existing_product.bcpcs = bcpcs
                    updated_product.add(existing_product)

                existing_product.save()
        else:
            if (
                is_valid_stock_code(str(product_sku))
            ):
                Product.objects.create(
                    product_sku=product_sku,
                    description=row['Description'],
                    qtyperpcs=row['ConversionFactor'],
                    bccs = row['BCCS'],
                    bcib = row['BCIB'],
                    bcpcs = row['BCPCS'])
                created_product_count += 1
    return {'created_product_count': created_product_count, 'updated_product_count': len(updated_product), 'updated_product': updated_product}


def process_excel_file_for_valuation(uploaded_file):
    deleted_valuation_entry = 0
    newly_added_valuation_entry = 0
    deleted_valuation_entry = Valuation.objects.all().delete()[0]

    df = pd.read_excel(uploaded_file)
    for index, row in df.iterrows():
        if (
            is_valid_stock_code(str(row['StockCode']))
        ):
            Valuation.objects.create(
                product_sku=row['StockCode'],
                cs=row['CS'],
                ib=row['IB'],
                pcs=row['PCS']
            )
            newly_added_valuation_entry += 1
    return {'deleted_valuation_entry': deleted_valuation_entry, 'newly_added_valuation_entry': newly_added_valuation_entry}


def is_valid_stock_code(stock_code):
    stock_code = str(stock_code).strip()
    valu_of_validation = 5 <= len(stock_code) <= 9 and all(char in '0123456789F' for char in stock_code)
    print(f'stockcode: {stock_code} => {valu_of_validation}')

    if stock_code == '21459':
        return HttpResponse(valu_of_validation)
    return valu_of_validation

def export_poduct_details(request):
    queryset = Product.objects.all()
    data = pd.DataFrame(list(queryset.values()))
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=product_data.xlsx'
    data.to_excel(response, index=False)
    return response




