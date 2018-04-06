****************************
Глава 2- приложение Checkout
****************************


**Состав и краткое описание**
=============================

Данное приложение служит цели оплаты услуги пользователем.

Имеет только один шаблон(checkout.html) и только одно представление(checkout)


**Представление Checkout**
==========================

Листинг::

    stripe.api_key = settings.STRIPE_SECRET_KEY

    @login_required
    def checkout(request):
        publishKey = settings.STRIPE_PUBLISHABLE_KEY
        customer_id = request.user.userstripe.stripe_id
        if request.method == 'POST':
            token = request.POST['stripeToken']
            # Создание платежа:
            try:
                # Создание покупателя:
                customer = stripe.Customer.retrieve({customer_id})
                customer.sources.create(source = {token})
                charge = stripe.Charge.create(
                    amount = 100,
                    currenvy = "usd",
                    customer = customer,
                    description = "Example charge"
                )
            except stripe.error.CardError as e:
                # Карта отклонена:
                pass
        context = {'publishKey': publishKey}
        template = 'checkout.html'
        return render(request, template, context)

**Страница оплаты:**

.. image:: _static/checkout.png
  :target: _static/checkout.png
