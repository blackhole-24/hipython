USE WNTRADE;
SELECT * FROM wntrade.주문세부;
/*
SELECT * FROM wntrade.사원;
SELECT * FROM wntrade.주문세부;
SELECT * FROM wntrade.주문;
*/ -- 주석
SELECT 고객번호, 고객회사명 FROM 고객;
SELECT 고객번호
,담당자명
,고객회사명 AS 이름
,마일리지 AS 포인트
FROM 고객;

SELECT 이름 AS 직원명
,주소
,직위 
,입사일
FROM 사원
WHERE 직위 = "사원";

SELECT * FROM wntrade.제품;
SELECT 제품명
, FORMAT(단가, 0) AS "단가"
,재고 AS "구매가능수량!!"
, FORMAT(단가 * 재고, 0) AS "주문가능금액"
FROM 제품
WHERE 단가 * 재고 >= 100000
ORDER BY 재고 DESC; -- ASC 어센딩(기본default), DESC 디센딩
# 사원인 직원의 이름과 입사일 정보 출력

-- #주문내역정보를 출력 - 제품번호, 단가, 주문수량, 할인율, 주문금액
SELECT * FROM wntrade.주문세부;
SELECT 제품번호
,format(단가, 0) AS "단가"
,주문수량
,할인율
,FORMAT(단가 * 주문수량, 0) AS "주문금액"
,FORMAT(단가 * 주문수량 * (1-할인율), 0) AS "할인금액"
FROM 주문세부
ORDER BY 5 DESC;
-- LIMIT 10

SELECT * FROM wntrade.고객;
SELECT 고객번호
,담당자명
,고객회사명
,FORMAT(마일리지, 0) AS "포인트"
,FORMAT(마일리지 + (마일리지 * 0.1), 0) AS "마일리지"
FROM 고객
WHERE 마일리지 >= 100000
ORDER BY 5 DESC;

-- 예제 2-4
SELECT 고객번호
,담당자명
,도시
,마일리지 AS 포인트
FROM 고객
WHERE 도시 = '서울특별시'
ORDER BY 마일리지 DESC;

-- 예제 2-5
SELECT *
FROM 고객
LIMIT 3;

-- 예제 2-6
SELECT *
FROM 고객
ORDER BY 마일리지 DESC
LIMIT 3;

-- 연습문제, WHERE, ORDER BY, LIMIT - 테이블 마다;;
SELECT 고객번호
,고객회사명
,담당자명
,담당자직위
,주소
,도시
,전화번호
,마일리지
FROM 고객
WHERE 도시 = "서울특별시"
ORDER BY 4 ASC
LIMIT 20;

SELECT 등급명
,하한마일리지
,상한마일리지
FROM 마일리지등급
WHERE 상한마일리지 <= 100000
ORDER BY 3 DESC
LIMIT 3;

SELECT 부서번호
,부서명
FROM 부서
WHERE 부서명 = "영업부"
LIMIT 1;

SELECT 사원번호
,이름
,직위
,성별
,생일
,입사일
,주소
,도시
FROM 사원
WHERE 도시 = "서울특별시"
order by 2 ASC
LIMIT 20;

SELECT DISTINCT 도시
FROM 고객;
--

SELECT 23 + 5 AS 더하기
,23 - 5 AS 빼기
,23 * 5 AS 곱하기
,23 / 5 AS 실수나누기
,23 DIV 5 AS 정수나누기
,23 %5 AS 나머지1
,23 MOD 5 AS 나머지2
; -- FROM 고객;

SELECT '오늘의 고객은', CURRENT_DATE, 담당자명
FROM 고객;

SELECT 23 >= 5
,23 <= 5 
,23 > 23
,23 < 23
,23 = 23
,23 != 23
,23 <> 23;

SELECT *
FROM 고객
WHERE 담당자직위 <> '대표이사';

SELECT * FROM wntrade. 주문
WHERE 주문일 < '2021-01-01';

SELECT *
FROM 고객
WHERE 도시 = '부산광역시'
AND 마일리지 < 1000;

-- 서울, 마일리지 5000 이상 
-- 서울 이거나, 마일리지 10000 이상
-- 서울특별시가 아닌 고객
-- 서울이 아니면서 마일리지 5000 이상
-- 서울특별시와 부산광역시 사는 고객

SELECT *
FROM 고객
WHERE 도시 = "서울특별시"
AND 마일리지 > 5000
ORDER BY 9 DESC;

SELECT *
FROM 고객
WHERE 도시 = "서울특별시"
AND 마일리지 > 10000
ORDER BY 9 DESC;

SELECT *
FROM 고객
WHERE 도시 != "서울특별시";

SELECT *
FROM 고객
WHERE 도시 != "서울특별시"
AND 마일리지 > 5000;

SELECT * 
FROM 고객
WHERE 도시 = "서울특별시" 
OR 도시 = "부산광역시";

SELECT 고객번호
,담당자명
,마일리지
,도시
FROM 고객
WHERE 도시 = '부산광역시'
UNION
SELECT 고객번호
,담당자명
,마일리지
,도시
FROM 고객
WHERE 마일리지 < 1000
ORDER BY 1;

SELECT 고객번호
,담당자명
,마일리지
,도시
FROM 고객
WHERE 도시 = '부산광역시'
UNION ALL
SELECT 고객번호
,담당자명
,마일리지
,도시
FROM 고객
WHERE 마일리지 < 1000
ORDER BY 1;

-- 단가가 5000점 이상이거나 할인율이 0.5 이상인 주문
-- 고객 도시, 사원 도시를 모두 1번씩만 출력

SELECT 제품번호
,단가
,주문수량
,할인율
FROM 주문세부
WHERE 단가 > '5000'
UNION
SELECT 제품번호
,단가
,주문수량
,할인율
FROM 주문세부
WHERE 할인율 > '0.5';

SELECT 도시 FROM 고객
UNION
SELECT 도시 FROM 사원;

SELECT *
FROM 고객
WHERE 지역 IS NULL;

SELECT * FROM 고객 WHERE 지역 IS NULL;
SELECT DISTINCT 지역 FROM 고객;
-- SELECT * FROM 고객 WHERE 지역 =''; --"
SELECT * FROM 고객 ORDER BY 지역 = '', 도시;

SELECT 고객번호
,담당자명
,담당자직위
FROM 고객
WHERE 담당자직위 = '영업 과장'
OR 담당자직위 = '마케팅 과장';

SELECT 고객번호
,담당자명
,담당자직위
FROM 고객
WHERE 담당자직위 IN ('영업 과장', '마케팅 과장');

SELECT 담당자명
,마일리지
FROM 고객
WHERE 마일리지 >= 100000
AND 마일리지 <= 200000;

SELECT 담당자명
,마일리지
FROM 고객
WHERE 마일리지 BETWEEN 100000 AND 200000;


-- IN, BETWEEN AND
# 부서가 A1, A2인 사원
# 주문일이 2020-06-01 ~ 2020-06-11

SELECT *
FROM 사원
WHERE 부서번호 IN('A1','A2');

SELECT *
FROM 주문
WHERE 주문일 BETWEEN '20200601' AND '2020-06-11';

SELECT *
FROM 주문
WHERE 주문일 < '2021-01-01';


USE WNTRADE;
/* -- QUERY 질의문 - SELECT 행단위로 추출하는 명령
 *SELECT 컬럼목록 - 값의 목록 지정, AS, 수식 사용법 (FORMAT(),0)
 *FROM 테이블목록
 *WHERE 조건식
 *ORDER BY 컬럼목록 - 출력시 정령 - ASC, DESC
 *LIMIT n - 출력의 개수 지정
 *DISTINCT - 컬럼에 나오는 값의 목록
*/

/*쿼리 실행순서
 *FROM
 *WHERE
 *SELECT
 *ORDER BY
 *LIMIT
*/

/*연산자 
 *수칙연산자, 비교연산자, 논리연산자, 집합연산자 (UNION, UNION ALL)
 *IS NULL
 *IN, BETWEEN AND
*/

/*SQL문 작성 규칙
 *대소문자 구분 X - 명령어, 테이블명, 컬럼명, 단, 컬럼의 값은 제외
 *여러 줄에 걸쳐 작성O -> 마지막에 ; 필수 "들여쓰기"
 *명령어는 대문자로 쓰는 것이 일반적
 *컬럼목록, 테이블 목록은 ,(콤마)로 연결한다. 순서가 중요!
*/

SELECT * FROM wntrade.고객;
SELECT '고객번호', '고객회사명', '담당자명', '담당자직위', '주소', '도시', '지역'
FROM wntrade.고객
where 고객번호 LIKE '_C%';

#첫번째가 C인 고객 'C%'
#세번째가 C인 고객 '__C%' '__C__'
#마지막이 C인 고객 '%C' '____C'

SELECT * FROM wntrade.고객;

#광역시, 고객번호 두번째/ 세번째가 C인 고객 추출
SELECT *
FROM 고객
WHERE 도시 LIKE '%광역시'
AND (고객번호 LIKE '_C%' 
OR 고객번호 LIKE '__C%'); #우선순위 ()



# 연습1. 서울, 마일리지 15천점 이상, 2만점 이하인 고객 목록
# 연습2. 고객이 사는 지역, 도시 목록 - 지역순, 도시순 기준으로 출력
# 연습3. 춘천, 과천 거주 고객 중 담당자직위가 이사 또는 사원인 고객 목록
# 연습4. 광역시, 특별시가 아닌 고객 중 마일리지 많은 고객 상위 3명이 누구일까??
# 연습5. 지역을 알고 있는 고객 중 담당자 직위가 대표이사가 아닌 전체고객목록




USE WNTRADE;

-- 단일행 함수
-- 1. 문자함수
-- 2. 숫자함수
-- 3. 날짜함수
-- 집계함수

USE WNTRADE;

select FIELD('SQL', 'SQL', 'JAVA', 'C');

select FIELD('오땅', '홈런볼', '오땅', '초콜릿'); #2

select REPLACE('ABC-DEF', '-', '*');

select REVERSE('ABCDEF');

select NOW(), SYSDATE(); -- 현재 날짜시간
select CURDATE(), CURTIME();

select NOW() as 'START', SLEEP(5), NOW() as 'END'; -- 시작시간 기준
select SYSDATE() as 'START',SLEEP(5),  SYSDATE() as 'END';  -- 호출시간 기준
 
SELECT 고객번호, IF(마일리지>1000, 'VIP', 'GOLD') AS 등급
FROM 고객

/*
주문금액 = 단가 * 주문수량
주문금약 >= 5000000 : 초과달성
주문금액 >= 4000000 : 달성
미달성
*/

SELECT * FROM wntrade.주문세부;

SELECT 주문번호
    , 단가
    , 주문수량
    , 단가 * 주문수량 AS 주문금액
    , CASE
        WHEN 단가 * 주문수량 >= 주문수량 * 5000000 THEN '초고달성'
        WHEN 단가 * 주문수량 >= 주문수량 * 4000000 THEN '달성'
        ELSE '미달성'
      END AS 달성여부
FROM 주문세부;



-- 마일리지 등급 부여 VIP, GOLD, SILVER, BRONZE
-- 부서코드 > 부서명으로



SELECT 고객회사명
    , 담당자명
    , 담당자직위
    , 도시
    , 마일리지
    , CASE
        WHEN 마일리지 >= 100000 THEN 'VIP'
        WHEN 마일리지 >= 50000 THEN 'GOLD'
        WHEN 마일리지 >= 10000 THEN 'SILVER'
        ELSE 'BRONZE'
	END AS '회원등급'
FROM 고객;


-- 부서코드 > 부서명으로
SELECT 사원번호, 이름, 부서번호,
  CASE 부서번호
    WHEN '10' THEN '영업부'
    WHEN '20' THEN '총무부'
    WHEN '30' THEN 'IT개발부'
    ELSE '기타부서'
  END AS 부서명_가상
FROM 사원;



-- 주문 테이블에 배송상태 추가 
-- 발송일 컬럼 기준, '배송대기' '빠른배송' '일반배송'으로 설정
SELECT 주문번호, 주문일, 발송일,
  CASE 
    WHEN 발송일 IS NULL THEN '배송대기'
    WHEN DATEDIFF(발송일, 주문일) <= 2 THEN '빠른배송'
    ELSE '일반배송'
  END AS 배송상태
FROM 주문;



/*연습1. 고객회사명 앞2글자 '*' 마스킹 처리
 * 연습2. 주문세부 정보중 주문금액, 할인금액, 실제주문금액 출력(1단위에서 버림)
 * 연습3. 전체 사원의 이름, 생일, 만나이, 입사일, 입사일수, 입사500일기념일 출력
 * 연습4. 고객 정보의 도시컬럼을 '대도시', '도시'로 구분하고 마일리지 VVIP, VIP, 일반고객 구분
 * 연습5. 주문테이블의 주문일을 주문년도, 분기, 월, 일, 요일, 한글요일로 출력
 * 연습6. 발송일이 요청일보다 7일 이상 늦은 주문건 출력
 * */

-- 집계함수
SELECT 도시
, COUNT(*)
, COUNT(고객번호)
, COUNT(도시)
, COUNT(DISTINCT 지역)
, SUM(마일리지)
, AVG(마일리지)
, MIN(마일리지)
FROM 고객
-- WHERE 도시 LIKE '서울%';
group by 도시;

-- 담당자 별로 집계
SELECT 담당자직위
, 도시
, COUNT(고객번호)
, SUM(마일리지)
, AVG(마일리지)
FROM 고객
group by 담당자직위, 도시
ORDER BY 1, 2;

-- GROUP BY 조건 HAVING 절
-- 고객 - 도시별로 그룹 - 고객수, 평균마일리지, 고객수가 > 10만 추출
SELECT 도시
, COUNT(고객번호)
, AVG(마일리지) 
FROM 고객
GROUP BY 도시
WITH ROLLUP
HAVING COUNT(고객번호) >= 10;

-- 고객번호 T로 시작하는 고객을 도시별로 묶어 마일리지 합 출력, 단, 1000점 이상만
SELECT 도시
, SUM(마일리지)
FROM 고객
WHERE 고객번호 LIKE 'T%'
GROUP BY 도시
WITH ROLLUP
HAVING SUM(마일리지) >= 1000;

-- 광역시 고객, 담당자 직위별로 최대마일리지, 단, 1만점 이상 레코드만 출력
SELECT 담당자직위
, MAX(마일리지)
FROM 고객
WHERE 도시 LIKE '%광역시'
GROUP BY 담당자직위
WITH ROLLUP -- 총계(TOTAL) 행 하나 더 추가 됨.
HAVING MAX(마일리지) >= 10000;

-- 연습1. 담당자 직위에 마케팅이 있는 고객의 담당자직위, 도시별 고객수 출력
-- 단, 담당자직위별 고객수와 전체 고객수도 출력alter

-- 연습2. 제품 주문년도별 주문건수 출력alter

-- 연습3. 주문년도, 분기별 주문건수 합게 출력

-- 연습4. 주문 요청일보다 발송이 늦어진 주문내역이 월별로 몇건인지 요약 조회
-- 주문월 순으로 정렬

-- 연습5. 아이스크림 제품명 별로 재고합 출력


USE WNTRADE;
/*
 * 테이블 갯수 1개 -> 심플 쿼리
 * 2개 이상 > 조인
 * 크로스 조인(카테지안프로덕트 연산) M개 X N개 = MN 개 결과를 반환
 * 내부 조인(이너조인) 조건에 만족하는 데이터만 반환 - 동등조인, 비동등조인 
 **/

-- CROSS JOIN > INNER JOIN - 동등 조인
SELECT 부서.부서번호 AS 부서부서번호, 사원.부서번호 AS 사원부서번호, 이름, 부서명
FROM 부서 JOIN 사원
ON 부서.부서번호 = 사원.부서번호
WHERE 이름 = '배재용';

-- 주문, 고객 ITCWH
SELECT 주문번호, 고객회사명
FROM 주문 JOIN 고객
ON 주문.고객번호 = 고객.고객번호
WHERE 주문.고객번호 = 'ITCWH';

-- 주문, 사원 INNER JOIN 주문번호별 
SELECT 주문번호, 주문.사원번호, 고객번호, 사원.이름 
FROM 주문 JOIN 사원
ON 주문.사원번호 = 사원.사원번호;

-- 고객, 제품 > 크로스조인
SELECT 고객회사명, 제품명
FROM 고객 JOIN 제품;

-- 고객, 마일리지 - 비동등 조인
SELECT 고객.고객회사명, 고객.마일리지, 마일리지등급.등급명
FROM 고객 JOIN 마일리지등급
ON 고객.마일리지 BETWEEN 마일리지등급.하한마일리지 AND 마일리지등급.상한마일리지
;

-- 예제 5-2 '이소미' 사원의 사원번호, 직위, 부서번호, 부서명
SELECT 사원번호
,직위
,사원.부서번호
,부서명 
FROM 사원 JOIN 부서
ON 사원.부서번호 = 부서.부서번호
WHERE 이름 = '이소미';

-- 예제 5-3 고객 회사들이 주문한 주문건수를 주문건수가 많은 순서대로 보이시오. 
-- 이때 고객 회사의 정보로는 고객번호, 담당자명, 고객회사명을 보이시오.
SELECT 고객.고객번호
		,담당자명
		,고객회사명
		,COUNT(*) AS 주문건수
FROM 고객
ON 고객.고객번호 = 주문.고객번호
GROUP BY 고객.고객번호
		,담당자명
        ,고객회사명
ORDER BY COUNT(*) DESC;

-- 사원입사일 이후 처리한 주문 조회 - 비동등 조인
SELECT 주문번호
, 이름 AS 사원명
, 입사일 
, 주문일
FROM 주문 JOIN 사원
ON 주문.사원번호 = 사원.사원번호
AND 주문.주문일 >= 사원.입사일;

-- 고객회사들이 주문한 건수 집계 > 건수가 많은 순서로 출력
SELECT 고객.고객번호, 담당자명, 고객회사명, COUNT(*) AS 주문건수
FROM 고객 JOIN 주문
ON 고객.고객번호 = 주문.고객번호
GROUP BY 고객.고객번호, 담당자명, 고객회사명 -- 고객.고객번호
ORDER BY COUNT(*) DESC;

-- 고객회사별 주문금액 합, 큰 금액 순으로 출력

SELECT 고객회사명
, SUM(주문수량*단가) AS 주문금액
FROM 고객 JOIN 주문 ON 고객.고객번호 = 주문.고객번호
		  JOIN 주문세부 ON 주문.주문번호 = 주문세부.주문번호
GROUP BY 고객회사명
ORDER BY 2 DESC;


FROM 사원;

SELECT DISTINCT 부서번호
FROM 사원;

SELECT COUNT(*)
FROM 부서;

SELECT 사원번호, 이름, 부서명
FROM 사원 LEFT JOIN 부서
ON 사원.부서번호 = 부서.부서번호
;

-- 사원이 없는 부서 
-- 주문 안한 고객

SELECT 사원번호, 이름, 부서명
FROM 사원 RIGHT JOIN 부서
ON 사원.부서번호 = 부서.부서번호;

SELECT 부서.부서명
FROM 사원 
RIGHT JOIN 부서 ON 사원.부서번호 = 부서.부서번호
WHERE 사원.사원번호 IS NULL;