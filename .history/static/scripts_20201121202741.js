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
        $('#practiceAyat').append(`Surah ${data.data.surahNumber}: ${data.data.surahName}`);

        for (let item of data.data.ayat) {
            if (item.rule.length === 0) {
                $('#practiceAyat').append(item.test_ayat)
            } else if ()
            console.log(item.test_ayat)
        }
    })
    
   

})
