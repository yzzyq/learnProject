package com.zyq.demo.DTO;

import lombok.Data;

@Data
public class SeckillResult<T> {

    private boolean success;

    private T data;

    private String error;

    public SeckillResult(boolean success, T data){
        this.success = success;
        this.data = data;
    }

    public SeckillResult(boolean success, String error){
        this.success = success;
        this.error = error;
    }

}
