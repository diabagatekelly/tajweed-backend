$('#ruleChoiceForm').on('submit', async function(e) {
    e.preventDefault();
    let rule = $('#inlineFormRuleSelect').val();
    let range = $('#inlineFormAyatSelect').val();

    let data = {
        ruleChosen: rule,
        range: range
    }

    let res = await axios.post('', data).then((data) => {
        console.log(data)
    })
    
   

})
