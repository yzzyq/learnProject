package com.zyq.demo.exception;

// 重复秒杀异常
public class repeatedSeckillException extends RuntimeException{

    public repeatedSeckillException(String message){
        super(message);
    }

    public repeatedSeckillException(String message, Throwable cause){
        super(message, cause);
    }

}
