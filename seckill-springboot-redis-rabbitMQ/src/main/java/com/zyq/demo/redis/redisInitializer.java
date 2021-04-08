package com.zyq.demo.redis;

import com.zyq.demo.SeckillEnum.SeckillSateEnum;
import com.zyq.demo.dao.SeckillMapper;
import com.zyq.demo.dao.cache.RedisDao;
import com.zyq.demo.entity.Seckill;
import com.zyq.demo.exception.redisNullException;
import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class redisInitializer implements InitializingBean {

    @Autowired
    private SeckillMapper seckillMapper;

    @Autowired
    private RedisDao redisDao;

    @Autowired
    private CacheBool cacheBool;

    @Override
    public void afterPropertiesSet() {
        List<Seckill> all_seckill = seckillMapper.queryAllSeckill();
        if(all_seckill.size() == 0){
            throw new redisNullException(SeckillSateEnum.DATA_NULL.getStateInfo());
        }


        for (Seckill one:all_seckill){
            redisDao.putSeckill(one);
            cacheBool.put(one.getSeckill_id(),true);
        }

    }
}
