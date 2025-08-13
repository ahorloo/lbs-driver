-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Aug 13, 2025 at 02:11 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `driver_logbook_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `daily_logbook`
--

CREATE TABLE `daily_logbook` (
  `id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `trip_no` varchar(100) DEFAULT NULL,
  `consignee` varchar(255) DEFAULT NULL,
  `terminal` varchar(255) DEFAULT NULL,
  `destination` varchar(255) DEFAULT NULL,
  `truck_no` varchar(100) DEFAULT NULL,
  `pickup_date` date DEFAULT NULL,
  `offloading_date` date DEFAULT NULL,
  `fuel` decimal(10,2) DEFAULT NULL,
  `road_expense` decimal(10,2) DEFAULT NULL,
  `toll` decimal(10,2) DEFAULT NULL,
  `advance_payment` decimal(10,2) DEFAULT NULL,
  `no_of_cont` int(11) DEFAULT NULL,
  `unit_price` decimal(10,2) DEFAULT NULL,
  `rate` decimal(10,2) DEFAULT NULL,
  `invoice_date` date DEFAULT NULL,
  `payment_rec_date` date DEFAULT NULL,
  `mode_of_payment` varchar(100) DEFAULT NULL,
  `remarks` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `trips`
--

CREATE TABLE `trips` (
  `id` int(11) NOT NULL,
  `device_name` varchar(100) NOT NULL,
  `trip_start` datetime DEFAULT NULL,
  `trip_end` datetime DEFAULT NULL,
  `start_location` varchar(255) NOT NULL,
  `end_location` varchar(255) NOT NULL,
  `route_length_km` float DEFAULT 0,
  `move_duration` varchar(50) DEFAULT '0',
  `stop_duration` varchar(50) DEFAULT '0',
  `stop_count` int(11) DEFAULT 0,
  `top_speed_kph` int(11) DEFAULT 0,
  `avg_speed_kph` int(11) DEFAULT 0,
  `overspeed_count` int(11) DEFAULT 0,
  `daily_mileage_km` float DEFAULT 0,
  `created_at` date DEFAULT NULL,
  `truck_number` varchar(20) DEFAULT NULL,
  `distance` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `trips`
--

INSERT INTO `trips` (`id`, `device_name`, `trip_start`, `trip_end`, `start_location`, `end_location`, `route_length_km`, `move_duration`, `stop_duration`, `stop_count`, `top_speed_kph`, `avg_speed_kph`, `overspeed_count`, `daily_mileage_km`, `created_at`, `truck_number`, `distance`) VALUES
(128, 'LBS-GB3281-22', NULL, NULL, 'Home', 'Home', 0.05, '0s', '21h 21min 1s', 0, 0, 0, 0, 0.05, '2025-08-01', NULL, NULL),
(129, 'LBS-GN3634-22', '2025-08-01 00:12:13', '2025-08-01 22:37:46', 'Kpone-Katamanso', 'Community 2', 27.57, '1h 8min 2s', '21h 29min 3s', 0, 0, 0, 0, 27.57, '2025-08-01', NULL, NULL),
(130, 'LBS-GR1583-14', NULL, NULL, 'Ashaiman', 'Ashaiman', 0.08, '0s', '8min 35s', 0, 0, 0, 0, 0.08, '2025-08-01', NULL, NULL),
(131, 'LBS-GW1509-17', '2025-08-01 14:58:09', '2025-08-01 20:54:24', 'Home', 'Tema', 14.02, '52min 47s', '5h 21min 0s', 0, 0, 0, 0, 14.02, '2025-08-01', NULL, NULL),
(132, 'LBS-GW3711-18', '2025-08-01 14:40:30', '2025-08-01 18:35:20', 'Tema', 'Ningo-Prampram', 36.96, '1h 35min 10s', '20h 12min 49s', 0, 0, 0, 0, 36.96, '2025-08-01', NULL, NULL),
(134, 'LBS-GW3711-18', '2025-08-02 09:50:52', '2025-08-02 16:44:30', 'Nigo-Prampram', 'Community 1', 39.26, '1h 28min 41s', '15h 37min 2s', 0, 0, 0, 0, 39.26, '2025-08-02', NULL, NULL),
(135, 'LBS-GB3281-22', NULL, NULL, 'Home', 'Home', 0, '0s', '11h 57min 7s', 0, 0, 0, 0, 0, '2025-08-03', NULL, NULL),
(136, 'LBS-GN3634-22', '2025-08-03 00:03:17', '2025-08-03 20:08:46', 'Harbor C8', 'Home', 95.94, '3h 7min 12s', '18h 35min 36s', 0, 0, 0, 0, 95.94, '2025-08-03', NULL, NULL),
(137, 'LBS-GW1509-17', '2025-08-03 00:00:08', '2025-08-03 18:53:44', 'C5', 'Home', 108.13, '3h 27min 13s', '15h 25min 53s', 0, 0, 0, 0, 108.13, '2025-08-03', NULL, NULL),
(138, 'LBS-GW3711-18', '2025-08-03 02:59:26', '2025-08-03 17:07:57', 'Weija,George Walker', 'Home', 107.66, '3h 27min 27s', '18h 36min 22s', 0, 0, 0, 0, 107.66, '2025-08-03', NULL, NULL),
(139, 'LBS-GN1687 Z', NULL, NULL, 'Home', 'Home', 0.02, '0s', '2h 35min 2s', 0, 0, 0, 0, 0.02, '2025-08-04', NULL, NULL),
(140, 'LBS-GN3634-22', NULL, NULL, 'Home', 'Home', 0.13, '0s', '20h 24min 20s', 0, 0, 0, 0, 0.13, '2025-08-04', NULL, NULL),
(141, 'LBS-GR1583-14', '2025-08-04 10:39:16', '2025-08-04 18:31:09', 'Ashaiman', 'Home', 15.22, '56min 5s', '9h 2min 54s', 0, 0, 0, 0, 15.22, '2025-08-04', NULL, NULL),
(142, 'LBS-GT3425-23', NULL, NULL, 'C1', 'C1', 0.08, '0s', '4h 48min 43s', 0, 0, 0, 0, 0.08, '2025-08-04', NULL, NULL),
(143, 'LBS-GW1509-17', '2025-08-04 13:15:22', '2025-08-04 17:10:19', 'Home', 'Ssnit,Flat', 12.34, '45min 23s', '3h 37min 47s', 0, 0, 0, 0, 12.34, '2025-08-04', NULL, NULL),
(144, 'LBS-GW3711-18', '2025-08-04 14:28:33', '2025-08-04 19:37:21', 'Home', 'Home', 8.27, '17min 40s', '19h 56min 32s', 0, 0, 0, 0, 8.27, '2025-08-04', NULL, NULL),
(145, 'LBS-GN3634-22', NULL, NULL, 'Home', 'Home', 0.05, '0s', '21h 21min 8s', 0, 0, 0, 0, 0.05, '2025-08-05', NULL, NULL),
(146, 'LBS-GR1583-14', '2025-08-05 21:34:16', '2025-08-05 21:41:16', 'Home', 'Prudential House ,C1', 4.07, '6min 31s', '20h 59min 3s', 0, 0, 0, 0, 4.07, '2025-08-05', NULL, NULL),
(147, 'LBS-GT3425-23', NULL, NULL, 'C1', 'C1', 0.23, '0s', '22h 4min 57s', 0, 0, 0, 0, 0.23, '2025-08-05', NULL, NULL),
(148, 'LBS-GW1509-17', '2025-08-05 13:47:28', '2025-08-05 16:16:48', 'Ssnit,Flat', 'C5', 5.15, '18min 34s', '4h 27min 37s', 0, 0, 0, 0, 5.15, '2025-08-05', NULL, NULL),
(149, 'LBS-GW3711-18', '2025-08-05 21:21:25', '2025-08-05 22:05:54', 'Home', 'Ssnit,Tema', 7.04, '16min 1s', '21h 43min 1s', 0, 0, 0, 0, 7.04, '2025-08-05', NULL, NULL),
(150, 'LBS-GN3634-22', '2025-08-06 12:41:19', '2025-08-06 20:27:20', 'Home', 'Home', 25.44, '1h 19min 16s', '18h 46min 5s', 0, 0, 0, 0, 25.44, '2025-08-06', NULL, NULL),
(151, 'LBS-GR1583-14', '2025-08-06 00:06:54', '2025-08-06 18:05:48', 'C5', 'Kpone Katamanso', 36.32, '2h 12s', '19h 17min 22s', 0, 0, 0, 0, 36.32, '2025-08-06', NULL, NULL),
(152, 'LBS-GT3425-23', NULL, NULL, 'C1', 'C1', 0.34, '0s', '22h 1min 57s', 0, 0, 0, 0, 0.34, '2025-08-06', NULL, NULL),
(153, 'LBS-GW1509-17', '2025-08-06 04:09:12', '2025-08-06 05:51:35', 'New Weija,Ga', 'Weija', 49.23, '1h 32min 14s', '15h 8min 0s', 0, 0, 0, 0, 49.23, '2025-08-06', NULL, NULL),
(154, 'LBS-GW3711-18', '2025-08-06 15:16:08', '2025-08-06 16:25:25', 'Fishing Harbour', 'Snnit Flat', 7.12, '22min 53s', '19h 34min 6s', 0, 0, 0, 0, 7.12, '2025-08-06', NULL, NULL),
(155, 'LBS-GN3634-22', '2025-08-07 07:19:15', '2025-08-07 22:46:35', 'Kpone Katamanso', 'High Tension', 39.1, '1h 44min 35s', '20h 57min 21s', 0, 0, 0, 0, 39.1, '2025-08-07', NULL, NULL),
(156, 'LBS-GR1583-14', '2025-08-07 09:35:11', '2025-08-07 18:38:30', 'Home', 'Ssnit Flat', 31.2, '1h 35min 47s', '21h 22min 31s', 0, 0, 0, 0, 31.2, '2025-08-07', NULL, NULL),
(157, 'LBS-GT3425-23', NULL, NULL, 'C1', 'C1', 0.23, '0s', '23h 42min 56s', 0, 0, 0, 0, 0.23, '2025-08-07', NULL, NULL),
(158, 'LBS-GW1509-17', '2025-08-07 17:22:43', '2025-08-07 19:52:26', 'Weija', 'Usher Town', 18.58, '52min 35s', '6h 31min 28s', 0, 0, 0, 0, 18.58, '2025-08-07', NULL, NULL),
(159, 'LBS-GW3711-18', '2025-08-07 00:55:51', '2025-08-07 01:24:33', 'Home', 'Home', 7.96, '12min 18s', '22h 39min 29s', 0, 0, 0, 0, 7.96, '2025-08-07', NULL, NULL),
(160, 'LBS-GN3634-22', '2025-08-08 01:34:27', '2025-08-08 22:22:09', 'Home', 'Kpone Kantamanso', 45.35, '1h 58min 12s', '19h 48min 40s', 0, 0, 0, 0, 45.35, '2025-08-08', NULL, NULL),
(161, 'LBS-GR1583-14', '2025-08-08 11:13:43', '2025-08-08 13:59:46', 'Ssnit,Flat', 'Pantang,Abokobi', 44.59, '1h 39min 34s', '20h 54s', 0, 0, 0, 0, 44.59, '2025-08-08', NULL, NULL),
(162, 'LBS-GT3425-23', NULL, NULL, 'C1', 'C1', 0.13, '0s', '13h 55min 35s', 0, 0, 0, 0, 0.13, '2025-08-08', NULL, NULL),
(163, 'LBS-GW1509-17', '2025-08-08 17:07:50', '2025-08-08 20:45:39', 'Usher Town', 'C5', 30.94, '1h 32min 7s', '7h 43min 28s', 0, 0, 0, 0, 30.94, '2025-08-08', NULL, NULL),
(164, 'LBS-GW3711-18', '2025-08-08 13:19:32', '2025-08-08 21:42:12', 'Home', 'Kantamanso', 30.85, '1h 37min 2s', '8h 12min 19s', 0, 0, 0, 0, 30.85, '2025-08-08', NULL, NULL),
(165, 'LBS-GN3634-22', '2025-08-09 12:04:54', '2025-08-09 19:59:10', 'Kpone,Katamanso', 'Home', 29.74, '1h 15min 45s', '19h 59min 12s', 0, 0, 0, 0, 29.74, '2025-08-09', NULL, NULL),
(166, 'LBS-GR1583-14', '2025-08-09 10:17:33', '2025-08-09 19:34:29', 'Pantang,Abokobi', 'Home', 55.39, '2h 4min 26s', '19h 17min 9s', 0, 0, 0, 0, 55.39, '2025-08-09', NULL, NULL),
(167, 'LBS-GT3425-23', NULL, NULL, 'C1', 'C1', 0.01, '0s', '10h 38min 49s', 0, 0, 0, 0, 0.01, '2025-08-09', NULL, NULL),
(168, 'LBS-GW1509-17', '2025-08-09 11:50:57', '2025-08-09 14:25:45', 'C5', 'Home', 9.25, '28min 6s', '2h 30min 16s', 0, 0, 0, 0, 9.25, '2025-08-09', NULL, NULL),
(169, 'LBS-GW3711-18', '2025-08-09 03:26:28', '2025-08-09 13:26:04', 'Ssnit,Flat', 'Home', 27, '1h 9min 56s', '19h 33min 21s', 0, 0, 0, 0, 27, '2025-08-09', NULL, NULL),
(170, 'LBS-GN3634-22', '2025-08-11 05:45:10', '2025-08-11 17:54:57', 'Home', 'Ssnit ,Flat', 12.86, '48min 46s', '19h 28min 48s', 0, 0, 0, 0, 12.86, '2025-08-11', NULL, NULL),
(171, 'LBS-GR1583-14', '2025-08-11 15:55:03', '2025-08-11 17:42:05', 'Home', 'Home', 6.99, '20min 23s', '19h 36min 11s', 0, 0, 0, 0, 6.99, '2025-08-11', NULL, NULL),
(172, 'LBS-GW1509-17', NULL, NULL, 'Home', 'Home', 0, '0s', '1min 0s', 0, 0, 0, 0, 0, '2025-08-11', NULL, NULL),
(173, 'LBS-GW3711-18', NULL, NULL, 'Home', 'Home', 0.01, '0s', '20h 37min 38s', 0, 0, 0, 0, 0.01, '2025-08-11', NULL, NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `daily_logbook`
--
ALTER TABLE `daily_logbook`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `trips`
--
ALTER TABLE `trips`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `daily_logbook`
--
ALTER TABLE `daily_logbook`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `trips`
--
ALTER TABLE `trips`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=174;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
