-- phpMyAdmin SQL Dump
-- version 4.6.6deb5
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 18, 2018 at 04:16 PM
-- Server version: 5.7.23-0ubuntu0.18.04.1
-- PHP Version: 7.2.7-0ubuntu0.18.04.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `game`
--
CREATE DATABASE IF NOT EXISTS `game` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `game`;

-- --------------------------------------------------------

--
-- Table structure for table `activateStation`
--

CREATE TABLE `activateStation` (
  `id` int(11) NOT NULL,
  `station` varchar(50) NOT NULL,
  `stage` varchar(50) NOT NULL,
  `timeRemaining` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `bombCost`
--

CREATE TABLE `bombCost` (
  `id` int(11) NOT NULL,
  `cost` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `bombsDeployed`
--

CREATE TABLE `bombsDeployed` (
  `id` int(110) NOT NULL,
  `room` int(11) NOT NULL,
  `stationName` varchar(11) NOT NULL,
  `timeDeployed` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bombsDeployed`
--

INSERT INTO `bombsDeployed` (`id`, `room`, `stationName`, `timeDeployed`) VALUES
(1, 2, 'CS12', '2018-09-16 18:37:04'),
(2, 2, 'CS22', '2018-09-16 19:19:12'),
(3, 2, 'AUD2', '2018-09-16 19:30:51'),
(4, 2, 'HAC2', '2018-09-16 19:45:12'),
(5, 2, 'MKP2', '2018-09-16 19:49:03'),
(6, 2, 'BMB2', '2018-09-16 23:02:34'),
(7, 2, 'MAS2', '2018-09-17 12:47:44');

-- --------------------------------------------------------

--
-- Table structure for table `cameras2allow`
--

CREATE TABLE `cameras2allow` (
  `id` int(11) NOT NULL,
  `room` varchar(200) NOT NULL,
  `allow` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `currency`
--

CREATE TABLE `currency` (
  `room` int(11) NOT NULL,
  `amount` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `currency`
--

INSERT INTO `currency` (`room`, `amount`) VALUES
(1, 11787),
(2, 4276);

-- --------------------------------------------------------

--
-- Table structure for table `currentColor`
--

CREATE TABLE `currentColor` (
  `id` int(11) NOT NULL,
  `station` varchar(50) NOT NULL,
  `color` varchar(50) NOT NULL,
  `lightON` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `currentColor`
--

INSERT INTO `currentColor` (`id`, `station`, `color`, `lightON`) VALUES
(1, 'wertwer', 'wertwre', 'orr');

-- --------------------------------------------------------

--
-- Table structure for table `hackCheck`
--

CREATE TABLE `hackCheck` (
  `id` int(11) NOT NULL,
  `roomstation` varchar(50) NOT NULL,
  `status` varchar(50) NOT NULL,
  `timeRemaining` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hackCheck`
--

INSERT INTO `hackCheck` (`id`, `roomstation`, `status`, `timeRemaining`) VALUES
(33, 'CS22', 'hacked', 60),
(34, 'AUD2', 'hacked', 60),
(35, 'CS12', 'hacked', 60),
(36, 'HAC2', 'hacked', 60);

-- --------------------------------------------------------

--
-- Table structure for table `hacks`
--

CREATE TABLE `hacks` (
  `id` int(11) NOT NULL,
  `team` varchar(50) NOT NULL,
  `howMany` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `hacks`
--

INSERT INTO `hacks` (`id`, `team`, `howMany`) VALUES
(1, '1', 294),
(2, '2', 4191);

-- --------------------------------------------------------

--
-- Table structure for table `market`
--

CREATE TABLE `market` (
  `id` int(11) NOT NULL,
  `text` varchar(100) NOT NULL,
  `cost` int(11) NOT NULL,
  `multipleAllowed` varchar(10) NOT NULL DEFAULT 'No'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `market`
--

INSERT INTO `market` (`id`, `text`, `cost`, `multipleAllowed`) VALUES
(1, 'When you mine one of your lights, you get an additional point.', 5, '1'),
(2, 'When you mine an opponents light, you get an additional point.', 3, '1'),
(3, 'When you mine a green light, you get 2 additional points.', 4, '1'),
(4, 'When you mine a red light, you get 2 additional points.', 4, '1'),
(5, 'When you mine a yellow light, you get 2 additional points.', 4, '1'),
(6, 'See two cameras at once.', 4, '1'),
(7, 'Turn off opponents audio for 5 minutes.', 4, '1'),
(8, 'Turn off opponents cameras for 5 minutes.', 5, '1'),
(9, 'Get 4 Hacks.', 6, '2'),
(10, 'Get 6 Hacks.', 8, '1'),
(11, 'Whenever you deploy a bomb, you redeploy all of your bombs.', 7, '1'),
(12, 'See the positions of all bombs your opponent has deployed.', 7, '1'),
(13, 'Detonate all bombs you have previously deployed 10 seconds after this is purchased.', 5, '1'),
(14, 'Pick a station. It cannot be hacked.', 3, '1'),
(15, 'Pick a station. Whenever your opponent hacks it, gain a point.', 3, '1'),
(16, 'Deploy a bomb.', 10, '1'),
(17, '1st level activations take 2 seconds less.', 4, '2'),
(18, 'When you mine an opponents light, you get an additional hack.', 4, '1'),
(19, '2nd level activations take 2 seconds less.', 4, '2'),
(20, '3rd level activations take 2 seconds less.', 4, '2'),
(21, 'Your bombs take 5 seconds less to detonate.', 3, '2'),
(22, 'Hacking Activations take 2 seconds less.', 3, '1'),
(23, 'Choose one of your terminals. Counter hack if opposite room hacks this terminal.', 3, '1'),
(24, 'All of your bombs change position to a random location.', 5, '1'),
(25, 'Reveal the location of one of your opponents bombs.', 3, '1'),
(26, 'Your bombs no longer generate audio alerts.', 3, '1'),
(27, 'Marketplace upgrades cost 1 less.', 3, '1'),
(28, 'Gain 15 points.', 12, '1');

-- --------------------------------------------------------

--
-- Table structure for table `marketCurrent`
--

CREATE TABLE `marketCurrent` (
  `id` int(11) NOT NULL,
  `text` varchar(100) NOT NULL,
  `cost` int(11) NOT NULL,
  `multipleAllowed` varchar(10) NOT NULL DEFAULT 'No',
  `purchased` varchar(10) NOT NULL DEFAULT 'No',
  `itemID` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `marketCurrent`
--

INSERT INTO `marketCurrent` (`id`, `text`, `cost`, `multipleAllowed`, `purchased`, `itemID`) VALUES
(2738, 'Pick a station. Whenever your opponent hacks it, gain a point.', 3, '1', 'Yes', 15),
(2739, 'See the positions of all bombs your opponent has deployed.', 7, '1', 'No', 12),
(2740, 'Get 4 Hacks.', 6, '2', 'No', 9);

-- --------------------------------------------------------

--
-- Table structure for table `marketOwned`
--

CREATE TABLE `marketOwned` (
  `id` int(11) NOT NULL,
  `text` varchar(255) NOT NULL,
  `numberOwned` int(11) NOT NULL,
  `team` int(11) NOT NULL,
  `itemID` int(10) NOT NULL,
  `activated` varchar(15) NOT NULL DEFAULT 'no'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `marketOwned`
--

INSERT INTO `marketOwned` (`id`, `text`, `numberOwned`, `team`, `itemID`, `activated`) VALUES
(158, 'Pick a station. Whenever your opponent hacks it, gain a point.', 1, 1, 15, 'no');

-- --------------------------------------------------------

--
-- Table structure for table `minesCurrent`
--

CREATE TABLE `minesCurrent` (
  `id` int(11) NOT NULL,
  `roomColor` varchar(50) NOT NULL,
  `current` varchar(50) NOT NULL,
  `timeStamp` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `minesCurrent`
--

INSERT INTO `minesCurrent` (`id`, `roomColor`, `current`, `timeStamp`) VALUES
(47, 'green1', 'no', '2018-08-25 18:15:02'),
(48, 'red2', 'no', '2018-08-25 18:15:02'),
(50, 'green2', 'no', '2018-08-25 18:15:51'),
(51, 'yellow1', 'no', '2018-08-25 18:16:43'),
(52, 'blue2', 'no', '2018-08-25 18:16:43'),
(53, 'red1', 'no', '2018-08-25 18:17:37'),
(54, 'yellow2', 'no', '2018-08-25 18:17:37'),
(55, 'blue1', 'no', '2018-08-25 18:18:07');

-- --------------------------------------------------------

--
-- Table structure for table `numberOfBombs`
--

CREATE TABLE `numberOfBombs` (
  `id` int(11) NOT NULL,
  `room` varchar(50) NOT NULL,
  `numberOfBombs` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `numberOfBombs`
--

INSERT INTO `numberOfBombs` (`id`, `room`, `numberOfBombs`) VALUES
(1, '1', 0),
(2, '2', 96);

-- --------------------------------------------------------

--
-- Table structure for table `playerLocation`
--

CREATE TABLE `playerLocation` (
  `id` int(11) NOT NULL,
  `mac` varchar(50) NOT NULL,
  `location` varchar(50) NOT NULL,
  `bleSignal` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `playerLocation`
--

INSERT INTO `playerLocation` (`id`, `mac`, `location`, `bleSignal`) VALUES
(1, 'ec:fe:7e:10:92:c6', 'MKP-1', '89.0');

-- --------------------------------------------------------

--
-- Table structure for table `starter`
--

CREATE TABLE `starter` (
  `id` int(11) NOT NULL,
  `starTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `endTime` datetime DEFAULT NULL,
  `r1Bonus` int(11) NOT NULL,
  `r2Bonus` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `starter`
--

INSERT INTO `starter` (`id`, `starTime`, `endTime`, `r1Bonus`, `r2Bonus`) VALUES
(5, '2018-09-07 22:43:08', NULL, 20, 20);

-- --------------------------------------------------------

--
-- Table structure for table `stationList`
--

CREATE TABLE `stationList` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `room` int(11) NOT NULL,
  `offset` int(20) NOT NULL,
  `distance` int(12) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stationList`
--

INSERT INTO `stationList` (`id`, `name`, `room`, `offset`, `distance`) VALUES
(1, 'CS11', 1, 0, 4),
(2, 'CS21', 1, 0, 4),
(3, 'AUD1', 1, 0, 4),
(4, 'HAC1', 1, 0, 4),
(5, 'MKP1', 1, -1, 4),
(6, 'BMB1', 1, 0, 4),
(7, 'MAS1', 1, 0, 4),
(8, 'MTR1', 1, 0, 4),
(9, 'MOR1', 1, 0, 4),
(10, 'CS12', 2, 0, 4),
(11, 'CS22', 2, 0, 4),
(12, 'AUD2', 2, 0, 4),
(13, 'HAC2', 2, 0, 4),
(14, 'MKP2', 2, 0, 4),
(15, 'BMB2', 2, 0, 4),
(16, 'MAS2', 2, 0, 4),
(17, 'MTR2', 2, 0, 4),
(18, 'MOR2', 2, 0, 4);

-- --------------------------------------------------------

--
-- Table structure for table `stationlocations`
--

CREATE TABLE `stationlocations` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `ip` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `stationlocations`
--

INSERT INTO `stationlocations` (`id`, `name`, `ip`) VALUES
(1, 'server', '10.255.1.254'),
(2, 'AUD-1', '10.255.1.96'),
(3, 'AUD-2', '1.1.1.1'),
(4, 'CAMERAOUT1_2', '10.255.1.90'),
(5, 'CAMERAOUT2_2', '10.255.1.171'),
(6, 'CAMERAOUT3_2', '10.255.1.235'),
(7, 'CAMERAOUT4_2', '10.255.1.6');

-- --------------------------------------------------------

--
-- Table structure for table `timeDoubler`
--

CREATE TABLE `timeDoubler` (
  `id` int(11) NOT NULL,
  `station` varchar(50) NOT NULL,
  `doubler` varchar(50) NOT NULL,
  `room` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `timeDoubler`
--

INSERT INTO `timeDoubler` (`id`, `station`, `doubler`, `room`) VALUES
(51, 'CS11', 'double', 1);

-- --------------------------------------------------------

--
-- Table structure for table `timer`
--

CREATE TABLE `timer` (
  `id` int(11) NOT NULL,
  `seconds` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `timer`
--

INSERT INTO `timer` (`id`, `seconds`) VALUES
(1, 60);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activateStation`
--
ALTER TABLE `activateStation`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bombCost`
--
ALTER TABLE `bombCost`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `bombsDeployed`
--
ALTER TABLE `bombsDeployed`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `stationName` (`stationName`);

--
-- Indexes for table `currency`
--
ALTER TABLE `currency`
  ADD PRIMARY KEY (`room`);

--
-- Indexes for table `currentColor`
--
ALTER TABLE `currentColor`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `hackCheck`
--
ALTER TABLE `hackCheck`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `roomstation` (`roomstation`);

--
-- Indexes for table `hacks`
--
ALTER TABLE `hacks`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `team` (`team`);

--
-- Indexes for table `market`
--
ALTER TABLE `market`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `marketCurrent`
--
ALTER TABLE `marketCurrent`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `marketOwned`
--
ALTER TABLE `marketOwned`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `minesCurrent`
--
ALTER TABLE `minesCurrent`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `roomColor` (`roomColor`);

--
-- Indexes for table `numberOfBombs`
--
ALTER TABLE `numberOfBombs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `playerLocation`
--
ALTER TABLE `playerLocation`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mac` (`mac`);

--
-- Indexes for table `starter`
--
ALTER TABLE `starter`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stationList`
--
ALTER TABLE `stationList`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stationlocations`
--
ALTER TABLE `stationlocations`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `timeDoubler`
--
ALTER TABLE `timeDoubler`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `timer`
--
ALTER TABLE `timer`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activateStation`
--
ALTER TABLE `activateStation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `bombCost`
--
ALTER TABLE `bombCost`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `bombsDeployed`
--
ALTER TABLE `bombsDeployed`
  MODIFY `id` int(110) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `currentColor`
--
ALTER TABLE `currentColor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `hackCheck`
--
ALTER TABLE `hackCheck`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;
--
-- AUTO_INCREMENT for table `hacks`
--
ALTER TABLE `hacks`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `market`
--
ALTER TABLE `market`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;
--
-- AUTO_INCREMENT for table `marketCurrent`
--
ALTER TABLE `marketCurrent`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2741;
--
-- AUTO_INCREMENT for table `marketOwned`
--
ALTER TABLE `marketOwned`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=159;
--
-- AUTO_INCREMENT for table `minesCurrent`
--
ALTER TABLE `minesCurrent`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=56;
--
-- AUTO_INCREMENT for table `numberOfBombs`
--
ALTER TABLE `numberOfBombs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `playerLocation`
--
ALTER TABLE `playerLocation`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `starter`
--
ALTER TABLE `starter`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `stationList`
--
ALTER TABLE `stationList`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT for table `stationlocations`
--
ALTER TABLE `stationlocations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `timeDoubler`
--
ALTER TABLE `timeDoubler`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;
--
-- AUTO_INCREMENT for table `timer`
--
ALTER TABLE `timer`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;--
-- Database: `phpmyadmin`
--
CREATE DATABASE IF NOT EXISTS `phpmyadmin` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `phpmyadmin`;

-- --------------------------------------------------------

--
-- Table structure for table `pma__bookmark`
--

CREATE TABLE `pma__bookmark` (
  `id` int(11) NOT NULL,
  `dbase` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `user` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `label` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `query` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Bookmarks';

-- --------------------------------------------------------

--
-- Table structure for table `pma__central_columns`
--

CREATE TABLE `pma__central_columns` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_type` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_length` text COLLATE utf8_bin,
  `col_collation` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_isNull` tinyint(1) NOT NULL,
  `col_extra` varchar(255) COLLATE utf8_bin DEFAULT '',
  `col_default` text COLLATE utf8_bin
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Central list of columns';

-- --------------------------------------------------------

--
-- Table structure for table `pma__column_info`
--

CREATE TABLE `pma__column_info` (
  `id` int(5) UNSIGNED NOT NULL,
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `column_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `comment` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `mimetype` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `transformation` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `transformation_options` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `input_transformation` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `input_transformation_options` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Column information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__designer_settings`
--

CREATE TABLE `pma__designer_settings` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `settings_data` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Settings related to Designer';

-- --------------------------------------------------------

--
-- Table structure for table `pma__export_templates`
--

CREATE TABLE `pma__export_templates` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `export_type` varchar(10) COLLATE utf8_bin NOT NULL,
  `template_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `template_data` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved export templates';

--
-- Dumping data for table `pma__export_templates`
--

INSERT INTO `pma__export_templates` (`id`, `username`, `export_type`, `template_name`, `template_data`) VALUES
(1, 'game', 'server', 'test', '{\"quick_or_custom\":\"quick\",\"what\":\"sql\",\"db_select[]\":[\"game\",\"phpmyadmin\"],\"output_format\":\"sendit\",\"filename_template\":\"@SERVER@\",\"remember_template\":\"on\",\"charset\":\"utf-8\",\"compression\":\"none\",\"maxsize\":\"\",\"codegen_structure_or_data\":\"data\",\"codegen_format\":\"0\",\"sql_include_comments\":\"something\",\"sql_header_comment\":\"\",\"sql_compatibility\":\"NONE\",\"sql_structure_or_data\":\"structure_and_data\",\"sql_create_table\":\"something\",\"sql_auto_increment\":\"something\",\"sql_create_view\":\"something\",\"sql_create_trigger\":\"something\",\"sql_backquotes\":\"something\",\"sql_type\":\"INSERT\",\"sql_insert_syntax\":\"both\",\"sql_max_query_size\":\"50000\",\"sql_hex_for_binary\":\"something\",\"sql_utc_time\":\"something\",\"mediawiki_structure_or_data\":\"data\",\"mediawiki_caption\":\"something\",\"mediawiki_headers\":\"something\",\"pdf_report_title\":\"\",\"pdf_structure_or_data\":\"data\",\"ods_null\":\"NULL\",\"ods_structure_or_data\":\"data\",\"texytext_structure_or_data\":\"structure_and_data\",\"texytext_null\":\"NULL\",\"htmlword_structure_or_data\":\"structure_and_data\",\"htmlword_null\":\"NULL\",\"latex_caption\":\"something\",\"latex_structure_or_data\":\"structure_and_data\",\"latex_structure_caption\":\"Structure of table @TABLE@\",\"latex_structure_continued_caption\":\"Structure of table @TABLE@ (continued)\",\"latex_structure_label\":\"tab:@TABLE@-structure\",\"latex_relation\":\"something\",\"latex_comments\":\"something\",\"latex_mime\":\"something\",\"latex_columns\":\"something\",\"latex_data_caption\":\"Content of table @TABLE@\",\"latex_data_continued_caption\":\"Content of table @TABLE@ (continued)\",\"latex_data_label\":\"tab:@TABLE@-data\",\"latex_null\":\"\\\\textit{NULL}\",\"yaml_structure_or_data\":\"data\",\"json_structure_or_data\":\"data\",\"csv_separator\":\",\",\"csv_enclosed\":\"\\\"\",\"csv_escaped\":\"\\\"\",\"csv_terminated\":\"AUTO\",\"csv_null\":\"NULL\",\"csv_structure_or_data\":\"data\",\"odt_structure_or_data\":\"structure_and_data\",\"odt_relation\":\"something\",\"odt_comments\":\"something\",\"odt_mime\":\"something\",\"odt_columns\":\"something\",\"odt_null\":\"NULL\",\"excel_null\":\"NULL\",\"excel_edition\":\"win\",\"excel_structure_or_data\":\"data\",\"phparray_structure_or_data\":\"data\",\"\":null,\"as_separate_files\":null,\"sql_dates\":null,\"sql_relation\":null,\"sql_mime\":null,\"sql_use_transaction\":null,\"sql_disable_fk\":null,\"sql_views_as_tables\":null,\"sql_metadata\":null,\"sql_drop_database\":null,\"sql_drop_table\":null,\"sql_if_not_exists\":null,\"sql_procedure_function\":null,\"sql_truncate\":null,\"sql_delayed\":null,\"sql_ignore\":null,\"ods_columns\":null,\"texytext_columns\":null,\"htmlword_columns\":null,\"json_pretty_print\":null,\"csv_removeCRLF\":null,\"csv_columns\":null,\"excel_removeCRLF\":null,\"excel_columns\":null}');

-- --------------------------------------------------------

--
-- Table structure for table `pma__favorite`
--

CREATE TABLE `pma__favorite` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `tables` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Favorite tables';

-- --------------------------------------------------------

--
-- Table structure for table `pma__history`
--

CREATE TABLE `pma__history` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `username` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `db` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `table` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `timevalue` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `sqlquery` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='SQL history for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__navigationhiding`
--

CREATE TABLE `pma__navigationhiding` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `item_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `item_type` varchar(64) COLLATE utf8_bin NOT NULL,
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Hidden items of navigation tree';

-- --------------------------------------------------------

--
-- Table structure for table `pma__pdf_pages`
--

CREATE TABLE `pma__pdf_pages` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `page_nr` int(10) UNSIGNED NOT NULL,
  `page_descr` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='PDF relation pages for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__recent`
--

CREATE TABLE `pma__recent` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `tables` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Recently accessed tables';

--
-- Dumping data for table `pma__recent`
--

INSERT INTO `pma__recent` (`username`, `tables`) VALUES
('game', '[{\"db\":\"game\",\"table\":\"hackCheck\"},{\"db\":\"game\",\"table\":\"timeDoubler\"},{\"db\":\"game\",\"table\":\"bombsDeployed\"},{\"db\":\"game\",\"table\":\"hacks\"},{\"db\":\"game\",\"table\":\"marketCurrent\"},{\"db\":\"game\",\"table\":\"marketOwned\"},{\"db\":\"game\",\"table\":\"currency\"},{\"db\":\"game\",\"table\":\"market\"},{\"db\":\"game\",\"table\":\"minesCurrent\"},{\"db\":\"game\",\"table\":\"bombCost\"}]');

-- --------------------------------------------------------

--
-- Table structure for table `pma__relation`
--

CREATE TABLE `pma__relation` (
  `master_db` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `master_table` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `master_field` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `foreign_db` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `foreign_table` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `foreign_field` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Relation table';

-- --------------------------------------------------------

--
-- Table structure for table `pma__savedsearches`
--

CREATE TABLE `pma__savedsearches` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `search_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `search_data` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved searches';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_coords`
--

CREATE TABLE `pma__table_coords` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `pdf_page_number` int(11) NOT NULL DEFAULT '0',
  `x` float UNSIGNED NOT NULL DEFAULT '0',
  `y` float UNSIGNED NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table coordinates for phpMyAdmin PDF output';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_info`
--

CREATE TABLE `pma__table_info` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `display_field` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_uiprefs`
--

CREATE TABLE `pma__table_uiprefs` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `prefs` text COLLATE utf8_bin NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Tables'' UI preferences';

--
-- Dumping data for table `pma__table_uiprefs`
--

INSERT INTO `pma__table_uiprefs` (`username`, `db_name`, `table_name`, `prefs`, `last_update`) VALUES
('game', 'game', 'currency', '{\"sorted_col\":\"`currency`.`room` ASC\"}', '2018-09-12 22:30:55'),
('game', 'game', 'marketCurrent', '{\"sorted_col\":\"`marketCurrent`.`id` ASC\"}', '2018-09-15 07:21:35'),
('game', 'game', 'marketOwned', '{\"sorted_col\":\"`activated` ASC\"}', '2018-09-15 07:05:54'),
('game', 'game', 'stationList', '{\"sorted_col\":\"`stationList`.`id` ASC\"}', '2018-09-12 08:10:16');

-- --------------------------------------------------------

--
-- Table structure for table `pma__tracking`
--

CREATE TABLE `pma__tracking` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `version` int(10) UNSIGNED NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  `schema_snapshot` text COLLATE utf8_bin NOT NULL,
  `schema_sql` text COLLATE utf8_bin,
  `data_sql` longtext COLLATE utf8_bin,
  `tracking` set('UPDATE','REPLACE','INSERT','DELETE','TRUNCATE','CREATE DATABASE','ALTER DATABASE','DROP DATABASE','CREATE TABLE','ALTER TABLE','RENAME TABLE','DROP TABLE','CREATE INDEX','DROP INDEX','CREATE VIEW','ALTER VIEW','DROP VIEW') COLLATE utf8_bin DEFAULT NULL,
  `tracking_active` int(1) UNSIGNED NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Database changes tracking for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__userconfig`
--

CREATE TABLE `pma__userconfig` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `timevalue` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `config_data` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User preferences storage for phpMyAdmin';

--
-- Dumping data for table `pma__userconfig`
--

INSERT INTO `pma__userconfig` (`username`, `timevalue`, `config_data`) VALUES
('game', '2018-09-07 21:21:20', '{\"collation_connection\":\"utf8mb4_unicode_ci\"}');

-- --------------------------------------------------------

--
-- Table structure for table `pma__usergroups`
--

CREATE TABLE `pma__usergroups` (
  `usergroup` varchar(64) COLLATE utf8_bin NOT NULL,
  `tab` varchar(64) COLLATE utf8_bin NOT NULL,
  `allowed` enum('Y','N') COLLATE utf8_bin NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User groups with configured menu items';

-- --------------------------------------------------------

--
-- Table structure for table `pma__users`
--

CREATE TABLE `pma__users` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `usergroup` varchar(64) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Users and their assignments to user groups';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pma__central_columns`
--
ALTER TABLE `pma__central_columns`
  ADD PRIMARY KEY (`db_name`,`col_name`);

--
-- Indexes for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `db_name` (`db_name`,`table_name`,`column_name`);

--
-- Indexes for table `pma__designer_settings`
--
ALTER TABLE `pma__designer_settings`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_user_type_template` (`username`,`export_type`,`template_name`);

--
-- Indexes for table `pma__favorite`
--
ALTER TABLE `pma__favorite`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__history`
--
ALTER TABLE `pma__history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`,`db`,`table`,`timevalue`);

--
-- Indexes for table `pma__navigationhiding`
--
ALTER TABLE `pma__navigationhiding`
  ADD PRIMARY KEY (`username`,`item_name`,`item_type`,`db_name`,`table_name`);

--
-- Indexes for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  ADD PRIMARY KEY (`page_nr`),
  ADD KEY `db_name` (`db_name`);

--
-- Indexes for table `pma__recent`
--
ALTER TABLE `pma__recent`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__relation`
--
ALTER TABLE `pma__relation`
  ADD PRIMARY KEY (`master_db`,`master_table`,`master_field`),
  ADD KEY `foreign_field` (`foreign_db`,`foreign_table`);

--
-- Indexes for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_savedsearches_username_dbname` (`username`,`db_name`,`search_name`);

--
-- Indexes for table `pma__table_coords`
--
ALTER TABLE `pma__table_coords`
  ADD PRIMARY KEY (`db_name`,`table_name`,`pdf_page_number`);

--
-- Indexes for table `pma__table_info`
--
ALTER TABLE `pma__table_info`
  ADD PRIMARY KEY (`db_name`,`table_name`);

--
-- Indexes for table `pma__table_uiprefs`
--
ALTER TABLE `pma__table_uiprefs`
  ADD PRIMARY KEY (`username`,`db_name`,`table_name`);

--
-- Indexes for table `pma__tracking`
--
ALTER TABLE `pma__tracking`
  ADD PRIMARY KEY (`db_name`,`table_name`,`version`);

--
-- Indexes for table `pma__userconfig`
--
ALTER TABLE `pma__userconfig`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__usergroups`
--
ALTER TABLE `pma__usergroups`
  ADD PRIMARY KEY (`usergroup`,`tab`,`allowed`);

--
-- Indexes for table `pma__users`
--
ALTER TABLE `pma__users`
  ADD PRIMARY KEY (`username`,`usergroup`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
--
-- AUTO_INCREMENT for table `pma__history`
--
ALTER TABLE `pma__history`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  MODIFY `page_nr` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
