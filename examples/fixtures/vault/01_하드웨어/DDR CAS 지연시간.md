---
title: DDR CAS 지연시간
type: technology
tags: [hardware, memory, latency]
---
# DDR CAS 지연시간

[[메모리 타이밍#CAS Latency|CAS Latency]]는 읽기 명령 뒤 데이터가 나오기까지의 CAS 구간을 클럭 주기 수로 나타낸다. CL이 같아도 동작 클럭이 다르면 실제 시간은 달라진다. DDR 전송률은 MT/s이며 대응 클럭은 전송률의 절반에 해당하는 MHz로 구분한다.

전송률을 R MT/s라고 하면 대응 클럭은 R/2 MHz다. 따라서 한 주기의 시간은 2000/R ns이고, CAS 구간은 `CL × 2000 ÷ R` ns다. 예를 들어 6000 MT/s·CL30은 `30 × 2000 ÷ 6000 = 10 ns`다. 5600 MT/s·CL40은 약 14.29 ns다. 모두 입력을 가정한 계산 예다.

```hmy-explorer
kind: ddr-cas
title: 전송률과 CL의 관계
description: 전송률과 CL을 바꾸어 이론 CAS 구간을 비교한다. 전체 메모리 접근 지연이나 제품 실측이 아니다.
baseline: {dataRate: 6000, cl: 30}
source: https://www.kingston.com/en/blog/gaming/cas-latency-cl-ram-timing-explained
```

행 활성화·프리차지, 컨트롤러의 처리와 대기열 등 다른 조건은 이 계산에 포함되지 않는다. 낮은 CAS 계산값을 모든 프로그램의 성능 순위로 바꿀 수 없다. 입력할 수 있다는 사실이 해당 CPU·보드·메모리에서 그 설정을 지원하거나 안정적으로 동작한다는 뜻도 아니다.

[[Memory Training|메모리 트레이닝]]과 QVL·UEFI 설정은 실제 구성에서 별도로 확인한다. 계산 모델은 전압 설정이나 오버클럭 절차를 제시하지 않는다.

## 참고 링크

- [Kingston, CAS Latency와 전송률을 이용한 계산](https://www.kingston.com/en/blog/gaming/cas-latency-cl-ram-timing-explained)
