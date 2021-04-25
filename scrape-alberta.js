const axios = require('axios');
const cheerio = require('cheerio');
const functions = require('save-data-helper'); // Loads some useful functions.

async function getData() {
  return new Promise(async (resolve, reject) => {
    try {
      const datePattern = /(?<=\/)[0-9]+(?=\/https:)/
      const sites = []
      const urls = [
        "https://www.ab.bluecross.ca/news/covid-19-immunization-program-information.php",
        "https://web.archive.org/web/20210225005407/https://www.ab.bluecross.ca/news/covid-19-immunization-program-information.php#pharmacy-box",
        "https://web.archive.org/web/20210319212329/https://www.ab.bluecross.ca/news/covid-19-immunization-program-information.php",
        "https://web.archive.org/web/20210320224934/https://www.ab.bluecross.ca/news/covid-19-immunization-program-information.php",
        "https://web.archive.org/web/20210321230730/https://www.ab.bluecross.ca/news/covid-19-immunization-program-information.php",
        "https://web.archive.org/web/20210313190450/https://www.ab.bluecross.ca/news/covid-19-immunization-program-information.php",
        "https://web.archive.org/web/20210406182112/https://www.ab.bluecross.ca/news/covid-19-immunization-program-information.php"
      ]
      for (url of urls) {
        const html = await axios.get(url);
        let $ = await cheerio.load(html.data);

        $("body > main > section > div > div > div.container-fluid.bkg-grey.padding-t-16.padding-b-56 > div > div > div, .box").each((i, element) => {
          const defaultDate = new Date()
          const site = {
            name: "",
            street: "",
            city: "",
            postal: "",
            province: "Alberta",
            date: defaultDate
          }

          site.city = $(element).find('p:nth-child(4)').text().toString().replace(/[\n|\t]+/gi, "")
          site.name = $(element).find('h4').text().toString().replace(/[\n|\t]+/gi, "")
          site.street = $(element).find('p:nth-child(2)').text().toString().replace(/[\n|\t]+/gi, " ")
          site.street = site.street.replace(site.city, "").replace(site.postal, "").replace(/BC|[\s]{2,}/gi, "").trim()
          try {
            const dateCode = url.match(datePattern)[0]
            const year = dateCode.slice(0, 4)
            const month = parseInt(dateCode.slice(4, 6)) - 1
            const day = dateCode.slice(6, 8)

            site.date = new Date(year, month, day)

          } catch { }
          site.link = url
          console.log(site)
          sites.push(site)


        })
      }
      return resolve(sites)
    } catch (err) {
      console.log(err)
    }

  })

}

getData().then((res) => {
  functions.saveData(res, "./data/raw/alberta-data-scrape", true, true)
})
