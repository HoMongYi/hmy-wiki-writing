---
title: SSD 인식 불량
type: diagnosis
tags: [hardware, storage, diagnosis]
---
# SSD 인식 불량

SSD가 탐색기에 보이지 않는 현상은 장치 연결, 운영체제의 디스크 인식, 볼륨 연결 중 어느 단계에서든 나타날 수 있다. 탐색기는 사용할 수 있는 볼륨을 보여 주므로 여기서 보이지 않는다는 사실만으로 SSD 고장을 확정할 수는 없다.

## 먼저 구분할 연결과 데이터

SATA 케이블을 쓰는 SSD, M.2 SATA, PCIe NVMe, USB 외장 케이스는 확인할 경로가 다르다. [[M.2]]와 [[NVMe]]는 같은 뜻이 아니다. 외장 케이스는 안쪽 SSD와 바깥 USB 연결 사이에 브리지가 있고, RAID/VMD 구성은 컨트롤러의 별도 화면과 드라이버를 거칠 수 있다.

기존 데이터가 있으면 초기화·포맷·새 볼륨 생성을 진행하지 않는다. 디스크 관리에서 초기화를 요청하거나 RAW로 보이더라도 현재 상태를 기록하고 쓰기 작업을 멈춘다. 데이터를 보존해야 할 상황의 우선순위는 새 저장 공간을 만드는 작업과 다르다.

## 인식 단계별 확인

펌웨어의 부팅 목록은 모든 저장장치 목록과 같지 않다. 모델 매뉴얼에서 SATA·NVMe·RAID 등 해당 연결의 확인 위치를 찾아야 한다. USB 장치나 별도 컨트롤러는 일반 NVMe 화면에 보이지 않을 수 있다.

Windows에서는 장치 관리자와 디스크 관리를 따로 확인한다. 컨트롤러가 열거됐다는 사실과 그 아래 SSD가 디스크로 등록됐다는 사실도 구분한다. 디스크 관리에 기존 볼륨이 있으나 탐색기에 없다면 드라이브 문자와 파일 시스템 상태가 단서가 된다.

```hmy-diagnosis
steps:
  - id: connection
    title: 실제 연결 방식과 기존 데이터 유무를 확인했는가
    yes: disk
    no: identify
  - id: identify
    title: 모델과 SATA·PCIe·USB·컨트롤러 경로를 확인하고 쓰기 작업은 보류
  - id: disk
    title: 디스크 관리에 해당 SSD가 디스크로 표시되는가
    yes: volume
    no: enumeration
  - id: volume
    title: 기존 볼륨과 드라이브 문자·파일 시스템 상태를 기록하고 초기화·포맷 금지
  - id: enumeration
    title: 실제 연결 경로에 맞는 확인 위치를 선택한다
    detail: '[[M.2]]라는 형태만으로 SATA와 PCIe를 구별할 수 없다. 장치 관리자의 컨트롤러와 디스크도 별개다.'
    choices:
      - {label: SATA 연결, target: sata}
      - {label: PCIe NVMe 연결, target: nvme}
      - {label: USB 브리지, target: usb}
      - {label: RAID 또는 VMD, target: controller}
  - id: sata
    title: SATA 데이터·전원 경로와 해당 포트의 공유 조건 확인
    action: 전원과 외부 전원을 분리하고 모델별 절차에 따라 케이블·포트를 한 변수씩 확인한다. 기존 데이터의 초기화·포맷은 진행하지 않는다.
  - id: nvme
    title: PCIe 슬롯 지원과 펌웨어의 장치 목록 확인
    action: 모델 매뉴얼에서 실제 슬롯의 프로토콜·공유 조건을 확인한다. 재장착 전에 전원과 외부 전원을 분리하고 배터리 모델은 전용 절차를 따른다.
  - id: usb
    title: USB 브리지와 디스크의 인식을 구분
    action: 호환되는 케이블·포트·외장 케이스를 한 변수씩 비교하고 디스크 상태를 기록한다. 초기화·포맷을 요구하면 중단한다.
  - id: controller
    title: 해당 RAID·VMD 컨트롤러의 디스크와 논리 볼륨 확인
    action: 공식 매뉴얼에서 확인 위치와 모델에 맞는 드라이버를 찾는다. 데이터 보존 절차 없이 컨트롤러 모드 변경·새 배열 생성·초기화·재구축을 실행하지 않는다.
```

## 교차 시험과 다음 조치

장치가 연결 경로에서 보이지 않을 때에는 해당 모델 매뉴얼에 따라 포트·케이블·장착 조건을 확인한다. 부품을 다시 장착하기 전에는 전원을 끄고 외부 전원을 분리하며 배터리가 있는 시스템은 모델별 절차를 따른다. 호환성이 확인된 다른 케이블이나 슬롯으로 한 변수씩 바꾸면 장치와 경로 문제를 구분하는 데 도움이 된다.

디스크가 다시 보이면 중요한 데이터를 먼저 보존한다. 한 번 인식됐다는 사실만으로 장시간 안정성까지 확인된 것은 아니다. 인식이 반복해서 끊기거나 데이터 접근이 불안정하면 반복 쓰기·복구 명령보다 데이터 보존과 전문 복구 가능성을 먼저 검토한다.

## 참고 링크

- [Microsoft, 디스크 관리 문제 해결](https://learn.microsoft.com/en-us/troubleshoot/windows-server/backup-and-storage/troubleshoot-disk-management)
- [Kingston, M.2 연결 방식과 슬롯 호환](https://www.kingston.com/en/ssd/ssd-faq)
