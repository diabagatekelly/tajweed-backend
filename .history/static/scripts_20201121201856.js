$('#ruleChoiceForm').on('submit', function(e) {
    e.preventDefault();
    let rule = $('#inlineFormRuleSelect').val();
    let range = $('#inlineFormAyatSelect').val();

    let data = {
        ruleChosen: rule,
        
    }
    
   

})



const generateAyat = async () => {
let res = await axios.post('', )
}