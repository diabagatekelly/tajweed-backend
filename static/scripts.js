$('#ruleChoiceForm').on('submit', async function (e) {
    e.preventDefault();
    let rule = $('#inlineFormRuleSelect').val();
    let range = $('#inlineFormAyatSelect').val();

    let status = '';

    let data = {
        ruleChosen: rule,
        range: range
    }
try {
    let res = await axios.post('/generate_ayat', data).then((data) => {
        console.log(data)

    let resultsOverview = data.data.ayat.filter(i => i.rule.length !== 0);

    console.log(resultsOverview)
    if (resultsOverview.length > 0) {
        status = 'go'
    } else  {
        status = 're-submit'
    }
console.log(status)
        if (status === 'go') {
            $('#practiceAyat').empty();
            $('#practiceAyat').append(`<h3>Surah ${data.data.surahNumber}: ${data.data.surahName}</h3>`);
    
            for (let item of data.data.ayat) {
    
                if (item.rule.length === 0) {
                    $('#practiceAyat').append(`<h2 class="mb-4">${item.test_ayat}</h2>`)
                } else if (item.rule.length !== 0) {
                    let ayat = item.test_ayat;
    
                    console.log(ayat)
                    let ruleMap = {}
    
                    let newAyat = '';
                    let sliceArr = [];
                    let letterArr = [];
    
                    for (let r of item.rule) {
    
                        ruleMap[`start${item.rule.indexOf(r)}`] = r.start;
                        ruleMap[`end${item.rule.indexOf(r)}`] = r.end;
    
                    }
    
                    console.log('rule lengh', item.rule.length)
                    console.log(ruleMap)
    
                    for (let i = 0; i < item.rule.length; i++) {
                        if (item.rule.length === 1) {
                            let ruleSubstr = item.test_ayat.substring(item.rule[0].start, item.rule[0].end);
                            let before = item.test_ayat.slice(0, item.rule[0].start);
                            let after = item.test_ayat.slice(item.rule[0].end);
                            ayat = before + `<span class="color">${ruleSubstr}</span>` + after;
                        } else if (item.rule.length > 1) {
    
    
    
    
                            console.log('start:', ruleMap[`start${i}`], 'end', ruleMap[`end${i}`])
                            let ruleSubstr = item.test_ayat.substring(ruleMap[`start${i}`], ruleMap[`end${i}`]);
                            if (i === 0) {
                                let before = item.test_ayat.slice(0, ruleMap[`start${i}`]);
                                console.log(i, ruleSubstr)
                                console.log(i, before)
                                let concat = newAyat.concat(before + `<span class="color">${ruleSubstr}</span>`)
                                console.log(i, concat)
                                newAyat = concat
                                console.log(i, newAyat)
    
                            } else if (i > 0 && i === item.rule.length - 1) {
                                let before = item.test_ayat.slice(ruleMap[`end${i - 1}`], ruleMap[`start${i}`])
                                let after = item.test_ayat.slice(ruleMap[`end${i}`]);
                                console.log('after', after)
    
                                let concat = newAyat.concat(before + `<span class="color">${ruleSubstr}</span>` + after);
                                newAyat = concat;
    
                                console.log('final', newAyat)
                            } else if (i > 0 && i < item.rule.length - 1) {
                                console.log('from', ruleMap[`end${i - 1}`], ruleMap[`start${i}`])
                                let concat = newAyat.concat(item.test_ayat.slice(ruleMap[`end${i - 1}`], ruleMap[`start${i}`]) + `<span class="color">${ruleSubstr}</span>`)
                                console.log(i, ruleSubstr)
                                console.log(i, concat)
                                newAyat = concat
    
                            }
    
                            ayat = newAyat;
                        }
    
                    }
    
                    $('#practiceAyat').append(`<h2 class="mb-4">${ayat}</h2>`)
                }
            }

        } else {
            $('#practiceAyat').empty();

            for (let item of data.data.ayat) {
                    $('#practiceAyat').append(`<h2 class="mb-4">${item.test_ayat}</h2>`)
            }
            $('#practiceAyat').append("<h3 class='text-center'>Oops!! These ayat don't have this rule. Please try again.</h3>");
        }
      
    })

}
catch(e) {
    console.log('oh no an error')
    $('#practiceAyat').empty();
    $('#practiceAyat').append("<h3 class='text-center'>Oops!! Something went wrong, please try again.</h3>");
}
    
})
