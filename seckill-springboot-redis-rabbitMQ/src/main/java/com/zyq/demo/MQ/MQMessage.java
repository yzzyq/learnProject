package com.zyq.demo.MQ;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class MQMessage {

    private long seckill_id;

    private long seckill_phone;

    private Date seckill_createTime;

}
