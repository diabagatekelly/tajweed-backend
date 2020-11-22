$('#ruleChoiceForm').on('submit', async function(e) {
    e.preventDefault();
    let rule = $('#inlineFormRuleSelect').val();
    let range = $('#inlineFormAyatSelect').val();

    let data = {
        ruleChosen: rule,
        range: range
    }

    let res = await axios.post('/generate_ayat', data).then((data) => {
        console.log(data)
        $('#practiceAyat').append(`<h3>Surah ${data.data.surahNumber}: ${data.data.surahName}</h3>`);

        for (let item of data.data.ayat) {
            if (item.rule.length === 0) {
                $('#practiceAyat').append(`<h5>${item.test_ayat}</h5>`)
            } else if (item.rule.length !== 0) {
                
                $('#practiceAyat').append('<h5>handle rule</h5>')
            }
        }
    })
    
   

})
