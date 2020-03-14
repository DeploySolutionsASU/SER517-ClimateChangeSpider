# SER517-ClimateChangeSpider

Instructions to setup the Fuseki sever:
1. Download the Apache Jena Fuseki from the https://jena.apache.org/download/index.cgi
2. Extract the downloaded zip file
3. Launch the Fuseki server by running this commmand `java -jar fuseki-server.jar` (the jar file is available in the root folder of the Fuseki installation directory)


Instructions to setup the python parser and load data into the Fuseki Sever:
1. Clone this repository `git clone https://github.com/DeploySolutionsASU/SER517-ClimateChangeSpider.git`
2. Create a virtual environment inside the project root folder `virtualenv -p python3 venv`
3. Active the virtual environment `source ./venv/bin/activate`
4. Install the dependencies `pip install -r requirements.txt`
5. Execute the Downloader.py `python3 Downloader.py`
5. Start the parser `python3 FusekiParser.py`

Steps to launch the Search UI:
```open the `html/search.html` in any web browser```

Note To Developer:
Use `pip freeze > requirements.txt` while adding new third-party python packages
