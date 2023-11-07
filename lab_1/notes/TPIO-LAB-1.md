# Uvod
- Stvaramo svoju platformu na MS Azure cloud-u
	- unos, pohrana i transformacija podataka
- Prva vjezba - dohvat podataka za obradu na platformi
	- Azure cloud, Event Hubs servis za data stream, naš Producer program koji cita reddit API i salje podatke na Event Hubs te naš Consumer koji cita s Event Hubsa
	- kontejnerizacija nasih programa te deployment istih putem Container Apps na Azure


# Microsoft Azure
- Napravija account, konvencija imenovanja resursa su sva mala slova s "-" izmedu, brisi ih ako su nepotrebni jer sve trosi credits


# Event Hubs
- Distribuirana platforma za obradu toka podataka - niska latencija, dobra integracija unutar i van Azure-a
- Event Hubs je "ulaz" u event pipeline = ingestor dogadaja
- Obrada milijuna dogadaja u sekundi
- Podaci idu u cvorista dogadaja, mogu se transformirati i pohraniti putem drugih alata
- Usporedba s Kafkom - Event Hubs je PaaS (platform as a service, sve vec spremno za tebe), Kafka je IaaS (infrastructure as a service, sami manageamo verzije i sve to)
	- ![[Pasted image 20231106174614.png|400]]

##### Kreiranje Event Huba


# Container Apps