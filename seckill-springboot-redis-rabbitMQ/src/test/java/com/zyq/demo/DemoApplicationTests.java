package com.zyq.demo;

import com.zyq.demo.dao.SuccessSeckillMapper;
import com.zyq.demo.entity.Success_seckill;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.List;

@SpringBootTest
class DemoApplicationTests {

    @Autowired
    private SuccessSeckillMapper successSeckillMapper;

    @Test
    void contextLoads() {
        Success_seckill success_seckill = successSeckillMapper.querySuccessSeckillById(10000,1983450);
        System.out.println(success_seckill);

        List<Success_seckill> all_seckill = successSeckillMapper.getAllSuccessSeckill();
        System.out.println(all_seckill);
    }

}
