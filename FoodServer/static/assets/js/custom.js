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
