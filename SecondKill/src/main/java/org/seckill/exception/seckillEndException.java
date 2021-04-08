package org.seckill.exception;

// 秒杀结束异常
public class seckillEndException extends RuntimeException{

    public seckillEndException(String message){
        super(message);
    }

    public seckillEndException(String message, Throwable cause){
        super(message, cause);
    }

}
