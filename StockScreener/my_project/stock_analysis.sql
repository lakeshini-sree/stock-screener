-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 19, 2026 at 03:34 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `stock_analysis`
--

-- --------------------------------------------------------

--
-- Table structure for table `alert`
--

CREATE TABLE `alert` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `condition_json` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`condition_json`)),
  `is_active` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alert`
--

INSERT INTO `alert` (`id`, `user_id`, `condition_json`, `is_active`) VALUES
(1, 1, '{\"revenue\": \">50000\", \"ebitda\": \">15000\"}', 1),
(2, 2, '{\"price\": \"<2000\"}', 1);

-- --------------------------------------------------------

--
-- Table structure for table `fundamental_data`
--

CREATE TABLE `fundamental_data` (
  `id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `quarter` varchar(10) DEFAULT NULL,
  `revenue` decimal(15,2) DEFAULT NULL,
  `profit` decimal(15,2) DEFAULT NULL,
  `eps` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fundamental_data`
--

INSERT INTO `fundamental_data` (`id`, `company_id`, `quarter`, `revenue`, `profit`, `eps`) VALUES
(1, 1, 'Q1-2024', 60000.00, 12000.00, 35.50),
(2, 1, 'Q2-2024', 62000.00, 13000.00, 37.20),
(3, 2, 'Q1-2024', 45000.00, 9000.00, 28.40),
(4, 3, 'Q1-2024', 120000.00, 25000.00, 45.80),
(5, 4, 'Q1-2024', 70000.00, 15000.00, 32.10);

-- --------------------------------------------------------

--
-- Table structure for table `historic_metrics`
--

CREATE TABLE `historic_metrics` (
  `id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL,
  `quarter` varchar(10) DEFAULT NULL,
  `revenue` decimal(15,2) DEFAULT NULL,
  `ebitda` decimal(15,2) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `recorded_at` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `historic_metrics`
--

INSERT INTO `historic_metrics` (`id`, `company_id`, `quarter`, `revenue`, `ebitda`, `price`, `recorded_at`) VALUES
(1, 1, 'Q1-2024', 60000.00, 18000.00, 3500.50, '2024-04-01'),
(2, 1, 'Q2-2024', 62000.00, 19000.00, 3650.75, '2024-07-01'),
(3, 2, 'Q1-2024', 45000.00, 14000.00, 1500.25, '2024-04-01'),
(4, 3, 'Q1-2024', 120000.00, 40000.00, 2800.90, '2024-04-01'),
(5, 4, 'Q1-2024', 70000.00, 22000.00, 1650.30, '2024-04-01');

-- --------------------------------------------------------

--
-- Table structure for table `portfolio`
--

CREATE TABLE `portfolio` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `company_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `portfolio`
--

INSERT INTO `portfolio` (`id`, `user_id`, `company_id`) VALUES
(1, 1, 1),
(2, 1, 2),
(3, 2, 3),
(4, 3, 1),
(5, 3, 4),
(6, 4, 2),
(7, 5, 3);

-- --------------------------------------------------------

--
-- Table structure for table `symbols`
--

CREATE TABLE `symbols` (
  `company_id` int(11) NOT NULL,
  `symbol` varchar(20) NOT NULL,
  `company_name` varchar(100) NOT NULL,
  `sector` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `symbols`
--

INSERT INTO `symbols` (`company_id`, `symbol`, `company_name`, `sector`) VALUES
(1, 'TCS', 'Tata Consultancy Services', 'IT'),
(2, 'INFY', 'Infosys Ltd', 'IT'),
(3, 'RELIANCE', 'Reliance Industries', 'Energy'),
(4, 'HDFCBANK', 'HDFC Bank Ltd', 'Banking');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `user_email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `user_email`, `password`, `created_at`) VALUES
(1, 'Lakeshini', 'lakeshini@gmail.com', 'password123', '2026-02-19 02:14:55'),
(2, 'Rahul', 'rahul@gmail.com', 'password456', '2026-02-19 02:14:55'),
(3, 'manjula', 'manju@gmail.com', 'm123', '2026-02-19 02:18:12'),
(4, 'amulya', 'a@gmail.com', 'ammu', '2026-02-19 02:18:12'),
(5, 'gani', 'gani@gmail.com', '123456', '2026-02-19 02:18:12');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alert`
--
ALTER TABLE `alert`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `fundamental_data`
--
ALTER TABLE `fundamental_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `company_id` (`company_id`);

--
-- Indexes for table `historic_metrics`
--
ALTER TABLE `historic_metrics`
  ADD PRIMARY KEY (`id`),
  ADD KEY `company_id` (`company_id`);

--
-- Indexes for table `portfolio`
--
ALTER TABLE `portfolio`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `company_id` (`company_id`);

--
-- Indexes for table `symbols`
--
ALTER TABLE `symbols`
  ADD PRIMARY KEY (`company_id`),
  ADD UNIQUE KEY `symbol` (`symbol`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_email` (`user_email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `alert`
--
ALTER TABLE `alert`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `fundamental_data`
--
ALTER TABLE `fundamental_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `historic_metrics`
--
ALTER TABLE `historic_metrics`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `portfolio`
--
ALTER TABLE `portfolio`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `symbols`
--
ALTER TABLE `symbols`
  MODIFY `company_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `alert`
--
ALTER TABLE `alert`
  ADD CONSTRAINT `alert_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `fundamental_data`
--
ALTER TABLE `fundamental_data`
  ADD CONSTRAINT `fundamental_data_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `symbols` (`company_id`);

--
-- Constraints for table `historic_metrics`
--
ALTER TABLE `historic_metrics`
  ADD CONSTRAINT `historic_metrics_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `symbols` (`company_id`);

--
-- Constraints for table `portfolio`
--
ALTER TABLE `portfolio`
  ADD CONSTRAINT `portfolio_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `portfolio_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `symbols` (`company_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
