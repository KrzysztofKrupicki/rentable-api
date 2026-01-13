-- 1. CZYSZCZENIE
TRUNCATE TABLE equipment_reviews, user_reviews, reservations, equipment, subcategories, categories, users RESTART IDENTITY CASCADE;

-- UŻYTKOWNICY (Hasło dla wszystkich: zaq12WSX)
INSERT INTO users (id, email, password) VALUES 
('9a6a22f8-5a70-4adc-97e3-9addf7e8ebe6', 'admin@rentableapi.com', '$2a$12$0E3uHziU.07AjjBfESlBMOVcGdc9vQdxn00Evdmn3JT/AoKpAHm3.'),
('93a133f3-09f0-453a-975a-14dc018a2692', 'jan.kowalski@gmail.com', '$2a$12$0E3uHziU.07AjjBfESlBMOVcGdc9vQdxn00Evdmn3JT/AoKpAHm3.'),
('921b0e63-69db-4792-8a9a-2c8951eda72a', 'anna.nowak@gmail.com', '$2a$12$0E3uHziU.07AjjBfESlBMOVcGdc9vQdxn00Evdmn3JT/AoKpAHm3.'),
('c7c295d5-9455-4484-8206-9f21b9ba50f9', 'natalia.akacjowa@gmail.com', '$2a$12$0E3uHziU.07AjjBfESlBMOVcGdc9vQdxn00Evdmn3JT/AoKpAHm3.'),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 'tomasz.debowy@gmail.com', '$2a$12$0E3uHziU.07AjjBfESlBMOVcGdc9vQdxn00Evdmn3JT/AoKpAHm3.');

-- KATEGORIE
INSERT INTO categories (id, name, description) VALUES 
(1, 'Aparaty', 'Body lustrzanek, bezlusterkowców i średni format'),
(2, 'Obiektywy', 'Optyka stałoogniskowa, zoomy i anamorficzne'),
(3, 'Oświetlenie', 'Lampy błyskowe, światło ciągłe i modyfikatory'),
(4, 'Audio', 'Mikrofony, rejestratory i systemy bezprzewodowe'),
(5, 'Stabilizacja', 'Gimbale, statywy i slidery'),
(6, 'Drony', 'Bezzałogowe statki powietrzne i akcesoria'),
(7, 'Akcesoria', 'Dodatki, filtry i monitory');

-- PODKATEGORIE
INSERT INTO subcategories (id, name, description, category_id) VALUES 
(1, 'Bezlusterkowce', 'Aparaty z wymienną optyką bez lustra', 1),
(2, 'Lustrzanki', 'Klasyczne lustrzanki cyfrowe', 1),
(3, 'Stałoogniskowe', 'Obiektywy o stałej ogniskowej', 2),
(4, 'Zoomy', 'Obiektywy ze zmienną ogniskową', 2),
(5, 'Lampy', 'Mocne lampy LED', 3),
(6, 'Mikrofony krawatowe', 'Dyskretne mikrofony do wywiadów', 4),
(7, 'Gimbale ręczne', 'Stabilizatory do aparatów i telefonów', 5),
(8, 'Statywy wideo', 'Ciężkie statywy z głowicą olejową', 5),
(9, 'Drony FPV', 'Drony do szybkich ujęć dynamicznych', 6),
(10, 'Drony klasyczne', 'Klasyczne drony do fotografii z powietrza', 6),
(11, 'Monitoring', 'Monitory podglądowe', 7),
(12, 'Kamery sportowe', 'Małe i poręczne kamery 4K', 1);

-- SPRZĘT
INSERT INTO equipment (id, name, description, subcategory_id, equipment_owner_id, price_per_day, is_available) VALUES 
(1, 'Sony Alpha 7S III', 'Król nocnych zdjęć i wideo. 4K 120fps.', 1, '93a133f3-09f0-453a-975a-14dc018a2692', 300, true),
(2, 'Tamron 28-75mm f/2.8 G2 (Sony E)', 'Uniwersalny zoom na reportaże.', 4, '921b0e63-69db-4792-8a9a-2c8951eda72a', 80, true),
(3, 'Aputure LS 600d Pro', 'Potężna lampa LED, Sidus Link.', 5, 'c7c295d5-9455-4484-8206-9f21b9ba50f9', 250, true),
(4, 'DJI Mic 2', 'Zestaw do wywiadów, 32-bit float.', 6, '479a60fe-5439-4678-9d6e-18e93e39d7cd', 90, true),
(5, 'DJI RS 4 Pro (Combo)', 'Najnowszy stabilizator od DJI.', 7, '93a133f3-09f0-453a-975a-14dc018a2692', 180, true),
(6, 'DJI RS 3 Pro (Combo)', 'Stabilizator z silnikiem Focus.', 7, '93a133f3-09f0-453a-975a-14dc018a2692', 120, false),
(7, 'Sachtler Ace XL', 'Statyw z głowicą olejową.', 8, 'c7c295d5-9455-4484-8206-9f21b9ba50f9', 100, false),
(8, 'DJI Avata 2 (Fly More Combo)', 'Dron FPV, gogle Goggles 3.', 9, '479a60fe-5439-4678-9d6e-18e93e39d7cd', 220, true),
(9, 'Atomos Ninja V+', 'Monitor/Recorder ProRes RAW.', 11, '921b0e63-69db-4792-8a9a-2c8951eda72a', 120, false),
(10, 'DJI Osmo Action 4', 'Pancerna kamera sportowa.', 12, '479a60fe-5439-4678-9d6e-18e93e39d7cd', 80, true);

-- REZERWACJE
INSERT INTO reservations (user_id, equipment_id, start_date, end_date, status, total_price) VALUES 
('921b0e63-69db-4792-8a9a-2c8951eda72a', 1, '2026-01-02', '2026-01-04', 'finished', 900),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 2, '2026-01-03', '2026-01-03', 'finished', 80),
('c7c295d5-9455-4484-8206-9f21b9ba50f9', 1, '2026-01-08', '2026-01-09', 'finished', 600),
('93a133f3-09f0-453a-975a-14dc018a2692', 3, '2026-01-11', '2026-01-15', 'confirmed', 1250),
('921b0e63-69db-4792-8a9a-2c8951eda72a', 8, '2026-01-12', '2026-01-14', 'confirmed', 660),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 1, '2026-01-20', '2026-01-22', 'waiting_for_payment', 900),
('c7c295d5-9455-4484-8206-9f21b9ba50f9', 4, '2026-01-18', '2026-01-19', 'pending', 180),
('93a133f3-09f0-453a-975a-14dc018a2692', 5, '2026-01-28', '2026-01-28', 'confirmed', 180),
('921b0e63-69db-4792-8a9a-2c8951eda72a', 10, '2026-01-15', '2026-01-16', 'canceled', 160),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 2, '2026-01-20', '2026-01-22', 'confirmed', 240);

-- RECENZJE SPRZĘTU
INSERT INTO equipment_reviews (reviewer_id, equipment_id, rating, comment) VALUES 
('921b0e63-69db-4792-8a9a-2c8951eda72a', 1, 10, 'Absolutny potwór w nocy. ISO 12800 bez szumu.'),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 2, 9, 'Bardzo ostre szkło, lekkie.'),
('c7c295d5-9455-4484-8206-9f21b9ba50f9', 1, 8, 'Body świetne, ale matryca lekko brudna.'),
('921b0e63-69db-4792-8a9a-2c8951eda72a', 10, 9, 'Stabilizacja RockSteady to magia.'),
('93a133f3-09f0-453a-975a-14dc018a2692', 3, 10, 'Robi słońce w środku nocy.'),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 8, 7, 'Super zabawa, ale bateria krótko trzyma.'),
('c7c295d5-9455-4484-8206-9f21b9ba50f9', 4, 10, 'Dźwięk krystaliczny, 32-bit float ratuje życie.'),
('93a133f3-09f0-453a-975a-14dc018a2692', 5, 9, 'Blokady ramion ułatwiają pracę.'),
('921b0e63-69db-4792-8a9a-2c8951eda72a', 2, 8, 'Szybki AF, solidny koń roboczy.'),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 1, 10, 'Najlepszy aparat wideo w tej cenie.');

-- RECENZJE UŻYTKOWNIKÓW
INSERT INTO user_reviews (reviewer_id, reviewed_user_id, rating, comment) VALUES 
('93a133f3-09f0-453a-975a-14dc018a2692', '921b0e63-69db-4792-8a9a-2c8951eda72a', 10, 'Wzorowy kontakt, sprzęt zwrócony czysty.'),
('921b0e63-69db-4792-8a9a-2c8951eda72a', '479a60fe-5439-4678-9d6e-18e93e39d7cd', 9, 'Wszystko ok, punktualnie.'),
('93a133f3-09f0-453a-975a-14dc018a2692', 'c7c295d5-9455-4484-8206-9f21b9ba50f9', 5, 'Sprzęt w piachu, czyszczenie trwało godzinę.'),
('c7c295d5-9455-4484-8206-9f21b9ba50f9', '93a133f3-09f0-453a-975a-14dc018a2692', 10, 'Profesjonalista, dba o sprzęt.'),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', '921b0e63-69db-4792-8a9a-2c8951eda72a', 10, 'Anna to świadoma użytkowniczka dronów.'),
('93a133f3-09f0-453a-975a-14dc018a2692', '479a60fe-5439-4678-9d6e-18e93e39d7cd', 3, 'Uwaga! Porysowana soczewka obiektywu.'),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', 'c7c295d5-9455-4484-8206-9f21b9ba50f9', 8, 'Dobry kontakt, ale 2h spóźnienia.'),
('93a133f3-09f0-453a-975a-14dc018a2692', '921b0e63-69db-4792-8a9a-2c8951eda72a', 10, 'Ponownie bezproblemowo.'),
('479a60fe-5439-4678-9d6e-18e93e39d7cd', '93a133f3-09f0-453a-975a-14dc018a2692', 10, 'Szybko i sprawnie.'),
('93a133f3-09f0-453a-975a-14dc018a2692', 'c7c295d5-9455-4484-8206-9f21b9ba50f9', 7, 'Tym razem czysto, ale znów spóźnienie.');