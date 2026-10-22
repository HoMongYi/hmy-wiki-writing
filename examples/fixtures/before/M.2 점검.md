---
title: M.2 점검
aliases: [M.2 장착 점검]
tags: [hardware, storage, procedure]
type: procedure
sources: [https://www.kingston.com/en/ssd/ssd-faq]
custom_field:
  preserve: true
---
# M.2 점검

M.2 슬롯은 제품에 따라 SATA 또는 PCIe 연결을 지원한다. SSD의 크기와 키 홈이 맞더라도 메인보드가 해당 연결 방식을 지원해야 사용할 수 있다.

장착 전에는 전원을 끄고 외부 전원을 분리한다. 배터리가 있는 시스템은 해당 모델의 분리 절차를 따른다. 기존 데이터가 있는 SSD는 초기화하거나 포맷하지 않는다.

## 연결 경로

연결 방식의 확인을 위해서는 메인보드 매뉴얼에서 해당 슬롯의 사양을 조회하는 것이 필요하다. 다른 슬롯이나 SATA 포트와 연결 자원을 공유하는 구성에서는 사용 조합에 따라 일부 포트가 비활성화될 수 있다.

[[PCI Express#CPU 직결과 칩셋 경유]]의 경로 설명과 [[M.2]]의 호환 조건을 함께 볼 수 있다.[^scope]

![CPU 직결과 칩셋 경유의 개념도](../_assets/data-path.svg)

[^scope]: 모양이 같은 슬롯이라도 실제 배선과 공유 조건은 보드별로 다르다.

## 참고 링크

- [Kingston M.2 SSD FAQ](https://www.kingston.com/en/ssd/ssd-faq)
