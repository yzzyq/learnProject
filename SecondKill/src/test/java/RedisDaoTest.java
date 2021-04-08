import org.junit.Test;
import org.junit.runner.RunWith;
import org.seckill.dao.cache.RedisDao;
import org.seckill.entity.Seckill;
import org.seckill.service.SeckillService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration({"classpath:spring-dao.xml","classpath:spring-service.xml"})
public class RedisDaoTest {

    @Autowired
    private RedisDao redisDao;

    @Autowired
    private SeckillService seckillService;

    @Test
    public void redisTest(){
        Seckill seckill = redisDao.getSeckill(10000);
        if(seckill == null){
            seckill = seckillService.getSeckillByIdService(10000);
            if(seckill != null){
                String result = redisDao.putSeckill(seckill);
                System.out.println(result);
                Seckill seckill_result = redisDao.getSeckill(10000);
                System.out.println(seckill_result);
            }
        }
    }


}
