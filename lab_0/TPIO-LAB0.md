# Git
- Sve ono osnovno
- Protected branches (mora se traziti pull request prije merge-a, ogranicenje tko smije mijenjati, automatizirani testovi...)


# Docker
- Pakiranje aplikacije u lagane i prenosive kontejnere s citavim operacijskim sustavom i bibliotekama
	- kad se pokrene kontejnerizirana aplikacija, vidi tocno one promjene s kojima je zapakirana - konzistencija
	- kontejneri su kao puno laksa verzija virtualnih strojeva
- GLAVNI KONCEPTI
	- **Slika** - ono u sto se pakira aplikacija i okruzenje (datoteke, biblioteke, metapodaci)
	- **Registar** - repozitorij na kojem se spremaju docker slike za dijeljenje (npr. [Docker Hub](https://hub.docker.com/))
	- **Kontejner** - proces izoliran od operacijskog sustava, Linux kontejner ; slika=blueprint,kontejner=realizacija
- Primjer
	- docker run busybox echo "Hello world" - povlaci sliku s docker huba i runna executable
	- ![[Pasted image 20231023130017.png|500]] 
- Kreacija slike
	- napraviti Dockerfile (u istom direktoriju kao app.js), u njega:
``` 
FROM node:7 
ADD app.js /app.js
ENTRYPOINT ["node", "app.js"]
```
- node i oznaka 7 (jer moze postojati vise razlicith verzija), sto ide u sliku, Entrypoint je komanda koja se izvrsava kad se pokrene slika
- nakon toga buildamo sliku:
```
docker build -t kubia .
```
- ![[Pasted image 20231023130647.png|500]]
- Komande
	- docker images - prikaz slika
	- docker run --name kubia-container -p 8080:8080 -d kubia -> runna nasu sliku
		- mapira nas port 8080 na port 8080 kontejnera
	- docker ps
		- ispis svih kontejnera koji runnaju
	- docker-compose up
		- ako imamo config.yaml i docker-compose.yaml mozemo runnati ovo
	- docker stop ime_kontejnera
		- **docker stop $(docker ps -a -q)** - sve



# Apache Kafka
- obrada i upravljanje tokom podataka u stvarnom vremenu (distributed event streaming platform)
- raspodijeljeni sustavi mogu pisati i citati poruke, spremati ih proizvoljno dugo vremena, obradivati ih real-time
- kafka mora biti pouzdan i ne padati, stoga se dize u clusterima - kada jedna instanca padne ostale instance pokrecu nove instance na drugim racunalima
- ![[Pasted image 20231023132120.png|500]] 
- problem bez kafke: razliciti sustavi trebaju svi dijeliti informacije
- rjesenje koje nudi kafka: svaki dio naseg sustava salje poruke na pojedini topic ili particiju unutar topica, a komponente koje citaju se pretplacuju na taj topic i preuzimaju ih
- ![[Pasted image 20231023132337.png|500]] 
- kafka se sastoji od Zookeper-a i Server-a (Broker na slici)
	- Zookeper - generalno odrzavanje klastera 
	- Broker - pohranjuju poruke (produceri im salju, consumeri ih uzimaju)
### Kafka lokalno
- najlakse podici uz Docker
- trebamo docker-compose.yaml i config.yaml i onda runnamo docker-compose up
- Komande:
	- docker exec kafka_kafka1_1 kafka-topics --bootstrap-server kafka_kafka1_1:9092 --list - lista topica
	- docker exec kafka_kafka1_1 kafka-topics --bootstrap-server kafka_kafka1_1:9092 --create --topic new_topic_name - kreacija novog topica
	- docker exec kafka_kafka1_1 kafka-topics --bootstrap-server kafka_kafka1_1:9092 --delete --topic new_topic_name - brisanje topica
	- docker exec --interactive --tty kafka_kafka1_1 kafka-console-producer --bootstrap-server kafka_kafka1_1:9092 --topic new_topic -> SLANJE PORUKA na zeljeni topic
	- docker exec --interactive --tty kafka_kafka1_1 kafka-console-consumer --bootstrap-server kafka_kafka1_1:9092 --topic new_topic --from-beginning -> Live slusanje poruka za topic (od zadnje procitane radi --from-beginning, i nastavlja slusati)
- Dalje koncepti
	- Particije - topics se mogu podijeliti na particije da se ubrza citanje
		- kad poruke stizu na topic, spremaju se u particije hashiranjem
	- Consumer grupe - svaki consumer mora biti u svojoj grupi 
		- konzumira poruke tako da se svaki consumer spoji na odredenu particiju i cita poruke s nje
		- Na primjer, ako su 3 particije, a samo jedan consumer u grupi, tada će taj consumer čitati poruke sa svih particija. Ako se doda još jedan consumer, jedan od njih će čitati s dvije particije, a drugi samo s jedne pa se tako već postiže određeni stupanj paralelizma. Dodavanjem još jednog consumera, svaki consumer čita s jedne particije i tada je broj consumera optmiziran za taj topic jer svaki consumer paralelno čita poruke s topica. U slučaju dodavanja još jednog consumera (sada ih ima 4, a particije su 3), jedan od consumera ne radi ništa jer su sve particije već zauzete.
		- --partitions (broj) -> naredba za kreiranje topica s particijama
			- docker exec <container_name> kafka-topics --bootstrap-server <container_name>:9092 --create --partitions 3 --topic <topic_name>
			- docker exec --interactive --tty <container_name> kafka-console-producer --bootstrap-server  <container_name>:9092 --property parse.key=true --property key.separator=: --topic <topic_name> -> da producer radi s kljucem i salje na particije, kljuc je naglasen ispred znaka “:”
			- consumer se pokrece isto, oni se automatski raspodjele
- Kowl
	- pokretanjem ovog docker-composea pokrenut je i Kowl, koji runna na localhost:8080 - graficko sucelje s kojim mozemo vidjeti kojoj particiji poruke pripadaju itd.