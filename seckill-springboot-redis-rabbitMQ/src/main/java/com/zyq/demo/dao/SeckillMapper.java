package com.zyq.demo.dao;

import com.zyq.demo.entity.Seckill;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.Date;
import java.util.List;
import java.util.Map;

@Mapper
@Repository
public interface SeckillMapper {

    // 查询全部的秒杀库存表
    List<Seckill> queryAllSeckill();

    List<Seckill> queryAllSeckillByLimit(@Param("offset") int offset, @Param("limit") int limit);

    // 根据id查询秒杀商品
    Seckill querySeckillById(long seckill_id);

    // 减库存操作
    int deleteSeckill(@Param("seckill_id") long seckill_id,@Param("killTime") Date killTime);

    void seckillByProcedure(Map<String, Object> paramMap);



}
