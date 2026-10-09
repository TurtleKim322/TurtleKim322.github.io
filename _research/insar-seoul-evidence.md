# 서울 PS-InSAR 시리즈 근거·검증 메모

이 문서는 시리즈 개정 시 확인한 근거와 공개 범위를 추적하는 저장소 내부 메모다. 사용자 계정 경로, Windows 장치명, 인증정보 또는 대용량 원본 자료는 기록하지 않는다. WSL 작업자료는 읽기 전용으로 확인했다. 분석 파일을 수정하거나 StaMPS를 재실행하지 않았다.

## 확인한 프로젝트 근거

| 공개 글 | 확인 자료 | 확인 결과 / 공개 범위 |
|---|---|---|
| #1 | 프로젝트 메모, StaMPS 작업 폴더 구조, patch 로그 | 124개 영상·20개 PATCH 기록. 처리 흐름 그림은 개념도. P9/P14 로그의 일부 완료를 전체 AOI/전체 patch 완료로 확대하지 않음. |
| #2 | 프로젝트 AOI 메모, PATCH 후보 지리 좌표 시각화 | AOI 126.75–127.20°E, 37.40–37.72°N. 실제 SAFE annotation과 SNAP 그래프 미확보. IW2/VV/burst 2–4는 기록값으로 표기. |
| #3 | SAFE annotation, GPT/XML, 전처리 로그 미확인 | draft 상태 유지. burst footprint와 124개 scene 처리 성공을 주장하지 않음. |
| #4 | P9 `ps1.mat`: `day`, `bperp`, `master_day`, `master_ix` | 124 scenes, master index 65, master date 2022-07-16, 수직 기준선 범위 −252.054–+481.418 m. P9 값이며 최적 master 근거로 쓰지 않음. |
| #5 | 실제 SNAP graph, pair log, ESD residual 미확인 | draft 상태 유지. 정합 개념 그림만 보유. 123쌍 전체 처리 완료로 쓰지 않음. |
| #6 | P9 `ph1.mat`, 영상 날짜 배열, 생성된 phase plots | phase plot은 P9 `angle(ph)` wrapped phase, −π–+π rad, indices 10/30/50/70. 인덱스 50은 2021-11-18. `.diff`는 복구/재생성하지 않음. |
| #7 | 각 PATCH의 `pscands.1.ij`, `ps1.mat`, 좌표 점검 | raw row sum 3,539,547; historical ij-pair dedup 2,572,868; current `n_ps` sum 3,539,534. 13-row difference aligns with invalid geocoded rows filtered during load. Values have different aggregation/stage semantics; no single “unique PS total.” |
| #8 | `calamp.out`, `STAMPS.log`, `ps_parms_initial.log`, parameter files, available C source/package records | initial lambda NaN; later `0.0554658`; P9 `n_trial_wraps=0.937572`; mean amplitude about 92.8078 in run record; Octave signal 1.4.7. Original RSLC unavailable, so endian is not independently validated from raw bytes. Parameter field counts (about 8 initial vs 61 valid) describe recorded setup, not a universal requirement. |
| #9 | P9 `ps1.mat`, `PATCH_9/STAMPS.log`, P14 `STAMPS.log`, existing plots | P9 candidates 303,941; gamma histogram median 0.8773 with zero nonfinite; P9 Step 3 selected 302,481 (Oct 6 log); P14 selected 460,353 (Oct 8 log). Height sentinel −32768 excluded; datum unconfirmed. Only patch-level statuses. |
| #10 | project-era storage notes and existing explanatory figure | ZIP124 ~546.3 GB; `stamps_final` ~192 GB; Windows free space ~1 GB then ~762 GB after cleanup. Historical values only; not current measurements. |

## Visual provenance

- `01-environment/pipeline-overview.png`: conceptual pipeline, not run evidence.
- `02-burst/iw2-burst-selection.png`: conceptual swath/burst diagram, not the product footprint.
- `04-master/baseline-time-network.png`: derived from P9 master date/baseline arrays.
- `05-coreg/tops-coregistration.png`: conceptual registration sequence, no residual measurements.
- `06-interferogram/wrapped-phase-*.png`: generated from remaining P9 phase matrix; phase is wrapped, not displacement.
- `07-candidates/patch-candidate-count.png`, `ps-candidate-spatial-map.png`: candidate rows/coordinates; not final PS displacement.
- `07-candidates/patch-boundaries.png`: conceptual overlap illustration.
- `09-stamps-step1-2/*`: existing P9 output figures; titles/quantity labels checked against current captions. `step2-coherence-histogram.png` is named misleadingly; it plots gamma and should be referred to as gamma histogram.
- `10-storage/wsl-storage-architecture.png`: conceptual storage relationship.

## Scientific and editorial boundaries

- A single ascending orbit gives LOS observations; do not label them vertical displacement without additional geometry and method.
- Wrapped interferometric phase is bounded modulo 2π and includes non-deformation terms.
- Gamma, `coh_ps`, `K_ps`, candidate counts, selected counts, and LOS time series are distinct quantities/stages.
- P9 is outside most of the recorded AOI; label it diagnostic only.
- Do not publish personal user/device paths. Generalize paths in examples.
- Do not claim Step 3 is complete for all 20 patches or a final deformation product exists.
- Keep #3 and #5 as drafts until primary project run artifacts are available.

## Primary references added to public articles

- Sentinel-1 Product Definition: https://sentiwiki.copernicus.eu/__attachments/1673968/S1-RS-MDA-52-7440-Sentinel-1-Product-Definition-2025-2.8.pdf
- ESA SNAP Back-Geocoding operator documentation: https://step.esa.int/main/wp-content/help/versions/13.0.0/snap-toolboxes/eu.esa.microwavetbx.sar.op.sentinel1.ui/operators/BackGeocodingOp.html
- Hooper et al. (2007), StaMPS method: https://doi.org/10.1029/2006JB004763
- Hooper et al. (2004), InSAR phase terms: https://doi.org/10.1029/2004GL021737
