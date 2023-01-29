-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 29, 2023 at 04:17 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.4.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `student_walailak_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `check_in`
--

CREATE TABLE `check_in` (
  `enter_id` int(11) NOT NULL,
  `enter_date` date NOT NULL,
  `enter_number` varchar(3) NOT NULL,
  `enter_added` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `check_in`
--

INSERT INTO `check_in` (`enter_id`, `enter_date`, `enter_number`, `enter_added`) VALUES
(9, '2023-01-29', '101', '2023-01-29 18:05:26'),
(10, '2023-01-29', '101', '2023-01-29 18:05:42'),
(11, '2023-01-29', '101', '2023-01-29 18:06:00'),
(12, '2023-01-29', '101', '2023-01-29 21:38:22'),
(13, '2023-01-29', '101', '2023-01-29 21:38:30');

-- --------------------------------------------------------

--
-- Table structure for table `check_out`
--

CREATE TABLE `check_out` (
  `out_id` int(11) NOT NULL,
  `out_date` date NOT NULL,
  `out_number` varchar(3) NOT NULL,
  `out_added` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `check_out`
--

INSERT INTO `check_out` (`out_id`, `out_date`, `out_number`, `out_added`) VALUES
(5, '2023-01-29', '101', '2023-01-29 21:41:20'),
(6, '2023-01-29', '101', '2023-01-29 21:41:30'),
(7, '2023-01-29', '101', '2023-01-29 21:41:40'),
(8, '2023-01-29', '101', '2023-01-29 21:41:50'),
(9, '2023-01-29', '101', '2023-01-29 21:42:01'),
(10, '2023-01-29', '101', '2023-01-29 21:42:11'),
(11, '2023-01-29', '101', '2023-01-29 21:42:21'),
(12, '2023-01-29', '101', '2023-01-29 21:42:30'),
(13, '2023-01-29', '101', '2023-01-29 21:42:40');

-- --------------------------------------------------------

--
-- Table structure for table `img_dataset`
--

CREATE TABLE `img_dataset` (
  `img_id` int(11) NOT NULL,
  `img_person` varchar(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `img_dataset`
--

INSERT INTO `img_dataset` (`img_id`, `img_person`) VALUES
(1, '101'),
(2, '101'),
(3, '101'),
(4, '101'),
(5, '101'),
(6, '101'),
(7, '101'),
(8, '101'),
(9, '101'),
(10, '101'),
(11, '101'),
(12, '101'),
(13, '101'),
(14, '101'),
(15, '101'),
(16, '101'),
(17, '101'),
(18, '101'),
(19, '101'),
(20, '101'),
(21, '101'),
(22, '101'),
(23, '101'),
(24, '101'),
(25, '101'),
(26, '101'),
(27, '101'),
(28, '101'),
(29, '101'),
(30, '101'),
(31, '101'),
(32, '101'),
(33, '101'),
(34, '101'),
(35, '101'),
(36, '101'),
(37, '101'),
(38, '101'),
(39, '101'),
(40, '101'),
(41, '101'),
(42, '101'),
(43, '101'),
(44, '101'),
(45, '101'),
(46, '101'),
(47, '101'),
(48, '101'),
(49, '101'),
(50, '101'),
(51, '101'),
(52, '101'),
(53, '101'),
(54, '101'),
(55, '101'),
(56, '101'),
(57, '101'),
(58, '101'),
(59, '101'),
(60, '101'),
(61, '101'),
(62, '101'),
(63, '101'),
(64, '101'),
(65, '101'),
(66, '101'),
(67, '101'),
(68, '101'),
(69, '101'),
(70, '101'),
(71, '101'),
(72, '101'),
(73, '101'),
(74, '101'),
(75, '101'),
(76, '101'),
(77, '101'),
(78, '101'),
(79, '101'),
(80, '101'),
(81, '101'),
(82, '101'),
(83, '101'),
(84, '101'),
(85, '101'),
(86, '101'),
(87, '101'),
(88, '101'),
(89, '101'),
(90, '101'),
(91, '101'),
(92, '101'),
(93, '101'),
(94, '101'),
(95, '101'),
(96, '101'),
(97, '101'),
(98, '101'),
(99, '101'),
(100, '101');

-- --------------------------------------------------------

--
-- Table structure for table `student_information`
--

CREATE TABLE `student_information` (
  `student_id` varchar(3) NOT NULL,
  `student_name` varchar(50) NOT NULL,
  `student_major` varchar(30) NOT NULL,
  `student_room` varchar(50) NOT NULL,
  `student_dormitory` varchar(50) NOT NULL,
  `student_added` datetime NOT NULL DEFAULT current_timestamp(),
  `student_active` varchar(1) NOT NULL DEFAULT 'Y'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `student_information`
--

INSERT INTO `student_information` (`student_id`, `student_name`, `student_major`, `student_room`, `student_dormitory`, `student_added`, `student_active`) VALUES
('101', 'Tanadon Jirapongsaton', 'SOFTWARE', '701', '7', '2023-01-29 18:04:50', 'Y');

-- --------------------------------------------------------

--
-- Table structure for table `unknow`
--

CREATE TABLE `unknow` (
  `id` int(11) NOT NULL,
  `createdAt` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `check_in`
--
ALTER TABLE `check_in`
  ADD PRIMARY KEY (`enter_id`),
  ADD KEY `enter_date` (`enter_date`);

--
-- Indexes for table `check_out`
--
ALTER TABLE `check_out`
  ADD PRIMARY KEY (`out_id`),
  ADD KEY `out_date` (`out_date`);

--
-- Indexes for table `img_dataset`
--
ALTER TABLE `img_dataset`
  ADD PRIMARY KEY (`img_id`);

--
-- Indexes for table `student_information`
--
ALTER TABLE `student_information`
  ADD PRIMARY KEY (`student_id`);

--
-- Indexes for table `unknow`
--
ALTER TABLE `unknow`
  ADD PRIMARY KEY (`id`),
  ADD KEY `createdAt` (`createdAt`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `check_in`
--
ALTER TABLE `check_in`
  MODIFY `enter_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `check_out`
--
ALTER TABLE `check_out`
  MODIFY `out_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `unknow`
--
ALTER TABLE `unknow`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
