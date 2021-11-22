## 크롤러 & 번역기

총 4개의 크로러와 번역기 1개 코드 작성


### 1.papers with code

papers with code의 task와 method를 각각 크롤링 하는 코드 (반드시 task -> method순으로 실행)

### 2. huggin face

huggin face의 method를 크롤링하는 코드

### 3. kci

kci 페이지는 동적으로 변하는 사이트이므로 평범한 GET 요청을 긁는 방법을 사용하지 않고,

POST 요청을 보내 받은 DATA를 처리하는 방법 사용

### 4. 번역기

papago 사이트는 GET요청을 통하여 긁는데 어려움이 있다는 것을 확인한 후

POST요청을 할 때 전송하는 데이터와 번역할 문장(여러 문장을 보내도 무관)을 같이 전송하여

받은 DATA를 처리하는 방법을 사용
