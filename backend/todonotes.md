### TODO

- Kalan istek sayısını gösterme
- APIKey
- Versioning
- URL Yapısı:
    - domain: `www.automotodata.com/`
    - subdomain: `www.api.automotodata.com/`


### Cache
`cache_page(60*1)` ile viewlarımızın hepsini 1 dakika cache aldık. Test aşaması bittikten sonra `cache_page(60*60*2)` ile 2 saat cache yapabiliriz. (Bütün veriler girildikten sonra arttırılmalı)


### Signals (CustomerUser, Subscription)
`CustomerUser` oluşturulduğu an, `account/signals.py` da belirtildiği gibi:
- Free Trial Planı seçiliyor
- Subscription user, plan ve paid_amount değerleri bunlara göre veriliyor ve oluşturuluyor 


`Subscription` oluşturulduğu ve güncellendiği an, `subscribe/signals.py` de belirtildiği gibi:
- **created** işleminde, `start_date` değerinin üstüne `period_duration` ekleniyor ve bu sayede `expiry_date` hesaplanıyor
- güncellemelerde `plan` fieldının `slug` değerine göre *if* kontrolleri yapılıyor ve `CustomerUser` modelinin `membership_type` değeri değiştiriliyorç