<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%--
  Created by IntelliJ IDEA.
  User: 19705
  Date: 2021-03-31
  Time: 14:28
  To change this template use File | Settings | File Templates.
--%>
<%@ page contentType="text/html;charset=UTF-8" language="java" %>
<html>
<head>
    <title>秒杀列表页</title>
    <%@ include file="common/head.jsp"%>
</head>
<body>
    <div class="container">
        <div class="panel panel-default">
            <div class="panel-heading text-center">
                <h2>秒杀列表</h2>
            </div>
            <div class="panel-body">
                <table class="table table-hover">
                    <thead>
                       <tr>
                           <th>名称</th>
                           <th>库存</th>
                           <th>开始时间</th>
                           <th>结束时间</th>
                           <th>创建时间</th>
                           <th>查看详情</th>
                       </tr>
                    </thead>
                    <tbody>
                       <c:forEach var="one" items="${all_seckills}">
                           <tr>
                               <td>${one.seckill_name}</td>
                               <td>${one.seckill_num}</td>
                               <td>
                                   <fmt:formatDate value="${one.seckill_startTime}" pattern="yyyy-MM-dd HH:mm:ss" />
                               </td>
                               <td>
                                   <fmt:formatDate value="${one.seckill_endTime}" pattern="yyyy-MM-dd HH:mm:ss" />
                               </td>
                               <td>
                                   <fmt:formatDate value="${one.seckill_createTime}" pattern="yyyy-MM-dd HH:mm:ss" />
                               </td>
                               <td>
                                   <a class="btn btn-info" href="/seckill/${one.seckill_id}/detail">查看详情</a>
                               </td>
                           </tr>
                       </c:forEach>

                    </tbody>
                </table>
            </div>
        </div>
    </div>

</body>
<!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
<script src="http://apps.bdimg.com/libs/jquery/2.0.0/jquery.min.js"></script>
<!-- 最新的 Bootstrap 核心 JavaScript 文件 -->
<script src="http://apps.bdimg.com/libs/bootstrap/3.3.0/js/bootstrap.min.js"></script>

</html>
