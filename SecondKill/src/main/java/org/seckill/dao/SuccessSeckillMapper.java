package org.seckill.dao;

import org.apache.ibatis.annotations.Param;
import org.seckill.entity.Success_seckill;

public interface SuccessSeckillMapper {

    // 插入一条秒杀记录
    int insertSuccessSeckill(@Param("seckill_id") long seckill_id,@Param("seckill_phone") long seckill_phone);

    // 根据id查询一条记录
    Success_seckill querySuccessSeckillById(@Param("seckill_id") long seckill_id,@Param("seckill_phone") long seckill_phone);

}
