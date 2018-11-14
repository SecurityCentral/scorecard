import io, json
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.defaulttags import register
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from rest_framework import views
from scorecard import models
from scorecard import product_pages, scoring

NOT_APPLICABLE = "not applicable"


def businessunitsview(request):
    bu_group_set = set()
    bu_score_set = set()
    product_list = models.Product.objects.filter(published=True).order_by('business_unit__bu_group__name')
    all_bu_scores = models.BUScore.objects.all().order_by('bu__name')
    for product in product_list:
        bu_group_set.add(product.business_unit.bu_group)
        for bu_score in all_bu_scores:
            if product.business_unit == bu_score.bu:
                bu_score_set.add(bu_score)
    bu_group_list = list(bu_group_set)
    bu_score_list = list(bu_score_set)

    @register.filter
    def get_unsupported_count(bu_score):
        return bu_score.items_total - bu_score.items_supported - bu_score.items_in_progress

    return render(request, 'scorecard/businessunits.html', {'bu_group_list': bu_group_list,
                                                            'bu_score_list': bu_score_list})


def proddetailsview(request):
    generate_pdf = False
    if request.GET.get('pdf') == '1':
        generate_pdf = True
    product_score = models.ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.TOTAL)
    proc = models.ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.PROCESS.lower())
    tech = models.ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.TECHNOLOGY.lower())
    comp = models.ProductScore.objects.get(product__id=request.GET.get('product'), category=scoring.COMPLIANCE.lower())
    proc_sub_categories_set = set()
    tech_sub_categories_set = set()
    comp_sub_categories_set = set()

    product_control_list = models.ProductControl.objects.\
        filter(Q(product=product_score.product) & ~Q(status=NOT_APPLICABLE)).\
        order_by('control__family__label', 'control__name')

    proc_list = models.ProductSecurityCapability.objects.\
        filter(Q(product=product_score.product) &
               Q(security_capability__category__name=scoring.PROCESS) & ~Q(status__name=NOT_APPLICABLE)).\
        order_by('security_capability__sub_category', 'security_capability__name')
    for proc_item in proc_list:
        proc_sub_categories_set.add(proc_item.security_capability.sub_category)
    proc_sub_categories_list = list(proc_sub_categories_set)

    tech_list = models.ProductSecurityCapability.objects.\
        filter(Q(product=product_score.product) &
               Q(security_capability__category__name=scoring.TECHNOLOGY) & ~Q(status__name=NOT_APPLICABLE)).\
        order_by('security_capability__sub_category', 'security_capability__name')
    for tech_item in tech_list:
        tech_sub_categories_set.add(tech_item.security_capability.sub_category)
    tech_sub_categories_list = list(tech_sub_categories_set)

    comp_list = models.ProductSecurityCapability.objects.\
        filter(Q(product=product_score.product) &
               Q(security_capability__category__name=scoring.COMPLIANCE) & ~Q(status__name=NOT_APPLICABLE)).\
        order_by('security_capability__sub_category', 'security_capability__name')
    for comp_item in comp_list:
        comp_sub_categories_set.add(comp_item.security_capability.sub_category)
    comp_sub_categories_list = list(comp_sub_categories_set)

    product_roles_list = models.ProductSecurityRole.objects.filter(Q(product=product_score.product)).\
        order_by('role__description')

    @register.filter
    def get_item(dictionary, key):
        return dictionary.get(key)

    if generate_pdf:
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(2*inch, 10*inch, "Hello world.")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        # response = FileResponse(buffer, as_attachment=False, filename='hello.pdf')
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="hello.pdf"'
        response.write(buffer.getvalue())
    else:
        response = render(request, 'scorecard/proddetails.html',
                  {'product_score': product_score,
                   'proc': proc,
                   'tech': tech,
                   'comp': comp,
                   'product_control_list': product_control_list,
                   'control_status_values': scoring.get_control_status_values(),
                   'proc_list': proc_list,
                   'tech_list': tech_list,
                   'comp_list': comp_list,
                   'proc_sub_categories_list': proc_sub_categories_list,
                   'tech_sub_categories_list': tech_sub_categories_list,
                   'comp_sub_categories_list': comp_sub_categories_list,
                   'product_roles_list': product_roles_list})
    return response


def health(request):
    return HttpResponse(status=200)


def productsview(request):
    business_unit = models.BusinessUnit.objects.get(id=request.GET.get('bu'))
    product_score_list = models.ProductScore.objects.filter(
        product__business_unit=business_unit, category=scoring.TOTAL, product__published=True)

    @register.filter
    def get_unsupported_count(product_score):
        return product_score.items_total - product_score.items_supported - product_score.items_in_progress

    return render(request, 'scorecard/products.html', {'product_score_list': product_score_list, 'bu': business_unit})


def submit(request):
    if 'update' in request.POST:
        product_pages.update_product_data()
    return redirect('/businessunitsview')


def result(errors):
    result_data = {'result': 'success'}

    if len(errors) > 0:
        result_data['result'] = 'failure'
        result_data['errors'] = []
        for error in errors:
            result_data['errors'].append(error)

    return HttpResponse(json.dumps(result_data), content_type='application/json')


def recalculate_product_scores(product_set):
    """
    Recalculates the scores of all products in product_set. Also recalculates the scores of their associated business
    units.

    :param product_set:
    """
    bu_set = set()
    for product in product_set:
        scoring.calculate_product_score(product.pk)
        bu_set.add(product.business_unit)
    for bu_id in bu_set:
        scoring.calculate_business_unit_score(bu_id)


class SyncProductPages(views.APIView):

    def post(self, request):
        """
        Synchronizes product and business group data with Product Pages. Does not delete any data, only adds or
        updates. Following the sync, a complete recalculation of all product and business unit scores is executed.
        """
        product_pages.update_product_data()
        return HttpResponse(status=200)


class CalculateAllProductScores(views.APIView):

    def post(self, request):
        """
        Recalculates the scores of all products and their respective business units.
        """
        scoring.calculate_all_product_scores()
        scoring.calculate_all_business_unit_scores()
        return HttpResponse(status=200)


class CalculateProductScores(views.APIView):

    def post(self, request):
        """
        Calculates the scores of the specified products and their respective business units.
        <br/>
        The body of this request should contain a list of ids of products whose scores should be calculated.
        <br/>
        For example:
        <br/>
        <pre>
        [
            {"id": 12},
            {"id": 9},
            {"id": 33}
        ]
        </pre>
        <br/>
        Returns a result of "success" if no issues were encountered. Example:
        <br/><br/>
        <pre>{"result": "success"}</pre>
        <br/>
        Otherwise, returns "failure" along with a list of error messages. Example:
        <br/><br/>
        <pre>{"result": "failure", "errors": ["Product with id '99' does not exist."]}</pre>
        """
        errors = []
        product_set = set()
        body = json.loads(request.body.decode('utf-8'))
        for product in body:
            try:
                product_set.add(models.Product.objects.get(pk=product['id']))
            except models.Product.DoesNotExist:
                errors.append("Product with id '%s' does not exist." % product["id"])
        recalculate_product_scores(product_set)
        return result(errors)


class UpdateProductCapabilities(views.APIView):

    def post(self, request):
        """
        Updates the statuses of the specified security capabilities for the specified products and recalculates the
        scores of the associated products and their respective business units.
        <br/>
        The body of this request should contain a list of products and their associated security capabilities with the
        desired statuses.
        <br/>
        For example:
        <br/>
        <pre>
        [
            {
                "name": "OpenShift Container Platform",
                "capabilities": [
                    {
                        "name": "Are you accounting for OWASP top 10 Critical Vuln flaws?",
                        "status": "implemented"
                    },
                    {
                        "name": "Documented Security Requirements",
                        "status": "none"
                    }
                ]
            },
            {
                "name": "Red Hat OpenStack Platform",
                "capabilities": [
                    {
                        "name": "Are you accounting for OWASP top 10 Critical Vuln flaws?",
                        "status": "planned"
                    },
                    {
                        "name": "Documented Security Requirements",
                        "status": "partial"
                    },
                    {
                        "name": "Documented Security Test Cases",
                        "status": "implemented"
                    }
                ]
            }
        ]
        </pre>
        <br/>
        Returns a result of "success" if no issues were encountered. Example:
        <br/><br/>
        <pre>{"result": "success"}</pre>
        <br/>
        Otherwise, returns "result":"failure" along with a list of error messages.
        """
        errors = []
        product_set = set()
        body = json.loads(request.body.decode('utf-8'))
        for product in body:
                capabilities = product['capabilities']
                for capability in capabilities:
                    try:
                        found_product = models.Product.objects.get(name=product['name'])
                        product_set.add(found_product)
                    except models.Product.DoesNotExist:
                        errors.append("Product '%s' does not exist." % product['name'])
                    try:
                        found_capability = models.ProductSecurityCapability.objects.get(
                            product__name=product['name'], security_capability__name=capability['name'])
                    except models.ProductSecurityCapability.DoesNotExist:
                        errors.append("Product security capability '%s' for product '%s' does not exist." %
                                      (capability['name'], product['name']))
                    try:
                        found_status = models.Status.objects.get(name=capability['status'])
                    except models.Status.DoesNotExist:
                        errors.append("Status '%s' does not exist for product security capability '%s' for product "
                                      "'%s'." % (capability['status'], capability['name'], product['name']))
                    found_capability.status = found_status
                    found_capability.save()
        recalculate_product_scores(product_set)
        return result(errors)
