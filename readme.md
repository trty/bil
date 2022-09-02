> 此项目为个人项目，用于处理django中高耗时业务的解决方案



现使用一个请求读取b站视频页面，处理并保存数据模拟一次业务

### 同步请求

```
GET
/add/?bv=bv1d44y1H7gP
{
    "success": true,
    "msg": "片 名 为 寄",
    "bv": "BV1d44y1H7gP"
}
```

耗时为500ms-1000ms

- 优点
  - 逻辑简单
- 缺点
  - 响应时间过慢

### 异步请求和轮询结果

```
GET
/add_sync/?bv=BV1d44y1H7gP
{
    "success": true,
    "msg": "正在加载"
}
```

耗时13ms

```
/info_sync?bv=BV1d44y1H7gP
```

耗时10ms

- 优点

  - 不需要等待业务执行时间

- 缺点
  - 需要前端轮询业务结果
  - 无法处理大量数据
