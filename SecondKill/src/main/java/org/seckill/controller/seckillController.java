package org.seckill.controller;
import org.seckill.DTO.Exposer;
import org.seckill.DTO.SeckillExecution;
import org.seckill.DTO.SeckillResult;
import org.seckill.SeckillEnum.SeckillSateEnum;
import org.seckill.entity.Seckill;
import org.seckill.exception.repeatedSeckillException;
import org.seckill.exception.seckillEndException;
import org.seckill.exception.seckillException;
import org.seckill.service.SeckillService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Date;
import java.util.List;

@Controller
@RequestMapping("/seckill")
public class seckillController {

    private final Logger logger = LoggerFactory.getLogger(this.getClass());

    @Autowired
    private SeckillService seckillService;

    @RequestMapping(value = "/list", method = RequestMethod.GET)
    public String list(Model model){
        List<Seckill> seckills = seckillService.getSeckillService();
        model.addAttribute("all_seckills",seckills);
        return "list";
    }

    @RequestMapping(value = "/{seckill_id}/detail", method = RequestMethod.GET)
    public String getDetail(@PathVariable("seckill_id") Long seckill_id, Model model){
        if(seckill_id == null){
            return "redirect:/seckill/list";
        }
        Seckill seckill = seckillService.getSeckillByIdService(seckill_id);
        if(seckill == null){
            return "forward:/seckill/list";
        }
        model.addAttribute("seckill",seckill);
        return "detail";
    }

    @ResponseBody
    @RequestMapping(value = "/{seckill_id}/exposer",
                    method = RequestMethod.POST,
                    produces = {"application/json;charset=UTF-8"})
    public SeckillResult<Exposer> getExposer(@PathVariable("seckill_id") Long seckill_id){
        SeckillResult<Exposer> seckillResult;
        try{
            Exposer exposer = seckillService.exportSeckillUrlService(seckill_id);
            System.out.println("exposer:" + exposer);
            seckillResult = new SeckillResult<Exposer>(true, exposer);
        }catch (Exception e){
            logger.error(e.getMessage(),e);
            seckillResult = new SeckillResult<Exposer>(false,e.getMessage());
        }
        System.out.println("seckillResult:" + seckillResult);
        return seckillResult;
    }

    @ResponseBody
    @RequestMapping(value = "/{seckill_id}/{md5}/seckillExecution",
                    method = RequestMethod.POST,
                    produces = {"application/json;charset=UTF-8"})
    public SeckillResult<SeckillExecution> getSeckillExecution(@PathVariable("seckill_id") Long seckill_id,
                                                               @PathVariable("md5") String md5,
                                                               @CookieValue(value = "killPhone", required = false)Long kill_phone){
        if(kill_phone == null){
            return new SeckillResult<SeckillExecution>(false,"未注册");
        }

        try{
//            SeckillExecution seckillExecution = seckillService.executeSeckillService(seckill_id,kill_phone,md5);
            // 使用存储过程进行调用
            System.out.println("--------------开始存储过程--------------------");
            SeckillExecution seckillExecution = seckillService.executeSeckillServiceProcedure(seckill_id,kill_phone,md5);
            System.out.println("--------------存储过程结束--------------------");
            return new SeckillResult<SeckillExecution>(true,seckillExecution);
        }catch (seckillEndException e){
            SeckillExecution seckillExecution = new SeckillExecution(seckill_id, SeckillSateEnum.END);
            return new SeckillResult<SeckillExecution>(true,seckillExecution);
        }catch (repeatedSeckillException e){
            SeckillExecution seckillExecution = new SeckillExecution(seckill_id, SeckillSateEnum.REPEAT_KILL);
            return new SeckillResult<SeckillExecution>(true,seckillExecution);
        }catch (seckillException e){
            SeckillExecution seckillExecution = new SeckillExecution(seckill_id, SeckillSateEnum.INNER_ERROR);
            return new SeckillResult<SeckillExecution>(true,seckillExecution);
        }
    }

    @ResponseBody
    @RequestMapping(value = "time/now", method = RequestMethod.GET)
    public SeckillResult getSeckillTime(){
        Date now = new Date();
        return new SeckillResult(true,now.getTime());
    }





}
