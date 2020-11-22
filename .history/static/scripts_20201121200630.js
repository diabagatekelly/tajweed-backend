$('#ruleChoiceForm').submit(function() {
    // get all the inputs into an array.
    var $inputs = $('#myForm :input');

    // not sure if you wanted this, but I thought I'd add it.
    // get an associative array of just the values.
    var values = {};
    $inputs.each(function() {
        values[this.name] = $(this).val();
    });

});



const generateAyat = async () => {
let res = await axios.post('', )
}