let ruleCount = 0;
let counter = 0;


$('#ruleChoiceForm').on('submit', async function (e) {
    e.preventDefault();
    counter = 0;
   
    let rule = $('#inlineFormRuleSelect').val();
    let range = $('#inlineFormAyatSelect').val();

    let status = '';

    let data = {
        ruleChosen: rule,
        range: range
    }
    // try {
    //     let res = await axios.post('/generate_ayat', data).then((data) => {
    //         console.log(data)

    //         let resultsOverview = data.data.ayat.filter(i => i.rule.length !== 0);

    //         if (resultsOverview.length > 0) {
    //             status = 'go'
    //         } else {
    //             status = 're-submit'
    //         }
    //         if (status === 'go') {
    //             $('#practiceAyat').empty();
    //             // $('#practiceAyat').append(`<h3>Surah ${data.data.surahNumber}: ${data.data.surahName}</h3>`);

    //             for (let item of data.data.ayat) {

    //                 if (item.rule.length === 0) {
    //                     $('#practiceAyat').append(`<h2 class="mb-4">(${item.surahNumber} : ${item.ayahNumber}) ${item.test_ayat}</h2>`)
    //                 } else if (item.rule.length !== 0) {
    //                     $("#practiceAyat").addClass('changeToPointer');

    //                     $('#scoreBoard').show();
                    
    //                     $('#score').empty();
    //                     $('#score').append(counter);
                    

    //                     let ayat = item.test_ayat;

    //                     let ruleMap = {}

    //                     let newAyat = '';

    //                     for (let r of item.rule) {

    //                         ruleMap[`start${item.rule.indexOf(r)}`] = r.start;
    //                         ruleMap[`end${item.rule.indexOf(r)}`] = r.end;

    //                     }


    //                     for (let i = 0; i < item.rule.length; i++) {
    //                         if (item.rule.length === 1) {
    //                             let ruleSubstr = item.test_ayat.substring(item.rule[0].start, item.rule[0].end);
    //                             let before = item.test_ayat.slice(0, item.rule[0].start);
    //                             let after = item.test_ayat.slice(item.rule[0].end);
    //                             ayat = before + `<span class="notFound">${ruleSubstr}</span>` + after;
    //                         } else if (item.rule.length > 1) {


    //                             let ruleSubstr = item.test_ayat.substring(ruleMap[`start${i}`], ruleMap[`end${i}`]);
    //                             if (i === 0) {
    //                                 let before = item.test_ayat.slice(0, ruleMap[`start${i}`]);
    //                                 let concat = newAyat.concat(before + `<span class="notFound">${ruleSubstr}</span>`)
    //                                 newAyat = concat

    //                             } else if (i > 0 && i === item.rule.length - 1) {
    //                                 let before = item.test_ayat.slice(ruleMap[`end${i - 1}`], ruleMap[`start${i}`])
    //                                 let after = item.test_ayat.slice(ruleMap[`end${i}`]);

    //                                 let concat = newAyat.concat(before + `<span class="notFound">${ruleSubstr}</span>` + after);
    //                                 newAyat = concat;

    //                             } else if (i > 0 && i < item.rule.length - 1) {
    //                                 let concat = newAyat.concat(item.test_ayat.slice(ruleMap[`end${i - 1}`], ruleMap[`start${i}`]) + `<span class="notFound">${ruleSubstr}</span>`)
    //                                 newAyat = concat

    //                             }

    //                             ayat = newAyat;

    //                         }

    //                     }

    //                     $('#practiceAyat').append(`<h2 class="mb-4">(${item.surahNumber} : ${item.ayahNumber}) ${ayat}</h2>`)
    //                 }
    //             }

    //         } else {
    //             $('#practiceAyat').empty();

    //             for (let item of data.data.ayat) {
    //                 $('#practiceAyat').append(`<h2 class="mb-4">(${item.surahNumber} : ${item.ayahNumber}) ${item.test_ayat}</h2>`)
    //             }
    //             $('#practiceAyat').append("<h3 class='text-center'>Oops!! These ayat don't have this rule. Please try again.</h3>");
    //             $('#scoreBoard').hide()

    //         }

    //     })

    // }
    // catch (e) {
    //     $('#scoreBoard').hide()
    //     console.log('oh no an error')
    //     $('#practiceAyat').empty();
    //     $('#practiceAyat').append("<h3 class='text-center'>Oops!! Something went wrong, please try again.</h3>");
    // }

    // let notFound = $('.notFound')

    // ruleCount = notFound.length
    // console.log(ruleCount)
    try {
        let res = await axios.post('/analysis', data).then((data) => {
            console.log(data)
        })
        }catch(e) {
            console.log(e)
        }
})



$('#practiceAyat').on('click', function(e) {
    console.log(e.target.classList)
    if (e.target.classList.contains('notFound')) {
        if(!e.target.classList.contains('found')) {
            counter = counter + 1
            e.target.classList.add('found')
        }
    }

    if (counter === 0 || counter < ruleCount) {
        $('#score').empty();
        $('#score').append(counter)
    
    } else if (ruleCount !== 0 && counter == ruleCount) {
        $('#score').empty();
        $('#score').append('You got them all!!')   
    }
})
