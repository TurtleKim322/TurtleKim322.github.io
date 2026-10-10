(function () {
  if (location.pathname.replace(/\/$/, '') !== '/categories') return;
  var routes = {"sar-basics": "/categories/sar-basics/", "security": "/categories/security/", "hobby": "/categories/hobby/", "personal-project": "/categories/personal-project/", "seoul-psinsar": "/categories/seoul-psinsar/", "my-hobby": "/categories/my-hobby/", "programming": "/categories/programming/", "algorithm": "/categories/algorithm/", "signal-processing": "/categories/signal-processing/", "quantum-computing": "/categories/quantum-computing/", "challenge": "/categories/challenge/", "paper-review": "/categories/paper-review/", "math": "/categories/math/", "satellite": "/categories/satellite/", "SAR": "/categories/sar-basics/", "보안": "/categories/security/", "취미": "/categories/hobby/", "개인 프로젝트": "/categories/personal-project/", "서울 PS-InSAR": "/categories/seoul-psinsar/", "나의 취미": "/categories/my-hobby/", "프로그래밍": "/categories/programming/", "알고리즘": "/categories/algorithm/", "신호처리": "/categories/signal-processing/", "양자 컴퓨터 프로그래밍": "/categories/quantum-computing/", "도전과제": "/categories/challenge/", "논문 리뷰": "/categories/paper-review/", "수학": "/categories/math/", "위성": "/categories/satellite/", "mathematics": "/categories/math/", "quantum-programming": "/categories/quantum-computing/"};
  function followBookmark() {
    var slug;
    try { slug = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    if (routes[slug]) location.replace(routes[slug]);
  }
  followBookmark();
  window.addEventListener('hashchange', followBookmark);
}());
