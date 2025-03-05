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
                        confirmButtonText: 'Cool',
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
        $.ajax({
            type: 'GET',
            url: url,
            // datat: {
            //     'food_id': food_id
            // },
            success: function (response) {
                console.log(response.status)
                if (response.status == "success") {
                    cart_count = response.cart_counter['cart_count']
                    $('#cart-counter').html(cart_count)
                    $('#quantity-' + food_id).html(response.qty)
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
                        confirmButtonText: 'Cool',
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

})