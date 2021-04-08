
var seckill = {
    // 封装秒杀相关的url
    URL : {
        now:function (){
            return '/seckill/time/now';
        },
        exposer:function (seckill_id){
            return '/seckill/'+seckill_id+'/exposer';
        },
        execution:function (seckill_id,md5){
            return '/seckill/'+seckill_id+'/'+md5+'/seckillExecution';
        },
    },

    handleSeckillkill: function (seckill_id,node){
        // 获取秒杀地址，控制显示逻辑，执行秒杀
        node.hide().html('<button class="btn btn-primary btn-lg" id="killBtn">开始秒杀</button>')
        console.log('handleSeckillkill:' + seckill_id);
        $.post(seckill.URL.exposer(seckill_id),{},function (result){
            // 在回调函数中，执行交互流程
            if(result && result['success']){
                // 开启秒杀，获取秒杀地址
                var exposer = result['data'];
                if(exposer['exposed']){
                    // 获取秒杀地址
                    var md5 = exposer['md5'];
                    var killUrl = seckill.URL.execution(seckill_id,md5);
                    console.log("killUrl:" + killUrl);
                    // 绑定按钮点击事件
                    $('#killBtn').one('click',function (){
                        // 下面就是开始真正的秒杀
                        // 1. 先禁用秒杀按钮
                        $(this).addClass('disabled');
                        // 2. 发送秒杀请求执行秒杀
                        $.post(killUrl,{},function (result){
                            console.log('result:' + result);
                           if(result && result['success']){
                               var killResult = result['data'];
                               var state = killResult['state'];
                               var stateInfo = killResult['statInfo'];
                               // 显示秒杀结果
                               node.html('<span class="label label-success">' + stateInfo + '</span>');
                           }
                        });
                    });
                    node.show();
                }else{
                    // 未开启秒杀
                    var now = exposer['now'];
                    var start = exposer['start'];
                    var end = exposer['end'];
                    // 重新计算计时逻辑
                    seckill.countdown(seckill_id,now,start,end);
                }
            }else{
                console.log("result:" + result);
            }
        });
    },

    // 验证手机号
    validatePhone: function (phone){
        if(phone && phone.length == 11 && !isNaN(phone)){
            return true;
        }else{
            return false;
        }
    },

    // 计时器
    countdown:function (seckillId,nowTime,seckillStart,seckillEnd){
        var killBox = $('#seckill-box');
        if(nowTime > seckillEnd){
            killBox.html('秒杀结束！');
        }else if(nowTime < seckillStart){
            // 秒杀还未开始，计时事件进行绑定
            var killTime = new Date(seckillStart + 1000);
            killBox.countdown(killTime,function (event){
                var format = event.strftime('秒杀倒计时：%D天 %H时 %M分 %S秒');
                killBox.html(format);
            }).on('finish.countdown',function (){
                seckill.handleSeckillkill(seckillId,killBox);
            });
        }else{
            // 秒杀开始
            seckill.handleSeckillkill(seckillId,killBox);
        }
    },

    // 详情页秒杀逻辑
    detail:{
        // 详情页初始化
        init:function(params){
            var killPhone = $.cookie('killPhone');
            var seckillId = params['seckill_id'];
            var seckillStart = params['seckill_startTime'];
            var seckillEnd = params['seckill_endTime'];

            console.log('killPhone:' + killPhone);
            if(!seckill.validatePhone(killPhone)) {
                console.log('开始填写用户信息');
                var killPhoneModal = $('#killPhoneModal');
                killPhoneModal.modal({
                    show: true, // 显示弹出层
                    backdrop: 'static',
                    keyboard: false
                });

                $('#killPhoneBtn').click(function(){
                    var inputPhone = $('#killPhoneKey').val();
                    console.log('inputPhone:' + inputPhone); // TODO
                    if(seckill.validatePhone(inputPhone)){
                        $.cookie('killPhone',inputPhone,{expires: 7, path: '/seckill'});
                        // 刷新页面
                        window.location.reload();
                    }else{
                        $('#killPhoneMessage').hide().html('<label class="label label-danger">手机号错误</label>').show(300);
                    }
                });
            }

            console.log('登录');
            // 已经登录
            // 计时交互
            var seckillId = params['seckill_id'];
            var seckillStart = params['seckill_startTime'];
            var seckillEnd = params['seckill_endTime'];
            console.log('detail:' + seckillId);
            $.get(seckill.URL.now(),{},function(result){
                if(result && result['success']){
                    var nowTime = result['data'];
                    seckill.countdown(seckillId,nowTime,seckillStart,seckillEnd);
                }else{
                    console.log('result:' + result);
                }
            });

        }

    }

}



