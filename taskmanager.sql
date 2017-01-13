-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 13 Sty 2017, 01:38
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
  `title` varchar(32) DEFAULT NULL,
  `description` varchar(160) DEFAULT NULL,
  `id` int(11) NOT NULL,
  `deadline` datetime DEFAULT NULL,
  `label` varchar(32) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `task`
--

INSERT INTO `task` (`title`, `description`, `id`, `deadline`, `label`) VALUES
('PRy', 'Zrobic programy na Przetwarzanie rownolegle', 1, '2017-01-31 00:00:00', 'important'),
('Zrobic Bazy Danych', 'Aplikacja laczaca sie z baza umozliwiajaca edycje danych', 2, '2017-01-25 00:00:00', 'important');

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
('87de4699450663eaa71825a97cdb9f30', '2017-01-20 01:28:48', 48),
('539ad8ec34dd2ce7f54f40a409845826', '2017-01-20 01:30:18', 49),
('d1dbbcc09cae19618b745df01d24c0500e511fa92ba40d71888ab69c404da4a8', '2017-01-20 01:31:25', 50),
('2697586f4ad93162961cc7c1c9f674a9fa5880aa0dfe3a642fffee7193f0ad1e', '2017-01-20 01:31:25', 51),
('e040b294cdfac875fbf125f5babbce7927ce74b855be2da88f9e7218a755d0a6', '2017-01-20 01:32:11', 52),
('99a051973f773acc068e85eb3dbeba81202c0c3720b07e16f75cea2e83e75fa0', '2017-01-20 01:33:43', 53);

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
('marcin', 'c5450079ce3aa5440cdea45c4be193bb', 'marcin@mrugas.com', 'admin', 1);

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
-- Indeksy dla zrzutów tabel
--

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
-- AUTO_INCREMENT dla tabeli `token`
--
ALTER TABLE `token`
  MODIFY `token_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=54;
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
