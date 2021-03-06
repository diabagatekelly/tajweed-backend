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
                let ayat = item.test_ayat;

                for (let r of item.rule) {
                    let ruleSubstr = item.test_ayat.substring(item.rule[0].start, item.rule[0].end + 1);
                    let before = item.test_ayat.slice(0, item.rule[0].start);
                    let after = item.test_ayat.slice(item.rule[0].end + 1);
                    ayat = `${before}<span class="color">${ruleSubstr}</span>${after}`
                }
                
                console.log(ayat)
                $('#practiceAyat').append(`<h5>${ayat}</h5>')
            }
        }
    })
    
   

})
