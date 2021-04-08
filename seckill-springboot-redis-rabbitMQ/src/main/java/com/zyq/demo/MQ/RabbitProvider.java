package com.zyq.demo.MQ;

import com.dyuproject.protostuff.LinkedBuffer;
import com.dyuproject.protostuff.ProtostuffIOUtil;
import com.dyuproject.protostuff.runtime.RuntimeSchema;
import com.zyq.demo.entity.Seckill;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RabbitProvider {

    private Logger logger = LoggerFactory.getLogger(this.getClass());

    private RuntimeSchema<MQMessage> schema = RuntimeSchema.createFrom(MQMessage.class);

    @Autowired
    private RabbitTemplate rabbitTemplate;

    public void sendInfo(MQMessage mqMessage){
        byte[] bytes = ProtostuffIOUtil.toByteArray(mqMessage,schema,
                LinkedBuffer.allocate(LinkedBuffer.DEFAULT_BUFFER_SIZE));

        logger.info("发送信息到消息队列中");
        rabbitTemplate.convertAndSend(MQConfig.EXCHANGE_NAME,MQConfig.ROUTE_KEY,bytes);
    }


}
