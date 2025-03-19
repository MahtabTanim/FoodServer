let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            componentRestrictions: { 'country': ["bd"] },
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";
    }
    // get the address components and assign them to the fields

    var geocoder = new google.maps.Geocoder()
    var lat = place.geometry.location.lat()
    $('#id_latitude').val(lat)
    var lng = place.geometry.location.lng()
    $('#id_longitude').val(lng)
    for (let i = 0; i < place.address_components.length; i++) {
        for (let j = 0; j < place.address_components[i].types.length; j++) {

            if (place.address_components[i].types[j] == "country") {
                $('#id_country').val(place.address_components[i].long_name)
            }
            if (place.address_components[i].types[j] == "postal_code") {
                $('#id_pin_code').val(place.address_components[i].long_name)
            }

            if (place.address_components[i].types[j] == "administrative_area_level_1") {
                $('#id_state').val(place.address_components[i].long_name)
            }
            if (place.address_components[i].types[j] == "administrative_area_level_2") {
                $('#id_city').val(place.address_components[i].long_name)
            }
        }
    }

}
//add to cart 
$(document).ready(function () {
    $('#ordersTable').DataTable();
    $(".add-to-cart").on("click", function (e) {
        e.preventDefault();
        food_id = $(this).attr('data-id')
        url = $(this).attr('data-url')
        $.ajax({
            type: 'GET',
            url: url,
            // data: {
            //     food_id: food_id
            // },
            success: function (response) {
                if (response.status == "success") {
                    cart_count = response.cart_counter['cart_count']
                    $('#cart-counter').html(cart_count)
                    $('#quantity-' + food_id).html(response.qty)
                    //calculation section
                    update_cart_prices(response)
                } else if (response.status == "login_required") {
                    Swal.fire({
                        title: response.status,
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'Login'
                    }).then(function () {
                        window.location = "/login"
                    })

                } else {
                    Swal.fire({
                        title: response.status,
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'OK',
                    })
                }
            },

        });
    });

    //remove from cart
    $(".remove-from-cart").on("click", function (e) {
        e.preventDefault();
        food_id = $(this).attr("data-id")
        url = $(this).attr("data-url")
        data_cart = $(this).attr("data-cart")
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == "success") {
                    cart_count = response.cart_counter['cart_count']
                    $('#cart-counter').html(cart_count)
                    $('#quantity-' + food_id).html(response.qty)
                    //calculation section
                    update_cart_prices(response)
                    //Delete item from fronend
                    delete_cart_item(response.qty, data_cart)
                } else if (response.status == "login_required") {
                    Swal.fire({
                        title: response.status,
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'Login'
                    }).then(function () {
                        window.location = "/login"
                    })

                } else {
                    Swal.fire({
                        title: response.status,
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'OK',
                    })
                }
            }
        });
    });


    // Delete cart item
    $(".delete-cart-item").on("click", function (e) {
        e.preventDefault();
        cart_id = $(this).attr("data-id")
        url = $(this).attr("data-url")
        data_cart = $(this).attr("data-cart")
        console.log(data_cart)
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == "success") {
                    cart_count = response.cart_counter['cart_count']
                    $('#cart-counter').html(cart_count)
                    update_cart_prices(response)
                    delete_cart_item(0, data_cart)
                } else if (response.status == "login_required") {
                    Swal.fire({
                        title: response.status,
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'Login'
                    }).then(function () {
                        window.location = "/login"
                    })

                } else {
                    console.log(response.status)
                    Swal.fire({
                        title: response.status,
                        text: response.message,
                        icon: 'error',
                        confirmButtonText: 'OK',
                    })
                }
            }
        });
    });


    $(".item-qty").each(function () {
        let item_id = $(this).attr("id");
        let item_quantity = $(this).attr("data-qty");
        $('#' + item_id).html(item_quantity);
    })
    //Add Opening Hour
    $(".add-hours").on("click", function (e) {
        e.preventDefault()
        day = document.getElementById("id_day").value
        from_hour = document.getElementById("id_from_hour").value;
        to_hour = document.getElementById("id_to_hour").value;
        is_closed = document.getElementById('id_is_closed').checked
        csrf_token = $("input[name=csrfmiddlewaretoken]").val()
        var url = $("#add_opening_hours_url").val()

        if ((is_closed && day != "") || (day != "" && from_hour != "" && to_hour != "")) {
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'day': day,
                    'from_hour': from_hour,
                    'to_hour': to_hour,
                    'is_closed': is_closed,
                    'csrfmiddlewaretoken': csrf_token,
                },
                success: function (response) {
                    console.log(response.status)
                    if (response.status == "success") {
                        id = response.id
                        day = response.day;
                        from_hour = response.from_hour;
                        to_hour = response.to_hour;
                        is_closed = response.is_closed;
                        if (is_closed == "true") {
                            html = '<tr id="hour-' + id + '"><td>  <b>' + day + '</b></td><td>Closed</td><td><a href="#" data-url = "/vendor/opening_hours/remove/' + id + '" class="remove_hour">Remove</a></td></tr>'
                        }
                        else {
                            html = '<tr id="hour-' + id + '"><td>  <b>' + day + '</b></td><td>' + from_hour + ' - ' + to_hour + '</td><td><a href="#" data-url = "/vendor/opening_hours/remove/' + id + '" class="remove_hour">Remove</a></td></tr>'
                        }
                        $(".opening_hours").append(html);
                        document.getElementById("opening_hours").reset();
                        Swal.fire({ text: "Added New Entry", icon: "success" })

                    } else {
                        Swal.fire({
                            title: response.message,
                            icon: "error"
                        });
                    }
                }

            });
        }
        else {
            Swal.fire({
                title: "Please fill all the fields",
                icon: "info"
            });
        }

    });
    //Remove Opening Hour
    $(document).on("click", ".remove_hour", function (e) {
        e.preventDefault();
        url = $(this).attr("data-url");
        $.ajax({
            type: 'GET',
            url: url,
            success: function (response) {
                if (response.status == "success") {
                    Swal.fire({ text: "Deleted", icon: "error" })
                    document.getElementById("hour-" + response.id).remove();
                } else {
                    Swal.fire({
                        text: response.message,
                        icon: 'error',
                    })
                }
            }
        });
    });


})

//Helper functions 

//Delete cart item from homepage 
function delete_cart_item(qty, data_cart) {
    if (qty == 0) {
        $('#' + data_cart).remove()
        Swal.fire({
            title: "Item has been deleted from cart ",
            icon: "success",
        });
        if (document.getElementById("menu-items-available") && document.getElementById("menu-items-available").childElementCount == 0) {
            $("#menu-items-available").html(
                `<div class="text-center p-5"><h3>Cart is Empty</h3><h4>Go to <a href="/marketplace" class="text-warning">Marketplace</a></h4></div>`
            )
        }
    }
}

function update_cart_prices(response) {
    if (window.location.pathname == "/cart/") {
        $('#subtotal').html(response.get_cart_total['subtotal'])
        $('#tax').html(response.get_cart_total['tax'])
        $('#total').html(response.get_cart_total['total'])
        tax_dict = response.get_cart_total['tax_dict']
        console.log(tax_dict)
        for (const [taxType, taxValue] of Object.entries(tax_dict)) {
            for (const [percentage, value] of Object.entries(taxValue)) {
                const taxElementId = `tax-${taxType}`;
                document.getElementById(taxElementId).innerHTML = value;
            }
        }
    } else {
        console.log("Not inside cart function")
    }
}