package com.zyq.demo.exception;

public class redisNullException extends RuntimeException{

    public redisNullException(String message){
        super(message);
    }

    public redisNullException(String message, Throwable cause){
        super(message,cause);
    }

}
