import com.sun.net.httpserver.Authenticator;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.seckill.dao.SeckillMapper;
import org.seckill.dao.SuccessSeckillMapper;
import org.seckill.entity.Seckill;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration({"classpath:spring-dao.xml"})
public class DaoTest {

    @Autowired
    SeckillMapper seckillMapper;

    @Autowired
    SuccessSeckillMapper successSeckillMapper;

    @Test
    public void testDaoSeckill() throws ParseException {
//        List<Seckill> result = seckillMapper.queryAllSeckill(0,3);
//        for(Seckill sc:result){
//            System.out.println(sc);
//        }
//
//        Seckill seckill = seckillMapper.querySeckillById(10000);
//        System.out.println(seckill);

        Date time = new Date();

        int num = seckillMapper.deleteSeckill(10000,time);
        System.out.println(num);

        int insert_num = successSeckillMapper.insertSuccessSeckill(10000,18952771);
        System.out.println(insert_num);

    }


}
