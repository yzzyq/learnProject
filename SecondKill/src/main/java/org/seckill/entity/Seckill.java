package org.seckill.entity;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.Date;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class Seckill {
    private long seckill_id;
    private String seckill_name;
    private int seckill_num;
    private Date seckill_startTime;
    private Date seckill_endTime;
    private Date seckill_createTime;
}
