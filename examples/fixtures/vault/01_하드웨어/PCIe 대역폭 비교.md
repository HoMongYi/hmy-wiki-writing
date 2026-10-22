---
title: PCIe 대역폭 비교
type: technology
tags: [hardware, pcie, bandwidth]
---
# PCIe 대역폭 비교

[[PCI Express]] 링크의 이론 전송량은 세대별 전송률과 실제 Lane 수를 함께 사용해 계산한다. GT/s는 전송률이고 GB/s는 바이트 단위 대역폭이다. 편도 값과 송수신 양방향 합계를 섞으면 같은 링크의 숫자도 두 배 차이로 보일 수 있다.

## 계산 조건

아래 비교는 모든 세대의 Lane 수를 ×4로 고정한다. 부호화에 쓰이는 비율만 반영하며 패킷 헤더·흐름 제어 등의 부하, 장치 처리 성능과 공유 업링크는 제외한다. GB는 십진 10억 바이트다.

| 세대 | Lane당 전송률 | 부호화 효율 |
| --- | --- | --- |
| Gen1 | 2.5 GT/s | 8/10 |
| Gen2 | 5 GT/s | 8/10 |
| Gen3 | 8 GT/s | 128/130 |
| Gen4 | 16 GT/s | 128/130 |
| Gen5 | 32 GT/s | 128/130 |

`편도 GB/s = 전송률(GT/s) × 부호화 효율 × Lane 수 ÷ 8`이다. Gen4 ×4는 `16 × 128/130 × 4 ÷ 8 ≈ 7.88 GB/s`가 된다. 막대의 값은 이 공식을 소수 둘째 자리로 반올림한 계산값이며 제품 실측이 아니다.

```hmy-spec
type: comparison
plot:
  unit: GB/s
  context: PCIe ×4 · 편도 · 부호화만 반영한 십진 이론 대역폭 · 프로토콜 부하 제외 · 실측 아님
  max: 16
  source: https://edc.intel.com/content/www/us/en/design/products/platforms/details/raptor-lake-s/13th-generation-core-processors-datasheet-volume-1-of-2/002/pci-express-architecture/
groups:
  - label: Lane 수를 ×4로 고정한 세대별 계산
    items:
      - {label: Gen1, value: '1.00'}
      - {label: Gen2, value: '2.00'}
      - {label: Gen3, value: '3.94'}
      - {label: Gen4, value: '7.88'}
      - {label: Gen5, value: '15.75'}
```

이 비교는 어떤 SSD가 실제로 이 속도에 도달한다는 뜻이 아니다. 제품의 최대 지원과 연결 시 협상된 세대·전기적 폭도 다를 수 있다. [[메인보드 데이터 경로]]의 공유 조건을 함께 읽는다. Gen6 이상은 FLIT·FEC 등의 전송 모델이 달라 이 표의 공식을 그대로 연장하지 않는다.

## 참고 링크

- [Intel 13세대 Core 데이터시트 002, PCI Express Architecture](https://edc.intel.com/content/www/us/en/design/products/platforms/details/raptor-lake-s/13th-generation-core-processors-datasheet-volume-1-of-2/002/pci-express-architecture/)
- [Microchip, PCIe 세대별 전송률과 방향 구분](https://www.microchip.com/en-us/solutions/data-centers-and-computing/data-center-solutions/technologies/pci-express-technology)
- [Intel 200·Z370 PCH 데이터시트, 부호화와 이론 대역폭 계산](https://www.intel.com.tw/content/dam/www/public/us/en/documents/datasheets/200-series-chipset-pch-datasheet-vol-1.pdf)
