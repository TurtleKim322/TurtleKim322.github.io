# 검색엔진 등록 안내

사이트: https://turtlekim322.github.io/

사이트맵: https://turtlekim322.github.io/sitemap.xml

robots.txt: https://turtlekim322.github.io/robots.txt

## 준비된 설정

- 글별 description, canonical, Open Graph와 BlogPosting JSON-LD
- 홈페이지 WebSite JSON-LD
- 실제 HTML 링크로 연결된 카테고리 페이지
- jekyll-sitemap을 통한 게시글·카테고리·고정 페이지 사이트맵 자동 생성
- robots.txt에서 크롤링 허용 및 사이트맵 위치 안내

글에 `description:`을 작성하면 검색 설명과 목록 요약에 우선 사용합니다. 없으면 excerpt, SEO에는 마지막으로 사이트 설명을 사용합니다. 설명은 해당 글의 내용을 자연스럽게 요약하세요.

## Google Search Console

1. [Search Console](https://search.google.com/search-console)에 본인 계정으로 로그인합니다.
2. **URL 접두어** 속성으로 `https://turtlekim322.github.io/`를 추가합니다. github.io의 DNS를 관리하지 않으므로 도메인 속성 대신 URL 접두어를 사용합니다.
3. 소유권 확인에서 **HTML 태그** 방식을 선택하고 `content="..."` 안의 실제 값만 복사합니다.
4. 저장소 `_config.yml`의 `google_site_verification:` 뒤에 실제 값을 따옴표로 감싸 입력하고 배포합니다. 예시의 USER_VALUE를 그대로 넣지 마세요.
5. 홈페이지 소스에 `google-site-verification` 태그가 출력되면 Search Console에서 확인합니다.
6. Sitemaps 메뉴에 `sitemap.xml`을 제출합니다.
7. URL 검사에 대표 글 주소를 넣어 라이브 URL을 테스트하고 색인 생성 요청을 합니다. 나머지 글은 사이트맵으로 알립니다.

확인 태그는 인증 뒤에도 유지합니다. [Google 소유권 확인 도움말](https://support.google.com/webmasters/answer/9008080), [사이트맵 제출 안내](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap).

## Naver Search Advisor

1. [네이버 서치어드바이저](https://searchadvisor.naver.com/)에서 웹마스터 도구에 로그인합니다.
2. `https://turtlekim322.github.io/`를 사이트로 등록합니다.
3. HTML 태그 소유확인 방식에서 `naver-site-verification`의 content 값을 받습니다.
4. `_config.yml`의 `naver_site_verification:`에 실제 값만 입력하고 배포합니다.
5. 소유확인을 완료하고 사이트맵 제출 메뉴에 위 사이트맵 주소를 입력합니다.
6. 수집·색인 리포트를 확인하고 필요한 대표 URL에 수집 요청을 합니다.

네이버는 콘텐츠 URL을 알리는 데 사이트맵을 권장합니다. [공식 사이트맵 제출 안내](https://searchadvisor.naver.com/guide/request-feed), [사이트 진단 안내](https://searchadvisor.naver.com/guide/report-diagnosis).

## Daum 검색등록

1. [Daum 검색등록](https://register.search.daum.net/)에 접속합니다.
2. 제공되는 사이트/블로그 등록 유형 중 해당되는 유형을 선택합니다.
3. 블로그 URL, 제목 `거북이 쉼터`, 사이트 소개와 화면에서 요구하는 정보를 직접 입력합니다.
4. 등록 조건과 동의 내용을 확인한 뒤 신청하고 결과를 확인합니다. 서비스의 신청 화면과 심사 기준에 따라 추가 정보가 필요할 수 있습니다.

## 완료 여부 구분

이번 수정은 사이트 코드와 등록 절차 준비입니다. 검색엔진 계정의 소유확인·사이트맵 제출·Daum 신청은 아직 수행하지 않았습니다. 설정값은 비워 두었으며 가짜 인증 태그를 출력하지 않습니다.

사이트맵 제출과 크롤링 허용만으로 검색 노출이 보장되지는 않습니다. 실제 수집과 색인은 각 검색엔진이 결정합니다. [Google 안내](https://developers.google.com/search/help/crawling-index-faq).
