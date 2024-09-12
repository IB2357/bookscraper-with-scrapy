# bookscraper
This is my first scraping project using [Scrapy](https://github.com/scrapy/scrapy) framework


## to run:
- clone this repo
```bash
git clone https://github.com/IB2357/bookscraper-with-scrapy.git

cd bookscraper-with-scrapy
```

- copy `example.env` to `.env`:
```bash
cp example.env env
```
- edit the configurations in .env 

- install deps:
```bash
pip install -r requirements.txt
```

- run the spider :
```bash
cd bookscraper/

scrapy crawl bookspider
```

##  to deploy with docker 

### for development
- go to `docker-compose.yaml`:

For development, leave the development block uncommented.

- build image and compose up: 
```bash 
docker compose build

docker compose up
```

___
### for deployment


- run `for_host.sh` :
```bash
sudo chmod +x for_host.sh

./for_host.sh
```


- create a scrapy server
 in "https://scrapeops.io" and add your server IP to it.

- edit `docker-compose.yaml`:

For production, uncomment the relevant production lines and comment out the development block when switching to production.

- build image and compose up: 
```bash 
docker compose build

docker compose up
```

## Acknowledgements

The bookscraper/ was developed as part of the **Scrapy Beginner Course** by **Joe Kearney**. You can find more information about the course [here](https://thepythonscrapyplaybook.com/freecodecamp-beginner-course/).
