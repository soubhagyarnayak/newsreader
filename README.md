# newsreader
![BuildDockerImage](https://github.com/soubhagyarnayak/newsreader/workflows/Python%20application/badge.svg)  
A set of python scripts to fetch relevant articles and news from web and index those for personal use.
Depending upon need the scrips can also summarize and analyze the content.

## Setup
The tool is tested for Python 3.12.

### Ubuntu

#### Install dev dependencies
apt-get install -y libpq-dev # to avoid pg_config error
apt-get install -y libcurl4-openssl-dev libssl-dev # to avoid curl-config error


#### Tesseract OCR (required for `TesseractTextExtractor`)
Tesseract main binary needs to be installed separately
```bash
apt-get install -y tesseract-ocr tesseract-ocr-ori
```
Odia language data is installed to `/usr/share/tesseract-ocr/5/tessdata/ori.traineddata`.

#### Install python dependencies
pip install -r requirements.txt

### MacOS

#### Install postgresql
brew install postgresql

#### Install openssl and dev dependencies
brew install curl-openssl
echo 'export PATH="/usr/local/opt/curl/bin:$PATH"' >> ~/.zshrc
export LDFLAGS="-L/usr/local/opt/curl/lib"
export CPPFLAGS="-I/usr/local/opt/curl/include"

brew reinstall openssl@1.1
export LDFLAGS="-L/usr/local/opt/openssl/lib"
export CPPFLAGS="-I/usr/local/opt/openssl/include"

#### Tesseract OCR (required for `TesseractTextExtractor`)
Tesseract main binary needs to be installed separately
```bash
brew install tesseract tesseract-lang
```
`tesseract-lang` includes Odia (`ori`) language data at `/opt/homebrew/share/tessdata/ori.traineddata`.

#### Install python dependencies
pip install -r requirements.txt


