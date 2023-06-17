// get the value of the country field when the page loads and store it
// in a variable
let countrySelected = $('#id_default_country').val();
// the value will be an empty string if the first option from the list
// is selected, so to determine if that's selected we can use this as a boolean
if(!countrySelected) {
    $('#id_default_country').css('color', '#aab7c4');
};
// we want to capture the change event and every time that happens
// get the value of it (which choice is made), and then determine the 
// color depending on the choice made
$('#id_default_country').change(function() {
    countrySelected = $(this).val();
    if(!countrySelected) {
        $(this).css('color', '#aab7c4');
    } else {
        $(this).css('color', '#000');
    }
});