package com.zyq.demo.DTO;

import com.zyq.demo.SeckillEnum.SeckillSateEnum;
import com.zyq.demo.entity.Success_seckill;
import lombok.Data;


// 秒杀状态类
@Data
public class SeckillExecution {

    // 秒杀商品id
    private long seckill_id;

    // 秒杀执行结果状态
    private int state;

    private Success_seckill success_seckill;

    // 状态表示
    private String statInfo;


    public SeckillExecution(long seckill_id, SeckillSateEnum state){
        this.seckill_id = seckill_id;
        this.state = state.getState();
        this.statInfo = state.getStateInfo();
    }

    public SeckillExecution(long seckill_id, SeckillSateEnum state,Success_seckill success_seckill){
        this.seckill_id = seckill_id;
        this.state = state.getState();
        this.statInfo = state.getStateInfo();
        this.success_seckill = success_seckill;
    }




}
