# HMY Block과 설명 형식 선택

아래 예시는 공통 parser·renderer와 Obsidian 저장 검증에 입력하는 독립 표본이다. 전체 schema가 아니며 현재 프로젝트의 canonical 문법을 먼저 읽는다.

## 항목 비교: hmy-spec

```hmy-spec
type: comparison
groups:
  - label: M.2
    items:
      - {label: 역할, value: 모듈 형태와 커넥터 구성}
      - {label: 확인할 조건, value: 슬롯과 모듈의 연결 규격}
      - {label: 설명 성격, value: 규격의 범위}
  - label: NVMe
    items:
      - {label: 역할, value: 호스트와 저장장치의 명령 규격}
      - {label: 확인할 조건, value: 장치와 호스트가 지원하는 전송}
      - {label: 설명 성격, value: 규격의 범위}
```

[고도화 예시](deep-improvement.md)는 같은 비교를 본문에서 이미 설명하므로 블록을 추가하지 않았다.

## 순서: hmy-guide

```hmy-guide
title: 기존 SSD의 상태 기록
version: Windows
steps:
  - title: 연결 방식 확인
    detail: SATA·PCIe·USB와 별도 컨트롤러 경로를 구분한다.
  - title: 장치와 디스크 상태 기록
    detail: 장치 관리자와 디스크 관리를 확인하되 기존 데이터의 초기화·포맷은 진행하지 않는다.
```

버전 표시는 문서 전환 기능이 아니다. 실제 분기는 [진단 예시](troubleshooting.md)의 hmy-diagnosis를 사용한다.

## 계산 결과: hmy-result

6000 MT/s와 CL30을 입력해 30 × 2000 ÷ 6000을 실제 계산한 값은 10.0 ns다. 아래 결과는 그 계산의 해석이며 메모리 제품이나 시스템의 실측 결과가 아니다.

```hmy-result
normal:
  - 입력한 전송률·CL로 계산한 CAS 구간은 10 ns다.
warning:
  - 시스템 전체 접근 지연과 장시간 안정성은 측정하지 않았다.
```

실제 시험을 하지 않은 [SSD 진단](troubleshooting.md)에는 결과 블록을 채우지 않았다.

## 사건과 연표

hmy-timeline은 [x86 역사](fixtures/vault/01_하드웨어/x86의%20역사.md), hmy-company-event는 [AMD](fixtures/vault/01_하드웨어/AMD.md)의 전체 YAML에서 확인할 수 있다. 날짜와 인수 관계는 각 문서의 공식 자료에 연결된다.

## 단일 이미지: hmy-media

다음 src는 fixture Vault 루트 기준이다. 자체 제작 개념도이며 특정 보드의 핀 배열·레인 수를 나타내지 않는다.

```hmy-media
src: _assets/data-path.svg
caption: CPU 직결과 칩셋 경유를 구분한 개념도
alt: CPU에서 장치로 직접 가는 경로와 칩셋을 거치는 경로
source: HMY Wiki Writing 자체 제작
license: MIT
```

경로 허용만으로 파일 존재와 권리를 확인한 것은 아니다. 단일 이미지와 지원되는 이미지 비교는 동영상·오디오·외부 임베드와 구분한다.

## 신호의 개념 순서

아래는 ATX PS_ON#과 PWR_OK의 의미를 설명하는 단순화다. PS_ON#이 active-low인 점과 주 출력의 안정 이후 상태를 구분하며, 단계 폭은 시간·전압 눈금이 아니다. PSU를 열거나 핀을 연결해 시험하는 절차가 아니다.

```hmy-signal
mode: conceptual
title: 주 출력 요청과 안정 표시
description: 신호의 개념적 상태만 표시한다. 단계 간격은 실제 지연시간이 아니며 전압 파형이나 부품 정상 판정이 아니다.
phases: [대기, 주 출력 요청, 출력 안정]
channels:
  - {name: PS_ON#, kind: logic, states: [high, low, low]}
  - {name: 주 출력, kind: rail, states: [low, unknown, high]}
  - {name: PWR_OK, kind: logic, states: [low, low, high]}
notes:
  - {phase: 3, text: PWR_OK는 출력 조건의 상태이며 CPU나 DRAM 불량 판정이 아니다.}
source: https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/2.0/2.1a/ps-on-required/
```

- [Intel, PS_ON# 의미](https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/2.0/2.1a/ps-on-required/)
- [Intel, PWR_OK 의미](https://edc.intel.com/content/www/us/en/design/ipla/software-development-platforms/client/platforms/alder-lake-desktop/atx-version-3-0-multi-rail-desktop-platform-power-supply-design-guide/2.0/2.1a/pwr-ok-required/)

## 같은 크기의 개념도 비교

두 SVG는 자체 제작 MIT 자산이다. 같은 장면의 전후 사진이 아니라 서로 다른 논리 경로를 비교한다. 양쪽 원본·권리가 정적 상태에 남고, 슬라이더는 실제 이미지 조건을 충족할 때만 활성화된다.

```hmy-media
src: _assets/cpu-direct.svg
alt: CPU에서 장치로 직접 이어지는 개념적 연결
label: CPU 직결
caption: 특정 제품의 물리 배선이나 실측 성능이 아니다.
source: HMY Wiki Writing 자체 제작
license: MIT
compare:
  src: _assets/chipset-shared.svg
  alt: CPU에서 칩셋을 거쳐 장치로 이어지는 개념적 연결
  label: 칩셋 경유
  caption: 같은 업링크를 사용하는 장치가 있을 수 있다.
  source: HMY Wiki Writing 자체 제작
  license: MIT
```

## 입력으로 바꾸는 PCIe 계산

기본 조건은 Gen4 ×4다. 부호화만 반영한 편도 십진 이론값은 약 7.88 GB/s이며 실제 전송 성능이 아니다. 정적 비교와 기술 설명은 [PCIe 비교 문서](fixtures/vault/01_하드웨어/PCIe%20대역폭%20비교.md)에 있다.

```hmy-explorer
kind: pcie-bandwidth
title: 세대와 Lane 수의 관계
description: PCIe 1~5세대의 편도 이론값을 비교한다. 프로토콜 부하와 장치 성능·공유 업링크는 제외하며 Gen6 이상에는 적용하지 않는다.
baseline: {generation: 4, lanes: 4}
source: https://edc.intel.com/content/www/us/en/design/products/platforms/details/raptor-lake-s/13th-generation-core-processors-datasheet-volume-1-of-2/002/pci-express-architecture/
```

관계·계층 diagram은 [메인보드 경로](fixtures/vault/01_하드웨어/메인보드%20데이터%20경로.md)와 [캐시 계층](fixtures/vault/01_하드웨어/CPU%20캐시%20계층.md), CAS explorer는 [DDR 계산](fixtures/vault/01_하드웨어/DDR%20CAS%20지연시간.md), choices는 [SSD 진단](fixtures/vault/01_하드웨어/SSD%20인식%20불량.md)에 있다. 설치 프로젝트가 해당 문법을 지원하지 않으면 정적 표·관계 목록·공식으로 설명한다.
