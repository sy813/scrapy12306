# 初始化数据库
CREATE DATABASE IF NOT EXISTS `12306`;

GRANT USAGE ON *.* TO '12306'@'localhost';
DROP USER '12306'@'localhost';

CREATE USER '12306'@'localhost'
  IDENTIFIED BY '12306';
GRANT ALL PRIVILEGES ON `12306`.* TO '12306'@'localhost';

# 创建抓取轮次表
CREATE TABLE `turns` (
  `id`        INTEGER PRIMARY KEY,
  `mark_time` TIMESTAMP NOT NULL
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# 创建代售点数据表
CREATE TABLE IF NOT EXISTS `agencies` (
  `province` VARCHAR(10) NOT NULL,
  `city`     VARCHAR(15) NOT NULL,
  `county`   VARCHAR(15) NOT NULL,
  `address`  VARCHAR(50) NOT NULL,
  `name`     VARCHAR(50) NOT NULL,
  `windows`  INT,
  `start`    TIME,
  `end`      TIME,
  `turn`     INTEGER     NOT NULL,
  PRIMARY KEY (`address`, `turn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# 创建站点数据表
CREATE TABLE IF NOT EXISTS `stations` (
  `bureau`    VARCHAR(10) NOT NULL,
  `station`   BOOLEAN     NOT NULL,
  `name`      VARCHAR(15) NOT NULL,
  `address`   VARCHAR(50) NOT NULL,
  `passenger` BOOLEAN     NOT NULL,
  `luggage`   BOOLEAN     NOT NULL,
  `package`   BOOLEAN     NOT NULL,
  `turn`      INTEGER     NOT NULL,
  PRIMARY KEY (`bureau`, `station`, `name`, `turn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# 创建车次表
CREATE TABLE IF NOT EXISTS `train_briefs` (
  `code`      VARCHAR(10) NOT NULL,
  `train_no`  VARCHAR(20) NOT NULL,
  `start`     VARCHAR(10) NOT NULL,
  `end`       VARCHAR(10) NOT NULL,
  `seat_type` VARCHAR(20) DEFAULT NULL,
  `turn`      INTEGER     NOT NULL,
  PRIMARY KEY (`code`, `turn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# 创建车次信息表
CREATE TABLE IF NOT EXISTS `train_infos` (
  `train_no`      VARCHAR(20) NOT NULL,
  `no`            TINYINT     NOT NULL,
  `station`       VARCHAR(15) NOT NULL,
  `type`          TINYINT     NOT NULL,
  `start_time`    TIME,
  `arrive_time`   TIME,
  `stopover_time` VARCHAR(10),
  `turn`          INTEGER     NOT NULL,
  PRIMARY KEY (`train_no`, `no`, `turn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# 创建站点代码表
CREATE TABLE IF NOT EXISTS `stations_code` (
  `name` VARCHAR(20) NOT NULL,
  `code` VARCHAR(6)  NOT NULL,
  `turn` INTEGER     NOT NULL,
  PRIMARY KEY (`name`, `turn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;

# 创建余票信息表
CREATE TABLE IF NOT EXISTS `train_tickets` (
  `train_no` VARCHAR(20) NOT NULL,
  `start`    VARCHAR(15) NOT NULL,
  `end`      VARCHAR(15) NOT NULL,
  `swz`      VARCHAR(10) NOT NULL,
  `tz`       VARCHAR(10) NOT NULL,
  `zy`       VARCHAR(10) NOT NULL,
  `ze`       VARCHAR(10) NOT NULL,
  `gr`       VARCHAR(10) NOT NULL,
  `rw`       VARCHAR(10) NOT NULL,
  `yw`       VARCHAR(10) NOT NULL,
  `rz`       VARCHAR(10) NOT NULL,
  `yz`       VARCHAR(10) NOT NULL,
  `wz`       VARCHAR(10) NOT NULL,
  `qt`       VARCHAR(10) NOT NULL,
  `turn`     INTEGER     NOT NULL,
  PRIMARY KEY (`train_no`, `start`, `end`, `turn`)
)
  ENGINE = InnoDB
  DEFAULT CHARSET = utf8;
