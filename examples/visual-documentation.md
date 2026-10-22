# 시각적 설명의 독립 예시

아래 문서는 기술 설명에 맞춰 서로 다른 형식을 선택한다. 운영 Vault의 원문을 복사하지 않았고 특정 제품의 실측값을 만들지 않았다. 사용 전에 대상 HMY의 실제 지원을 확인한다.

| 문서 | 설명 방식 | 이유 |
| --- | --- | --- |
| [메인보드 데이터 경로](fixtures/vault/01_하드웨어/메인보드%20데이터%20경로.md) | 본문 + 관계형 diagram | CPU 직결·칩셋 공유의 경로를 선택해서 연결 |
| [PCIe 대역폭 비교](fixtures/vault/01_하드웨어/PCIe%20대역폭%20비교.md) | 부호화 표 + spec.plot | 조건과 계산값을 구분하고 세대별 차이 표시 |
| [DDR CAS 지연시간](fixtures/vault/01_하드웨어/DDR%20CAS%20지연시간.md) | 공식·기본 계산 + explorer | 입력을 바꾸어 CL·전송률의 관계 탐색 |
| [CPU 캐시 계층](fixtures/vault/01_하드웨어/CPU%20캐시%20계층.md) | 계층 diagram + 공유 범위 설명 | 논리적 계층과 물리 구조·제품별 차이 구분 |
| [SSD 인식 불량](fixtures/vault/01_하드웨어/SSD%20인식%20불량.md) | 진단 + choices/detail/action | 인식 단계와 실제 연결 경로에 따라 점검 |

[블록 표본](hmy-blocks.md)에는 신호 개념도, 이미지 비교와 PCIe 입력 탐색도 있다. 표본은 문법·조작 확인용이며 모든 문서에 이 UI를 추가하라는 템플릿이 아니다. [NVMe 개선본](deep-improvement.md)과 [Light Edit](light-edit.md)는 핵심 공백이 시각화가 아니어서 기존 형식을 유지한다.

스킬은 지원되지 않는 기능을 구현하지 않는다. older HMY에서 diagram/explorer를 읽지 못하면 관계 목록·Mermaid·공식·정적 표로 같은 내용을 전달한다. 계산기 입력 허용 범위는 하드웨어 호환성 보장이 아니다. [검증 기록](../evals/visual-results.md)은 native/Quartz/Obsidian 앱을 구분한다.
