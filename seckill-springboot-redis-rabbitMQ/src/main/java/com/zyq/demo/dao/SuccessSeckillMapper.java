package com.zyq.demo.dao;

import com.zyq.demo.entity.Success_seckill;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Mapper
@Repository
public interface SuccessSeckillMapper {

    // 插入一条秒杀记录
    int insertSuccessSeckill(@Param("seckill_id") long seckill_id,@Param("seckill_phone") long seckill_phone);

    // 根据id查询一条记录
    Success_seckill querySuccessSeckillById(@Param("seckill_id") long seckill_id, @Param("seckill_phone") long seckill_phone);

    List<Success_seckill> getAllSuccessSeckill();


}
