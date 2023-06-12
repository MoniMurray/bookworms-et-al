// get the stripe public key and client secret from the template using jQuery

var stripePublicKey = $('#id_stripe_public_key').text().slice(1, -1);
var clientSecret = $('#id_client_secret').text().slice(1, -1);

// in order to set up Stripe, create a var using our stripe public key

var stripe = Stripe(stripePublicKey);

// now use it to create an instance of stripe elements

var elements = stripe.elements();

// use it to create a card element

var style = {
    base: {
        color: '#000',
        fontWeight: '500',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSize: '16px',
        fontSmoothing: 'antialiased',
            '::placeholder': {
                color: '#aab7c4',
            },
    },
    invalid: {
        iconColor: '#dc3545',
        color: '#dc3545',
    },
    };

    var card = elements.create('card', {style: style});

    // and finally mount the card element to the div in 
    // Fieldset 3 'User's Payment Information'

    card.mount('#card-element');

    // Handle realtime validation errors on the card element on Checkout page

    // add a listener to the card element for the change event, every time it changes, check for errors
    card.addEventListener('change', function (event){
        var errorDiv = document.getElementById('card-errors');
        // if there are errors display them in the card errors div on checkout page
        if (event.error) {
            var html = `
                <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                </span>
                <span>${event.error.message}</span>
            `;
            $(errorDiv).html(html);
        } else {
            errorDiv.textContent = '';
        }
    });

    // Add an event listener to the Payment form's submit event

    var form = document.getElementById('payment-form');

    // prevent the form's devault action, ie. to POST
    form.addEventListener('submit', function(ev) {
        ev.preventDefault();
        // while the card is being processed by Stripe, disable it to prevent multiple submissions
        card.update({'disabled': true});
        $('#submit-button').attr('disabled', true);
        // form fade out to layout overlay with spinner for payment processing
        $('#payment-form').fadeToggle(100);
        $('#loading-overlay').fadeToggle(100);

        var saveInfo = Boolean($('#id-save-info').attr('checked'));
        var csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
        var postData = {
            'csrfmiddlewaretoken': csrfToken,
            'client_secret': clientSecret,
            'save_info': saveInfo,
        };        
        var url = '/checkout/cache_checkout_data/';
        $.post(url, postData).done(function () {
        // use the stripe confirmcardpayment() method to send the card info securely to Stripe
            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        name: $.trim(form.full_name.value),
                        phone: $.trim(form.phone_number.value),
                        email: $.trim(form.email.value),
                        address: {
                            line1: $.trim(form.address_line1.value),
                            line2: $.trim(form.address_line2.value),
                            city: $.trim(form.town_or_city.value),
                            country: $.trim(form.country.value),
                            county: $.trim(form.county_or_state.value),
                        }
                    }
                },
                shipping: {
                    name: $.trim(form.full_name.value),
                    phone: $.trim(form.phone_number.value),
                    address: {
                            line1: $.trim(form.address_line1.value),
                            line2: $.trim(form.address_line2.value),
                            city: $.trim(form.town_or_city.value),
                            postcode: $.trim(form.post_code.value),
                            country: $.trim(form.country.value),
                            county: $.trim(form.county_or_state.value),
                        }
                },
            }).then(function(result) {
                if (result.error) {
                    var errorDiv = document.getElementById('card-errors');
                    var html = `
                    <span class="icon" role="alert">
                    <i class="fas fa-times"></i>
                    </span>
                    <span>${result.error.message}</span>`;
                    $(errorDiv).html(html);
                    // reverse fade out 
                    $('#payment-form').fadeToggle(100);
                    $('#loading-overlay').fadeToggle(100);
                    // reenable card
                    card.update({'disabled': false});
                    $('#submit-button').attr('disabled', false);
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        form.submit();
                    }
                }
            });
        }).fail(function () {
            // just reload the page, the error will be in django messages
            location.reload();
        })
    });
   
