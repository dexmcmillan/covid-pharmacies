const axios = require('axios');
const cheerio = require('cheerio');
const functions = require('save-data-helper'); // Loads some useful functions.

async function getData() {
  return new Promise(async (resolve, reject) => {
    try {
        const sites = []
        const url = "https://immunizebc.ca/initial-covid-19-vaccines-pharmacies"

        const html = await axios.get(url);
        let $ = await cheerio.load(html.data);

        $("table > tbody:nth-child(1) > tr").each((i, element) => {
                const defaultDate = new Date()
                const site = {
                    name: "",
                    street: "",
                    city: "",
                    postal: "",
                    province: "British Columbia",
                    date: defaultDate
                }

                site.city = $(element).find('td:nth-child(1)').text().toString().replace(/[\n|\t]+/gi, "")
                site.name = $(element).find('td:nth-child(2)').text().toString().replace(/[\n|\t]+/gi, "")
                site.street = $(element).find('td:nth-child(3)').text().toString().replace(/[\n|\t]+/gi, " ")
                site.postal = site.street.slice(site.street.length-7)
                site.street = site.street.replace(site.city, "").replace(site.postal, "").replace(/BC|[\s]{2,}/gi, "").trim()
                
                site.link = url
                console.log(site)
                sites.push(site)
            
            
        })
        
        return resolve(sites)
    } catch(err) {
        console.log(err)
    }

  })

}

getData().then((res) => {
    console.log(res)
    functions.saveData(res,"./data/raw/bc-data-scrape", true, true)
})
