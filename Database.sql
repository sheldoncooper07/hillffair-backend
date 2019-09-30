SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";
CREATE DATABASE IF NOT EXISTS `hillffair` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `hillffair`;

CREATE TABLE `clubs` (
  `id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `logo` varchar(100) NOT NULL,
  `info` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `coreteam` (
  `id` int(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `profile_pic` varchar(100) NOT NULL,
  `position` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `likes` (
  `id` int(11) NOT NULL,
  `post` int(11) NOT NULL,
  `firebase_id` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `profile` (
  `firebase_id` varchar(100) NOT NULL,
  `rollno` varchar(20) DEFAULT NULL,
  `branch` varchar(8) DEFAULT NULL,
  `mobile` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `points` int(11) NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `url` varchar(255) NOT NULL,
  `rating` int(10) NOT NULL DEFAULT 1500,
  `quiz_rating` int(10) NOT NULL DEFAULT 1000,
  `referral_friend` varchar(100) NOT NULL,
  `face_smash_status` boolean DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `quiz` (
  `id` int(10) NOT NULL,
  `ques` varchar(1000) NOT NULL,
  `ans` int(2) NOT NULL,
  `option1` varchar(100) NOT NULL,
  `option2` varchar(100) NOT NULL,
  `option3` varchar(100) NOT NULL,
  `option4` varchar(100) NOT NULL,
  `category` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `schedule` (
  `event_id` int(10) NOT NULL AUTO_INCREMENT,
  `club_id` int(10) DEFAULT NULL,
  `club_name` varchar(100) DEFAULT NULL,
  `event_name` varchar(100) DEFAULT NULL,
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  'venue' varchar(200) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `sponsors` (
  `id` int(10) NOT NULL,
  `sponsor_name` varchar(100) NOT NULL,
  `sponsor_logo` varchar(100) NOT NULL,
  `sponsor_info` varchar(1000) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `wall` (
  `id` int(11) NOT NULL,
  `firebase_id` varchar(100) NOT NULL,
  `likes` int(100) DEFAULT NULL,
  `url` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


ALTER TABLE `clubs`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `coreteam`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `likes`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `profile`
  ADD PRIMARY KEY (`firebase_id`);

ALTER TABLE `quiz`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `schedule`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `sponsors`
  ADD PRIMARY KEY (`id`);

ALTER TABLE `wall`
  ADD PRIMARY KEY (`id`);


ALTER TABLE `clubs`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;
ALTER TABLE `coreteam`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;
ALTER TABLE `likes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `quiz`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;
ALTER TABLE `schedule`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;
ALTER TABLE `sponsors`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;
ALTER TABLE `wall`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;