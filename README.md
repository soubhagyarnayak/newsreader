# newsreader
![BuildDockerImage](https://github.com/soubhagyarnayak/newsreader/workflows/Python%20application/badge.svg)  
A set of python scripts to fetch relevant articles and news from web and index those for personal use.
Depending upon need the scrips can also summarize and analyze the content.

## Setup
The tool is tested for Python 3.12.
### Ubuntu
apt-get install -y libpq-dev # to avoid pg_config error  
apt-get install -y libcurl4-openssl-dev libssl-dev # to avoid curl-config error  
pip install -r requirements.txt  

### MacOS
brew install postgresql

brew install curl-openssl
echo 'export PATH="/usr/local/opt/curl/bin:$PATH"' >> ~/.zshrc
export LDFLAGS="-L/usr/local/opt/curl/lib"     
export CPPFLAGS="-I/usr/local/opt/curl/include"

brew reinstall openssl@1.1
export LDFLAGS="-L/usr/local/opt/openssl/lib"                                  
export CPPFLAGS="-I/usr/local/opt/openssl/include"


