DROP TABLE IF EXISTS est_present, periode_de_vente, vente, recolte, production, produits, semaine, saison, categorie_produit, maraichers, marches;
CREATE TABLE marches
(
    id_marche     INT AUTO_INCREMENT,
    date_marche    DATE NOT NULL,
    lieu_du_marche TEXT NOT NULL,
    PRIMARY KEY (id_marche)
);

CREATE TABLE maraichers
(
    id_maraicher     INT AUTO_INCREMENT,
    nom_maraicher    VARCHAR(50) NOT NULL,
    prenom_maraicher VARCHAR(50) NOT NULL,
    adresse          TEXT,
    numero_de_tel    VARCHAR(50),
    PRIMARY KEY (id_Maraicher)
);

CREATE TABLE categorie_produit
(
    id_categorie_produit INT AUTO_INCREMENT,
    libelle_categorie    VARCHAR(50),
    PRIMARY KEY (id_categorie_produit)
);
CREATE TABLE saison
(
    id_saison      INT AUTO_INCREMENT,
    libelle_saison VARCHAR(50),
    PRIMARY KEY (id_saison)
);

CREATE TABLE semaine
(
    id_semaine INT AUTO_INCREMENT,
    PRIMARY KEY (id_semaine)
);

CREATE TABLE produits
(
    id_produit           INT AUTO_INCREMENT,
    libelle_produit      VARCHAR(50) NOT NULL,
    id_categorie_produit INT         NOT NULL,
    PRIMARY KEY (id_produit),
    FOREIGN KEY (id_categorie_produit) REFERENCES categorie_produit (id_categorie_produit)
);

CREATE TABLE recolte
(
    id_recolte        INT AUTO_INCREMENT,
    quantite_recoltee INT,
    id_semaine        INT NOT NULL,
    id_produit        INT NOT NULL,
    id_maraicher      INT NOT NULL,
    PRIMARY KEY (id_recolte),
    FOREIGN KEY (id_semaine) REFERENCES semaine (id_semaine),
    FOREIGN KEY (id_produit) REFERENCES produits (id_produit),
    FOREIGN KEY (id_maraicher) REFERENCES maraichers (id_maraicher)
);

CREATE TABLE vente
(
    id_vente            INT AUTO_INCREMENT,
    prix_de_vente       INT,
    quantitee_vendue    INT,
    prix_total_de_vente INT,
    id_semaine          INT NOT NULL,
    id_produit          INT NOT NULL,
    id_marche          INT NOT NULL,
    id_maraicher        INT NOT NULL,
    PRIMARY KEY (id_vente),
    FOREIGN KEY (id_semaine) REFERENCES semaine (id_semaine),
    FOREIGN KEY (id_produit) REFERENCES produits (id_produit),
    FOREIGN KEY (id_marche) REFERENCES marches (id_marche),
    FOREIGN KEY (id_maraicher) REFERENCES maraichers (id_maraicher)
);

CREATE TABLE est_present
(
    id_marche   INT,
    id_Maraicher INT,
    PRIMARY KEY (id_marche, id_Maraicher),
    FOREIGN KEY (id_marche) REFERENCES marches (id_marche),
    FOREIGN KEY (id_Maraicher) REFERENCES maraichers (id_Maraicher)
);

CREATE TABLE production
(
    id_production    INT AUTO_INCREMENT,
    id_maraicher     INT,
    id_produit       INT,
    surface_cultivee INT,
    PRIMARY KEY (id_production),
    FOREIGN KEY (id_maraicher) REFERENCES maraichers (id_maraicher),
    FOREIGN KEY (id_produit) REFERENCES produits (id_produit)
);
CREATE TABLE periode_de_vente
(
    id_produit INT,
    id_saison  INT,
    PRIMARY KEY (id_produit, id_saison),
    FOREIGN KEY (id_produit) REFERENCES produits (id_produit),
    FOREIGN KEY (id_saison) REFERENCES saison (id_saison)
);


-- INSERT


INSERT INTO marches (date_marche, lieu_du_marche)
VALUES ('2023-11-15', 'Belfort'),
       ('2023-11-16', 'Libreville'),
       ('2023-11-17', 'Chèvremont');

INSERT INTO maraichers (id_maraicher, nom_maraicher, prenom_maraicher, adresse, numero_de_tel)
VALUES ('1', 'Hollande', 'François', '5 rue des Mirabelles', '0754646478'),
       ('2', 'Girado', 'Jérôme', '9 rue Lafayette', '0624897548'),
       ('3', 'Poulain', 'Amélie', '1 rue de plancher-bas', '0748952154'),
       ('4', 'Vuyon', 'Hugo', '8 avenue Denfert-Rochereau', '0678123651');

INSERT INTO categorie_produit (id_categorie_produit, libelle_categorie)
VALUES ('1', 'Légumes'),
       ('2', 'Fruits'),
       ('3', 'Herbes aromatiques');

INSERT INTO saison (id_saison, libelle_saison)
VALUES ('1', 'Été'),
       ('2', 'Automne'),
       ('3', 'Hiver'),
       ('4', 'Printemps');

INSERT INTO semaine (id_semaine) VALUE
    ('1'),
    ('2'),
    ('3');

INSERT INTO produits (libelle_produit, id_categorie_produit)
VALUES ('Tomates', 1),
       ('Pommes', 2),
       ('Persil', 3);


INSERT INTO recolte (id_recolte, quantite_recoltee, id_semaine, id_produit, id_maraicher)
VALUES (1, 100, 1, 1, 1),
       (2, 150, 1, 2, 4),
       (3, 75, 2, 3, 3);

INSERT INTO vente (prix_de_vente, quantitee_vendue, prix_total_de_vente, id_semaine, id_produit, id_marche,
                   id_maraicher)
VALUES (2, 50, 100, 1, 1, 1, 1),
       (3, 100, 300, 1, 2, 2, 2),
       (1, 30, 30, 2, 3, 3, 3);

INSERT INTO est_present (id_marche, id_maraicher)
VALUES (1, 1),
       (2, 2),
       (3, 3);

INSERT INTO production (id_production, id_maraicher, id_produit, surface_cultivee)
VALUES (1, 1, 1, 13),
       (2, 2, 2, 56),
       (3, 3, 3, 76);

INSERT INTO periode_de_vente (id_produit, id_saison)
VALUES (1, 1),
       (2, 2),
       (3, 3);


-- REQUETES


-- total des ventes par marches
SELECT marches.lieu_du_marche, SUM(vente.prix_total_de_vente) AS total_ventes
FROM marches
         INNER JOIN vente ON marches.id_marche = vente.id_marche
GROUP BY marches.lieu_du_marche;

-- recolte moyenne par produit
SELECT produits.libelle_produit, AVG(recolte.quantite_recoltee) AS moyenne_recolte
FROM produits
         INNER JOIN recolte ON produits.id_produit = recolte.id_produit
GROUP BY produits.libelle_produit;

-- nombre de produits vendus par saison
SELECT saison.libelle_saison, COUNT(DISTINCT vente.id_produit) AS nombre_produits_vendus
FROM saison
         INNER JOIN periode_de_vente ON saison.id_saison = periode_de_vente.id_saison
         INNER JOIN vente ON periode_de_vente.id_produit = vente.id_produit
GROUP BY saison.libelle_saison;

-- recoltes par maraîchers
SELECT M.nom_maraicher,
       R.id_produit,
       SUM(R.quantite_recoltee) AS total_recolte,
       V.id_produit             AS produit_plus_vendu,
       COUNT(V.id_produit)      AS nb_ventes_produit_plus_vendu
FROM maraichers M
         LEFT JOIN
     recolte R ON M.id_maraicher = R.id_maraicher
         LEFT JOIN
     vente V ON M.id_maraicher = V.id_maraicher
GROUP BY M.nom_maraicher, R.id_produit, V.id_produit
ORDER BY M.nom_maraicher, SUM(R.quantite_recoltee) DESC;
SHOW TABLES;

SELECT produits.libelle_produit, SUM(production.surface_cultivee) AS surface_totale
        FROM production
        JOIN produits ON production.id_produit = produits.id_produit
        GROUP BY produits.libelle_produit;
