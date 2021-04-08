import org.junit.Test;
import org.junit.runner.RunWith;
import org.seckill.DTO.Exposer;
import org.seckill.DTO.SeckillExecution;
import org.seckill.entity.Seckill;
import org.seckill.service.SeckillService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.test.context.ContextConfiguration;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.util.List;

@RunWith(SpringJUnit4ClassRunner.class)
@ContextConfiguration({"classpath:spring-dao.xml","classpath:spring-service.xml"})
public class ServiceTest {
    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private SeckillService seckillService;

    @Test
    public void serviceTest(){
//        List<Seckill> seckills = seckillService.getSeckillService();
//        System.out.println(seckills);
//
//        Seckill seckill = seckillService.getSeckillByIdService(10000);
//        System.out.println(seckill);
//
        Exposer exposer = seckillService.exportSeckillUrlService(10000);
        System.out.println(exposer);
//
//        SeckillExecution seckillExecution = seckillService.executeSeckillService(10000,159856,exposer.getMd5());
//        System.out.println(seckillExecution);


        SeckillExecution seckillExecution = seckillService.executeSeckillServiceProcedure(10000,159856,exposer.getMd5());
        System.out.println(seckillExecution);

    }



}
