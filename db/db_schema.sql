
-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Erstellungszeit: 07. Mai 2025 um 10:55
-- Server-Version: 10.11.11-MariaDB-ubu2204
-- PHP-Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `ss-2025-18`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `auto`
--

CREATE TABLE `auto` (
  `autoid` int(13) NOT NULL,
  `marke` varchar(9) NOT NULL,
  `modell` varchar(15) NOT NULL,
  `baujahr` int(10) NOT NULL,
  `leistung` int(9) NOT NULL,
  `preis` int(9) NOT NULL,
  `url` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `auto`
--

INSERT INTO `auto` (`autoid`, `marke`, `modell`, `baujahr`, `leistung`, `preis`, `url`) VALUES
(1, 'Mercedes', 'G 500', 2021, 422, 110000, 'G 500.png'),
(2, 'Mercedes', 'V 300d', 2023, 239, 70000, 'V 300d.png'),
(3, 'Mercedes', 'A 200', 2023, 136, 36000, 'A 200.png'),
(4, 'Mercedes', 'B 250e', 2023, 218, 42000, 'B 250e.png'),
(5, 'Mercedes', 'C 300d', 2023, 265, 55000, 'C 300d.png'),
(6, 'Mercedes', 'E 220d', 2023, 197, 60000, 'E 220d.png'),
(7, 'Mercedes', 'GLC 300e', 2023, 313, 63000, 'GLC 300e.png'),
(8, 'Mercedes', 'GLE 400d', 2023, 330, 85000, 'GLE 400d.png'),
(9, 'Mercedes ', 'GLS 580', 2023, 489, 115000, 'GLS 580.png'),
(10, 'Mercedes', 'CLA 250e', 2023, 218, 45000, 'CLA 250e.png'),
(11, 'Mercedes', 'EQS 450+', 2023, 333, 105000, 'EQS 450+.png'),
(12, 'Mercedes', 'GT 63S E', 2023, 843, 200000, 'AMG GT 63 S E Performance.png');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Finanzierungsanfrage`
--

CREATE TABLE `Finanzierungsanfrage` (
  `ID` int(11) NOT NULL,
  `Nutzer_ID` int(11) NOT NULL,
  `Auto_ID` int(11) NOT NULL,
  `Monate` smallint(6) NOT NULL,
  `Anzahlung` decimal(10,2) NOT NULL,
  `Monatliche_Rate` decimal(10,2) NOT NULL,
  `Terminwunsch` datetime NOT NULL,
  `Status` enum('angefragt','genehmigt','abgelehnt') NOT NULL,
  `erstellt am` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Kaufvertrag`
--

CREATE TABLE `Kaufvertrag` (
  `Kaufvertrag_ID` int(11) NOT NULL,
  `Finanzierungs_ID` int(11) NOT NULL,
  `Datum_Erstellung` datetime NOT NULL,
  `PDF_Pfad` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `users`
--

CREATE TABLE `users` (
  `User_ID` int(11) NOT NULL,
  `vorname` varchar(255) DEFAULT NULL,
  `nachname` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `passwort` varchar(255) DEFAULT NULL,
  `role` varchar(20) DEFAULT 'customer'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `users`
--

INSERT INTO `users` (`User_ID`, `vorname`, `nachname`, `email`, `passwort`, `role`) VALUES
(8, 'Enes', 'enes', 'enes@novadrive.de', 'scrypt:32768:8:1$crRAMfWzNaStIy5Z$42be564f763b2e126c7b2a967e015bb193d83668231bdb3a7d7b2c56fee70c96d5ffd33a3fd9124895d1dbd5dbacbae8f960b77dbb6eb36912875ab628d51e94', 'admin'),
(12, 'weiopofhow', 'mustermann', 'deine@gmail.com', 'scrypt:32768:8:1$rv175ND2x3pkmr4j$b9f04c9a52affc0dbd0a32aebee922a4c467b517ad86cb211cea43db5b63d2e1cefd4ea863c29b24ed26a494ec026a613a655c7e3c442d5b72a440a74a58b6d2', 'customer');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `auto`
--
ALTER TABLE `auto`
  ADD PRIMARY KEY (`autoid`);

--
-- Indizes für die Tabelle `Finanzierungsanfrage`
--
ALTER TABLE `Finanzierungsanfrage`
  ADD PRIMARY KEY (`ID`),
  ADD KEY `Nutzer_ID` (`Nutzer_ID`),
  ADD KEY `Auto_ID` (`Auto_ID`);

--
-- Indizes für die Tabelle `Kaufvertrag`
--
ALTER TABLE `Kaufvertrag`
  ADD PRIMARY KEY (`Kaufvertrag_ID`) USING BTREE,
  ADD KEY `Finanzierungs_ID` (`Finanzierungs_ID`);

--
-- Indizes für die Tabelle `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`User_ID`) USING BTREE;

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `Finanzierungsanfrage`
--
ALTER TABLE `Finanzierungsanfrage`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `Kaufvertrag`
--
ALTER TABLE `Kaufvertrag`
  MODIFY `Kaufvertrag_ID` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `users`
--
ALTER TABLE `users`
  MODIFY `User_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `Finanzierungsanfrage`
--
ALTER TABLE `Finanzierungsanfrage`
  ADD CONSTRAINT `Finanzierungsanfrage_ibfk_1` FOREIGN KEY (`Nutzer_ID`) REFERENCES `users` (`User_ID`),
  ADD CONSTRAINT `Finanzierungsanfrage_ibfk_2` FOREIGN KEY (`Auto_ID`) REFERENCES `auto` (`autoid`);

--
-- Constraints der Tabelle `Kaufvertrag`
--
ALTER TABLE `Kaufvertrag`
  ADD CONSTRAINT `Kaufvertrag_ibfk_1` FOREIGN KEY (`Finanzierungs_ID`) REFERENCES `Finanzierungsanfrage` (`ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

