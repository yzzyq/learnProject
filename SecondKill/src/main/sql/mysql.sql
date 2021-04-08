
DELIMITER $$

CREATE PROCEDURE `seckill`.`success_seckill`
      (in seckill_id bigint,in seckill_phone bigint,
         in seckill_time timestamp , out seckill_result int)
      BEGIN
         DECLARE insert_count int DEFAULT 0;
         START TRANSACTION;
         insert ignore into
          Success_seckill(seckill_id,seckill_phone,seckill_createTime)
        values
          (seckill_id,seckill_phone,seckill_time);
        select row_count() into insert_count;
        IF (insert_count = 0) THEN
          ROLLBACK;
          SET seckill_result = -1;
        ELSEIF(insert_count < 0) THEN
          ROLLBACK;
          SET seckill_result = -2;
        ELSE
          update seckill
          set seckill_num = seckill_num - 1
          where seckill_id = seckill_id
               and seckill_startTime < seckill_time
               and seckill_endTime > seckill_time
               and seckill_num > 0;
          select row_count() into insert_count;
          IF (insert_count = 0) THEN
            ROLLBACK;
            set seckill_result = 0;
          ELSEIF(insert_count < 0) THEN
            ROLLBACK;
            set seckill_result = -2;
          ELSE
            COMMIT;
            SET seckill_result = 1;
          END IF;
        END IF;
      END$$
DELIMITER $$
DELIMITER ;

set @r_result = -3;

call success_seckill(10003,18952771679,now(),@r_result)

select @r_result;






