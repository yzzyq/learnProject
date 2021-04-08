package com.zyq.demo.dao.cache;


import com.dyuproject.protostuff.LinkedBuffer;
import com.dyuproject.protostuff.ProtostuffIOUtil;
import com.dyuproject.protostuff.runtime.RuntimeSchema;
import com.zyq.demo.entity.Seckill;
import org.redisson.RedissonLock;
import org.redisson.api.RLock;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import redis.clients.jedis.Jedis;
import redis.clients.jedis.JedisPool;

// redis缓存数据库中存放
@Component
public class RedisDao {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private JedisPool jedisPool;

    private RuntimeSchema<Seckill> schema = RuntimeSchema.createFrom(Seckill.class);


    public Seckill getSeckill(long seckill_id){
        try{
            Jedis jedis = jedisPool.getResource();

            try{
                String key = "seckill_id" + seckill_id;
                byte[] bytes = jedis.get(key.getBytes());

                if(bytes != null){
                    Seckill seckill = new Seckill();
                    ProtostuffIOUtil.mergeFrom(bytes,seckill,schema);
                    return seckill;
                }
            }finally {
                jedis.close();
            }
        }catch (Exception e){
            logger.error(e.getMessage(),e);
        }
        return null;
    }

    public String putSeckill(Seckill seckill){
        try{
            Jedis jedis = jedisPool.getResource();

            try{
                String key = "seckill_id" + seckill.getSeckill_id();
                byte[] bytes = ProtostuffIOUtil.toByteArray(seckill,schema,
                        LinkedBuffer.allocate(LinkedBuffer.DEFAULT_BUFFER_SIZE));

                int timeout = 60*60;

                String result = jedis.setex(key.getBytes(),timeout,bytes);
                return result;
            }finally {
                jedis.close();
            }

        }catch (Exception e){
            logger.error(e.getMessage(),e);
        }
        return null;
    }

    public Integer updateSeckill(long seckill_id){
        try{
            Jedis jedis = jedisPool.getResource();
            String key = "seckill_id" + seckill_id;

            Seckill seckill = getSeckill(seckill_id);

            try{
                seckill.setSeckill_num(seckill.getSeckill_num() - 1);
                putSeckill(seckill);
                return seckill.getSeckill_num();
            }finally {
                jedis.close();
            }

        }catch (Exception e){
            logger.error(e.getMessage(),e);
        }
        return null;

    }

}
