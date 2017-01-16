-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 16 Sty 2017, 11:12
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
-- Struktura tabeli dla tabeli `group_task`
--

CREATE TABLE `group_task` (
  `group_id` int(11) NOT NULL,
  `task_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

--
-- Indeksy dla zrzutów tabel
--

--
-- Indexes for table `group_task`
--
ALTER TABLE `group_task`
  ADD PRIMARY KEY (`group_id`,`task_id`),
  ADD KEY `FK_ASS_6` (`task_id`),
  ADD KEY `FK_ASS_7` (`group_id`);

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `group_task`
--
ALTER TABLE `group_task`
  ADD CONSTRAINT `FK_ASS_6` FOREIGN KEY (`group_id`) REFERENCES `group_names` (`id`),
  ADD CONSTRAINT `FK_ASS_7` FOREIGN KEY (`task_id`) REFERENCES `task` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
