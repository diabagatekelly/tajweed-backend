$('#ruleChoiceForm').on('submit', function(e) {
    e.preventDefault();
    let rule = $('#inlineFormRuleSelect').val();
    let range = $('#inlineFormAyatSelect').val();
    console.log(rule, range)
   

})



const generateAyat = async () => {
let res = await axios.post('', )
}