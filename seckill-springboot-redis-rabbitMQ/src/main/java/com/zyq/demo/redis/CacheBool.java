package com.zyq.demo.redis;

import com.zyq.demo.SeckillEnum.SeckillSateEnum;
import com.zyq.demo.exception.redisNullException;
import org.springframework.stereotype.Component;

import java.util.HashMap;
import java.util.Map;

@Component
public class CacheBool {

    Map<Long, Boolean> cache_data = new HashMap<>();

    // 插入，如果存在的话，那么就变成更新
    public int put(long seckill_id, boolean is_exists){
        if(cache_data.containsKey(seckill_id)){
            cache_data.put(seckill_id, is_exists);
            return is_exists == cache_data.get(seckill_id)?1:0;
        }else{
            int old_num = cache_data.size();
            cache_data.put(seckill_id,is_exists);
            return cache_data.size() - old_num;
        }
    }


    public boolean get(long seckill_id){
        if(!cache_data.containsKey(seckill_id)){
            throw new redisNullException(SeckillSateEnum.DATA_NULL.getStateInfo());
        }

        return cache_data.get(seckill_id);
    }


}
