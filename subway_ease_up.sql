-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2023-08-07 10:48:26
-- 服务器版本： 10.4.22-MariaDB
-- PHP 版本： 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `subway_ease_up`
--

-- --------------------------------------------------------

--
-- 表的结构 `access_signal`
--

CREATE TABLE `access_signal` (
  `idx` int(11) NOT NULL,
  `cid` int(5) NOT NULL,
  `route_way` varchar(3) NOT NULL,
  `leave_station` int(3) NOT NULL,
  `enter_station` int(3) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `access_signal`
--

INSERT INTO `access_signal` (`idx`, `cid`, `route_way`, `leave_station`, `enter_station`, `timestamp`) VALUES
(1, 168, 'OT1', 1, 0, '2023-07-28 18:26:15'),
(2, 168, 'OT1', 1, 0, '2023-07-29 11:00:00'),
(3, 168, 'OT1', 2, 1, '2023-07-29 14:41:07'),
(4, 168, 'OT1', 3, 2, '2023-07-29 14:55:41'),
(5, 168, 'OT1', 0, 0, '2023-07-29 15:01:35'),
(6, 168, 'OT1', 1, 0, '2023-07-29 15:50:45'),
(7, 168, 'OT1', 0, 0, '2023-07-30 09:10:04'),
(8, 168, 'OT1', 1, 0, '2023-07-30 10:03:31'),
(9, 168, 'OT1', 1, 1, '2023-07-30 10:20:56'),
(10, 168, 'OT1', 1, 0, '2023-07-30 12:57:34'),
(11, 168, 'OT1', 0, 0, '2023-07-30 13:11:49'),
(12, 168, 'OT1', 1, 0, '2023-07-31 07:54:40'),
(13, 168, 'OT1', 0, 0, '2023-07-31 08:01:45'),
(14, 168, 'OT1', 3, 3, '2023-07-31 13:02:06'),
(15, 168, 'OT1', 0, 0, '2023-07-31 16:45:09'),
(17, 168, 'OT1', 1, 0, '2023-07-31 16:53:50'),
(18, 168, 'OT1', 1, 1, '2023-07-31 16:54:00'),
(19, 168, 'OT1', 2, 1, '2023-07-31 16:54:10'),
(20, 168, 'OT1', 2, 2, '2023-07-31 16:54:22'),
(21, 168, 'OT1', 3, 2, '2023-07-31 16:54:32'),
(22, 168, 'OT1', 3, 3, '2023-07-31 16:54:42'),
(23, 168, 'OT1', 4, 3, '2023-07-31 16:54:53'),
(24, 168, 'OT1', 4, 4, '2023-07-31 16:55:03'),
(25, 168, 'OT1', 3, 3, '2023-07-31 17:00:44'),
(26, 168, 'OT1', 4, 3, '2023-07-31 17:01:13'),
(27, 168, 'OT1', 4, 4, '2023-07-31 17:01:23'),
(28, 168, 'OT1', 0, 0, '2023-07-31 17:05:21'),
(29, 168, 'OT1', 1, 0, '2023-07-31 17:05:38'),
(30, 168, 'OT1', 1, 1, '2023-07-31 17:05:48'),
(31, 168, 'OT1', 2, 1, '2023-07-31 17:05:59'),
(32, 168, 'OT1', 2, 2, '2023-07-31 17:06:14'),
(33, 168, 'OT1', 3, 2, '2023-07-31 17:06:24'),
(34, 168, 'OT1', 3, 3, '2023-07-31 17:06:34'),
(35, 168, 'OT1', 4, 3, '2023-07-31 17:06:50'),
(36, 168, 'OT1', 4, 4, '2023-07-31 17:07:05'),
(37, 168, 'OT1', 2, 1, '2023-08-01 12:50:24'),
(38, 168, 'OT1', 2, 1, '2023-08-01 17:08:51'),
(39, 168, 'OT1', 2, 1, '2023-08-01 17:33:27'),
(40, 168, 'OT1', 2, 1, '2023-08-01 17:42:18'),
(41, 168, 'OT1', 1, 0, '2023-08-01 18:05:03'),
(42, 133, 'OT1', 2, 1, '2023-08-01 18:05:03'),
(43, 168, 'OT1', 1, 0, '2023-08-01 18:07:19'),
(44, 168, 'OT1', 2, 1, '2023-08-02 03:21:02'),
(45, 168, 'OT1', 3, 2, '2023-08-02 03:22:00'),
(46, 133, 'OT1', 1, 0, '2023-08-02 03:34:33'),
(47, 168, 'OT1', 2, 1, '2023-08-02 03:35:20'),
(48, 168, 'OT1', 1, 0, '2023-08-02 03:41:00'),
(49, 133, 'OT1', 1, 0, '2023-08-02 03:47:49'),
(50, 168, 'OT1', 1, 1, '2023-08-02 04:02:31'),
(51, 168, 'OT1', 2, 1, '2023-08-02 04:02:48'),
(52, 168, 'OT1', 2, 2, '2023-08-02 04:02:59'),
(53, 168, 'OT1', 3, 2, '2023-08-02 04:03:11'),
(54, 168, 'OT1', 1, 0, '2023-08-02 05:32:19'),
(55, 168, 'OT1', 1, 0, '2023-08-02 07:37:41'),
(56, 168, 'OT1', 1, 0, '2023-08-02 07:46:47'),
(57, 168, 'OT1', 0, 0, '2023-08-02 08:24:49'),
(58, 168, 'OT1', 1, 0, '2023-08-02 08:32:52'),
(59, 168, 'OT1', 1, 1, '2023-08-02 08:33:03'),
(60, 168, 'OT1', 2, 1, '2023-08-02 08:34:33'),
(61, 168, 'OT1', 2, 2, '2023-08-02 08:34:44'),
(62, 168, 'OT1', 3, 2, '2023-08-02 08:35:55'),
(63, 168, 'OT1', 3, 3, '2023-08-02 08:36:05'),
(64, 168, 'OT1', 0, 0, '2023-08-02 08:39:30'),
(65, 168, 'OT1', 3, 3, '2023-08-03 02:28:43'),
(66, 168, 'OT1', 0, 0, '2023-08-03 02:57:44'),
(67, 168, 'OT1', 1, 0, '2023-08-03 02:58:57'),
(68, 168, 'OT1', 1, 1, '2023-08-03 03:01:00'),
(69, 168, 'OT1', 2, 1, '2023-08-03 03:02:00'),
(70, 168, 'OT1', 2, 2, '2023-08-03 03:04:01'),
(71, 168, 'OT1', 3, 2, '2023-08-03 03:05:02'),
(72, 168, 'OT1', 3, 3, '2023-08-03 03:07:03'),
(73, 168, 'OT1', 0, 0, '2023-08-03 13:48:06'),
(74, 168, 'OT1', 1, 0, '2023-08-03 13:50:35'),
(75, 168, 'OT1', 1, 1, '2023-08-03 13:52:36'),
(76, 168, 'OT1', 2, 1, '2023-08-03 13:53:37'),
(77, 168, 'OT1', 2, 2, '2023-08-03 13:55:37'),
(78, 168, 'OT1', 3, 2, '2023-08-03 13:56:38'),
(79, 168, 'OT1', 0, 0, '2023-08-03 13:58:54'),
(80, 168, 'OT1', 0, 0, '2023-08-03 14:06:40'),
(81, 168, 'OT1', 0, 0, '2023-08-03 14:10:58'),
(84, 168, 'OT1', 1, 1, '2023-08-03 15:55:03'),
(85, 168, 'OT1', 0, 0, '2023-08-03 16:06:18'),
(86, 168, 'OT1', 1, 0, '2023-08-03 16:12:57'),
(87, 168, 'OT1', 2, 2, '2023-08-03 16:41:20'),
(89, 176, 'O1', 0, 0, '2023-08-03 16:49:21'),
(90, 168, 'OT1', 2, 1, '2023-08-03 17:02:39'),
(91, 168, 'OT1', 2, 2, '2023-08-03 17:03:42'),
(92, 168, 'OT1', 3, 2, '2023-08-03 17:04:50'),
(93, 168, 'OT1', 2, 1, '2023-08-04 08:19:06'),
(94, 168, 'O1', 2, 1, '2023-08-04 08:28:13'),
(95, 168, 'OT1', 2, 1, '2023-08-04 09:30:45'),
(96, 168, 'O1', 2, 1, '2023-08-04 09:53:59'),
(97, 168, 'O1', 2, 2, '2023-08-04 09:55:00'),
(98, 168, 'O1', 0, 0, '2023-08-04 09:57:07'),
(99, 168, 'OT1', 0, 0, '2023-08-04 10:04:16'),
(100, 168, 'OT1', 1, 0, '2023-08-04 10:04:53'),
(101, 168, 'OT1', 1, 1, '2023-08-04 10:05:04'),
(102, 168, 'OT1', 2, 1, '2023-08-04 10:05:19'),
(103, 168, 'OT1', 2, 2, '2023-08-04 10:05:37'),
(104, 168, 'OT1', 3, 2, '2023-08-04 10:05:47'),
(105, 168, 'OT1', 3, 3, '2023-08-04 10:05:58'),
(106, 168, 'O1', 0, 0, '2023-08-04 10:06:31'),
(107, 168, 'O1', 1, 0, '2023-08-05 13:01:23'),
(108, 168, 'O1', 1, 1, '2023-08-05 13:01:34'),
(109, 168, 'O1', 2, 1, '2023-08-05 13:01:44'),
(110, 168, 'O1', 2, 2, '2023-08-05 13:01:54'),
(111, 168, 'O1', 3, 2, '2023-08-05 13:02:04'),
(112, 168, 'O1', 3, 3, '2023-08-05 13:02:15'),
(113, 168, 'O1', 1, 0, '2023-08-05 13:03:29'),
(114, 168, 'O1', 1, 1, '2023-08-05 13:03:42'),
(115, 168, 'O1', 2, 1, '2023-08-05 13:03:55'),
(116, 168, 'O1', 2, 2, '2023-08-05 13:04:12'),
(117, 168, 'O1', 3, 2, '2023-08-05 13:04:23'),
(118, 168, 'O1', 3, 3, '2023-08-05 13:04:35'),
(119, 168, 'O1', 1, 0, '2023-08-05 13:06:55'),
(120, 168, 'O1', 1, 0, '2023-08-05 13:36:15'),
(121, 168, 'OT1', 1, 0, '2023-08-05 13:42:55'),
(122, 133, 'O1', 1, 0, '2023-08-05 13:45:56'),
(124, 133, 'O1', 1, 1, '2023-08-05 13:59:02'),
(125, 133, 'O1', 1, 0, '2023-08-05 14:03:37'),
(126, 168, 'O1', 0, 0, '2023-08-05 14:06:13'),
(127, 168, 'O1', 4, 4, '2023-08-05 14:06:35'),
(129, 168, 'OT1', 0, 0, '2023-08-07 02:32:52'),
(130, 168, 'OT1', 1, 0, '2023-08-07 02:34:02'),
(131, 168, 'OT1', 1, 1, '2023-08-07 02:34:12'),
(132, 168, 'OT1', 2, 1, '2023-08-07 02:34:23'),
(133, 168, 'OT1', 2, 2, '2023-08-07 02:34:38'),
(134, 168, 'OT1', 3, 2, '2023-08-07 02:34:48'),
(135, 168, 'OT1', 3, 3, '2023-08-07 02:35:04'),
(136, 168, 'OT1', 0, 0, '2023-08-07 02:45:06'),
(137, 168, 'OT1', 1, 0, '2023-08-07 02:49:08'),
(138, 168, 'OT1', 1, 1, '2023-08-07 03:13:06'),
(139, 168, 'OT1', 2, 1, '2023-08-07 03:13:17'),
(140, 168, 'OT1', 2, 2, '2023-08-07 03:13:43'),
(141, 168, 'OT1', 3, 2, '2023-08-07 03:13:54'),
(142, 168, 'OT1', 3, 3, '2023-08-07 03:14:04'),
(143, 168, 'OT1', 0, 0, '2023-08-07 06:11:11'),
(144, 168, 'OT1', 1, 0, '2023-08-07 06:13:13'),
(145, 168, 'OT1', 1, 1, '2023-08-07 06:13:23'),
(146, 168, 'OT1', 2, 1, '2023-08-07 06:14:27'),
(147, 168, 'OT1', 2, 2, '2023-08-07 06:14:39'),
(148, 168, 'OT1', 3, 2, '2023-08-07 06:14:51'),
(149, 168, 'OT1', 3, 3, '2023-08-07 06:15:03'),
(150, 168, 'OT1', 0, 0, '2023-08-07 06:17:39'),
(151, 168, 'OT1', 1, 0, '2023-08-07 06:18:11'),
(152, 168, 'OT1', 1, 1, '2023-08-07 06:21:37'),
(153, 168, 'OT1', 2, 1, '2023-08-07 06:21:47');

-- --------------------------------------------------------

--
-- 表的结构 `carriage_info`
--

CREATE TABLE `carriage_info` (
  `idx` int(11) NOT NULL,
  `cid` int(5) NOT NULL,
  `cNo` int(3) NOT NULL,
  `pNum` enum('不壅擠','尚可','壅擠') DEFAULT '不壅擠',
  `air` int(4) NOT NULL DEFAULT 0,
  `volume` int(4) NOT NULL DEFAULT 0,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `carriage_info`
--

INSERT INTO `carriage_info` (`idx`, `cid`, `cNo`, `pNum`, `air`, `volume`, `timestamp`) VALUES
(1, 168, 1, '不壅擠', 20, 50, '2023-07-28 18:25:03'),
(2, 168, 2, '不壅擠', 20, 50, '2023-07-28 18:25:04'),
(3, 168, 3, '不壅擠', 20, 50, '2023-07-28 18:25:04'),
(4, 168, 1, '不壅擠', 21, 21, '2023-07-29 11:00:57'),
(5, 168, 1, '尚可', 21, 21, '2023-08-01 10:28:42'),
(6, 168, 2, '不壅擠', 21, 21, '2023-08-01 10:28:42'),
(7, 168, 3, '不壅擠', 21, 21, '2023-08-01 10:28:42'),
(8, 133, 1, '不壅擠', 34, 34, '2023-08-05 14:01:41'),
(9, 133, 2, '不壅擠', 34, 34, '2023-08-05 14:01:41'),
(10, 133, 3, '不壅擠', 34, 34, '2023-08-05 14:01:41'),
(11, 133, 2, '不壅擠', 34, 34, '2023-08-05 14:04:58');

-- --------------------------------------------------------

--
-- 表的结构 `facility_location`
--

CREATE TABLE `facility_location` (
  `idx` int(11) NOT NULL,
  `sid` varchar(3) NOT NULL,
  `sName` varchar(15) NOT NULL,
  `way` enum('OT1','O1') NOT NULL,
  `facility_type` varchar(15) NOT NULL,
  `facility_way` varchar(3) DEFAULT NULL,
  `relative_position` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `facility_location`
--

INSERT INTO `facility_location` (`idx`, `sid`, `sName`, `way`, `facility_type`, `facility_way`, `relative_position`) VALUES
(1, 'O1', '西子灣', 'OT1', 'display_panel', NULL, 1),
(2, 'O1', '西子灣', 'OT1', 'stairs', 'OT1', 4.5),
(3, 'O1', '西子灣', 'OT1', 'escalator', 'OT1', 7.5),
(4, 'O1', '西子灣', 'OT1', 'stairs', 'OT1', 9.5),
(5, 'O1', '西子灣', 'OT1', 'display_panel', NULL, 10.5),
(6, 'O1', '西子灣', 'OT1', 'elevator', NULL, 11),
(7, 'O1', '西子灣', 'OT1', 'stairs', 'O1', 12),
(8, 'O1', '西子灣', 'OT1', 'escalator', 'O1', 12),
(9, 'O2', '鹽埕埔', 'OT1', 'display_panel', NULL, 2.5),
(10, 'O2', '鹽埕埔', 'OT1', 'escalator', 'OT1', 5.5),
(11, 'O2', '鹽埕埔', 'OT1', 'stairs', 'OT1', 9),
(12, 'O2', '鹽埕埔', 'OT1', 'elevator', NULL, 9.5),
(13, 'O2', '鹽埕埔', 'OT1', 'display_panel', NULL, 10),
(14, 'O2', '鹽埕埔', 'OT1', 'escalator', 'O1', 12),
(15, 'O2', '鹽埕埔', 'O1', 'display_panel', NULL, 3.5),
(16, 'O2', '鹽埕埔', 'O1', 'escalator', 'O1', 7),
(17, 'O2', '鹽埕埔', 'O1', 'display_panel', NULL, 9),
(18, 'O2', '鹽埕埔', 'O1', 'elevator', NULL, 12),
(19, 'O2', '鹽埕埔', 'O1', 'stairs', 'OT1', 12),
(20, 'O2', '鹽埕埔', 'O1', 'escalator', 'OT1', 12),
(21, 'O4', '市議會(舊址)', 'OT1', 'display_panel', NULL, 1.5),
(22, 'O4', '市議會(舊址)', 'OT1', 'display_panel', NULL, 3.5),
(23, 'O4', '市議會(舊址)', 'OT1', 'escalator', 'O1', 4),
(24, 'O4', '市議會(舊址)', 'OT1', 'display_panel', NULL, 8.5),
(25, 'O4', '市議會(舊址)', 'OT1', 'stairs', 'O1', 9.5),
(26, 'O4', '市議會(舊址)', 'OT1', 'elevator', NULL, 12),
(27, 'O4', '市議會(舊址)', 'OT1', 'stairs', 'OT1', 12),
(28, 'O4', '市議會(舊址)', 'OT1', 'escalator', 'OT1', 12),
(29, 'O4', '市議會(舊址)', 'O1', 'display_panel', NULL, 1.5),
(30, 'O4', '市議會(舊址)', 'O1', 'display_panel', NULL, 4.5),
(31, 'O4', '市議會(舊址)', 'O1', 'escalator', 'OT1', 5.5),
(32, 'O4', '市議會(舊址)', 'O1', 'display_panel', NULL, 8.5),
(33, 'O4', '市議會(舊址)', 'O1', 'stairs', 'OT1', 8.5),
(34, 'O4', '市議會(舊址)', 'O1', 'elevator', NULL, 12),
(35, 'O4', '市議會(舊址)', 'O1', 'stairs', 'O1', 12),
(36, 'O4', '市議會(舊址)', 'O1', 'escalator', 'O1', 12),
(37, 'O5', '美麗島', 'OT1', 'escalator', 'O1', 5),
(38, 'O5', '美麗島', 'OT1', 'display_panel', NULL, 5),
(39, 'O5', '美麗島', 'OT1', 'stairs', 'O1', 9),
(40, 'O5', '美麗島', 'OT1', 'elevator', NULL, 10.5),
(41, 'O5', '美麗島', 'OT1', 'display_panel', NULL, 10.5),
(42, 'O5', '美麗島', 'OT1', 'stairs', 'O1', 11),
(43, 'O5', '美麗島', 'OT1', 'escalator', 'O1', 12),
(44, 'O5', '美麗島', 'OT1', 'stairs', 'O1', 12),
(45, 'O5', '美麗島', 'O1', 'display_panel', NULL, 3),
(46, 'O5', '美麗島', 'O1', 'stairs', 'O1', 4),
(47, 'O5', '美麗島', 'O1', 'escalator', 'O1', 7.5),
(48, 'O5', '美麗島', 'O1', 'display_panel', NULL, 7.5),
(49, 'O5', '美麗島', 'O1', 'stairs', 'O1', 11),
(50, 'O5', '美麗島', 'O1', 'elevator', NULL, 12),
(51, 'O5', '美麗島', 'O1', 'stairs', 'O1', 12),
(52, 'O5', '美麗島', 'O1', 'escalator', 'O1', 12),
(56, 'O1', '西子灣', 'O1', 'stairs', 'O1', 2),
(57, 'O1', '西子灣', 'O1', 'escalator', 'O1', 3),
(58, 'O1', '西子灣', 'O1', 'stairs', 'O1', 4.5),
(59, 'O1', '西子灣', 'O1', 'elevator', '', 12),
(60, 'O1', '西子灣', 'O1', 'stairs', 'OT1', 12),
(61, 'O1', '西子灣', 'O1', 'escalator', 'OT1', 12);

-- --------------------------------------------------------

--
-- 表的结构 `pma__bookmark`
--

CREATE TABLE `pma__bookmark` (
  `id` int(10) UNSIGNED NOT NULL,
  `dbase` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `user` varchar(255) COLLATE utf8_bin NOT NULL DEFAULT '',
  `label` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '',
  `query` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Bookmarks';

-- --------------------------------------------------------

--
-- 表的结构 `pma__central_columns`
--

CREATE TABLE `pma__central_columns` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_type` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_length` text COLLATE utf8_bin DEFAULT NULL,
  `col_collation` varchar(64) COLLATE utf8_bin NOT NULL,
  `col_isNull` tinyint(1) NOT NULL,
  `col_extra` varchar(255) COLLATE utf8_bin DEFAULT '',
  `col_default` text COLLATE utf8_bin DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Central list of columns';

-- --------------------------------------------------------

--
-- 表的结构 `pma__column_info`
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
-- 表的结构 `pma__designer_settings`
--

CREATE TABLE `pma__designer_settings` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `settings_data` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Settings related to Designer';

-- --------------------------------------------------------

--
-- 表的结构 `pma__export_templates`
--

CREATE TABLE `pma__export_templates` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `export_type` varchar(10) COLLATE utf8_bin NOT NULL,
  `template_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `template_data` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved export templates';

-- --------------------------------------------------------

--
-- 表的结构 `pma__favorite`
--

CREATE TABLE `pma__favorite` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `tables` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Favorite tables';

-- --------------------------------------------------------

--
-- 表的结构 `pma__history`
--

CREATE TABLE `pma__history` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `username` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `db` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `table` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp(),
  `sqlquery` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='SQL history for phpMyAdmin';

-- --------------------------------------------------------

--
-- 表的结构 `pma__navigationhiding`
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
-- 表的结构 `pma__pdf_pages`
--

CREATE TABLE `pma__pdf_pages` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `page_nr` int(10) UNSIGNED NOT NULL,
  `page_descr` varchar(50) CHARACTER SET utf8 NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='PDF relation pages for phpMyAdmin';

-- --------------------------------------------------------

--
-- 表的结构 `pma__recent`
--

CREATE TABLE `pma__recent` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `tables` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Recently accessed tables';

-- --------------------------------------------------------

--
-- 表的结构 `pma__relation`
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
-- 表的结构 `pma__savedsearches`
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
-- 表的结构 `pma__table_coords`
--

CREATE TABLE `pma__table_coords` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `pdf_page_number` int(11) NOT NULL DEFAULT 0,
  `x` float UNSIGNED NOT NULL DEFAULT 0,
  `y` float UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table coordinates for phpMyAdmin PDF output';

-- --------------------------------------------------------

--
-- 表的结构 `pma__table_info`
--

CREATE TABLE `pma__table_info` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT '',
  `display_field` varchar(64) COLLATE utf8_bin NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table information for phpMyAdmin';

-- --------------------------------------------------------

--
-- 表的结构 `pma__table_uiprefs`
--

CREATE TABLE `pma__table_uiprefs` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `prefs` text COLLATE utf8_bin NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Tables'' UI preferences';

-- --------------------------------------------------------

--
-- 表的结构 `pma__tracking`
--

CREATE TABLE `pma__tracking` (
  `db_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `table_name` varchar(64) COLLATE utf8_bin NOT NULL,
  `version` int(10) UNSIGNED NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  `schema_snapshot` text COLLATE utf8_bin NOT NULL,
  `schema_sql` text COLLATE utf8_bin DEFAULT NULL,
  `data_sql` longtext COLLATE utf8_bin DEFAULT NULL,
  `tracking` set('UPDATE','REPLACE','INSERT','DELETE','TRUNCATE','CREATE DATABASE','ALTER DATABASE','DROP DATABASE','CREATE TABLE','ALTER TABLE','RENAME TABLE','DROP TABLE','CREATE INDEX','DROP INDEX','CREATE VIEW','ALTER VIEW','DROP VIEW') COLLATE utf8_bin DEFAULT NULL,
  `tracking_active` int(1) UNSIGNED NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Database changes tracking for phpMyAdmin';

-- --------------------------------------------------------

--
-- 表的结构 `pma__userconfig`
--

CREATE TABLE `pma__userconfig` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `config_data` text COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User preferences storage for phpMyAdmin';

-- --------------------------------------------------------

--
-- 表的结构 `pma__usergroups`
--

CREATE TABLE `pma__usergroups` (
  `usergroup` varchar(64) COLLATE utf8_bin NOT NULL,
  `tab` varchar(64) COLLATE utf8_bin NOT NULL,
  `allowed` enum('Y','N') COLLATE utf8_bin NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User groups with configured menu items';

-- --------------------------------------------------------

--
-- 表的结构 `pma__users`
--

CREATE TABLE `pma__users` (
  `username` varchar(64) COLLATE utf8_bin NOT NULL,
  `usergroup` varchar(64) COLLATE utf8_bin NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Users and their assignments to user groups';

-- --------------------------------------------------------

--
-- 表的结构 `station`
--

CREATE TABLE `station` (
  `idx` int(11) NOT NULL,
  `sid` varchar(3) NOT NULL,
  `sName` varchar(15) NOT NULL,
  `route` enum('O','R','C') NOT NULL,
  `route_order` int(3) NOT NULL,
  `english_name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `station`
--

INSERT INTO `station` (`idx`, `sid`, `sName`, `route`, `route_order`, `english_name`) VALUES
(1, 'O1', '西子灣', 'O', 0, 'Sizihwan'),
(2, 'O2', '鹽埕埔', 'O', 1, 'Yanchengpu'),
(3, 'O4', '市議會(舊址)', 'O', 2, 'City Council (Former Site)'),
(4, 'O5', '美麗島', 'O', 3, 'Formosa Boulevard'),
(5, 'OT1', '大寮(前庄)', 'O', 4, 'Daliao');

-- --------------------------------------------------------

--
-- 表的结构 `station_exit`
--

CREATE TABLE `station_exit` (
  `idx` int(11) NOT NULL,
  `sid` varchar(3) NOT NULL,
  `eNo` int(2) NOT NULL,
  `eName` varchar(20) NOT NULL,
  `eName_en` varchar(50) NOT NULL,
  `ePosition` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `station_exit`
--

INSERT INTO `station_exit` (`idx`, `sid`, `eNo`, `eName`, `eName_en`, `ePosition`) VALUES
(1, 'O1', 2, '香蕉碼頭', 'Banana Pier', 1),
(2, 'O1', 1, '西子灣', 'Sizihwan Bay', 4),
(3, 'O2', 2, '高雄國際會議中心', 'Inernational Convention Center', 1),
(4, 'O2', 3, '新樂街', 'Sinie St.', 2),
(5, 'O2', 4, '五福四路', 'Wufu 4th Road', 4.2),
(6, 'O2', 1, '高雄流行音樂中心', 'Kaohsiung Music Center', 4.1),
(7, 'O4', 4, '六合觀光夜市', 'Liouhe Night Market', 1.1),
(8, 'O4', 3, '中正四路', 'Jhongheng 4th Rd.', 1),
(9, 'O4', 2, '自強二路', 'Zihciang 2nd Rd.', 4.2),
(10, 'O4', 1, '愛河', 'Love River', 4.1),
(11, 'O5', 8, '土地銀行', 'Land Bank', 1.4),
(12, 'O5', 7, '興華路', 'Singhua Rd.', 1.3),
(13, 'O5', 6, '中正三路', 'Jhongheng 3th Rd.', 1.2),
(14, 'O5', 5, '高雄郵局', 'Kaohsiung Post Office', 1.1),
(15, 'O5', 11, '中山一路(婚紗區)', 'Jhongshan 1st Rd.', 4.7),
(16, 'O5', 10, '中山一路(北)', 'Jhongshan 1st Rd.(North)', 4.6),
(17, 'O5', 9, '台灣人壽', 'Taiwan Life Insurance', 4.5),
(18, 'O5', 4, '中正三路', 'Jhongheng 3th Rd.', 4.4),
(19, 'O5', 3, '南華觀光夜市', 'Nanhua Night Market', 4.3),
(20, 'O5', 2, '第一銀行', 'First Bank', 4.2),
(21, 'O5', 1, '華南銀行', 'Hua Nan Bank', 4.1);

--
-- 转储表的索引
--

--
-- 表的索引 `access_signal`
--
ALTER TABLE `access_signal`
  ADD PRIMARY KEY (`idx`);

--
-- 表的索引 `carriage_info`
--
ALTER TABLE `carriage_info`
  ADD PRIMARY KEY (`idx`);

--
-- 表的索引 `facility_location`
--
ALTER TABLE `facility_location`
  ADD PRIMARY KEY (`idx`);

--
-- 表的索引 `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `pma__central_columns`
--
ALTER TABLE `pma__central_columns`
  ADD PRIMARY KEY (`db_name`,`col_name`);

--
-- 表的索引 `pma__column_info`
--
ALTER TABLE `pma__column_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `db_name` (`db_name`,`table_name`,`column_name`);

--
-- 表的索引 `pma__designer_settings`
--
ALTER TABLE `pma__designer_settings`
  ADD PRIMARY KEY (`username`);

--
-- 表的索引 `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_user_type_template` (`username`,`export_type`,`template_name`);

--
-- 表的索引 `pma__favorite`
--
ALTER TABLE `pma__favorite`
  ADD PRIMARY KEY (`username`);

--
-- 表的索引 `pma__history`
--
ALTER TABLE `pma__history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`,`db`,`table`,`timevalue`);

--
-- 表的索引 `pma__navigationhiding`
--
ALTER TABLE `pma__navigationhiding`
  ADD PRIMARY KEY (`username`,`item_name`,`item_type`,`db_name`,`table_name`);

--
-- 表的索引 `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  ADD PRIMARY KEY (`page_nr`),
  ADD KEY `db_name` (`db_name`);

--
-- 表的索引 `pma__recent`
--
ALTER TABLE `pma__recent`
  ADD PRIMARY KEY (`username`);

--
-- 表的索引 `pma__relation`
--
ALTER TABLE `pma__relation`
  ADD PRIMARY KEY (`master_db`,`master_table`,`master_field`),
  ADD KEY `foreign_field` (`foreign_db`,`foreign_table`);

--
-- 表的索引 `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_savedsearches_username_dbname` (`username`,`db_name`,`search_name`);

--
-- 表的索引 `pma__table_coords`
--
ALTER TABLE `pma__table_coords`
  ADD PRIMARY KEY (`db_name`,`table_name`,`pdf_page_number`);

--
-- 表的索引 `pma__table_info`
--
ALTER TABLE `pma__table_info`
  ADD PRIMARY KEY (`db_name`,`table_name`);

--
-- 表的索引 `pma__table_uiprefs`
--
ALTER TABLE `pma__table_uiprefs`
  ADD PRIMARY KEY (`username`,`db_name`,`table_name`);

--
-- 表的索引 `pma__tracking`
--
ALTER TABLE `pma__tracking`
  ADD PRIMARY KEY (`db_name`,`table_name`,`version`);

--
-- 表的索引 `pma__userconfig`
--
ALTER TABLE `pma__userconfig`
  ADD PRIMARY KEY (`username`);

--
-- 表的索引 `pma__usergroups`
--
ALTER TABLE `pma__usergroups`
  ADD PRIMARY KEY (`usergroup`,`tab`,`allowed`);

--
-- 表的索引 `pma__users`
--
ALTER TABLE `pma__users`
  ADD PRIMARY KEY (`username`,`usergroup`);

--
-- 表的索引 `station`
--
ALTER TABLE `station`
  ADD PRIMARY KEY (`idx`);

--
-- 表的索引 `station_exit`
--
ALTER TABLE `station_exit`
  ADD PRIMARY KEY (`idx`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `access_signal`
--
ALTER TABLE `access_signal`
  MODIFY `idx` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=154;

--
-- 使用表AUTO_INCREMENT `carriage_info`
--
ALTER TABLE `carriage_info`
  MODIFY `idx` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- 使用表AUTO_INCREMENT `facility_location`
--
ALTER TABLE `facility_location`
  MODIFY `idx` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- 使用表AUTO_INCREMENT `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `pma__column_info`
--
ALTER TABLE `pma__column_info`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `pma__history`
--
ALTER TABLE `pma__history`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  MODIFY `page_nr` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `station`
--
ALTER TABLE `station`
  MODIFY `idx` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- 使用表AUTO_INCREMENT `station_exit`
--
ALTER TABLE `station_exit`
  MODIFY `idx` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
