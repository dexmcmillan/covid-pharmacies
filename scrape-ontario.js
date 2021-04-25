const axios = require('axios');
const cheerio = require('cheerio');
const functions = require('save-data-helper'); // Loads some useful functions.

async function getData() {
  return new Promise(async (resolve, reject) => {
    try {
        const sites = []
        const urls = [
            'https://covid-19.ontario.ca/vaccine-locations'
        ]
        for (url of urls) {
            const html = await axios.get(url);

            let $ = await cheerio.load(html.data);
    
            $(".ontario-assessment-centre-card__wrapper").each((i, element) => {
                    const defaultDate = new Date()
                    const site = {
                        name: "",
                        street: "",
                        city: "",
                        postal: "",
                        date: defaultDate
                    }
                    site.name = $(element).find('div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(1)').text().toString()

                    const addressPattern = /[0-9]+\s.*/
                    const postalPattern = /[A-Za-z][0-9][A-Za-z]\s?[0-9][A-Za-z][0-9]/
                    const cityPattern = /[A-Z][A-Za-z]+\s?,\s[A-Z]{2}/
                    const datePattern = /(?<=\/)[0-9]+(?=\/https:)/

                    const bit1 = $(element).find('div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(2)').text().toString()
                    const bit2 = $(element).find('div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(3)').text().toString()
                    const bit3 = $(element).find('div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(4)').text().toString()
                    const bit4 = $(element).find('div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > p:nth-child(5)').text().toString()

                    const bits = bit1 + " " + bit2 + " " + bit3 + " " + bit4
                    try {
                        site.postal = bits.match(postalPattern)[0].toUpperCase()
                    }catch {}
                    
                    try {
                        site.city = bits.match(cityPattern)[0]
                    }catch {}

                    try {
                        const address = bits.replace(site.postal, "").replace(site.city, "").replace("Call this location to make an appointment.", "").trim()
                        site.street = address.match(addressPattern)[0]
                    }catch {}

                    try {
                        const dateCode = url.match(datePattern)[0]
                        const year = dateCode.slice(0, 4)
                        const month = parseInt(dateCode.slice(4, 6)) - 1
                        const day = dateCode.slice(6, 8)

                        site.date = new Date(year, month, day)
                        
                    } catch {}
                    site.link = url
                    console.log(site)
                    sites.push(site)
                
                
            })
        }
        
        return resolve(sites)
    } catch(err) {
        console.log(err)
    }

  })

}

getData().then((res) => {
    console.log(res)
    functions.saveData(res,"./data-ontario-2",true, true)
})
