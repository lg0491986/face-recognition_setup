# 昨日均价
## 获取地址
http://104.128.90.215:5002/avg_deal_price?symbol=btcusdt    
symbol表示交易对，比如这里是指btcusdt    

## 返回格式
```
{
  "avg": 11173.4995, 
  "ret": 0, 
  "symbol": "btcusdt"
}
```
如果ret为其他值，则表示错误，详细的错误信息，可以参考返回的msg内容
