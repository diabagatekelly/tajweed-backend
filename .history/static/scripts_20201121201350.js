$('#ruleChoiceForm').on('change', function(e) {
    e.preventDefault();
    let rule = .find(':selected').data('capacity');
    $('#ruleChoiceForm').val(capacityValue);

})



const generateAyat = async () => {
let res = await axios.post('', )
}