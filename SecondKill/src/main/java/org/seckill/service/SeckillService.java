package org.seckill.service;

import org.seckill.DTO.Exposer;
import org.seckill.DTO.SeckillExecution;
import org.seckill.entity.Seckill;

import java.util.List;

public interface SeckillService {

    // 查询所有的秒杀记录
    List<Seckill> getSeckillService();

    // 查询单个秒杀记录
    Seckill getSeckillByIdService(long seckill_id);

    // 输出秒杀接口
    Exposer exportSeckillUrlService(long seckill_id);

    // 执行秒杀
    SeckillExecution executeSeckillService(long seckill_id, long seckill_phone, String md5);

    // 使用存储过程执行秒杀
    SeckillExecution executeSeckillServiceProcedure(long seckill_id, long seckill_phone, String md5);

}
