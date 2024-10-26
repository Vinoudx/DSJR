

SET FOREIGN_KEY_CHECKS=0;
DROP Database IF EXISTS 'erp';
CREATE Database erp;

-- ----------------------------
-- Table structure for bom
-- ----------------------------
DROP TABLE IF EXISTS `bom`;
CREATE TABLE `bom` (
  `零件号` varchar(50) NOT NULL,
  `描述` varchar(50) NOT NULL,
  `装配数量` int(50) NOT NULL,
  `单位` varchar(50) NOT NULL,
  `层次` varchar(50) NOT NULL
)CHARSET=utf8mb4;

INSERT INTO `bom` VALUES ('20100', '镜框', '1', 'ge', '1');
INSERT INTO `bom` VALUES ('20110', '镜架', '1', 'ge', '2');
INSERT INTO `bom` VALUES ('20120', '镜腿', '2', 'ge', '2');
INSERT INTO `bom` VALUES ('20130', '鼻托', '2', 'ge', '2');
INSERT INTO `bom` VALUES ('20109', '螺钉', '4', 'ge', '2');
INSERT INTO `bom` VALUES ('20300', '镜片', '2', 'ge', '1');
INSERT INTO `bom` VALUES ('20109', '螺钉', '2', 'ge', '1');

DROP TABLE IF EXISTS `库存表`;
CREATE TABLE `库存表` (
  `物料号` varchar(50) NOT NULL,
  `物料名称` varchar(50) NOT NULL,
  `工序库存` int(50) NOT NULL,
  `资材库存` int(50) NOT NULL
)CHARSET=utf8mb4;

INSERT INTO `库存表` VALUES ('20000', '眼镜', '0', '0');
INSERT INTO `库存表` VALUES ('20109', '螺钉', '10', '50');
INSERT INTO `库存表` VALUES ('20100', '镜框', '0', '0');
INSERT INTO `库存表` VALUES ('20110', '镜架', '0', '0');
INSERT INTO `库存表` VALUES ('20120', '镜腿', '10', '20');
INSERT INTO `库存表` VALUES ('20130', '鼻托', '0', '0');
INSERT INTO `库存表` VALUES ('20300', '镜片', '0', '0');

DROP TABLE IF EXISTS `物料表`;
CREATE TABLE `物料表` (
  `物料名` varchar(50) NOT NULL,
  `名称` varchar(50) NOT NULL,
  `单位` varchar(50) NOT NULL,
  `调配方式` varchar(50) NOT NULL,
  `损耗率` float(50,2) NOT NULL,
  `作业提前期` float(50,0) NOT NULL
)CHARSET=utf8mb4;

INSERT INTO `物料表` VALUES ('20000', '眼镜', 'fu', 'produce', '0.00', '1');
INSERT INTO `物料表` VALUES ('20109', '螺钉', 'ge', 'buy', '0.10', '0');
INSERT INTO `物料表` VALUES ('20100', '镜框', 'fu', 'produce', '0.00', '2');
INSERT INTO `物料表` VALUES ('20110', '镜架', 'ge', 'buy', '0.00', '0');
INSERT INTO `物料表` VALUES ('20120', '镜腿', 'ge', 'buy', '0.00', '0');
INSERT INTO `物料表` VALUES ('20130', '鼻托', 'gr', 'buy', '0.00', '0');
INSERT INTO `物料表` VALUES ('20300', '镜片', 'pian', 'buy', '0.00', '0');


DROP TABLE IF EXISTS `调配构成表`;
CREATE TABLE `调配构成表` (
  `调配基准编号` varchar(50) NOT NULL,
  `调配区代码` varchar(50) NOT NULL,
  `父物料号` varchar(50) NOT NULL,
  `父物料名称` varchar(50) NOT NULL,
  `子物料号` varchar(50) NOT NULL,
  `子物料名称` varchar(50) NOT NULL,
  `构成数` int(50) NOT NULL,
  `配料提前期` int(50) NOT NULL,
  `供应商提前期` int(50) NOT NULL
)CHARSET=utf8mb4;

INSERT INTO `调配构成表` VALUES ('000001', 'L001', '20000', '眼镜', '20100', '镜框', '1', '0', '0');
INSERT INTO `调配构成表` VALUES ('000001', 'L001', '20000', '眼镜', '20300', '镜片', '2', '1', '20');
INSERT INTO `调配构成表` VALUES ('000001', 'L001', '20000', '眼镜', '20109', '螺钉', '2', '1', '10');
INSERT INTO `调配构成表` VALUES ('000001', 'L003', '20100', '镜框', '20110', '镜架', '1', '1', '20');
INSERT INTO `调配构成表` VALUES ('000001', 'L003', '20100', '镜框', '20120', '镜腿', '2', '1', '10');
INSERT INTO `调配构成表` VALUES ('000001', 'L003', '20100', '镜框', '20130', '鼻托', '2', '1', '18');
INSERT INTO `调配构成表` VALUES ('000001', 'L003', '20100', '镜框', '20109', '螺钉', '4', '1', '10');
