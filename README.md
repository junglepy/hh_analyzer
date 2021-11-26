# hh_analyzer (flask web app)
This is flask web app based on data about it vacancies from hh.ru.

Provides the following features:
* Comparison of professions based on similar skills
* Brief statistics on each profession
* Recommendation for choosing professions based on your skills (in develop)

Live demo: [yasta.ru](https://yasta.ru)

# Installation
Copy repository:</br>
git clone https://github.com/JUNglePy/hh_analyzer.git

Create docker image: </br>
docker build -t yasta:latest .

Run docker:</br>
docker run --name yasta -d -p 80:5000 --rm yasta

Open: </br>
http://localhost/

Stop: </br>
docker stop yasta