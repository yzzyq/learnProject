package com.zyq.demo.service;



import com.zyq.demo.DTO.Exposer;
import com.zyq.demo.DTO.SeckillExecution;
import com.zyq.demo.MQ.MQMessage;
import com.zyq.demo.entity.Seckill;
import com.zyq.demo.entity.Success_seckill;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public interface SeckillService {

    // 查询所有的秒杀记录
    List<Seckill> getSeckillService();

    // 查询秒杀记录
    Success_seckill getSuSeckillService(long seckill_id, long seckill_phone);

    // 查询单个秒杀记录
    Seckill getSeckillByIdService(long seckill_id);

    // 输出秒杀接口
    Exposer exportSeckillUrlService(long seckill_id);

    // 执行秒杀
    SeckillExecution executeSeckillService(long seckill_id, long seckill_phone, String md5);

    // 执行秒杀
    SeckillExecution seckillService(MQMessage message);


}
