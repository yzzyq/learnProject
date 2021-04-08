package org.seckill.dao;

import org.apache.ibatis.annotations.Param;
import org.seckill.entity.Seckill;

import java.util.Date;
import java.util.List;
import java.util.Map;

public interface SeckillMapper {

    // 查询全部的秒杀库存表
    List<Seckill> queryAllSeckill(@Param("offset") int offset,@Param("limit") int limit);

    // 根据id查询秒杀商品
    Seckill querySeckillById(long seckill_id);

    // 减库存操作
    int deleteSeckill(@Param("seckill_id") long seckill_id,@Param("killTime") Date killTime);

    void seckillByProcedure(Map<String, Object> paramMap);

}
