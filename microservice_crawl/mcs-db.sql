-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2021-12-15 07:10:43
-- 伺服器版本： 10.4.21-MariaDB
-- PHP 版本： 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫: `mcs-db`
--

-- --------------------------------------------------------

--
-- 資料表結構 `booking`
--

CREATE TABLE `booking` (
  `id` int(10) NOT NULL,
  `user_id` varchar(50) NOT NULL,
  `user_name` varchar(50) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `movie_name` varchar(50) NOT NULL,
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 資料表結構 `movies_rank`
--

CREATE TABLE `movies_rank` (
  `id` int(10) NOT NULL,
  `movies_name` varchar(50) NOT NULL,
  `rank` int(10) NOT NULL,
  `title` varchar(50) NOT NULL,
  `rate` double NOT NULL,
  `web_link` varchar(1000) NOT NULL,
  `poster_link` varchar(1000) NOT NULL,
  `date` date NOT NULL,
  `length` varchar(50) NOT NULL,
  `company` varchar(50) NOT NULL,
  `director` varchar(50) NOT NULL,
  `introduction` varchar(1000) NOT NULL,
  `timetable_link` varchar(1000) NOT NULL,
  `screenshot_link` varchar(1000) NOT NULL,
  `screenshot_file_link` varchar(1000) NOT NULL,
  PRIMARY KEY ('id')
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`id`);

--
-- 資料表索引 `movies_rank`
--
ALTER TABLE `movies_rank`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
