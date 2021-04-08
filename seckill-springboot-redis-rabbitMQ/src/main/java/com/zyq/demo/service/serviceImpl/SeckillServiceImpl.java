package com.zyq.demo.service.serviceImpl;

import com.zyq.demo.DTO.Exposer;
import com.zyq.demo.DTO.SeckillExecution;
import com.zyq.demo.MQ.MQMessage;
import com.zyq.demo.MQ.RabbitProvider;
import com.zyq.demo.SeckillEnum.SeckillSateEnum;
import com.zyq.demo.dao.SeckillMapper;
import com.zyq.demo.dao.SuccessSeckillMapper;
import com.zyq.demo.dao.cache.RedisDao;
import com.zyq.demo.entity.Seckill;
import com.zyq.demo.entity.Success_seckill;
import com.zyq.demo.exception.repeatedSeckillException;
import com.zyq.demo.exception.seckillEndException;
import com.zyq.demo.exception.seckillException;
import com.zyq.demo.redis.CacheBool;
import com.zyq.demo.service.SeckillService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.util.DigestUtils;

import java.util.Date;
import java.util.List;

@Service
public class SeckillServiceImpl implements SeckillService {

    private Logger logger = LoggerFactory.getLogger(this.getClass());

    private final String slat = new Date().getTime() + "44878ahdjkashdnmzcndhsad435436)(*&%$#";

    @Autowired
    private SeckillMapper seckillMapper;

    @Autowired
    private SuccessSeckillMapper successSeckillMapper;

    @Autowired
    private RedisDao redisDao;

    @Autowired
    private CacheBool cacheBool;

    @Autowired
    private RabbitProvider rabbitProvider;

    public List<Seckill> getSeckillService() {
        return seckillMapper.queryAllSeckillByLimit(0,5);
    }

    @Override
    public Success_seckill getSuSeckillService(long seckill_id, long seckill_phone) {
        return successSeckillMapper.querySuccessSeckillById(seckill_id,seckill_phone);
    }

    public Seckill getSeckillByIdService(long seckill_id) {
        return seckillMapper.querySeckillById(seckill_id);
    }

    // 使用redis来优化并发操作
    public Exposer exportSeckillUrlService(long seckill_id) {
        // 1. 没有这个秒杀商品
//        Seckill seckill = seckillMapper.querySeckillById(seckill_id);
        // 使用redis来改进
        Seckill seckill = redisDao.getSeckill(seckill_id);

        if(seckill == null) {
//            return new Exposer(false, seckill_id);
            // 使用redis来改进
            seckill = seckillMapper.querySeckillById(seckill_id);
            if(seckill == null){
                return new Exposer(false,seckill_id);
            }else{
                redisDao.putSeckill(seckill);
            }
        }
        // 2. 秒杀还未开启
        Date startTime = seckill.getSeckill_startTime();
        Date endTime = seckill.getSeckill_endTime();
        Date now = new Date();
        if(now.getTime() < startTime.getTime() || now.getTime() > endTime.getTime()){
            return new Exposer(false,seckill_id,now.getTime(),startTime.getTime(),endTime.getTime());
        }
        // 3. 秒杀开启
        // 先使用加密md5转化为私密链接
        String md5 = getMD5(seckill_id);
        return new Exposer(true,md5,seckill_id);
    }

    private String getMD5(long seckill_id) {
        String base = seckill_id + "/" + slat;
        return DigestUtils.md5DigestAsHex(base.getBytes());
    }

    // 执行秒杀
    // 秒杀过程使用先插入，再更新操作，先插入的话，可以挡住一些主键冲突的
    // 使用存储过程来减少行级锁持有时间
//    @Transactional
    public SeckillExecution executeSeckillService(long seckill_id, long seckill_phone, String md5)
            throws seckillException, seckillEndException, repeatedSeckillException {
        // 1. 判断链接是否正确
        if(md5 == null || !md5.equals(getMD5(seckill_id))){
            throw new seckillException(SeckillSateEnum.DATA_REWRITE.getStateInfo());
        }

        try {
            Date now = new Date();

            // 判断内存中是否还能秒杀
            if(!cacheBool.get(seckill_id)){
                // 库存中已经没有数据，秒杀结束
                throw new seckillEndException(SeckillSateEnum.END.getStateInfo());
            }

            // 判断是否还有秒杀资格
            if(successSeckillMapper.querySuccessSeckillById(seckill_id,seckill_phone) != null){
                // 无法插入，那么就会发生重复插入的问题
                throw new repeatedSeckillException(SeckillSateEnum.REPEAT_KILL.getStateInfo());
            }

            // 从redis中减库存
            long seckill_num = redisDao.updateSeckill(seckill_id);
            if(seckill_num < 0){
                cacheBool.put(seckill_id,false);
                throw new seckillEndException(SeckillSateEnum.END.getStateInfo());
            }

            // 请求入队
            MQMessage message = new MQMessage(seckill_id,seckill_phone,new Date());
            rabbitProvider.sendInfo(message);

            return new SeckillExecution(seckill_id, SeckillSateEnum.WAIT);

        }catch (seckillEndException e1){
            throw e1;
        }catch (repeatedSeckillException e2){
            throw e2;
        }catch (Exception e){
            logger.error(e.getMessage(),e);
            throw new seckillException(SeckillSateEnum.INNER_ERROR.getStateInfo() + e.getMessage());
        }
    }

    // 执行秒杀
    // 秒杀过程使用先插入，再更新操作，先插入的话，可以挡住一些主键冲突的
    // 使用存储过程来减少行级锁持有时间
    @Transactional
    public SeckillExecution seckillService(MQMessage message)
            throws seckillException, seckillEndException, repeatedSeckillException {
        long seckill_id = message.getSeckill_id();
        long seckill_phone = message.getSeckill_phone();

        Date now = message.getSeckill_createTime();
        try {
            // 2. 执行插入操作
            int insertCount = successSeckillMapper.insertSuccessSeckill(seckill_id, seckill_phone);

            if (insertCount <= 0) {
                // 无法插入，那么就会发生重复插入的问题
                throw new repeatedSeckillException(SeckillSateEnum.REPEAT_KILL.getStateInfo());
            } else {
                // 2. 执行减库存操作
                int updateCount = seckillMapper.deleteSeckill(seckill_id, now);

                if (updateCount <= 0) {
                    // 无法减库存，秒杀结束
                    throw new seckillEndException(SeckillSateEnum.END.getStateInfo());
                } else {
                    // 秒杀成功
                    Success_seckill success_seckill = successSeckillMapper.querySuccessSeckillById(seckill_id, seckill_phone);
                    return new SeckillExecution(seckill_id, SeckillSateEnum.SUCCESS, success_seckill);
                }
            }
        }catch (seckillEndException e1){
            throw e1;
        }catch (repeatedSeckillException e2){
            throw e2;
        }catch (Exception e){
            logger.error(e.getMessage(),e);
            throw new seckillException(SeckillSateEnum.INNER_ERROR.getStateInfo() + e.getMessage());
        }
    }

}
