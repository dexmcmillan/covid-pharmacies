echo "Scraping files..."
echo "Scraping Alberta pharmacies..."
node scrape-alberta.js;
echo "Scraping BC pharmacies..."
node scrape-bc.js;
echo "Scraping Ontario pharmacies..."
node scrape-ontario.js;
echo "Done scraping!"