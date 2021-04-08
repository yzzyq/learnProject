package org.seckill.DTO;

import lombok.AllArgsConstructor;
import lombok.Data;
import org.seckill.SeckillEnum.SeckillSateEnum;
import org.seckill.entity.Success_seckill;

// 秒杀成功类
@Data
public class SeckillExecution {

    // 秒杀商品id
    private long seckill_id;

    // 秒杀执行结果状态
    private int state;

    // 状态表示
    private String statInfo;

    // 秒杀成功
    private Success_seckill success_seckill;

    public SeckillExecution(long seckill_id, SeckillSateEnum state, Success_seckill success_seckill){
        this.seckill_id = seckill_id;
        this.state = state.getState();
        this.statInfo = state.getStateInfo();
        this.success_seckill = success_seckill;
    }

    public SeckillExecution(long seckill_id, SeckillSateEnum state){
        this.seckill_id = seckill_id;
        this.state = state.getState();
        this.statInfo = state.getStateInfo();
        this.success_seckill = success_seckill;
    }




}
