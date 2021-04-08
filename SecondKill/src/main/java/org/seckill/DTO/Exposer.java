package org.seckill.DTO;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.Date;

// 秒杀开启类
@Data
@AllArgsConstructor
public class Exposer {

    // 是否开启秒杀
    private boolean exposed;
    // 链接加密策略
    private String md5;
    // 秒杀商品id
    private long seckill_id;
    // 系统当前时间
    private long now;
    // 秒杀开启时间
    private long start;
    // 秒杀结束时间
    private long end;

    public Exposer(boolean exposed, long seckill_id){
        this.exposed = exposed;
        this.seckill_id = seckill_id;
    }

    public Exposer(boolean exposed, long seckill_id, long now, long startTime, long endTime) {
        this.exposed = exposed;
        this.seckill_id = seckill_id;
        this.now = now;
        this.start = startTime;
        this.end = endTime;
    }

    public Exposer(boolean exposed, String md5, long seckill_id) {
        this.exposed = exposed;
        this.md5 = md5;
        this.seckill_id = seckill_id;
    }
}
