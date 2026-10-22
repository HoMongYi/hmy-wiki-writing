---
title: CPU 캐시 계층
type: technology
tags: [hardware, cpu, cache]
---
# CPU 캐시 계층

CPU 캐시는 반복해서 사용하는 코드와 데이터를 코어 가까이에 보관해 더 먼 메모리까지 접근하는 일을 줄인다. L1·L2·L3라는 이름은 논리적 계층을 나타내며 용량·지연·공유 범위는 마이크로아키텍처에 따라 다르다.

```hmy-diagram
title: 코어와 메모리 사이의 논리적 계층
description: 여러 단계의 캐시가 있는 CPU를 단순화한 개념도다. 실물 배치·용량·실측 지연을 표시하지 않으며 모든 요청이 매번 각 계층을 순서대로 통과한다는 뜻은 아니다.
layout: layers
nodes:
  - {id: core, label: CPU 코어, detail: 필요한 명령과 데이터에 접근한다.}
  - {id: l1, label: L1, detail: 코어 가까이의 캐시이며 명령·데이터 분리 등 실제 구성은 제품별로 다르다.}
  - {id: l2, label: L2, detail: 코어별 전용인 제품과 코어 묶음이 공유하는 제품이 있다.}
  - {id: llc, label: L3 또는 마지막 캐시, detail: 존재 여부와 공유 범위·포함 정책은 제품별로 다르다.}
  - {id: dram, label: 주 메모리, detail: 컨트롤러와 메모리 채널을 통해 접근한다.}
edges:
  - {from: core, to: l1, label: 가까운 캐시 접근}
  - {from: l1, to: l2, label: 하위 계층의 데이터가 필요할 수 있음}
  - {from: l2, to: llc, label: 더 먼 캐시 계층}
  - {from: llc, to: dram, label: 캐시에 없는 데이터의 메모리 경로}
source: https://www.intel.com/content/www/us/en/support/articles/000027820/processors/intel-xeon-processors.html
```

한 코어 전용인 캐시는 같은 코어의 접근 특성과 연결되고, 여러 코어가 공유하는 캐시는 다른 코어의 부하와 일관성 유지 조건도 영향을 받는다. L2가 항상 코어별 전용인 것은 아니다. Intel의 E-core 기술 자료에는 여러 코어가 L2를 공유하는 구성이 설명되어 있다. 그림 하나의 공유 관계를 모든 CPU에 적용할 수 없는 이유다.

캐시 적중·미스, 프리페치, 다른 코어가 가진 데이터, 메모리 컨트롤러 상태에 따라 실제 요청 경로가 달라진다. 포함형·비포함형 같은 정책도 계층 이름만으로 정해지지 않는다. 캐시 용량만으로 프로그램 성능이나 전체 접근 지연을 계산할 수 없다.

DRAM 쪽 지연의 한 부분은 [[DDR CAS 지연시간]]에서 다룬다. 캐시와 CPU 내부 연결을 실제 제품에 적용할 때에는 해당 마이크로아키텍처의 자료를 함께 읽는다.

## 참고 링크

- [Intel, Xeon 계열의 캐시 계층과 정책 차이](https://www.intel.com/content/www/us/en/support/articles/000027820/processors/intel-xeon-processors.html)
- [Intel, E-core의 L1과 공유 L2 구조](https://intel.github.io/optimization-zone/hardware/HWPrefetchTuning/)
