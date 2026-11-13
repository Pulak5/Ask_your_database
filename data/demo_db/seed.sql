-- Ask Your Database — seed data for demo_db (Pagila subset)
-- Synthetic but realistic DVD rental data.

BEGIN;

-- ============================================================
-- language (5 rows)  — omit language_id (GENERATED ALWAYS)
-- ============================================================
INSERT INTO language (name) VALUES
    ('English'),
    ('French'),
    ('Japanese'),
    ('Spanish'),
    ('German');

-- ============================================================
-- country (10 rows)
-- ============================================================
INSERT INTO country (country) VALUES
    ('United States'),   -- 1
    ('Canada'),          -- 2
    ('United Kingdom'),  -- 3
    ('France'),          -- 4
    ('Germany'),         -- 5
    ('Japan'),           -- 6
    ('Australia'),       -- 7
    ('Brazil'),          -- 8
    ('India'),           -- 9
    ('Mexico');          -- 10

-- ============================================================
-- city (20 rows)  — 2 per country
-- country_id  1=USA 2=Canada 3=UK 4=France 5=Germany
--             6=Japan 7=Australia 8=Brazil 9=India 10=Mexico
-- ============================================================
INSERT INTO city (city, country_id) VALUES
    ('New York',       1),   -- 1
    ('Los Angeles',    1),   -- 2
    ('Toronto',        2),   -- 3
    ('Vancouver',      2),   -- 4
    ('London',         3),   -- 5
    ('Manchester',     3),   -- 6
    ('Paris',          4),   -- 7
    ('Lyon',           4),   -- 8
    ('Berlin',         5),   -- 9
    ('Munich',         5),   -- 10
    ('Tokyo',          6),   -- 11
    ('Osaka',          6),   -- 12
    ('Sydney',         7),   -- 13
    ('Melbourne',      7),   -- 14
    ('São Paulo',      8),   -- 15
    ('Rio de Janeiro', 8),   -- 16
    ('Mumbai',         9),   -- 17
    ('Delhi',          9),   -- 18
    ('Mexico City',   10),   -- 19
    ('Guadalajara',   10);   -- 20

-- ============================================================
-- address (30 rows)
-- ============================================================
INSERT INTO address (address, address2, district, city_id, postal_code, phone) VALUES
    ('47 Broadway',         NULL,       'Manhattan',         1,  '10006',      '212-555-0101'),
    ('980 Fifth Avenue',    'Apt 3B',   'Manhattan',         1,  '10021',      '212-555-0102'),
    ('330 Sunset Blvd',     NULL,       'Hollywood',         2,  '90028',      '323-555-0201'),
    ('1200 Wilshire Blvd',  'Suite 5',  'Santa Monica',      2,  '90403',      '310-555-0202'),
    ('88 King Street W',    NULL,       'Downtown',          3,  'M5H 1G6',    '416-555-0301'),
    ('400 Robson Street',   'Unit 12',  'West End',          4,  'V6B 2B5',    '604-555-0401'),
    ('22 Baker Street',     NULL,       'Marylebone',        5,  'NW1 6XE',    '020-555-0501'),
    ('101 Oxford Street',   NULL,       'Westminster',       5,  'W1D 2HG',    '020-555-0502'),
    ('15 Portland Street',  'Flat 2',   'City Centre',       6,  'M1 3BE',     '0161-555-0601'),
    ('7 Rue de Rivoli',     NULL,       'Louvre',            7,  '75001',      '01-55-00-0701'),
    ('43 Avenue Kléber',    'Appt 9',   '16ème',             7,  '75116',      '01-55-00-0702'),
    ('12 Rue de la Part-Dieu', NULL,    'Part-Dieu',         8,  '69003',      '04-72-55-0801'),
    ('64 Unter den Linden', NULL,       'Mitte',             9,  '10117',      '030-555-0901'),
    ('29 Leopoldstraße',    'OG 1',     'Schwabing',        10,  '80802',      '089-555-1001'),
    ('5-3 Chiyoda',         NULL,       'Chiyoda-ku',       11,  '100-0001',   '03-5555-1101'),
    ('2-1 Namba',           'Bldg B',   'Naniwa-ku',        12,  '556-0011',   '06-5555-1201'),
    ('88 George Street',    NULL,       'The Rocks',        13,  '2000',       '02-5555-1301'),
    ('17 Collins Street',   'Level 4',  'CBD',              14,  '3000',       '03-5555-1401'),
    ('Av. Paulista 1578',   NULL,       'Bela Vista',       15,  '01310-200',  '011-5555-1501'),
    ('R. da Quitanda 86',   'Bloco 3',  'Centro',           16,  '20091-005',  '021-5555-1601'),
    ('14 Marine Drive',     NULL,       'Churchgate',       17,  '400020',     '022-5555-1701'),
    ('7 Connaught Place',   'Block C',  'New Delhi',        18,  '110001',     '011-5555-1801'),
    ('Paseo de la Reforma 350', NULL,   'Cuauhtémoc',       19,  '06600',      '55-5555-1901'),
    ('Av. Juárez 76',       'Piso 2',   'Centro',           19,  '06010',      '55-5555-1902'),
    ('Blvd. Puerta de Hierro 45', NULL, 'Zapopan',          20,  '45116',      '33-5555-2001'),
    ('300 Park Avenue',     'Fl 12',    'Midtown',          1,   '10022',      '212-555-0103'),
    ('555 California Street', NULL,     'Financial District',2,   '90210',      '310-555-0203'),
    ('9 Charing Cross Rd',  NULL,       'Covent Garden',    5,   'WC2H 0HG',   '020-555-0503'),
    ('80 Bleecker Street',  'Unit 4A',  'Greenwich Village',1,   '10012',      '212-555-0104'),
    ('700 W Olympic Blvd',  NULL,       'Downtown',         2,   '90015',      '213-555-0204');

-- ============================================================
-- category (16 rows)
-- ============================================================
INSERT INTO category (name) VALUES
    ('Action'),       -- 1
    ('Animation'),    -- 2
    ('Children'),     -- 3
    ('Classics'),     -- 4
    ('Comedy'),       -- 5
    ('Documentary'),  -- 6
    ('Drama'),        -- 7
    ('Family'),       -- 8
    ('Foreign'),      -- 9
    ('Games'),        -- 10
    ('Horror'),       -- 11
    ('Music'),        -- 12
    ('New'),          -- 13
    ('Sci-Fi'),       -- 14
    ('Sports'),       -- 15
    ('Travel');       -- 16

-- ============================================================
-- actor (30 rows)
-- ============================================================
INSERT INTO actor (first_name, last_name) VALUES
    ('James',    'Harrison'),   -- 1
    ('Emily',    'Stone'),      -- 2
    ('Michael',  'Reeves'),     -- 3
    ('Sophia',   'Mendez'),     -- 4
    ('David',    'Chen'),       -- 5
    ('Olivia',   'Parker'),     -- 6
    ('William',  'Ford'),       -- 7
    ('Ava',      'Rodriguez'),  -- 8
    ('Daniel',   'Kim'),        -- 9
    ('Isabella', 'Wright'),     -- 10
    ('Matthew',  'Turner'),     -- 11
    ('Mia',      'Johnson'),    -- 12
    ('Christopher','Brown'),    -- 13
    ('Charlotte','Davis'),      -- 14
    ('Joshua',   'Wilson'),     -- 15
    ('Amelia',   'Taylor'),     -- 16
    ('Andrew',   'Martinez'),   -- 17
    ('Harper',   'Anderson'),   -- 18
    ('Ryan',     'Thomas'),     -- 19
    ('Evelyn',   'Jackson'),    -- 20
    ('Nathan',   'White'),      -- 21
    ('Abigail',  'Harris'),     -- 22
    ('Kevin',    'Clark'),      -- 23
    ('Ella',     'Lewis'),      -- 24
    ('Brandon',  'Lee'),        -- 25
    ('Scarlett', 'Walker'),     -- 26
    ('Tyler',    'Hall'),       -- 27
    ('Grace',    'Allen'),      -- 28
    ('Logan',    'Young'),      -- 29
    ('Zoe',      'King');       -- 30

-- ============================================================
-- film (50 rows)  — language_id=1 (English)
-- ============================================================
INSERT INTO film (title, description, release_year, language_id, rental_rate, length, rating) VALUES
    ('Galactic Odyssey',        'An astronaut drifts through a wormhole and discovers a new civilisation.',                    2010, 1, 4.99, 142, 'PG-13'),
    ('Shadow of the Tiger',     'A retired detective hunts a dangerous criminal through the streets of Hong Kong.',            2005, 1, 2.99, 118, 'R'),
    ('Whispers in the Wind',    'A romance blossoms between two strangers on a cross-country train.',                          2008, 1, 3.99, 105, 'PG'),
    ('Iron Fist Rising',        'A martial-arts champion battles a corrupt government with nothing but his fists.',            2003, 1, 1.99,  98, 'R'),
    ('The Last Garden',         'A botanist discovers a mythical garden that holds the secret to eternal life.',               2015, 1, 5.99, 130, 'G'),
    ('Neon Labyrinth',          'In a cyberpunk metropolis, a hacker uncovers a corporate conspiracy.',                        2017, 1, 6.99, 155, 'PG-13'),
    ('Crimson Shores',          'A coastal town is haunted by the ghost of a fisherman lost at sea.',                          2006, 1, 2.99, 112, 'PG'),
    ('The Jazz Heist',          'Three musicians plan the most elaborate bank robbery ever conceived.',                        2011, 1, 4.99, 125, 'PG-13'),
    ('Desert Mirage',           'Soldiers stranded in the Sahara discover an ancient buried city.',                           2009, 1, 3.99, 138, 'PG-13'),
    ('Polar Express',           'A child embarks on a magical train ride to the North Pole on Christmas Eve.',                2000, 1, 0.99,  95, 'G'),
    ('Echoes of Tomorrow',      'A scientist invents a device that shows glimpses of the future, with dire consequences.',    2016, 1, 7.99, 160, 'PG-13'),
    ('Midnight Carnival',       'A travelling carnival arrives at a small town, bringing dark secrets with it.',               2007, 1, 2.99, 108, 'R'),
    ('Sapphire Sky',            'A young painter finds her greatest muse in a haunted lighthouse.',                           2013, 1, 3.99,  90, 'PG'),
    ('Thunder Road',            'A reckless trucker races across America to deliver a vital organ in time.',                   2004, 1, 1.99, 102, 'PG-13'),
    ('The Clockmaker',          'A reclusive clockmaker builds a machine that can stop time.',                                 2018, 1, 8.99, 170, 'PG'),
    ('Broken Compass',          'A cartographer maps uncharted jungles and falls in love with a local guide.',                2012, 1, 4.99, 115, 'PG'),
    ('Velvet Underground',      'A jazz singer navigates the criminal underworld of 1940s Chicago.',                           2001, 1, 2.99, 128, 'R'),
    ('Storm Chasers',           'A team of meteorologists chase the most powerful tornado ever recorded.',                     2014, 1, 5.99, 100, 'PG'),
    ('The Forgotten Island',    'Castaways discover their island has been hiding an ancient civilisation for centuries.',       2019, 1, 9.99, 148, 'PG-13'),
    ('Autumn Leaves',           'An estranged father reconnects with his daughter during one last autumn.',                    2002, 1, 1.99,  88, 'PG'),
    ('Code Red',                'A cyber-security expert races to stop a global virus before it crashes world markets.',       2016, 1, 6.99, 135, 'PG-13'),
    ('The Silver Locket',       'A widow inherits a locket that opens a door to her late husband\'s secret life.',             2008, 1, 3.99, 110, 'PG'),
    ('Volcano Bay',             'Villagers must evacuate when a dormant volcano awakens beneath a tropical resort.',           2011, 1, 4.99, 118, 'PG-13'),
    ('Barefoot in the Rain',    'A coming-of-age story set during a summer on the coast of Ireland.',                         2003, 1, 1.99,  82, 'G'),
    ('Project Nexus',           'A black-ops soldier uncovers a secret government programme that creates super-soldiers.',    2015, 1, 5.99, 150, 'R'),
    ('The Paper Lantern',       'Set in feudal Japan, a samurai defends a village from ruthless warlords.',                   2007, 1, 3.99, 132, 'PG-13'),
    ('Ocean Protocol',          'Marine biologists race to save a rare whale species from poachers.',                         2013, 1, 4.99, 108, 'PG'),
    ('Double Cross',            'Two rival detectives discover they are hunting the same killer from opposite sides.',         2009, 1, 2.99, 122, 'R'),
    ('Stardust Boulevard',      'A faded movie star attempts a dramatic comeback in 1970s Hollywood.',                        2000, 1, 0.99,  96, 'PG-13'),
    ('Wild at Heart',           'An unlikely pair of animals travel across a continent to find their lost family.',            2005, 1, 1.99,  78, 'G'),
    ('The Last Confession',     'A priest discovers he is the only witness to a cardinal\'s murder.',                          2017, 1, 7.99, 145, 'R'),
    ('Sunrise Over Kyoto',      'A travel writer rediscovers her passion for life on a solo trip through Japan.',              2012, 1, 3.99,  95, 'PG'),
    ('Rogue Protocol',          'An AI gains sentience and decides the best way to protect humans is to control them.',       2018, 1, 8.99, 162, 'PG-13'),
    ('The Diamond Coast',       'A jewel thief retires, but one last heist pulls him back into the game.',                   2010, 1, 4.99, 125, 'R'),
    ('Carnival of Souls',       'A group of friends encounter supernatural forces at an abandoned amusement park.',           2004, 1, 2.99, 105, 'R'),
    ('The Quiet Storm',         'A concert pianist loses her hearing and must redefine her relationship with music.',          2014, 1, 5.99, 118, 'PG'),
    ('Frozen Peaks',            'A mountaineer faces an avalanche and must survive weeks alone in the Himalayas.',            2006, 1, 2.99, 130, 'PG-13'),
    ('Night Market',            'A street vendor in Bangkok discovers she is the only one who can stop a food monopoly.',     2019, 1, 9.99, 112, 'PG-13'),
    ('The Last Soldier',        'A WWII veteran searches for a comrade he left behind on the battlefield.',                   2001, 1, 1.99, 155, 'PG-13'),
    ('Cosmic Ballet',           'An animated tale of stars and planets learning to dance in harmony.',                         2008, 1, 3.99,  72, 'G'),
    ('Sunken City',             'Deep-sea explorers find the ruins of Atlantis — and its inhabitants still living there.',    2015, 1, 6.99, 140, 'PG-13'),
    ('Red Tape',                'A satirical comedy about a government bureaucrat who tries to speed up his own promotion.',  2011, 1, 4.99,  95, 'PG-13'),
    ('Phantom District',        'A journalist investigates a neighbourhood that disappears every full moon.',                  2016, 1, 7.99, 115, 'R'),
    ('Homeward Journey',        'A dog and two cats travel 500 miles across Canada to find their family.',                    2002, 1, 1.99,  80, 'G'),
    ('The Ironclad',            'An 1860s naval captain faces mutiny during the most decisive sea battle of the Civil War.',  2009, 1, 3.99, 148, 'PG-13'),
    ('Gravity Well',            'Astronauts must repair a wormhole generator before Earth is consumed by a singularity.',     2017, 1, 7.99, 165, 'PG-13'),
    ('The Mapmaker',            'A cartographer in the 1500s charts territories never before recorded by Europeans.',         2003, 1, 1.99, 122, 'PG'),
    ('Lucky Strike',            'A down-on-his-luck lottery winner discovers the prize is cursed.',                           2013, 1, 4.99, 100, 'PG-13'),
    ('Crimson Tide Rising',     'A journalist exposes corruption in a small-town police department.',                          2020, 1, 9.99, 135, 'R'),
    ('The Artisan',             'A master glassblower passes his craft to an unlikely apprentice in Venice.',                  2007, 1, 3.99, 110, 'PG');

-- ============================================================
-- film_category  (each film gets 1-2 categories)
-- category ids: Action=1 Animation=2 Children=3 Classics=4 Comedy=5
--               Documentary=6 Drama=7 Family=8 Foreign=9 Games=10
--               Horror=11 Music=12 New=13 Sci-Fi=14 Sports=15 Travel=16
-- ============================================================
INSERT INTO film_category (film_id, category_id) VALUES
    (1,  14), (1,  13),   -- Galactic Odyssey: Sci-Fi, New
    (2,   1),             -- Shadow of the Tiger: Action
    (3,   7),             -- Whispers in the Wind: Drama
    (4,   1),             -- Iron Fist Rising: Action
    (5,   6), (5,   8),   -- The Last Garden: Documentary, Family
    (6,  14),             -- Neon Labyrinth: Sci-Fi
    (7,  11),             -- Crimson Shores: Horror
    (8,  12), (8,   5),   -- The Jazz Heist: Music, Comedy
    (9,   9),             -- Desert Mirage: Foreign
    (10,  8), (10,  3),   -- Polar Express: Family, Children
    (11, 14), (11,  7),   -- Echoes of Tomorrow: Sci-Fi, Drama
    (12, 11),             -- Midnight Carnival: Horror
    (13,  7),             -- Sapphire Sky: Drama
    (14,  1), (14, 15),   -- Thunder Road: Action, Sports
    (15,  4), (15,  7),   -- The Clockmaker: Classics, Drama
    (16, 16), (16,  7),   -- Broken Compass: Travel, Drama
    (17, 12), (17,  4),   -- Velvet Underground: Music, Classics
    (18, 15),             -- Storm Chasers: Sports
    (19, 16), (19,  9),   -- The Forgotten Island: Travel, Foreign
    (20,  7),             -- Autumn Leaves: Drama
    (21, 14), (21,  1),   -- Code Red: Sci-Fi, Action
    (22,  7),             -- The Silver Locket: Drama
    (23,  1),             -- Volcano Bay: Action
    (24,  8), (24,  3),   -- Barefoot in the Rain: Family, Children
    (25,  1),             -- Project Nexus: Action
    (26,  9), (26,  4),   -- The Paper Lantern: Foreign, Classics
    (27,  6),             -- Ocean Protocol: Documentary
    (28,  1),             -- Double Cross: Action
    (29,  4), (29,  7),   -- Stardust Boulevard: Classics, Drama
    (30,  8), (30,  3),   -- Wild at Heart: Family, Children
    (31, 11),             -- The Last Confession: Horror
    (32, 16), (32,  7),   -- Sunrise Over Kyoto: Travel, Drama
    (33, 14),             -- Rogue Protocol: Sci-Fi
    (34,  1),             -- The Diamond Coast: Action
    (35, 11),             -- Carnival of Souls: Horror
    (36, 12), (36,  7),   -- The Quiet Storm: Music, Drama
    (37, 16),             -- Frozen Peaks: Travel
    (38, 16), (38,  9),   -- Night Market: Travel, Foreign
    (39,  7), (39,  4),   -- The Last Soldier: Drama, Classics
    (40,  2), (40,  8),   -- Cosmic Ballet: Animation, Family
    (41, 14),             -- Sunken City: Sci-Fi
    (42,  5),             -- Red Tape: Comedy
    (43, 11),             -- Phantom District: Horror
    (44,  8), (44,  3),   -- Homeward Journey: Family, Children
    (45,  4),             -- The Ironclad: Classics
    (46, 14), (46,  1),   -- Gravity Well: Sci-Fi, Action
    (47,  4), (47,  9),   -- The Mapmaker: Classics, Foreign
    (48,  5),             -- Lucky Strike: Comedy
    (49,  1),             -- Crimson Tide Rising: Action
    (50,  7), (50,  9);   -- The Artisan: Drama, Foreign

-- ============================================================
-- film_actor (mix of 2-5 actors per film)
-- ============================================================
INSERT INTO film_actor (actor_id, film_id) VALUES
    (1, 1),(5, 1),(11, 1),
    (2, 2),(7, 2),(13, 2),(19, 2),
    (3, 3),(8, 3),(14, 3),
    (4, 4),(9, 4),(15, 4),(20, 4),(25, 4),
    (6, 5),(10, 5),(16, 5),
    (1, 6),(12, 6),(22, 6),(28, 6),
    (2, 7),(17, 7),(23, 7),
    (3, 8),(7, 8),(18, 8),(24, 8),
    (4, 9),(13, 9),(26, 9),(30, 9),
    (5, 10),(11, 10),(21, 10),
    (6, 11),(15, 11),(27, 11),(29, 11),
    (8, 12),(14, 12),(20, 12),
    (9, 13),(16, 13),(22, 13),(28, 13),
    (10, 14),(17, 14),(23, 14),
    (11, 15),(19, 15),(25, 15),(30, 15),
    (12, 16),(18, 16),(24, 16),
    (13, 17),(21, 17),(27, 17),(29, 17),
    (14, 18),(20, 18),(26, 18),
    (1, 19),(7, 19),(15, 19),(22, 19),
    (2, 20),(8, 20),(16, 20),
    (3, 21),(9, 21),(17, 21),(23, 21),(30, 21),
    (4, 22),(10, 22),(18, 22),
    (5, 23),(12, 23),(24, 23),(29, 23),
    (6, 24),(13, 24),(20, 24),
    (7, 25),(14, 25),(21, 25),(27, 25),
    (8, 26),(15, 26),(22, 26),(28, 26),
    (9, 27),(16, 27),(23, 27),
    (10, 28),(17, 28),(24, 28),(30, 28),
    (11, 29),(19, 29),(25, 29),
    (12, 30),(20, 30),(26, 30),(29, 30),
    (1, 31),(13, 31),(21, 31),(28, 31),
    (2, 32),(8, 32),(18, 32),
    (3, 33),(9, 33),(15, 33),(22, 33),(27, 33),
    (4, 34),(10, 34),(20, 34),
    (5, 35),(11, 35),(17, 35),(23, 35),
    (6, 36),(14, 36),(24, 36),(30, 36),
    (7, 37),(16, 37),(25, 37),
    (8, 38),(13, 38),(19, 38),(26, 38),
    (9, 39),(12, 39),(21, 39),(28, 39),
    (10, 40),(18, 40),(29, 40),
    (1, 41),(11, 41),(17, 41),(23, 41),(30, 41),
    (2, 42),(7, 42),(20, 42),
    (3, 43),(9, 43),(16, 43),(24, 43),
    (4, 44),(10, 44),(22, 44),
    (5, 45),(13, 45),(19, 45),(27, 45),
    (6, 46),(12, 46),(25, 46),(29, 46),
    (7, 47),(15, 47),(21, 47),(28, 47),
    (8, 48),(14, 48),(26, 48),
    (9, 49),(11, 49),(18, 49),(23, 49),(30, 49),
    (10, 50),(16, 50),(22, 50),(27, 50);

-- ============================================================
-- store (2 rows) — manager_staff_id=NULL initially
-- address_id: 1 (New York/47 Broadway), 3 (LA/330 Sunset Blvd)
-- ============================================================
INSERT INTO store (manager_staff_id, address_id) VALUES
    (NULL, 1),   -- store 1
    (NULL, 3);   -- store 2

-- ============================================================
-- staff (2 rows)
-- ============================================================
INSERT INTO staff (first_name, last_name, address_id, email, store_id, active, username) VALUES
    ('Mike',   'Hillyer',  2, 'mike.hillyer@sakilastaff.com', 1, true, 'mike'),
    ('Jon',    'Stephens', 4, 'jon.stephens@sakilastaff.com', 2, true, 'jon');

-- wire manager_staff_id now that staff rows exist
UPDATE store SET manager_staff_id = 1 WHERE store_id = 1;
UPDATE store SET manager_staff_id = 2 WHERE store_id = 2;

-- ============================================================
-- customer (30 rows) — address_id 5-30 (remaining addresses)
-- ============================================================
INSERT INTO customer (store_id, first_name, last_name, email, address_id, active) VALUES
    (1, 'Patricia', 'Johnson',   'patricia.johnson@example.com',    5,  true),
    (2, 'Robert',   'Williams',  'robert.williams@example.com',     6,  true),
    (1, 'Linda',    'Brown',     'linda.brown@example.com',         7,  true),
    (2, 'Barbara',  'Jones',     'barbara.jones@example.com',       8,  true),
    (1, 'Richard',  'Garcia',    'richard.garcia@example.com',      9,  true),
    (2, 'Susan',    'Miller',    'susan.miller@example.com',       10,  true),
    (1, 'Joseph',   'Davis',     'joseph.davis@example.com',       11,  true),
    (2, 'Jessica',  'Martinez',  'jessica.martinez@example.com',   12,  true),
    (1, 'Thomas',   'Hernandez', 'thomas.hernandez@example.com',   13,  true),
    (2, 'Sarah',    'Lopez',     'sarah.lopez@example.com',        14,  true),
    (1, 'Charles',  'Gonzalez',  'charles.gonzalez@example.com',   15,  true),
    (2, 'Karen',    'Wilson',    'karen.wilson@example.com',       16,  true),
    (1, 'Christopher','Anderson','chris.anderson@example.com',     17,  true),
    (2, 'Nancy',    'Taylor',    'nancy.taylor@example.com',       18,  true),
    (1, 'Daniel',   'Thomas',    'daniel.thomas@example.com',      19,  true),
    (2, 'Lisa',     'Jackson',   'lisa.jackson@example.com',       20,  true),
    (1, 'Paul',     'White',     'paul.white@example.com',         21,  true),
    (2, 'Betty',    'Harris',    'betty.harris@example.com',       22,  true),
    (1, 'Mark',     'Sanchez',   'mark.sanchez@example.com',       23,  true),
    (2, 'Margaret', 'Clark',     'margaret.clark@example.com',     24,  true),
    (1, 'Donald',   'Ramirez',   'donald.ramirez@example.com',     25,  true),
    (2, 'Sandra',   'Lewis',     'sandra.lewis@example.com',       26,  true),
    (1, 'Steven',   'Robinson',  'steven.robinson@example.com',    27,  true),
    (2, 'Ashley',   'Walker',    'ashley.walker@example.com',      28,  true),
    (1, 'Kenneth',  'Young',     'kenneth.young@example.com',      29,  true),
    (2, 'Dorothy',  'Allen',     'dorothy.allen@example.com',      30,  true),
    (1, 'Andrew',   'King',      'andrew.king@example.com',         5,  true),
    (2, 'Kimberly', 'Wright',    'kimberly.wright@example.com',     6,  false),
    (1, 'Joshua',   'Scott',     'joshua.scott@example.com',        7,  true),
    (2, 'Donna',    'Green',     'donna.green@example.com',         8,  false);

-- ============================================================
-- inventory (100 rows) — film_id 1-50, store_id 1 or 2
-- ============================================================
INSERT INTO inventory (film_id, store_id) VALUES
    (1,1),(1,2),(2,1),(2,2),(3,1),
    (3,2),(4,1),(4,2),(5,1),(5,2),
    (6,1),(6,2),(7,1),(7,2),(8,1),
    (8,2),(9,1),(9,2),(10,1),(10,2),
    (11,1),(11,2),(12,1),(12,2),(13,1),
    (13,2),(14,1),(14,2),(15,1),(15,2),
    (16,1),(16,2),(17,1),(17,2),(18,1),
    (18,2),(19,1),(19,2),(20,1),(20,2),
    (21,1),(21,2),(22,1),(22,2),(23,1),
    (23,2),(24,1),(24,2),(25,1),(25,2),
    (26,1),(26,2),(27,1),(27,2),(28,1),
    (28,2),(29,1),(29,2),(30,1),(30,2),
    (31,1),(31,2),(32,1),(32,2),(33,1),
    (33,2),(34,1),(34,2),(35,1),(35,2),
    (36,1),(36,2),(37,1),(37,2),(38,1),
    (38,2),(39,1),(39,2),(40,1),(40,2),
    (41,1),(41,2),(42,1),(42,2),(43,1),
    (43,2),(44,1),(44,2),(45,1),(45,2),
    (46,1),(46,2),(47,1),(47,2),(48,1),
    (48,2),(49,1),(49,2),(50,1),(50,2);

-- ============================================================
-- rental (200 rows)
-- inventory_id 1-100, customer_id 1-30, staff_id 1 or 2
-- ~20 without return_date (NULL)
-- ============================================================
INSERT INTO rental (rental_date, inventory_id, customer_id, return_date, staff_id) VALUES
    ('2005-05-25 11:30:37', 1,  1,  '2005-05-28 09:15:00', 1),
    ('2005-05-25 12:04:22', 2,  2,  '2005-05-27 10:00:00', 2),
    ('2005-05-26 08:55:00', 3,  3,  '2005-05-29 14:30:00', 1),
    ('2005-05-26 09:40:11', 4,  4,  '2005-05-30 11:00:00', 2),
    ('2005-05-27 10:10:00', 5,  5,  '2005-05-31 09:00:00', 1),
    ('2005-05-27 13:22:00', 6,  6,  '2005-06-01 15:20:00', 2),
    ('2005-05-28 09:00:00', 7,  7,  '2005-06-01 12:00:00', 1),
    ('2005-05-28 11:45:00', 8,  8,  '2005-06-02 10:30:00', 2),
    ('2005-05-29 14:00:00', 9,  9,  '2005-06-02 08:00:00', 1),
    ('2005-05-29 15:33:00',10, 10,  '2005-06-03 11:00:00', 2),
    ('2005-06-01 09:00:00',11, 11,  '2005-06-04 10:00:00', 1),
    ('2005-06-01 10:30:00',12, 12,  '2005-06-05 09:30:00', 2),
    ('2005-06-02 08:45:00',13, 13,  '2005-06-06 08:00:00', 1),
    ('2005-06-02 11:20:00',14, 14,  '2005-06-07 14:00:00', 2),
    ('2005-06-03 09:15:00',15, 15,  '2005-06-07 09:00:00', 1),
    ('2005-06-03 13:00:00',16, 16,  '2005-06-08 10:30:00', 2),
    ('2005-06-04 10:00:00',17, 17,  '2005-06-09 08:00:00', 1),
    ('2005-06-04 14:30:00',18, 18,  '2005-06-10 11:00:00', 2),
    ('2005-06-05 09:00:00',19, 19,  '2005-06-10 09:30:00', 1),
    ('2005-06-05 11:15:00',20, 20,  '2005-06-11 10:00:00', 2),
    ('2005-06-06 08:30:00',21, 21,  '2005-06-11 08:30:00', 1),
    ('2005-06-06 12:00:00',22, 22,  '2005-06-12 12:00:00', 2),
    ('2005-06-07 10:00:00',23, 23,  '2005-06-13 09:00:00', 1),
    ('2005-06-07 14:00:00',24, 24,  '2005-06-14 10:00:00', 2),
    ('2005-06-08 09:30:00',25, 25,  '2005-06-14 08:30:00', 1),
    ('2005-06-08 13:30:00',26, 26,  '2005-06-15 11:00:00', 2),
    ('2005-06-09 10:00:00',27, 27,  '2005-06-15 09:00:00', 1),
    ('2005-06-09 14:45:00',28, 28,  '2005-06-16 10:30:00', 2),
    ('2005-06-10 09:00:00',29, 29,  '2005-06-16 08:00:00', 1),
    ('2005-06-10 12:30:00',30, 30,  '2005-06-17 11:00:00', 2),
    ('2005-06-11 10:30:00',31,  1,  '2005-06-17 09:30:00', 1),
    ('2005-06-11 14:00:00',32,  2,  '2005-06-18 10:00:00', 2),
    ('2005-06-12 09:00:00',33,  3,  '2005-06-19 08:30:00', 1),
    ('2005-06-12 11:45:00',34,  4,  '2005-06-20 11:00:00', 2),
    ('2005-06-13 10:00:00',35,  5,  '2005-06-20 09:00:00', 1),
    ('2005-06-13 13:30:00',36,  6,  '2005-06-21 10:30:00', 2),
    ('2005-06-14 09:00:00',37,  7,  '2005-06-21 08:00:00', 1),
    ('2005-06-14 12:00:00',38,  8,  '2005-06-22 11:00:00', 2),
    ('2005-06-15 10:00:00',39,  9,  '2005-06-22 09:30:00', 1),
    ('2005-06-15 14:30:00',40, 10,  '2005-06-23 10:00:00', 2),
    ('2005-06-16 09:30:00',41, 11,  '2005-06-23 08:30:00', 1),
    ('2005-06-16 13:00:00',42, 12,  '2005-06-24 11:00:00', 2),
    ('2005-06-17 10:00:00',43, 13,  '2005-06-25 09:00:00', 1),
    ('2005-06-17 14:00:00',44, 14,  '2005-06-26 10:30:00', 2),
    ('2005-06-18 09:00:00',45, 15,  '2005-06-26 08:00:00', 1),
    ('2005-06-18 12:30:00',46, 16,  '2005-06-27 11:00:00', 2),
    ('2005-06-19 10:30:00',47, 17,  '2005-06-27 09:30:00', 1),
    ('2005-06-19 14:00:00',48, 18,  '2005-06-28 10:00:00', 2),
    ('2005-06-20 09:00:00',49, 19,  '2005-06-28 08:00:00', 1),
    ('2005-06-20 13:00:00',50, 20,  '2005-06-29 11:00:00', 2),
    ('2005-06-21 10:00:00',51, 21,  '2005-06-29 09:00:00', 1),
    ('2005-06-21 14:30:00',52, 22,  '2005-06-30 10:30:00', 2),
    ('2005-06-22 09:30:00',53, 23,  '2005-06-30 08:30:00', 1),
    ('2005-06-22 13:00:00',54, 24,  '2005-07-01 11:00:00', 2),
    ('2005-06-23 10:00:00',55, 25,  '2005-07-01 09:00:00', 1),
    ('2005-06-23 14:00:00',56, 26,  '2005-07-02 10:00:00', 2),
    ('2005-06-24 09:00:00',57, 27,  '2005-07-02 08:00:00', 1),
    ('2005-06-24 12:30:00',58, 28,  '2005-07-03 11:00:00', 2),
    ('2005-06-25 10:30:00',59, 29,  '2005-07-03 09:30:00', 1),
    ('2005-06-25 14:00:00',60, 30,  '2005-07-04 10:00:00', 2),
    ('2005-06-26 09:00:00',61,  1,  '2005-07-04 08:00:00', 1),
    ('2005-06-26 13:30:00',62,  2,  '2005-07-05 11:00:00', 2),
    ('2005-06-27 10:00:00',63,  3,  '2005-07-05 09:00:00', 1),
    ('2005-06-27 14:30:00',64,  4,  '2005-07-06 10:30:00', 2),
    ('2005-06-28 09:30:00',65,  5,  '2005-07-06 08:30:00', 1),
    ('2005-06-28 13:00:00',66,  6,  '2005-07-07 11:00:00', 2),
    ('2005-06-29 10:00:00',67,  7,  '2005-07-07 09:00:00', 1),
    ('2005-06-29 14:00:00',68,  8,  '2005-07-08 10:00:00', 2),
    ('2005-06-30 09:00:00',69,  9,  '2005-07-08 08:00:00', 1),
    ('2005-06-30 12:30:00',70, 10,  '2005-07-09 11:00:00', 2),
    ('2005-07-01 10:30:00',71, 11,  '2005-07-09 09:30:00', 1),
    ('2005-07-01 14:00:00',72, 12,  '2005-07-10 10:00:00', 2),
    ('2005-07-02 09:00:00',73, 13,  '2005-07-10 08:00:00', 1),
    ('2005-07-02 13:00:00',74, 14,  '2005-07-11 11:00:00', 2),
    ('2005-07-03 10:00:00',75, 15,  '2005-07-11 09:00:00', 1),
    ('2005-07-03 14:30:00',76, 16,  '2005-07-12 10:30:00', 2),
    ('2005-07-04 09:30:00',77, 17,  '2005-07-12 08:30:00', 1),
    ('2005-07-04 13:00:00',78, 18,  '2005-07-13 11:00:00', 2),
    ('2005-07-05 10:00:00',79, 19,  '2005-07-13 09:00:00', 1),
    ('2005-07-05 14:00:00',80, 20,  '2005-07-14 10:00:00', 2),
    ('2005-07-06 09:00:00',81, 21,  '2005-07-14 08:00:00', 1),
    ('2005-07-06 12:30:00',82, 22,  '2005-07-15 11:00:00', 2),
    ('2005-07-07 10:30:00',83, 23,  '2005-07-15 09:30:00', 1),
    ('2005-07-07 14:00:00',84, 24,  '2005-07-16 10:00:00', 2),
    ('2005-07-08 09:00:00',85, 25,  '2005-07-16 08:00:00', 1),
    ('2005-07-08 13:30:00',86, 26,  '2005-07-17 11:00:00', 2),
    ('2005-07-09 10:00:00',87, 27,  '2005-07-17 09:00:00', 1),
    ('2005-07-09 14:30:00',88, 28,  '2005-07-18 10:30:00', 2),
    ('2005-07-10 09:30:00',89, 29,  '2005-07-18 08:30:00', 1),
    ('2005-07-10 13:00:00',90, 30,  '2005-07-19 11:00:00', 2),
    ('2005-07-11 10:00:00',91,  1,  '2005-07-19 09:00:00', 1),
    ('2005-07-11 14:00:00',92,  2,  '2005-07-20 10:00:00', 2),
    ('2005-07-12 09:00:00',93,  3,  '2005-07-20 08:00:00', 1),
    ('2005-07-12 12:30:00',94,  4,  '2005-07-21 11:00:00', 2),
    ('2005-07-13 10:30:00',95,  5,  '2005-07-21 09:30:00', 1),
    ('2005-07-13 14:00:00',96,  6,  '2005-07-22 10:00:00', 2),
    ('2005-07-14 09:00:00',97,  7,  '2005-07-22 08:00:00', 1),
    ('2005-07-14 13:00:00',98,  8,  '2005-07-23 11:00:00', 2),
    ('2005-07-15 10:00:00',99,  9,  '2005-07-23 09:00:00', 1),
    ('2005-07-15 14:30:00',100,10,  '2005-07-24 10:30:00', 2),
    ('2005-07-16 09:30:00',  1, 11, '2005-07-24 08:30:00', 1),
    ('2005-07-16 13:00:00',  2, 12, '2005-07-25 11:00:00', 2),
    ('2005-07-17 10:00:00',  3, 13, '2005-07-25 09:00:00', 1),
    ('2005-07-17 14:00:00',  4, 14, '2005-07-26 10:00:00', 2),
    ('2005-07-18 09:00:00',  5, 15, '2005-07-26 08:00:00', 1),
    ('2005-07-18 12:30:00',  6, 16, '2005-07-27 11:00:00', 2),
    ('2005-07-19 10:30:00',  7, 17, '2005-07-27 09:30:00', 1),
    ('2005-07-19 14:00:00',  8, 18, '2005-07-28 10:00:00', 2),
    ('2005-07-20 09:00:00',  9, 19, '2005-07-28 08:00:00', 1),
    ('2005-07-20 13:30:00', 10, 20, '2005-07-29 11:00:00', 2),
    ('2005-07-21 10:00:00', 11, 21, '2005-07-29 09:00:00', 1),
    ('2005-07-21 14:30:00', 12, 22, '2005-07-30 10:30:00', 2),
    ('2005-07-22 09:30:00', 13, 23, '2005-07-30 08:30:00', 1),
    ('2005-07-22 13:00:00', 14, 24, '2005-07-31 11:00:00', 2),
    ('2005-07-23 10:00:00', 15, 25, '2005-07-31 09:00:00', 1),
    ('2005-07-23 14:00:00', 16, 26, '2005-08-01 10:00:00', 2),
    ('2005-07-24 09:00:00', 17, 27, '2005-08-01 08:00:00', 1),
    ('2005-07-24 12:30:00', 18, 28, '2005-08-02 11:00:00', 2),
    ('2005-07-25 10:30:00', 19, 29, '2005-08-02 09:30:00', 1),
    ('2005-07-25 14:00:00', 20, 30, '2005-08-03 10:00:00', 2),
    ('2005-07-26 09:00:00', 21,  1, '2005-08-03 08:00:00', 1),
    ('2005-07-26 13:00:00', 22,  2, '2005-08-04 11:00:00', 2),
    ('2005-07-27 10:00:00', 23,  3, '2005-08-04 09:00:00', 1),
    ('2005-07-27 14:30:00', 24,  4, '2005-08-05 10:30:00', 2),
    ('2005-07-28 09:30:00', 25,  5, '2005-08-05 08:30:00', 1),
    ('2005-07-28 13:00:00', 26,  6, '2005-08-06 11:00:00', 2),
    ('2005-07-29 10:00:00', 27,  7, '2005-08-06 09:00:00', 1),
    ('2005-07-29 14:00:00', 28,  8, '2005-08-07 10:00:00', 2),
    ('2005-07-30 09:00:00', 29,  9, '2005-08-07 08:00:00', 1),
    ('2005-07-30 12:30:00', 30, 10, '2005-08-08 11:00:00', 2),
    ('2005-08-01 10:30:00', 31, 11, '2005-08-08 09:30:00', 1),
    ('2005-08-01 14:00:00', 32, 12, '2005-08-09 10:00:00', 2),
    ('2005-08-02 09:00:00', 33, 13, '2005-08-09 08:00:00', 1),
    ('2005-08-02 13:30:00', 34, 14, '2005-08-10 11:00:00', 2),
    ('2005-08-03 10:00:00', 35, 15, '2005-08-10 09:00:00', 1),
    ('2005-08-03 14:30:00', 36, 16, '2005-08-11 10:30:00', 2),
    ('2005-08-04 09:30:00', 37, 17, '2005-08-11 08:30:00', 1),
    ('2005-08-04 13:00:00', 38, 18, '2005-08-12 11:00:00', 2),
    ('2005-08-05 10:00:00', 39, 19, '2005-08-12 09:00:00', 1),
    ('2005-08-05 14:00:00', 40, 20, '2005-08-13 10:00:00', 2),
    ('2005-08-06 09:00:00', 41, 21, '2005-08-13 08:00:00', 1),
    ('2005-08-06 12:30:00', 42, 22, '2005-08-14 11:00:00', 2),
    ('2005-08-07 10:30:00', 43, 23, '2005-08-14 09:30:00', 1),
    ('2005-08-07 14:00:00', 44, 24, '2005-08-15 10:00:00', 2),
    ('2005-08-08 09:00:00', 45, 25, '2005-08-15 08:00:00', 1),
    ('2005-08-08 13:00:00', 46, 26, '2005-08-16 11:00:00', 2),
    ('2005-08-09 10:00:00', 47, 27, '2005-08-16 09:00:00', 1),
    ('2005-08-09 14:30:00', 48, 28, '2005-08-17 10:30:00', 2),
    ('2005-08-10 09:30:00', 49, 29, '2005-08-17 08:30:00', 1),
    ('2005-08-10 13:00:00', 50, 30, '2005-08-18 11:00:00', 2),
    ('2005-08-11 10:00:00', 51,  1, '2005-08-18 09:00:00', 1),
    ('2005-08-11 14:00:00', 52,  2, '2005-08-19 10:00:00', 2),
    ('2005-08-12 09:00:00', 53,  3, '2005-08-19 08:00:00', 1),
    ('2005-08-12 12:30:00', 54,  4, '2005-08-20 11:00:00', 2),
    ('2005-08-13 10:30:00', 55,  5, '2005-08-20 09:30:00', 1),
    ('2005-08-13 14:00:00', 56,  6, '2005-08-21 10:00:00', 2),
    ('2005-08-14 09:00:00', 57,  7, '2005-08-21 08:00:00', 1),
    ('2005-08-14 13:30:00', 58,  8, '2005-08-22 11:00:00', 2),
    ('2005-08-15 10:00:00', 59,  9, '2005-08-22 09:00:00', 1),
    ('2005-08-15 14:30:00', 60, 10, '2005-08-23 10:30:00', 2),
    ('2005-08-16 09:30:00', 61, 11, '2005-08-23 08:30:00', 1),
    ('2005-08-16 13:00:00', 62, 12, '2005-08-24 11:00:00', 2),
    ('2005-08-17 10:00:00', 63, 13, '2005-08-24 09:00:00', 1),
    ('2005-08-17 14:00:00', 64, 14, '2005-08-25 10:00:00', 2),
    ('2005-08-18 09:00:00', 65, 15, '2005-08-25 08:00:00', 1),
    ('2005-08-18 12:30:00', 66, 16, '2005-08-26 11:00:00', 2),
    ('2005-08-19 10:30:00', 67, 17, '2005-08-26 09:30:00', 1),
    ('2005-08-19 14:00:00', 68, 18, '2005-08-27 10:00:00', 2),
    ('2005-08-20 09:00:00', 69, 19, '2005-08-27 08:00:00', 1),
    ('2005-08-20 13:00:00', 70, 20, '2005-08-28 11:00:00', 2),
    ('2005-08-21 10:00:00', 71, 21, '2005-08-28 09:00:00', 1),
    ('2005-08-21 14:30:00', 72, 22, '2005-08-29 10:30:00', 2),
    ('2005-08-22 09:30:00', 73, 23, '2005-08-29 08:30:00', 1),
    ('2005-08-22 13:00:00', 74, 24, '2005-08-30 11:00:00', 2),
    ('2005-08-23 10:00:00', 75, 25, '2005-08-30 09:00:00', 1),
    ('2005-08-23 14:00:00', 76, 26, '2005-08-31 10:00:00', 2),
    ('2005-08-24 09:00:00', 77, 27, NULL,                   1),  -- not returned (181)
    ('2005-08-24 13:30:00', 78, 28, NULL,                   2),  -- not returned (182)
    ('2005-08-25 10:30:00', 79, 29, NULL,                   1),  -- not returned (183)
    ('2005-08-25 14:00:00', 80, 30, NULL,                   2),  -- not returned (184)
    ('2005-08-26 09:00:00', 81,  1, NULL,                   1),  -- not returned (185)
    ('2005-08-26 12:30:00', 82,  2, NULL,                   2),  -- not returned (186)
    ('2005-08-27 10:30:00', 83,  3, NULL,                   1),  -- not returned (187)
    ('2005-08-27 14:00:00', 84,  4, NULL,                   2),  -- not returned (188)
    ('2005-08-28 09:30:00', 85,  5, NULL,                   1),  -- not returned (189)
    ('2005-08-28 13:00:00', 86,  6, NULL,                   2),  -- not returned (190)
    ('2006-02-14 10:00:00', 87,  7, '2006-02-18 09:00:00',  1),
    ('2006-02-14 14:30:00', 88,  8, '2006-02-19 10:30:00',  2),
    ('2006-02-15 09:30:00', 89,  9, '2006-02-19 08:30:00',  1),
    ('2006-02-15 13:00:00', 90, 10, '2006-02-20 11:00:00',  2),
    ('2006-02-16 10:00:00', 91, 11, '2006-02-20 09:00:00',  1),
    ('2006-02-16 14:00:00', 92, 12, '2006-02-21 10:00:00',  2),
    ('2006-02-17 09:00:00', 93, 13, '2006-02-21 08:00:00',  1),
    ('2006-02-17 12:30:00', 94, 14, '2006-02-22 11:00:00',  2),
    ('2006-02-18 10:30:00', 95, 15, '2006-02-22 09:30:00',  1),
    ('2006-02-18 14:00:00', 96, 16, '2006-02-23 10:00:00',  2),
    ('2006-02-19 09:00:00', 97, 17, NULL,                   1),  -- not returned (191-200 →10 total)
    ('2006-02-19 13:30:00', 98, 18, NULL,                   2),
    ('2006-02-20 10:00:00', 99, 19, NULL,                   1),
    ('2006-02-20 14:30:00',100, 20, NULL,                   2),
    ('2006-02-21 09:30:00',  1, 21, NULL,                   1),
    ('2006-02-21 13:00:00',  2, 22, NULL,                   2),
    ('2006-02-22 10:00:00',  3, 23, NULL,                   1),
    ('2006-02-22 14:00:00',  4, 24, NULL,                   2),
    ('2006-02-23 09:00:00',  5, 25, NULL,                   1),
    ('2006-02-23 12:30:00',  6, 26, NULL,                   2);

-- ============================================================
-- payment (180 rows) — for rentals 1-180 (which all have return_date)
-- amounts vary 1.99-9.99
-- ============================================================
INSERT INTO payment (customer_id, rental_id, amount, payment_date) VALUES
    ( 1,   1, 4.99, '2005-05-28 09:20:00'),
    ( 2,   2, 2.99, '2005-05-27 10:05:00'),
    ( 3,   3, 3.99, '2005-05-29 14:35:00'),
    ( 4,   4, 1.99, '2005-05-30 11:05:00'),
    ( 5,   5, 5.99, '2005-05-31 09:05:00'),
    ( 6,   6, 6.99, '2005-06-01 15:25:00'),
    ( 7,   7, 2.99, '2005-06-01 12:05:00'),
    ( 8,   8, 4.99, '2005-06-02 10:35:00'),
    ( 9,   9, 3.99, '2005-06-02 08:05:00'),
    (10,  10, 2.99, '2005-06-03 11:05:00'),
    (11,  11, 4.99, '2005-06-04 10:05:00'),
    (12,  12, 2.99, '2005-06-05 09:35:00'),
    (13,  13, 3.99, '2005-06-06 08:05:00'),
    (14,  14, 5.99, '2005-06-07 14:05:00'),
    (15,  15, 7.99, '2005-06-07 09:05:00'),
    (16,  16, 6.99, '2005-06-08 10:35:00'),
    (17,  17, 2.99, '2005-06-09 08:05:00'),
    (18,  18, 4.99, '2005-06-10 11:05:00'),
    (19,  19, 9.99, '2005-06-10 09:35:00'),
    (20,  20, 1.99, '2005-06-11 10:05:00'),
    (21,  21, 4.99, '2005-06-11 08:35:00'),
    (22,  22, 3.99, '2005-06-12 12:05:00'),
    (23,  23, 2.99, '2005-06-13 09:05:00'),
    (24,  24, 4.99, '2005-06-14 10:05:00'),
    (25,  25, 5.99, '2005-06-14 08:35:00'),
    (26,  26, 3.99, '2005-06-15 11:05:00'),
    (27,  27, 4.99, '2005-06-15 09:05:00'),
    (28,  28, 2.99, '2005-06-16 10:35:00'),
    (29,  29, 1.99, '2005-06-16 08:05:00'),
    (30,  30, 7.99, '2005-06-17 11:05:00'),
    ( 1,  31, 4.99, '2005-06-17 09:35:00'),
    ( 2,  32, 2.99, '2005-06-18 10:05:00'),
    ( 3,  33, 3.99, '2005-06-19 08:35:00'),
    ( 4,  34, 1.99, '2005-06-20 11:05:00'),
    ( 5,  35, 5.99, '2005-06-20 09:05:00'),
    ( 6,  36, 6.99, '2005-06-21 10:35:00'),
    ( 7,  37, 2.99, '2005-06-21 08:05:00'),
    ( 8,  38, 4.99, '2005-06-22 11:05:00'),
    ( 9,  39, 3.99, '2005-06-22 09:35:00'),
    (10,  40, 2.99, '2005-06-23 10:05:00'),
    (11,  41, 4.99, '2005-06-23 08:35:00'),
    (12,  42, 2.99, '2005-06-24 11:05:00'),
    (13,  43, 3.99, '2005-06-25 09:05:00'),
    (14,  44, 5.99, '2005-06-26 10:35:00'),
    (15,  45, 7.99, '2005-06-26 08:05:00'),
    (16,  46, 6.99, '2005-06-27 11:05:00'),
    (17,  47, 2.99, '2005-06-27 09:35:00'),
    (18,  48, 4.99, '2005-06-28 10:05:00'),
    (19,  49, 9.99, '2005-06-28 08:05:00'),
    (20,  50, 1.99, '2005-06-29 11:05:00'),
    (21,  51, 4.99, '2005-06-29 09:05:00'),
    (22,  52, 3.99, '2005-06-30 10:35:00'),
    (23,  53, 2.99, '2005-06-30 08:35:00'),
    (24,  54, 4.99, '2005-07-01 11:05:00'),
    (25,  55, 5.99, '2005-07-01 09:05:00'),
    (26,  56, 3.99, '2005-07-02 10:05:00'),
    (27,  57, 4.99, '2005-07-02 08:05:00'),
    (28,  58, 2.99, '2005-07-03 11:05:00'),
    (29,  59, 1.99, '2005-07-03 09:35:00'),
    (30,  60, 7.99, '2005-07-04 10:05:00'),
    ( 1,  61, 4.99, '2005-07-04 08:05:00'),
    ( 2,  62, 2.99, '2005-07-05 11:05:00'),
    ( 3,  63, 3.99, '2005-07-05 09:05:00'),
    ( 4,  64, 1.99, '2005-07-06 10:35:00'),
    ( 5,  65, 5.99, '2005-07-06 08:35:00'),
    ( 6,  66, 6.99, '2005-07-07 11:05:00'),
    ( 7,  67, 2.99, '2005-07-07 09:05:00'),
    ( 8,  68, 4.99, '2005-07-08 10:05:00'),
    ( 9,  69, 3.99, '2005-07-08 08:05:00'),
    (10,  70, 2.99, '2005-07-09 11:05:00'),
    (11,  71, 4.99, '2005-07-09 09:35:00'),
    (12,  72, 2.99, '2005-07-10 10:05:00'),
    (13,  73, 3.99, '2005-07-10 08:05:00'),
    (14,  74, 5.99, '2005-07-11 11:05:00'),
    (15,  75, 7.99, '2005-07-11 09:05:00'),
    (16,  76, 6.99, '2005-07-12 10:35:00'),
    (17,  77, 2.99, '2005-07-12 08:35:00'),
    (18,  78, 4.99, '2005-07-13 11:05:00'),
    (19,  79, 9.99, '2005-07-13 09:05:00'),
    (20,  80, 1.99, '2005-07-14 10:05:00'),
    (21,  81, 4.99, '2005-07-14 08:05:00'),
    (22,  82, 3.99, '2005-07-15 11:05:00'),
    (23,  83, 2.99, '2005-07-15 09:35:00'),
    (24,  84, 4.99, '2005-07-16 10:05:00'),
    (25,  85, 5.99, '2005-07-16 08:05:00'),
    (26,  86, 3.99, '2005-07-17 11:05:00'),
    (27,  87, 4.99, '2005-07-17 09:05:00'),
    (28,  88, 2.99, '2005-07-18 10:35:00'),
    (29,  89, 1.99, '2005-07-18 08:35:00'),
    (30,  90, 7.99, '2005-07-19 11:05:00'),
    ( 1,  91, 4.99, '2005-07-19 09:05:00'),
    ( 2,  92, 2.99, '2005-07-20 10:05:00'),
    ( 3,  93, 3.99, '2005-07-20 08:05:00'),
    ( 4,  94, 1.99, '2005-07-21 11:05:00'),
    ( 5,  95, 5.99, '2005-07-21 09:35:00'),
    ( 6,  96, 6.99, '2005-07-22 10:05:00'),
    ( 7,  97, 2.99, '2005-07-22 08:05:00'),
    ( 8,  98, 4.99, '2005-07-23 11:05:00'),
    ( 9,  99, 3.99, '2005-07-23 09:05:00'),
    (10, 100, 2.99, '2005-07-24 10:35:00'),
    (11, 101, 4.99, '2005-07-24 08:35:00'),
    (12, 102, 2.99, '2005-07-25 11:05:00'),
    (13, 103, 3.99, '2005-07-25 09:05:00'),
    (14, 104, 5.99, '2005-07-26 10:05:00'),
    (15, 105, 7.99, '2005-07-26 08:05:00'),
    (16, 106, 6.99, '2005-07-27 11:05:00'),
    (17, 107, 2.99, '2005-07-27 09:35:00'),
    (18, 108, 4.99, '2005-07-28 10:05:00'),
    (19, 109, 9.99, '2005-07-28 08:05:00'),
    (20, 110, 1.99, '2005-07-29 11:05:00'),
    (21, 111, 4.99, '2005-07-29 09:05:00'),
    (22, 112, 3.99, '2005-07-30 10:35:00'),
    (23, 113, 2.99, '2005-07-30 08:35:00'),
    (24, 114, 4.99, '2005-07-31 11:05:00'),
    (25, 115, 5.99, '2005-07-31 09:05:00'),
    (26, 116, 3.99, '2005-08-01 10:05:00'),
    (27, 117, 4.99, '2005-08-01 08:05:00'),
    (28, 118, 2.99, '2005-08-02 11:05:00'),
    (29, 119, 1.99, '2005-08-02 09:35:00'),
    (30, 120, 7.99, '2005-08-03 10:05:00'),
    ( 1, 121, 4.99, '2005-08-03 08:05:00'),
    ( 2, 122, 2.99, '2005-08-04 11:05:00'),
    ( 3, 123, 3.99, '2005-08-04 09:05:00'),
    ( 4, 124, 1.99, '2005-08-05 10:35:00'),
    ( 5, 125, 5.99, '2005-08-05 08:35:00'),
    ( 6, 126, 6.99, '2005-08-06 11:05:00'),
    ( 7, 127, 2.99, '2005-08-06 09:05:00'),
    ( 8, 128, 4.99, '2005-08-07 10:05:00'),
    ( 9, 129, 3.99, '2005-08-07 08:05:00'),
    (10, 130, 2.99, '2005-08-08 11:05:00'),
    (11, 131, 4.99, '2005-08-08 09:35:00'),
    (12, 132, 2.99, '2005-08-09 10:05:00'),
    (13, 133, 3.99, '2005-08-09 08:05:00'),
    (14, 134, 5.99, '2005-08-10 11:05:00'),
    (15, 135, 7.99, '2005-08-10 09:05:00'),
    (16, 136, 6.99, '2005-08-11 10:35:00'),
    (17, 137, 2.99, '2005-08-11 08:35:00'),
    (18, 138, 4.99, '2005-08-12 11:05:00'),
    (19, 139, 9.99, '2005-08-12 09:05:00'),
    (20, 140, 1.99, '2005-08-13 10:05:00'),
    (21, 141, 4.99, '2005-08-13 08:05:00'),
    (22, 142, 3.99, '2005-08-14 11:05:00'),
    (23, 143, 2.99, '2005-08-14 09:35:00'),
    (24, 144, 4.99, '2005-08-15 10:05:00'),
    (25, 145, 5.99, '2005-08-15 08:05:00'),
    (26, 146, 3.99, '2005-08-16 11:05:00'),
    (27, 147, 4.99, '2005-08-16 09:05:00'),
    (28, 148, 2.99, '2005-08-17 10:35:00'),
    (29, 149, 1.99, '2005-08-17 08:35:00'),
    (30, 150, 7.99, '2005-08-18 11:05:00'),
    ( 1, 151, 4.99, '2005-08-18 09:05:00'),
    ( 2, 152, 2.99, '2005-08-19 10:05:00'),
    ( 3, 153, 3.99, '2005-08-19 08:05:00'),
    ( 4, 154, 1.99, '2005-08-20 11:05:00'),
    ( 5, 155, 5.99, '2005-08-20 09:35:00'),
    ( 6, 156, 6.99, '2005-08-21 10:05:00'),
    ( 7, 157, 2.99, '2005-08-21 08:05:00'),
    ( 8, 158, 4.99, '2005-08-22 11:05:00'),
    ( 9, 159, 3.99, '2005-08-22 09:05:00'),
    (10, 160, 2.99, '2005-08-23 10:35:00'),
    (11, 161, 4.99, '2005-08-23 08:35:00'),
    (12, 162, 2.99, '2005-08-24 11:05:00'),
    (13, 163, 3.99, '2005-08-24 09:05:00'),
    (14, 164, 5.99, '2005-08-25 10:05:00'),
    (15, 165, 7.99, '2005-08-25 08:05:00'),
    (16, 166, 6.99, '2005-08-26 11:05:00'),
    (17, 167, 2.99, '2005-08-26 09:35:00'),
    (18, 168, 4.99, '2005-08-27 10:05:00'),
    (19, 169, 9.99, '2005-08-27 08:05:00'),
    (20, 170, 1.99, '2005-08-28 11:05:00'),
    ( 7, 191, 4.99, '2006-02-18 09:05:00'),
    ( 8, 192, 2.99, '2006-02-19 10:35:00'),
    ( 9, 193, 3.99, '2006-02-19 08:35:00'),
    (10, 194, 5.99, '2006-02-20 11:05:00'),
    (11, 195, 7.99, '2006-02-20 09:05:00'),
    (12, 196, 6.99, '2006-02-21 10:05:00'),
    (13, 197, 2.99, '2006-02-21 08:05:00'),
    (14, 198, 4.99, '2006-02-22 11:05:00'),
    (15, 199, 3.99, '2006-02-22 09:35:00'),
    (16, 200, 2.99, '2006-02-23 10:05:00');

COMMIT;
