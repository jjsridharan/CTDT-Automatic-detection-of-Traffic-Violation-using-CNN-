-- phpMyAdmin SQL Dump
-- version 4.7.7
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Apr 03, 2018 at 10:43 AM
-- Server version: 10.1.31-MariaDB
-- PHP Version: 7.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `id2536892_ctdt`
--

-- --------------------------------------------------------

--
-- Table structure for table `Unregisteredvehicle`
--

CREATE TABLE `Unregisteredvehicle` (
  `lplate` varchar(25) COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `Unregisteredvehicle`
--

INSERT INTO `Unregisteredvehicle` (`lplate`) VALUES
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound'),
('notfound');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `username` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `licenseplate` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`username`, `licenseplate`, `amount`) VALUES
('Ramanathan', 'TN 10 AW 4493', 165),
('user', 'tn33d407', 500),
('', 'tn33e407', 500);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`licenseplate`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
