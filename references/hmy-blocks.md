# HMY Block 선택과 검증

정본은 사용 프로젝트의 docs/HMY_BLOCKS.md, docs/architecture/visual-blocks.md와 packages/hmy-wiki-core다. types/structured/blocks/render와 visual·intelligent 관련 모듈, 실제 Obsidian editing/validation을 확인한다. 이 패키지는 schema/parser를 복제하지 않는다.

| 블록 | 적절한 정보 |
| --- | --- |
| hmy-spec | 구조화된 항목·그룹, comparison, 근거 데이터의 plot |
| hmy-guide | 실제 순서가 있는 절차. 진행 UI는 설치된 enhancer 확인 |
| hmy-diagnosis | 관찰별 분기·점검·후속 조치 |
| hmy-result | 실제 관찰 또는 명시한 계산 결과의 해석 |
| hmy-timeline | 검증된 사건의 시간 관계 |
| hmy-company-event | 인수·합병·분사 등 관계 변화 |
| hmy-media | 단일 이미지·설명, 지원 시 compare |
| hmy-signal | 실측이 아닌 논리 신호·전원 순서 개념도 |
| hmy-diagram | 지원 구현에서 요소·관계·경로의 탐색 |
| hmy-explorer | 지원 구현에서 DDR CAS·PCIe 이론 대역폭 입력 탐색 |

이 목록을 모든 설치 버전의 지원 보장으로 읽지 않는다. HMY_BLOCK_LANGUAGES와 parse/serialize/render, 플러그인 저장, enhancer를 확인하고 사용할 블록만 검증한다. 신규 로컬 기능은 원격 main이나 운영 사이트에 없을 수 있다. [구현별 검증 기록](../evals/visual-results.md)을 확인한다.

새 블록은 canonical YAML, legacy pipe/DSL은 기존 원문 호환용이다. 시작 키로 구조화 YAML을 구분하며 깨진 YAML을 legacy로 우회하지 않는다. 문서와 코드가 다르면 실제 동작하는 형식을 확인하고 차이는 내부 보고에 남긴다.

- spec의 type은 사양 분류다. 문서 type과 구분하고 임의 title·description을 붙이지 않는다. plot의 숫자·단위·조건·근거는 [수치 설명](data-visualization.md)을 따른다.
- guide는 steps가 필요하다. version과 meta를 함께 쓰지 않는다. 순서와 번호는 실제 모델을 따른다.
- diagnosis의 yes/no 또는 choices.target은 실제 고유 ID를 가리킨다. detail/action/choices 같은 확장 필드와 순환·대상 검증을 확인한다. parser 통과만으로 저장이나 클릭 동작을 보장하지 않는다.
- result를 채우기 위해 가상의 시험을 만들지 않는다. 계산 결과는 입력·공식과 계산 범위를 밝힌다.
- signal은 conceptual·phases·channels·source를 실제 계약에 맞춘다. 시간·전압 파형·오실로스코프 데이터로 소개하지 않는다.
- diagram의 노드와 연결 대상, explorer의 kind·baseline·허용값은 실제 모델을 읽는다. 범용 chart·calculator·compatibility 블록을 새로 만들어내지 않는다.
- media의 compare에는 양쪽 alt·출처·권리와 비교 조건을 확인한다. 경로 허용은 파일 존재·재사용권 확인이 아니다. 동영상·오디오·외부 임베드와 구분한다.
- Wikilink는 해당 필드와 플랫폼의 resolver를 실제 확인한다. unresolved 링크를 가짜 URL로 만들거나 본문의 필요한 참고 링크를 제거하지 않는다.
- Markdown heading과 실제 블록 제목을 연속 중복하지 않는다. 본문은 원리·조건, 블록은 구조·탐색을 맡는다.

[블록 예시](../examples/hmy-blocks.md)는 독립 fixture다. 사용 이유와 정적 대체는 [설명 형식](visual-explanations.md), 조작과 플랫폼 경계는 [인터랙티브 설명](interactive-documentation.md)에서 확인한다.
