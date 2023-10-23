# Rjesenja zadataka

### 1. Kreirajte topic “input-topic” s 3 particije.

docker exec zadaci_kafka1_1 kafka-topics --bootstrap-server zadaci_kafka1_1:9092 --create --partitions 3 --topic input-topic

### 2. Ispišite sve topice i provjerite je li input-topic kreiran.

docker exec zadaci_kafka1_1 kafka-topics --bootstrap-server zadaci_kafka1_1:9092 --list

### 3. Pošaljite poruke tako da specificirate ključeve; pošaljite barem 6 poruka s 3 različita ključa (parovi poruka s istim ključem).

docker exec --interactive --tty zadaci_kafka1_1 kafka-console-producer --bootstrap-server zadaci_kafka1_1:9092 --property parse.key=true --property key.separator=: --topic input-topic

\>Key:Message
x6

### 4. Pročitajte poslane poruke.

docker exec --interactive --tty zadaci_kafka1_1 kafka-console-consumer --bootstrap-server zadaci_kafka1_1:9092 --topic input-topic --from-beginning

### 5. Pogledajte stanje topica na Kowl UI-u (obratite pozornost na ključeve i kako oni utječu na particije).

Ključevi 2 i 3 korespondiraju particiji 2, a ključ 1 particiji 0.