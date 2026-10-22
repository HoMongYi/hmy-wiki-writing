---
title: NVMe
aliases: [NVM Express]
tags: [hardware, storage]
sources: [https://nvmexpress.org/specifications/]
---
# NVMe

NVMe는 호스트 소프트웨어가 비휘발성 저장장치와 통신하는 방식을 정의한다. PC의 PCIe SSD에서는 운영체제의 드라이버와 SSD 컨트롤러가 명령과 완료 정보를 교환한다.

M.2는 모듈의 형태와 연결 규격을 다루며 NVMe와 같은 뜻이 아니다. [[PCI Express]]와 [[M.2]]는 서로 다른 층위의 규격이다.

## 호스트에서 컨트롤러까지

호스트는 SSD를 사용하는 시스템 쪽이고, 컨트롤러는 저장장치의 명령을 처리하는 쪽이다. 응용 프로그램의 파일 요청은 운영체제의 저장장치 계층을 거쳐 장치 명령으로 전달된다. NVMe는 이 경계에서 명령과 상태를 주고받는 규칙을 제공한다. 파일 이름이나 디렉터리 구조 자체를 SSD의 명령 큐에 그대로 보내는 것은 아니다.

## 제출 큐와 완료 큐

PCIe NVMe의 기본 동작에서 호스트 소프트웨어는 제출 큐에 명령을 기록한다. 컨트롤러는 명령을 가져와 처리하고 완료 큐에 상태를 남긴다. 호스트가 큐의 새 항목을 알리는 doorbell과 큐의 순환 구조는 요청마다 소프트웨어와 장치가 같은 자리를 덮어쓰지 않도록 역할을 나눈다. 이 기본 구조는 NVM Express 1.0e의 Theory of Operation에 설명돼 있다.

큐 항목의 순서와 실제 명령 완료 순서는 같지 않을 수 있다. 호스트는 완료 항목의 제출 큐 식별자와 명령 식별자를 통해 어떤 요청의 결과인지 찾는다. 완료 큐는 파일 데이터 자체가 아니라 명령의 완료 정보를 전달한다. 이 구분은 장치가 인식되는 것, 명령이 완료되는 것, 파일을 정상적으로 읽는 것이 서로 다른 관찰인 이유를 보여 준다.

## PCIe와 M.2가 맡는 부분

NVMe는 저장장치 명령의 의미를, PCIe는 호스트와 컨트롤러 사이의 전송 경로를 맡는다. PCIe 세대와 레인 폭은 그 경로의 조건이다. 같은 NVMe 장치라도 연결 경로와 작업 조건이 다르면 실제 처리량은 달라지므로 규격 이름만으로 측정 성능을 알 수는 없다.

M.2 모듈을 선택할 때에는 길이·키 홈과 함께 슬롯이 지원하는 SATA/PCIe 연결을 본다. 물리적으로 들어간다는 사실만으로 통신 방식까지 맞는 것은 아니다. 여러 저장장치의 조합은 보드의 공유 자원에도 영향을 받을 수 있다. 구체적인 배선은 [[PCI Express#CPU 직결과 칩셋 경유]]에서 설명한다.

NVMe 전체가 M.2나 PC 내부 PCIe SSD에 한정되는 것은 아니다. 규격군에는 다른 전송 방식도 있으므로 이 문서의 큐·연결 설명은 PC 내부 PCIe SSD의 기본 동작 범위로 읽는다.

## 참고 링크

- [NVM Express 규격](https://nvmexpress.org/specifications/)
- [NVM Express 1.0e, 1.4 Theory of Operation — 기본 큐 구조의 역사적 규격](https://nvmexpress.org/wp-content/uploads/2013/04/NVM_10e_specification.pdf)
- [Microsoft NVME_COMPLETION_ENTRY — 완료 항목과 명령 식별](https://learn.microsoft.com/en-us/windows/win32/api/nvme/ns-nvme-nvme_completion_entry)
- [Kingston M.2 SSD FAQ](https://www.kingston.com/en/ssd/ssd-faq)
