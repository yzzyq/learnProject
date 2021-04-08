package org.seckill.exception;

// 所有秒杀异常的基类
public class seckillException extends RuntimeException{

    public seckillException(String message){
        super(message);
    }

    public seckillException(String message, Throwable cause){
        super(message, cause);
    }
}
