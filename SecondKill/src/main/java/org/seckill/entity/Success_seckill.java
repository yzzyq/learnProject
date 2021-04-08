package org.seckill.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Success_seckill {
    private long seckill_id;
    private long seckill_phone;
    private int seckill_state;
    private Date seckill_createTime;

    // 秒杀明细记录表中包含了多种秒杀商品，这里就存在多对一的关系
    private Seckill seckill;

}
