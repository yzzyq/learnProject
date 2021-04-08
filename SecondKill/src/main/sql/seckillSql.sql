
CREATE DATABASE `seckill`;

USE `seckill`;

/*
 秒杀库存表
*/
CREATE TABLE IF NOT EXISTS `seckill`(
   `seckill_id` bigint NOT NULL AUTO_INCREMENT COMMENT '秒杀商品编号',
   `seckill_name` varchar(120) NOT NULL COMMENT '秒杀商品名',
   `seckill_num` int NOT NULL COMMENT '库存',
   `seckill_startTime` timestamp NOT NULL COMMENT '秒杀开始时间',
   `seckill_endTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '秒杀结束时间',
   `seckill_createTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '秒杀创建时间',
   primary key (`seckill_id`),
   key idx_start_time(`seckill_startTime`),
   key idx_end_time(`seckill_endTime`),
   key idx_create_time(`seckill_createTime`)
)ENGINE=INNODB AUTO_INCREMENT=10000 DEFAULT CHARSET=utf8 COMMENT='秒杀库存表';

insert into
   seckill(`seckill_name`,`seckill_num`,`seckill_startTime`,`seckill_endTime`)
values
   ('小米6秒杀',200,'2021-4-1 10:00:00','2021-4-1 11:00:00'),
   ('红米40秒杀',100,'2021-4-2 10:00:00','2021-4-2 11:00:00'),
   ('iphone12秒杀',300,'2021-4-3 10:00:00','2021-4-3 11:00:00');


/*
秒杀明细记录表
 */
CREATE TABLE IF NOT EXISTS success_secill(
   `seckill_id` bigint NOT NULL AUTO_INCREMENT COMMENT '秒杀商品编号',
   `seckill_phone` bigint NOT NULL COMMENT '秒杀手机号',
   `seckill_state` int NOT NULL DEFAULT -1 COMMENT '秒杀状态-1无效，0成功，1付款',
   `seckill_createTime` timestamp NOT NULL COMMENT '秒杀创建时间',
   primary key(`seckill_id`,`seckill_phone`),
   key id_create_time(`seckill_createTime`)
)ENGINE=INNODB DEFAULT CHARSET=utf8 COMMENT='秒杀明细记录表';

mysql -uroot -p

