-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mariadb
-- Erstellungszeit: 22. Jun 2025 um 14:06
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
  `autoid` int(11) NOT NULL,
  `marke` varchar(9) NOT NULL,
  `modell` varchar(15) NOT NULL,
  `baujahr` int(10) NOT NULL,
  `leistung` int(9) NOT NULL,
  `preis` int(9) NOT NULL,
  `url` varchar(50) NOT NULL,
  `hubraum` decimal(10,2) DEFAULT NULL,
  `kraftstoffverbrauch` decimal(10,2) DEFAULT NULL,
  `getriebeart` varchar(50) DEFAULT NULL,
  `antriebsart` varchar(50) DEFAULT NULL,
  `umweltplakette` varchar(30) DEFAULT NULL,
  `info` text CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `auto`
--

INSERT INTO `auto` (`autoid`, `marke`, `modell`, `baujahr`, `leistung`, `preis`, `url`, `hubraum`, `kraftstoffverbrauch`, `getriebeart`, `antriebsart`, `umweltplakette`, `info`) VALUES
(1, 'Mercedes', 'G 500', 2020, 422, 110000, 'G 500.png', 3.98, 10.90, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', 'WOOOOOWWWWWWW '),
(2, 'Mercedes', 'V 300d', 2023, 239, 70000, 'V 300d.jpg', 1.95, 6.30, '9-GANG-AUTOMATIK', 'Hinterradantrieb', 'Grün (Euro 6)', NULL),
(3, 'Mercedes', 'A 200', 2021, 136, 36000, 'a200.jpg', 1.33, 5.80, '7-GANG-AUTOMATIK', 'Vorderradantrieb', 'Grün (Euro 6)', NULL),
(4, 'Mercedes', 'B 250e', 2018, 218, 42000, 'b250e.jpg', 1.32, 1.20, '1-GANG-AUTOMATIK', 'Vorderradantrieb', 'Grün (E-Auto)', NULL),
(5, 'Mercedes', 'C 300d', 2024, 265, 55000, 'c 300d.jpg', 1.99, 4.90, '9-GANG-AUTOMATIK', 'Hinterradantrieb', 'Grün (Euro 6)', NULL),
(6, 'Mercedes', 'E 220d', 2023, 197, 60000, 'E 220d.jpg', 1.99, 4.70, '9-GANG-AUTOMATIK', 'Hinterradantrieb', 'Grün (Euro 6)', NULL),
(7, 'Mercedes', 'GLC 300e', 2022, 313, 63000, 'glc 300e.jpg', 2.00, 2.20, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(8, 'Mercedes', 'GLE 400d', 2023, 330, 85000, 'GLE 400d.jpg', 2.93, 7.70, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(9, 'Mercedes ', 'GLS 580', 2023, 489, 115000, 'GLS 580.jpg', 3.98, 11.70, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(10, 'Mercedes', 'CLA 250e', 2019, 218, 45000, 'CLA 250e.jpg', 1.33, 1.40, '8-GANG-AUTOMATIK', 'Vorderradantrieb', 'Grün (Euro 6)', NULL),
(11, 'Mercedes', 'EQS 450+', 2024, 333, 105000, 'eqs 450+.jpg', 0.00, 0.00, '1-GANG-AUTOMATIK', 'Hinterradantrieb', 'Grün (E-Auto)', NULL),
(12, 'Mercedes', 'GT 63S E', 2024, 843, 200000, 'gts 63e.jpg', 3.98, 8.60, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(13, 'Mercedes ', 'EQS SUV 580', 2023, 400, 129000, 'eqs 580.jpg', 0.00, 0.00, '1-GANG AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (E-Auto)', NULL),
(14, 'Mercedes', 'GLC 400', 2024, 381, 80000, 'GLC 400.jpg', 2.00, 1.90, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(15, 'Mercedes', 'E 450 4MATIC', 2025, 370, 74000, 'e 450.jpg', 3.00, 7.80, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(16, 'Mercedes', 'C 43 AMG', 2023, 408, 72000, 'C 43.jpg', 2.00, 9.10, '9-Gang-Automatik', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(17, 'Mercedes', 'S 580e', 2022, 510, 128000, 'S 580e.jpg', 3.00, 1.20, '9-Gang-Automatik', 'Hinterradantrieb', 'Grün (Euro 6)', NULL),
(18, 'Mercedes', 'GLE 350de', 2021, 320, 76000, 'GLE350.jpg', 2.00, 1.10, '9-Gang-Automatik', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(19, 'Mercedes', 'E53 AMG', 2018, 435, 89000, 'E53.jpg', 3.00, 8.90, '9-Gang-Automatik', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL),
(20, 'Mercedes', 'AMG GT 43', 2023, 367, 115000, 'GT43.jpg', 3.00, 9.40, '9-GANG-AUTOMATIK', 'Permanenter Allradantrieb', 'Grün (Euro 6)', NULL);

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `favorites`
--

CREATE TABLE `favorites` (
  `id` int(11) NOT NULL,
  `User_ID` int(11) NOT NULL,
  `autoid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `favorites`
--

INSERT INTO `favorites` (`id`, `User_ID`, `autoid`) VALUES
(40, 36, 1),
(36, 36, 5),
(47, 40, 1),
(49, 40, 2),
(48, 40, 3),
(50, 42, 19),
(51, 43, 9),
(52, 55, 1);

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
  `Status` varchar(20) DEFAULT NULL,
  `erstellt_am` timestamp NOT NULL DEFAULT current_timestamp(),
  `schlussrate` decimal(10,2) NOT NULL DEFAULT 0.00,
  `info` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Finanzierungsanfrage`
--

INSERT INTO `Finanzierungsanfrage` (`ID`, `Nutzer_ID`, `Auto_ID`, `Monate`, `Anzahlung`, `Monatliche_Rate`, `Terminwunsch`, `Status`, `erstellt_am`, `schlussrate`, `info`) VALUES
(118, 55, 1, 36, 20000.00, 1700.00, '2025-06-19 00:00:00', 'genehmigt', '2025-06-21 23:46:07', 30000.00, 'Finanzierungsanfrage');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `Kaufvertrag`
--

CREATE TABLE `Kaufvertrag` (
  `Kaufvertrag_ID` int(11) NOT NULL,
  `Datum_Erstellung` datetime NOT NULL,
  `vorname` varchar(100) DEFAULT NULL,
  `nachname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `kunde_adresse` text DEFAULT NULL,
  `kunde_telefon` varchar(50) DEFAULT NULL,
  `kunde_id` int(11) DEFAULT NULL,
  `auto_id` int(11) DEFAULT NULL,
  `Monate` int(11) DEFAULT NULL,
  `Anzahlung` int(11) DEFAULT NULL,
  `Schlussrate` int(11) DEFAULT NULL,
  `Monatliche_Rate` decimal(10,2) DEFAULT NULL,
  `Info` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `Kaufvertrag`
--

INSERT INTO `Kaufvertrag` (`Kaufvertrag_ID`, `Datum_Erstellung`, `vorname`, `nachname`, `email`, `kunde_adresse`, `kunde_telefon`, `kunde_id`, `auto_id`, `Monate`, `Anzahlung`, `Schlussrate`, `Monatliche_Rate`, `Info`) VALUES
(7, '2025-06-11 13:53:41', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(9, '2025-06-11 14:49:47', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(10, '2025-06-11 14:53:29', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(11, '2025-06-11 14:56:03', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(12, '2025-06-11 14:58:47', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(14, '2025-06-15 21:33:26', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(33, '2025-06-20 13:38:05', 'Marco', 'Zimmerman', 'Zimmerman@gmail.com', 'Heilbronner Str.63 , 74076 Heilbronn', '015908131827', 42, 19, 60, 30000, 20000, 663.00, 'Finanzierungsanfrage'),
(34, '2025-06-20 13:39:45', 'John', 'Müller', 'J.Mueller@gmail.com', 'Südstraße 32, 74078 Heilbronn', '015903112311', 43, 9, 0, 0, 115000, 0.00, 'Barkauf'),
(35, '2025-06-20 13:41:13', 'Felix', 'Braun', 'braunfelix@gmail.com', 'Albert-Einstein-Straße 23, 70195 Stuttgart', '015906101625', 44, 14, 24, 40000, 15000, 1062.50, 'Finanzierungsanfrage'),
(36, '2025-06-20 13:45:42', 'Ann-Sophie', 'Krämer', 'Kraemer.Ann@gmail.com', 'Marktplatz 19,70372 Stuttgart', '015909184732', 45, 1, 36, 50000, 10000, 1416.67, 'Finanzierungsanfrage'),
(37, '2025-06-20 13:51:30', 'Maria', 'Held', 'marieheld90@gmail.com', 'Unter der Leiter 19, 74076 Heilbronn', '015905043932', 46, 1, 0, 0, 110000, 0.00, 'Barkauf'),
(38, '2025-06-20 13:56:20', 'Lea', 'Durst', 'lea.durst@gmail.com', 'Hallerstr. 28 , 74076 Heilbronn', '015909382713', 47, 15, 36, 35000, 10000, 821.67, 'Finanzierungsanfrage'),
(39, '2025-06-20 14:01:44', 'Daniel', 'Scholz', 'danielscholz@gmail.com', 'Hauptstraße 2, 74821 Mosbach', '015909483721', 48, 10, 26, 20000, 10000, 588.46, 'Finanzierungsanfrage'),
(40, '2025-06-20 14:09:29', 'Luca', 'Berger', 'lucaberger@gmail.com', 'Kirchplatz 39; 74906 Bad Rappenau', '015909354632', 50, 8, 36, 80000, 3000, 56.67, 'Finanzierungsanfrage'),
(41, '2025-06-20 14:12:30', 'Lisa', 'Grönemeyer', 'lisa1997@gmail.com', 'Heilbronner str. 23, 74906 Bad Rappenau', '015908274832', 49, 15, 0, 0, 74000, 0.00, 'Barkauf'),
(42, '2025-06-20 14:16:46', 'Tobias', 'Hohn', 'Tobihohn@gmail.com', 'Leopoldsplatz 27, 69412 Eberbach', '017239483721', 51, 17, 0, 0, 128000, 0.00, 'Barkauf'),
(44, '2025-06-21 22:04:52', 'Enes', 'Bülkü', 'enes@novadrive.hn', 'Heilbron 74000, Straße 35', '0123456789', 25, 2, 0, 0, 70000, 0.00, 'Barkauf'),
(45, '2025-06-21 22:24:31', 'ali', 'yeeeee', 'aye@gmail.com', 'Lugoweg 13', '3453425346235', 52, 11, 100, 0, 40000, 663.00, 'Finanzierungsanfrage'),
(46, '2025-06-22 00:19:49', 'ali', 'yeeeee', 'aye@gmail.com', 'sxwdcwwed', '6866860670', 52, 14, 100, 0, 40000, 408.00, 'Finanzierungsanfrage'),
(47, '2025-06-22 11:32:25', 'Enes', 'Bülkü', 'enes@novadrive.hn', 'dsfsdf', '432434321', 25, 1, 0, 0, 110000, 0.00, 'Barkauf');

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `reviews`
--

CREATE TABLE `reviews` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL CHECK (`rating` between 1 and 5),
  `comment` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `admin_response` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Daten für Tabelle `reviews`
--

INSERT INTO `reviews` (`id`, `user_id`, `rating`, `comment`, `created_at`, `admin_response`) VALUES
(34, 46, 5, 'Sehr gepflegte Fahrzeuge und eine große Auswahl! Ich habe mich für einen Mercedes G 500 entschieden und war begeistert vom Zustand und Komfort. Klare Empfehlung für alle, die Wert auf Qualität legen.', '2025-06-20 13:49:39', 'Liebe Maria,\r\nherzlichen Dank für deine tolle Bewertung und deinem Vertrauen in unser Autohaus! Es freut uns sehr zu hören, dass du mit deinem neuen Mercedes G 500 so zufrieden bist. Qualität und Fahrzeugpflege haben für uns oberste Priorität – umso schöner, dass du das genauso wahrgenommen hast. Wir wünschen dir allzeit gute und sichere Fahrt und stehen dir jederzeit gerne wieder zur Verfügung!'),
(35, 47, 5, 'Ich habe eine Finanzierung angefragt und wurde ausführlich beraten. Die monatlichen Raten waren fair kalkuliert und transparent. Keine versteckten Kosten!', '2025-06-20 13:54:04', 'Liebe Lea,\r\ndanke für deine Bewertung! Transparenz und faire Konditionen sind für uns selbstverständlich. Schön, dass du dich gut beraten gefühlt hast – das ist unser Ziel. 🚘✨'),
(36, 42, 4, 'Freundliches Team, schnelle Abwicklung und ein tolles Auto – besser geht’s nicht! Ich wurde sehr herzlich empfangen und habe mich von Anfang an gut aufgehoben gefühlt.', '2025-06-20 13:57:21', 'Hallo Marco,\r\nvielen Dank für dein Vertrauen! Wir freuen uns sehr, dass du dich bei uns wohlgefühlt hast. Unser Team freut sich immer über so ein schönes Lob. Bis bald bei NovaDrive Heilbronn!'),
(37, 48, 4, 'Die Auswahl an Fahrzeugen war super, allerdings musste ich bei der Abholung etwas warten, obwohl ich einen Termin hatte. Das Auto selbst war top – sauber und wie beschrieben. Trotzdem wäre ein etwas besseres Zeitmanagement wünschenswert.', '2025-06-20 14:00:45', 'Hallo Daniel,\r\nvielen Dank für dein ehrliches Feedback! Es tut uns leid, dass es bei der Abholung zu einer Verzögerung kam. Wir arbeiten daran, unsere Abläufe weiter zu optimieren, damit Termine künftig noch reibungsloser ablaufen. Umso mehr freut es uns, dass du mit dem Fahrzeug zufrieden warst. Danke für dein Vertrauen!'),
(38, 49, 3, 'Die Mitarbeiter waren sehr freundlich, aber ich hätte mir vor Vertragsabschluss etwas mehr Informationen zur Versicherung und möglichen Zusatzkosten gewünscht. Letztlich war alles okay, aber mehr Klarheit im Voraus wäre hilfreich.', '2025-06-20 14:04:44', 'Liebe Lisa,\r\ndanke für deine konstruktive Rückmeldung! Wir nehmen deinen Hinweis sehr ernst und werden unsere Informationsunterlagen überarbeiten, um künftig noch transparenter zu kommunizieren. Es freut uns, dass am Ende alles gut verlaufen ist – wir würden uns freuen, dich bald wieder begrüßen zu dürfen!'),
(39, 50, 5, 'Alles top! Vom ersten Kontakt bis zur Abholung lief alles reibungslos. Besonders beeindruckt hat mich die ehrliche Beratung – ich hatte nie das Gefühl, dass mir etwas „aufgeschwatzt“ wird. Das Auto war wie neu. Jederzeit wieder!', '2025-06-20 14:08:00', 'Lieber Luca,\r\nganz herzlichen Dank für deine wunderbare Bewertung! Ehrliche und transparente Beratung ist für uns eine Selbstverständlichkeit – schön, dass du das so empfunden hast. Wir freuen uns sehr, dass du rundum zufrieden warst und wünschen dir weiterhin viel Freude mit deinem Fahrzeug. 🚗'),
(40, 51, 5, 'Ich habe mich für den Mercedes S 580e im Barkauf entschieden – und ich bin mehr als zufrieden. Das Fahrzeug war in makellosem Zustand, und die Abwicklung war schnell, transparent und ohne jeglichen Druck. Besonders positiv: keine versteckten Gebühren, keine Spielchen – einfach professionell. Danke an das Team von NovaDrive für diesen Premium-Service!', '2025-06-20 14:15:48', 'Lieber Tobias, \r\nherzlichen Glückwunsch zu deinem neuen Mercedes S 580e – eine exzellente Wahl! Es freut uns sehr, dass du mit dem Barkauf und unserer Abwicklung so zufrieden bist. Transparenz und Vertrauen stehen für uns an erster Stelle. Vielen Dank für dein Feedback und viel Freude mit deinem Fahrzeug der Oberklasse! 🥇🚘');

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
(21, 'Benni', 'David', 'Benni@novadrive.hn', 'scrypt:32768:8:1$OPcrelHpub2kaP23$0339115f9d969efef015058d0529c3ff4467e5ddeb9ac7707913814c9639c1a95649d2b704270d5ed8ba348e56f7af0105c06207574e9faee5bd9249e317348f', 'admin'),
(25, 'Enes', 'Bülkü', 'enes@novadrive.hn', 'scrypt:32768:8:1$cdSHO39ejIHCT1be$a96eaae2572bd4138183986fdddcc4ebfa5112cbad38a08834e1fcd4d6612cbe957c0c9aed939e2e7acf3cf3eb6467e5791ef246e05b531a05291826a04bef20', 'admin'),
(27, 'ben', 'david', 'ben@gmail.com', 'scrypt:32768:8:1$TWzrn3zdwPIb5TYn$fba4ebacb72528fa7125ad267606dbb73cd5bd2c73aa450c9bac2e5a16aef7d3e24a5cecf95873f4fa06eb2ec242f64cc899a9b5d091601a1765e628b3b852ae', 'customer'),
(33, 'Max', 'Mustermann', 'max@gmail.com', 'scrypt:32768:8:1$wCXk0AKRzlmCYeXA$40c723a538ad0aa17e9cb689a0a69eb1e26169cace1ef03e2a081f3b7258fcbaa8b35f8cef2e98ca9893900bd2cec716f93eb54f13fb82dbdeebc8f29fa69ca1', 'admin'),
(36, 'Sipan', 'Dölek', 'sipan@novadrive.hn', 'scrypt:32768:8:1$CYq6mA0RTZYySoHu$856686d9009877e58687f1d62eb47ebee5fff499d0f5769dba32715840a8d211e0e1a2a86867a1590400d1bea2abdc0cb4456f066718aefea127ffca0dd01fe2', 'admin'),
(40, 'ali', 'yenil', 'ali2@novadrive.hn', 'scrypt:32768:8:1$I9mXcJfal8XMOTRK$4137a02f28e402f6c7228c207d6ab39080441f7d254a8b8ad9c76c04a2a5e1b0d42aed97a39779b018b36b9c6d047588f6b0e42e49f204bb140f165a5e08e092', 'admin'),
(42, 'Marco', 'Zimmerman', 'Zimmerman@gmail.com', 'scrypt:32768:8:1$43xJX1Lo5KPAAHGE$d02b508d8b2c39e1906cedec7a85916b8e1438109fe506e48931957854ea838348941b5d888292fc93aafc2513b29870f1b00c110d359a5d32f8054e413af782', 'customer'),
(43, 'John', 'Müller', 'J.Mueller@gmail.com', 'scrypt:32768:8:1$kxbbXSBmKvPKg1Yo$9188ea48a1e0ed3f87b0069f268b20069de01ab6415418578b3b00345e2b824b7e9085fc97935e3396f16acc8df8dbbd342280313a4df5408545c3e5829ad67b', 'customer'),
(44, 'Felix', 'Braun', 'braunfelix@gmail.com', 'scrypt:32768:8:1$H3ZlL768HfwiGUBB$1bc3a70a691d558e573e13f0a88a4cd313233d32271ed7d68905879d71d94cca483f3e732c9277818d8208a9e43f1c2cc64bf7908c066b932a7e37d713ec6dee', 'customer'),
(45, 'Ann-Sophie', 'Krämer', 'Kraemer.Ann@gmail.com', 'scrypt:32768:8:1$A4Heoq0s8ekEP8MP$4d87f2d576b3ebcf0b72bf99e4de760970c33c4f22b53a97bdb00e72b22caf81a19f84d90b46d3fc534f7b49c8fcd755a739f6a8f18fd664aaa44ecf2028d611', 'customer'),
(46, 'Maria', 'Held', 'marieheld90@gmail.com', 'scrypt:32768:8:1$SWnajT12md6AmNkV$29e0c0e8c70ef0484cf68e6396d139db1aa8b95716c3086ecbb5f020c7c82f008c889ab43840e4ab46fc42962af6cc21e13f1f2eed9251ee0da911f5347d23e8', 'customer'),
(47, 'Lea', 'Durst', 'lea.durst@gmail.com', 'scrypt:32768:8:1$OzfziuNg4gG2JL2q$4148bc4f438fb028333f5f070c9e87b4e7f8e36db054a6046aa185c605fa341381a04accb4c05697a8fc242154339f10c8fd9597551a92f01ec90a78571c7ed8', 'customer'),
(48, 'Daniel', 'Scholz', 'danielscholz@gmail.com', 'scrypt:32768:8:1$8sD8tcpIHpGM99kD$c20c462e3424a2aef2eadae3f5f692342a4fd934e69180510e53f640f3230ea45bdfafd07b64cf1abbf73c128b613f238284d35c5377e4f6375e0038757fabb8', 'customer'),
(49, 'Lisa', 'Grönemeyer', 'lisa1997@gmail.com', 'scrypt:32768:8:1$pvbReBe7dpr4Malp$9a9bac537fc9a9cb78833d1db8aac88d745bba465cb60ca32beed30e8bb3d063a54b44a76a8a9fd149441924cd427ada251f1339aff0d34e0172e4f4e3b833ad', 'customer'),
(50, 'Luca', 'Berger', 'lucaberger@gmail.com', 'scrypt:32768:8:1$liTGTgavlyl9lUbX$604cd1fd0564896a3755a780a62674cd854215abf28cd2953dbb0b63f489890e4841977dae53d676c5d8d95c13f86f7d6363bae6207f1ff63aea961cbb7b6376', 'customer'),
(51, 'Tobias', 'Hohn', 'Tobihohn@gmail.com', 'scrypt:32768:8:1$s57tL0jHv2qSApR3$52a72a259faf8c5762b97f53b362fb30e7dea44fdbabde0160c0ddd15200d275eb6361f9eef73bc93f3962a9542d04244370196fecefa39107b2c5e6ed7f6bd7', 'customer'),
(52, 'ali', 'yeeeee', 'aye@gmail.com', 'scrypt:32768:8:1$xG9ROunLJLbbeSne$6097ea1e48b63e57f808d08f8a86414809b507c036f58fba3f94abad2deff1e5907813b7f33fbe5d5cc2d3d44edb95ea967c0a0b6fbf73b40b851275ba27d3aa', 'admin'),
(54, 'ali', 'test', 'test@gmail.com', 'scrypt:32768:8:1$N7Bn5MJkoi7EyAPM$876dc59614628470bf30dfe6a99e44a84505c944f75ef9f4967de66d66cdc4bb517cf4f8f0b0c4a870475f2a529fb919752768bd395fe3f5a14568e5fa186097', 'admin'),
(55, 'Ali Abiiiiii', 'test', 'test3@gmail.com', 'scrypt:32768:8:1$lvVGrSbf2WJ1PT1N$b9fc53f47aa17628cb0137a46b422c50d7adcb54bab80fed232a85faff68760d886cc6c03634832a430e8af84b3eabbb1c10e7f6e2a46eb042eb04f7ab4d215c', 'customer');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `auto`
--
ALTER TABLE `auto`
  ADD PRIMARY KEY (`autoid`);

--
-- Indizes für die Tabelle `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_auto` (`User_ID`,`autoid`),
  ADD KEY `autoid` (`autoid`);

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
  ADD KEY `fk_kunde` (`kunde_id`),
  ADD KEY `fk_auto` (`auto_id`);

--
-- Indizes für die Tabelle `reviews`
--
ALTER TABLE `reviews`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_reviews_user` (`user_id`);

--
-- Indizes für die Tabelle `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`User_ID`) USING BTREE;

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `auto`
--
ALTER TABLE `auto`
  MODIFY `autoid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT für Tabelle `favorites`
--
ALTER TABLE `favorites`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=53;

--
-- AUTO_INCREMENT für Tabelle `Finanzierungsanfrage`
--
ALTER TABLE `Finanzierungsanfrage`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=120;

--
-- AUTO_INCREMENT für Tabelle `Kaufvertrag`
--
ALTER TABLE `Kaufvertrag`
  MODIFY `Kaufvertrag_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- AUTO_INCREMENT für Tabelle `reviews`
--
ALTER TABLE `reviews`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT für Tabelle `users`
--
ALTER TABLE `users`
  MODIFY `User_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `users` (`User_ID`) ON DELETE CASCADE,
  ADD CONSTRAINT `favorites_ibfk_2` FOREIGN KEY (`autoid`) REFERENCES `auto` (`autoid`) ON DELETE CASCADE;

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
  ADD CONSTRAINT `fk_auto` FOREIGN KEY (`auto_id`) REFERENCES `auto` (`autoid`) ON DELETE SET NULL,
  ADD CONSTRAINT `fk_kunde` FOREIGN KEY (`kunde_id`) REFERENCES `users` (`User_ID`) ON DELETE SET NULL;

--
-- Constraints der Tabelle `reviews`
--
ALTER TABLE `reviews`
  ADD CONSTRAINT `fk_reviews_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`User_ID`) ON DELETE SET NULL ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
