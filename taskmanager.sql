-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 13 Sty 2017, 23:38
-- Wersja serwera: 5.7.14
-- Wersja PHP: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `taskmanager`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL,
  `app` varchar(255) COLLATE utf8_polish_ci NOT NULL,
  `name` varchar(255) COLLATE utf8_polish_ci NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `group_names`
--

CREATE TABLE `group_names` (
  `name` varchar(32) DEFAULT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `role`
--

CREATE TABLE `role` (
  `role_name` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `role`
--

INSERT INTO `role` (`role_name`) VALUES
('admin'),
('user');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `task`
--

CREATE TABLE `task` (
  `title` varchar(32) CHARACTER SET utf8 DEFAULT NULL,
  `description` varchar(160) CHARACTER SET utf8 DEFAULT NULL,
  `id` int(11) NOT NULL,
  `deadline` datetime DEFAULT NULL,
  `label` varchar(32) CHARACTER SET utf8 DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `task`
--

INSERT INTO `task` (`title`, `description`, `id`, `deadline`, `label`) VALUES
('Zrobic PRy', 'Zadnie 1: Pomiar lini cachu\r\nzadanie 2: OpenMp\r\nZadania 3: CUDA zadanie nr 14 ', 1, '2017-01-25 00:00:00', 'important'),
('Wybrac studentow', 'przejrzec oferty studentow', 3, '2017-03-14 00:00:00', 'normal'),
('BazyDanych', 'Zrobic aplikacje na bazy danych', 4, '2017-01-15 00:00:00', 'VERY IMPORTATNT'),
('Napisac sztuczna inteligencje', 'Gra w Kozy', 5, '2017-02-15 00:00:00', 'normal'),
('PC repair', 'naprawic komputer', 7, '2017-01-12 23:00:00', 'not important'),
('PC repair', 'naprawic komputer', 8, '2017-01-12 23:00:00', 'not important'),
('Kupić sukienki', 'Iść na zapkuy', 9, '2017-12-12 23:00:00', 'IMPORTANT'),
('Pomalować pokój', 'Kupić farbę i nałożyć na ściany', 13, '2017-01-13 23:00:00', 'IMPORTANT'),
('Iść po zakupy', 'Kupić sałatę i pomidory', 14, '2017-01-21 23:00:00', 'low priorytet');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `token`
--

CREATE TABLE `token` (
  `access_token` varchar(64) DEFAULT NULL,
  `expiration_date` datetime DEFAULT NULL,
  `token_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `token`
--

INSERT INTO `token` (`access_token`, `expiration_date`, `token_ID`) VALUES
('cbnasdk3lsadmlaksd3iuq9', '2017-01-24 00:00:00', 1),
('2bf69e757356c280c79cf305a46bbe278c94bdd3a31787aff666e2d8fb0a8486', '2017-01-20 20:30:53', 123),
('468d18517cac1903299e2ea9441a15ae9682785c843141892f76a3ce41db0515', '2017-01-20 20:36:22', 124),
('a24ae563a3f661298204b11f39fa5929d05ae8f6ee057ff0473e5fb1a79206bf', '2017-01-20 20:45:29', 125),
('0d25036aede0865de841bdd93b9971cb779e1e979619dd525dbc72cc3663e049', '2017-01-20 21:39:01', 126),
('98604fe38d3b7f66d84e8750d08c758e398d6f56e8db764cd5ebd8eb25a3287e', '2017-01-20 23:02:27', 127),
('f264042e8d2e67abe6b497918208701a505407671f093c6230513e3acf67b9f1', '2017-01-20 23:23:23', 128),
('b0e2ebfe16d54c22102be7f4263b92744923c0d9b3b115aa3cf6b52c0f27c327', '2017-01-20 23:27:47', 129),
('51362416ae8b12e4cc959957d10d4b594a86902dc3c3ad808e5e143e4bcfa0cd', '2017-01-20 23:28:31', 130),
('5ade312e316bb684338a902d3bf394a9b2a84a067d305e4b71b393f35d607900', '2017-01-20 23:29:01', 131),
('82eaf44f6182343fa4512c3492a144fd7bc1a9d5e2c3d2e95888dc31b823c081', '2017-01-20 23:29:03', 132),
('a180d429842c6f5cb2a57203693aa92e64398827b2088dffcc5055fd4659729f', '2017-01-20 23:29:04', 133),
('4d9bb61330c8379a76092c9f4af44f616da77331c27acc4d962a3776a4c9a9fb', '2017-01-20 23:33:27', 134);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `user`
--

CREATE TABLE `user` (
  `name` varchar(32) NOT NULL,
  `password` varchar(32) DEFAULT NULL,
  `email` varchar(32) DEFAULT NULL,
  `role_role_name` varchar(32) NOT NULL,
  `token_token_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `user`
--

INSERT INTO `user` (`name`, `password`, `email`, `role_role_name`, `token_token_ID`) VALUES
('agata', 'd84fc63a101c4c62e2d5e46567d6e81d', 'pink@princess.pl', 'user', 134),
('kuba', '08e2f45ac80035898d41a533d079c811', 'kuba@gmail.com', 'user', 1),
('marcin', 'c5450079ce3aa5440cdea45c4be193bb', 'marcin@mrugas.com', 'admin', 125),
('olek', '3f6dae8f3027d1b1142aa147f180483c', 'olo_lolo@gmail.com', 'user', 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `user_group`
--

CREATE TABLE `user_group` (
  `user_name` varchar(32) NOT NULL,
  `group_names_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `user_task`
--

CREATE TABLE `user_task` (
  `user_name` varchar(32) NOT NULL,
  `task_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `user_task`
--

INSERT INTO `user_task` (`user_name`, `task_id`) VALUES
('marcin', 1),
('kuba', 3),
('marcin', 4),
('marcin', 5),
('marcin', 8),
('agata', 9),
('agata', 13),
('agata', 14);

--
-- Indeksy dla zrzutów tabel
--

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `group_names`
--
ALTER TABLE `group_names`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `role`
--
ALTER TABLE `role`
  ADD PRIMARY KEY (`role_name`);

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `token`
--
ALTER TABLE `token`
  ADD PRIMARY KEY (`token_ID`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`name`),
  ADD KEY `user_role_FK` (`role_role_name`),
  ADD KEY `user_token_FK` (`token_token_ID`);

--
-- Indexes for table `user_group`
--
ALTER TABLE `user_group`
  ADD PRIMARY KEY (`user_name`,`group_names_id`),
  ADD KEY `FK_ASS_5` (`group_names_id`);

--
-- Indexes for table `user_task`
--
ALTER TABLE `user_task`
  ADD PRIMARY KEY (`user_name`,`task_id`),
  ADD KEY `FK_ASS_2` (`task_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT dla tabeli `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT dla tabeli `task`
--
ALTER TABLE `task`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT dla tabeli `token`
--
ALTER TABLE `token`
  MODIFY `token_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=135;
--
-- AUTO_INCREMENT dla tabeli `user_group`
--
ALTER TABLE `user_group`
  MODIFY `group_names_id` int(11) NOT NULL AUTO_INCREMENT;
--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `user_role_FK` FOREIGN KEY (`role_role_name`) REFERENCES `role` (`role_name`),
  ADD CONSTRAINT `user_token_FK` FOREIGN KEY (`token_token_ID`) REFERENCES `token` (`token_ID`);

--
-- Ograniczenia dla tabeli `user_group`
--
ALTER TABLE `user_group`
  ADD CONSTRAINT `FK_ASS_4` FOREIGN KEY (`user_name`) REFERENCES `user` (`name`),
  ADD CONSTRAINT `FK_ASS_5` FOREIGN KEY (`group_names_id`) REFERENCES `group_names` (`id`);

--
-- Ograniczenia dla tabeli `user_task`
--
ALTER TABLE `user_task`
  ADD CONSTRAINT `FK_ASS_1` FOREIGN KEY (`user_name`) REFERENCES `user` (`name`),
  ADD CONSTRAINT `FK_ASS_2` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
