DROP TABLE IF EXISTS est_present, produit, periode_de_vente, Vente,recolte ,Produits , Semaine, Saison ,categorie_produit , Maraichers , marches;
CREATE TABLE marches(
   Id_marches INT AUTO_INCREMENT,
   Date_marche DATE NOT NULL,
   Lieu_du_marche TEXT NOT NULL,
   PRIMARY KEY(Id_marches)
);

CREATE TABLE Maraichers(
   Id_Maraicher INT AUTO_INCREMENT,
   Nom_maraicher VARCHAR(50) NOT NULL,
   prenom_maraicher VARCHAR(50) NOT NULL,
   Adresse TEXT,
   numero_de_tel VARCHAR(50),
   PRIMARY KEY(Id_Maraicher)
);

CREATE TABLE categorie_produit(
   Id_categorie_produit INT AUTO_INCREMENT,
   libelle_categorie VARCHAR(50),
   PRIMARY KEY(Id_categorie_produit)
);
CREATE TABLE Saison(
   Id_saison INT AUTO_INCREMENT,
   libelle_saison VARCHAR(50),
   PRIMARY KEY(Id_saison)
);

CREATE TABLE Semaine(
   Id_Semaine INT AUTO_INCREMENT,
   PRIMARY KEY(Id_Semaine)
);

CREATE TABLE Produits(
   Id_produit INT AUTO_INCREMENT,
   libelle_produit VARCHAR(50) NOT NULL,
   Id_categorie_produit INT NOT NULL,
   PRIMARY KEY(Id_produit),
   FOREIGN KEY(Id_categorie_produit) REFERENCES categorie_produit(Id_categorie_produit)
);

CREATE TABLE recolte(
   Id_recolte INT AUTO_INCREMENT,
   quantite_recoltee INT,
   Id_Semaine INT NOT NULL,
   Id_produit INT NOT NULL,
   Id_Maraicher INT NOT NULL,
   PRIMARY KEY(Id_recolte),
   FOREIGN KEY(Id_Semaine) REFERENCES Semaine(Id_Semaine),
   FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit),
   FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher)
);

CREATE TABLE Vente(
   Id_Vente INT AUTO_INCREMENT,
   Prix_de_vente INT,
   Quantitée_vendue INT,
   Prix_total_de_vente INT,
   Id_Semaine INT NOT NULL,
   Id_produit INT NOT NULL,
   Id_marches INT NOT NULL,
   Id_Maraicher INT NOT NULL,
   PRIMARY KEY(Id_Vente),
   FOREIGN KEY(Id_Semaine) REFERENCES Semaine(Id_Semaine),
   FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit),
   FOREIGN KEY(Id_marches) REFERENCES marches(Id_marches),
   FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher)
);

CREATE TABLE est_present(
   Id_marches INT,
   Id_Maraicher INT,
   PRIMARY KEY(Id_marches, Id_Maraicher),
   FOREIGN KEY(Id_marches) REFERENCES marches(Id_marches),
   FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher)
);

CREATE TABLE produit (
    Id_Maraicher INT,
    Id_produit INT,
   Surface_cultivee INT,
    PRIMARY KEY(Id_Maraicher, Id_produit),
    FOREIGN KEY(Id_Maraicher) REFERENCES Maraichers(Id_Maraicher),
    FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit)
);
CREATE TABLE periode_de_vente(
   Id_produit INT,
   Id_saison INT,
   PRIMARY KEY(Id_produit, Id_saison),
   FOREIGN KEY(Id_produit) REFERENCES Produits(Id_produit),
   FOREIGN KEY(Id_saison) REFERENCES Saison(Id_saison)
);



-- INSERT


INSERT INTO marches (Date_marche, Lieu_du_marche) VALUES
('2023-11-15', 'Belfort'),
('2023-11-16', 'Libreville'),
('2023-11-17', 'Chèvremont');

INSERT INTO Maraichers (Id_Maraicher, Nom_maraicher, prenom_maraicher, Adresse, numero_de_tel) VALUES
('1', 'Hollande', 'François', '5 rue des Mirabelles', '0754646478'),
('2', 'Girado', 'Jérôme', '9 rue Lafayette', '0624897548'),
('3', 'Poulain', 'Amélie', '1 rue de plancher-bas', '0748952154'),
('4', 'Vuyon', 'Hugo', '8 avenue Denfert-Rochereau', '0678123651');

INSERT INTO categorie_produit (Id_categorie_produit, libelle_categorie) VALUES
('1','Légumes'),
('2','Fruits'),
('3','Herbes aromatiques');

INSERT INTO Saison (Id_saison, libelle_saison) VALUES
('1','Été'),
('2','Automne'),
('3','Hiver'),
('4','Printemps');

INSERT INTO Semaine (Id_Semaine) VALUE
('1'),
('2'),
('3');

INSERT INTO Produits (libelle_produit, Id_categorie_produit) VALUES
('Tomates', 1),
('Pommes', 2),
('Persil', 3);


INSERT INTO recolte (Id_recolte, quantite_recoltee, Id_Semaine, Id_produit, Id_Maraicher) VALUES
(1, 100, 1, 1, 1),
(2, 150, 1, 2, 4),
(3, 75, 2, 3, 3);

INSERT INTO Vente (Prix_de_vente, Quantitée_vendue, Prix_total_de_vente, Id_Semaine, Id_produit, Id_marches, Id_Maraicher) VALUES
(2, 50, 100, 1, 1, 1, 1),
(3, 100, 300, 1, 2, 2, 2),
(1, 30, 30, 2, 3, 3, 3);

INSERT INTO est_present (Id_marches, Id_Maraicher) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO produit (Id_Maraicher, Id_produit) VALUES
(1, 1),
(2, 2),
(3, 3);

INSERT INTO periode_de_vente (Id_produit, Id_saison) VALUES
(1, 1),
(2, 2),
(3, 3);


-- REQUETES


-- total des ventes par marches
SELECT marches.Lieu_du_marche, SUM(Vente.Prix_total_de_vente) AS Total_ventes
FROM marches
INNER JOIN Vente ON marches.Id_marches = Vente.Id_marches
GROUP BY marches.Lieu_du_marche;

-- recolte moyenne par produit
SELECT Produits.libelle_produit, AVG(recolte.quantite_recoltee) AS Moyenne_recolte
FROM Produits
INNER JOIN recolte ON Produits.Id_produit =recolte.Id_produit
GROUP BY Produits.libelle_produit;

-- nombre de produits vendus par saison
SELECT Saison.libelle_saison, COUNT(DISTINCT Vente.Id_produit) AS Nombre_produits_vendus
FROM Saison
INNER JOIN periode_de_vente ON Saison.Id_saison = periode_de_vente.Id_saison
INNER JOIN Vente ON periode_de_vente.Id_produit = Vente.Id_produit
GROUP BY Saison.libelle_saison;

-- recoltes par maraîchers
SELECT
    M.Nom_maraicher,
    R.Id_produit,
    SUM(R.quantite_recoltee) AS Total_recolte,
    V.Id_produit AS Produit_plus_vendu,
    COUNT(V.Id_produit) AS Nb_ventes_produit_plus_vendu
FROM
    Maraichers M
LEFT JOIN
   recolte R ON M.Id_Maraicher = R.Id_Maraicher
LEFT JOIN
    Vente V ON M.Id_Maraicher = V.Id_Maraicher
GROUP BY
    M.Nom_maraicher, R.Id_produit, V.Id_produit
ORDER BY
    M.Nom_maraicher, SUM(R.quantite_recoltee) DESC;


