$('#ruleChoiceForm').on('change', function(e) {
    e.preventDefault();
    let rule = $('#ruleChoiceForm').find(':selected').data('inlineFormRuleSelect');
    $('#ruleChoiceForm').val(capacityValue);

})



const generateAyat = async () => {
let res = await axios.post('', )
}