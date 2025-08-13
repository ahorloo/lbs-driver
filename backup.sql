-- MariaDB dump 10.19  Distrib 10.4.28-MariaDB, for osx10.10 (x86_64)
--
-- Host: localhost    Database: driver_logbook_db
-- ------------------------------------------------------
-- Server version	10.4.28-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `daily_logbook`
--

DROP TABLE IF EXISTS `daily_logbook`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `daily_logbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `remarks` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `daily_logbook`
--

LOCK TABLES `daily_logbook` WRITE;
/*!40000 ALTER TABLE `daily_logbook` DISABLE KEYS */;
/*!40000 ALTER TABLE `daily_logbook` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trips`
--

DROP TABLE IF EXISTS `trips`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trips` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
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
  `distance` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=135 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trips`
--

LOCK TABLES `trips` WRITE;
/*!40000 ALTER TABLE `trips` DISABLE KEYS */;
INSERT INTO `trips` VALUES (128,'LBS-GB3281-22',NULL,NULL,'Home','Home',0.05,'0s','21h 21min 1s',0,0,0,0,0.05,'2025-08-01',NULL,NULL),(129,'LBS-GN3634-22','2025-08-01 00:12:13','2025-08-01 22:37:46','Kpone-Katamanso','Community 2',27.57,'1h 8min 2s','21h 29min 3s',0,0,0,0,27.57,'2025-08-01',NULL,NULL),(130,'LBS-GR1583-14',NULL,NULL,'Ashaiman','Ashaiman',0.08,'0s','8min 35s',0,0,0,0,0.08,'2025-08-01',NULL,NULL),(131,'LBS-GW1509-17','2025-08-01 14:58:09','2025-08-01 20:54:24','Home','Tema',14.02,'52min 47s','5h 21min 0s',0,0,0,0,14.02,'2025-08-01',NULL,NULL),(132,'LBS-GW3711-18','2025-08-01 14:40:30','2025-08-01 18:35:20','Tema','Ningo-Prampram',36.96,'1h 35min 10s','20h 12min 49s',0,0,0,0,36.96,'2025-08-01',NULL,NULL),(134,'LBS-GW3711-18','2025-08-02 09:50:52','2025-08-02 16:44:30','Nigo-Prampram','Community 1',39.26,'1h 28min 41s','15h 37min 2s',0,0,0,0,39.26,'2025-08-02',NULL,NULL);
/*!40000 ALTER TABLE `trips` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-03  9:58:35
