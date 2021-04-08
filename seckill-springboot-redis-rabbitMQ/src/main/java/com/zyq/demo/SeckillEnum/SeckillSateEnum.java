package com.zyq.demo.SeckillEnum;



public enum SeckillSateEnum {

    SUCCESS(1,"秒杀成功"),
    WAIT(2,"等待秒杀"),
    END(0, "秒杀结束"),
    REPEAT_KILL(-1,"重复秒杀"),
    INNER_ERROR(-2,"系统异常"),
    DATA_REWRITE(-3,"数据篡改"),
    DATA_NULL(-4,"数据为空");

    private int state;

    private String stateInfo;

    SeckillSateEnum(int state, String stateInfo) {
        this.state = state;
        this.stateInfo = stateInfo;
    }

    public int getState() {
        return state;
    }

    public void setState(int state) {
        this.state = state;
    }

    public String getStateInfo() {
        return stateInfo;
    }

    public void setStateInfo(String stateInfo) {
        this.stateInfo = stateInfo;
    }

    public static SeckillSateEnum stateOf(int index){
        for(SeckillSateEnum state:values()){
            if(state.getState() == index){
                return state;
            }
        }
        return null;
    }
}
