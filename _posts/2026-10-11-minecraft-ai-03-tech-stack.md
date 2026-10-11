---
title: "[Minecraft AI #03] 로컬 환경에서 Minecraft AI를 개발하기 위한 기술 검토"
date: 2026-10-11 09:02:00 +0900
permalink: /minecraft-ai/03-tech-stack/
categories: [취미, 개인 프로젝트, 마인크래프트 AI]
project: minecraft-ai
project_order: 3
tags: [Minecraft, Python, PyTorch, MineRL, Mineflayer, 프로젝트 기획]
toc: true
toc_sticky: true
breadcrumbs: false
description: "Python·PyTorch·Gymnasium·PPO와 MineRL·Malmo·Mineflayer를 검토합니다. 공식 자료에서 확인한 유지보수 상태와 실제 설치 전 확인할 호환성 조건을 구분합니다."
excerpt: "모든 도구는 아직 검토 후보입니다. Minecraft 버전과 Java·Python·Node.js 의존성을 함께 살펴보고, 오래된 연구 환경의 재현 가능성을 먼저 확인하려 합니다."
---

{% include minecraft-ai-path.html %}

**기술 스택은 미확정이다.** 아래 내용은 2026-10-11에 확인한 공식 문서·저장소를 바탕으로 한 검토이며, 이 프로젝트에서 설치나 게임 실행을 검증한 결과가 아니다.
{: .notice--info}

## 로컬 PC에서 시작하려는 이유

초기에는 학습 속도보다 관찰과 문제 추적이 중요하다. 캐릭터가 어떤 행동을 했는지 화면으로 보고, 같은 실행의 로그와 비교하며, 환경 초기화가 제대로 됐는지 확인하려 한다. 로컬 실행은 이 과정을 가까이에서 살펴볼 수 있고 실험 파일의 위치와 보관 방식도 직접 관리하기 쉽다.

그렇다고 로컬이 비용이나 속도 면에서 항상 유리한 것은 아니다. 게임 렌더링, 월드 처리, 모델 갱신과 영상 인코딩이 한 PC의 자원을 나눠 쓴다. 현재 PC의 GPU·VRAM·RAM 용량과 학습 처리량은 아직 조사하지 않았으며, 특정 하드웨어로 충분하다고 단정하지 않는다.

## 공통 학습 도구 후보

| 후보 | 맡기려는 역할과 장점 | 단점·검증할 사항 |
| --- | --- | --- |
| Minecraft Java Edition | 연구 도구와 봇 생태계를 활용할 게임 환경 | 도구가 지원하는 게임 버전과 Java 런타임이 일치해야 함 |
| Python | 학습·평가·데이터 분석 코드 통합 | 구형 게임 도구가 요구하는 Python과 최신 학습 패키지 요구사항 충돌 가능 |
| PyTorch | 정책 신경망과 GPU 연산 | OS·GPU·드라이버에 맞는 설치 조합과 메모리 사용량 검증 필요 |
| Gymnasium | 환경 API 및 관측·행동 공간 정의 | Minecraft 연결과 월드 초기화를 대신 제공하지는 않음 |
| PPO / Stable-Baselines3 | 기준 알고리즘과 학습·저장 기능 | 희소 보상 문제는 별도로 해결해야 하며 행동 공간 변환이 필요할 수 있음 |

[PyTorch 설치 안내](https://pytorch.org/get-started/locally/)에서 OS와 연산 플랫폼에 맞는 패키지를 고른 뒤 CPU와 GPU 동작을 각각 확인할 예정이다. Python 버전이나 CUDA 조합을 지금 임의로 고정하지 않는다. 최종 조합을 확인한 시점에 버전과 설치 방법을 기록하려 한다.

[SB3 PPO 문서](https://stable-baselines3.readthedocs.io/en/master/modules/ppo.html)의 지원 표에서는 Dict 관측을 사용할 수 있지만 Dict 행동 공간은 지원하지 않는다. 게임 API가 키 입력·카메라·상호작용을 딕셔너리로 제공한다면 그대로 연결할 수 없다는 뜻이다. 초기에는 제한된 Discrete 또는 MultiDiscrete 행동 집합으로 줄일지 검토하고, 변환 과정에서 행동 의미가 달라지는지도 확인하려 한다.

## 게임 연결 후보 비교

| 후보 | 검토하는 이유 | 부담과 제약 |
| --- | --- | --- |
| MineRL | Minecraft 강화학습 환경과 연구 자료를 함께 검토할 수 있음 | 버전별 관측·행동·데이터셋 차이, 오래된 의존성 |
| Project Malmo | 미션과 관측·보상을 설정하는 실험 설계를 참고할 수 있음 | 보관된 프로젝트로 최신 환경 지원을 기대하기 어려움 |
| Mineflayer / Node.js | 캐릭터 접속, 이동, 블록·체력·인벤토리 API를 활용할 수 있음 | 강화학습 환경이 아니므로 Python 연결, 스텝 동기화, 초기화를 직접 설계해야 함 |

이 도구들을 한꺼번에 설치하는 구상을 하고 있지는 않다. MineRL이나 Malmo를 바탕으로 연구 환경을 재현하는 경로와, Mineflayer를 게임 제어 계층으로 두고 학습용 어댑터를 작성하는 경로를 비교한 뒤 선택하려 한다.

## MineRL과 Malmo의 유지보수 상태

공식 GitHub API의 저장소·릴리스 정보를 함께 확인했다. `pushed_at`은 저장소 활동 신호이며, 안정적인 릴리스나 설치 성공을 뜻하지 않는다. 아래 상태는 확인일 이후 바뀔 수 있다.

| 공식 저장소 | 2026-10-11 확인 상태 | 판단 |
| --- | --- | --- |
| [MineRL](https://github.com/minerllabs/minerl) | 보관 상태 아님. 최신 정식 릴리스 조회는 v1.0.2, 2023-08-23. 저장소 push 시각은 2025-01-22 | 최신 PC에서의 사용 가능 여부를 설치 재현으로 판단해야 함 |
| [Project Malmo](https://github.com/microsoft/malmo) | 보관 상태. 최신 정식 릴리스 조회는 0.37.0, 2018-11-05 | 신규 개발의 기본안으로 확정하기보다 재현 가능성과 유지 부담을 먼저 평가 |
| [Mineflayer](https://github.com/PrismarineJS/mineflayer) | 보관 상태 아님. 최신 정식 릴리스 조회는 4.39.0, 2026-09-06 | 활동이 있어도 선택한 서버·플러그인 조합은 별도 검증 필요 |

MineRL 공식 README는 v0.3·v0.4·v1.0 계열을 구분한다. v1.0 계열의 기본 관측은 픽셀 중심이며, 기존처럼 인벤토리 관측을 기본 제공한다고 가정하면 안 된다. 설치 안내에는 JDK 8이 명시되고 예제는 구형 Gym API를 사용한다. 따라서 최신 Gymnasium과 연결하려면 반환값뿐 아니라 종료 의미와 공간 정의도 검증해야 한다. 예전 MineRL-v0 데이터 미러 중단 공지도 있어, 데이터셋 접근성을 당연한 전제로 두지 않는다. 근거는 [공식 README](https://github.com/minerllabs/minerl#readme)에 있다.

Malmo는 일반 네이티브 구현과 MalmoEnv 경로가 구분돼 있고, API와 예제가 서로 같지 않다. 보관된 코드가 반드시 실행 불가능하다는 뜻은 아니지만, 최신 Python이나 Minecraft를 지원한다는 뜻도 아니다. 기존 실험을 재현할 때 필요한 과거 버전 조합과 빌드 부담부터 확인해야 한다. [공식 시작 안내](https://github.com/microsoft/malmo#getting-started)를 기준으로 별도 검토할 예정이다.

상태 확인 근거: [MineRL 저장소 정보](https://api.github.com/repos/minerllabs/minerl), [MineRL 최신 릴리스](https://api.github.com/repos/minerllabs/minerl/releases/latest), [Malmo 저장소 정보](https://api.github.com/repos/microsoft/malmo), [Malmo 최신 릴리스](https://api.github.com/repos/microsoft/malmo/releases/latest), [Mineflayer 최신 릴리스](https://api.github.com/repos/PrismarineJS/mineflayer/releases/latest). 이 API 링크는 조회 시점의 최신 값을 반환한다.

## Mineflayer 경로에서 직접 해결해야 할 것

Mineflayer 공식 README는 Node.js 18 이상을 요구하며 지원 Minecraft 버전 목록을 제공한다. 실제 개발에서는 유지보수되는 Node.js 버전과 선택한 Mineflayer 릴리스·서버 버전 조합을 고정해 검증하려 한다. 블록과 엔티티 등의 구조화 정보는 편리하지만 사람의 화면 관측보다 많은 정보를 줄 수 있어, 정책에 허용할 범위를 따로 정해야 한다. [공식 기능 및 설치 안내](https://github.com/PrismarineJS/mineflayer#readme)

또한 Mineflayer는 일반 게임 클라이언트의 렌더링 화면 자체를 제공하는 도구가 아니다. 사용자가 캐릭터를 관찰할 별도 클라이언트 또는 뷰어가 필요할 수 있다. Python 학습기와 Node.js 제어 계층 사이에는 요청 ID, 타임아웃, 스텝 완료 응답을 정의하고, 같은 행동이 중복 실행되지 않도록 설계할 계획이다.

## 버전보다 먼저 정할 검증 순서

1. 원하는 관측이 구조화 정보인지 픽셀인지 정하고 후보별 제공 범위를 대조한다.
2. OS, Minecraft, Java, Python 또는 Node.js, 학습 패키지 버전 표를 작성한다.
3. 격리된 개발 환경에서 연결과 기본 행동, 종료·재접속을 확인한다.
4. 동일한 초기 조건으로 월드를 반복 초기화할 수 있는지 확인한다.
5. Gymnasium 계약과 관측·행동 공간에 실제 반환 데이터가 맞는지 점검한다.
6. 짧은 데이터 수집으로 환경 스텝 처리량, 메모리, GPU 사용량과 녹화 영향을 측정한다.

위 항목은 모두 예정이며 이번 문서화 작업에서는 실행하지 않았다. 환경의 렌더링이나 월드 처리가 병목이면 GPU를 늘려도 전체 속도는 크게 변하지 않을 수 있다. 픽셀 해상도, 프레임 누적 수, 병렬 환경 수와 배치 크기를 하나씩 바꿔 병목을 찾을 계획이다.

## 잠정 결론과 다음 단계

현시점에서 특정 도구를 최종 선정할 근거는 부족하다. **반복 가능한 초기화와 필요한 관측을 제공하는 조합**을 우선 기준으로 삼고, 작은 학습 실험이 재현된 뒤 확장 여부를 결정하려 한다.

[다음 글에서는 관찰 화면, 녹화와 행동 로그를 연결하는 설계]({{ '/minecraft-ai/04-observability/' | relative_url }})를 정리한다. 실행할 도구를 고르는 일만큼, 실행 후 무엇을 근거로 판단할지 정하는 일도 필요하다.

{% include minecraft-ai-series.html %}
