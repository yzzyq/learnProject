package com.zyq.demo.MQ;

import com.dyuproject.protostuff.ProtostuffIOUtil;
import com.dyuproject.protostuff.runtime.RuntimeSchema;
import com.zyq.demo.DTO.SeckillExecution;
import com.zyq.demo.DTO.SeckillResult;
import com.zyq.demo.SeckillEnum.SeckillSateEnum;
import com.zyq.demo.exception.repeatedSeckillException;
import com.zyq.demo.exception.seckillEndException;
import com.zyq.demo.exception.seckillException;
import com.zyq.demo.service.SeckillService;
import org.springframework.amqp.rabbit.annotation.Exchange;
import org.springframework.amqp.rabbit.annotation.Queue;
import org.springframework.amqp.rabbit.annotation.QueueBinding;
import org.springframework.amqp.rabbit.annotation.RabbitListener;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RabbitConsumer {

    @Autowired
    SeckillService seckillService;

    private RuntimeSchema<MQMessage> schema = RuntimeSchema.createFrom(MQMessage.class);

    @RabbitListener(bindings = {
            @QueueBinding(
                    value = @Queue(value = MQConfig.QUEUE_NAME,
                            durable = "true"),
                    exchange = @Exchange(name = MQConfig.EXCHANGE_NAME,
                            type = "topic",
                            durable = "true"),
                    key = {MQConfig.ROUTE_KEY}
            )
    })
    public void consumer(byte[] bytes){
        MQMessage message = new MQMessage();
        ProtostuffIOUtil.mergeFrom(bytes,message,schema);
        System.out.println(message);

        try{
            SeckillExecution seckillExecution = seckillService.seckillService(message);
        }catch (seckillEndException e){
            SeckillExecution seckillExecution = new SeckillExecution(message.getSeckill_id(), SeckillSateEnum.END);
        }catch (repeatedSeckillException e){
            SeckillExecution seckillExecution = new SeckillExecution(message.getSeckill_id(), SeckillSateEnum.REPEAT_KILL);
        }catch (seckillException e){
            SeckillExecution seckillExecution = new SeckillExecution(message.getSeckill_id(), SeckillSateEnum.INNER_ERROR);
        }

    }



}
