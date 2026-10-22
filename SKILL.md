---
name: hmy-wiki-writing
description: HMY Wiki의 PC 하드웨어 문서를 새로 쓰거나 문장 교정, 전면 고도화, 기술 최신화, 지식 연결 및 품질 감사를 수행할 때 사용한다. Obsidian과 Quartz 5가 공유하는 Markdown, Frontmatter, Wikilink와 HMY Block을 보존하며 기술 원리·규격·진단·기업·역사를 설명하고 실제 지원되는 도식·수치 비교·인터랙티브 설명을 선택한다. 위키 엔진이나 플러그인 개발에는 적용하지 않는다.
license: MIT
---

# HMY Wiki Writing

독자가 기술을 이해하고 관련 지식을 찾아 실제 PC 환경에 적용할 수 있는 문서를 만든다. 좋은 기존 문장은 유지한다. 길이·수정량·블록 수는 품질 지표가 아니다.

## 시작과 범위

지정 프로젝트의 실제 루트와 가까운 AGENTS.md를 확인한다. monorepo 루트와 Obsidian의 vault/는 다르다. [프로젝트 연결](references/obsidian-quartz.md)에서 공개 범위와 실제 검사 도구를 확인한다. 이미 조사한 유효한 결과는 재사용한다.

docs/HMY_WIKI_AUTHORING.md와 docs/HMY_CONTENT_POLICY.md를 적용하되 사용자 요청의 범위와 권한을 우선한다. 스킬 호출 자체는 전체 원본 수정이나 운영 게시 승인이 아니다. 기존 승인으로 충분한 작업은 다시 묻지 않는다. 프로젝트에 접근하지 못하면 제공 원문으로 초안을 작성하고 통합 검증 한계를 보고한다.

## 편집 모드

| 모드 | 결과 |
| --- | --- |
| New Writing | 파일명·title·aliases·본문을 검색한 뒤 독립 가치가 있는 문서를 작성한다. |
| Light Edit | 요청한 문장·문단만 고친다. 별도 보고를 요청한 오류는 본문에서도 삭제·수정하지 않는다. 새 제목·섹션·메타데이터를 추가하지 않는다. |
| Rewrite | 유효한 사실·조건을 보존하며 설명 순서·문단·표를 재구성한다. |
| Deep Improvement | 근거 조사, 원리·관계·실사용 설명 확장과 구조 재설계를 수행한다. |
| Review Only | 원본을 수정하지 않고 위치·근거·영향·권장 변경을 보고한다. |
| Refresh | 변경된 주장과 적용 시점을 갱신하고 역사적 사실을 보존한다. |

## 필요한 참조 선택

문장 교정은 [한국어 설명](references/writing-style.md)과 [보존](references/frontmatter.md)으로 시작한다. 다른 자료는 해당 작업에 필요할 때만 읽는다.

| 작업 | 자료 |
| --- | --- |
| 새 글·구성 | [유형](references/document-types.md), [지식 구조](references/knowledge-architecture.md) |
| 주장·수치·규격·호환성 | [근거](references/technical-accuracy.md), [하드웨어 규격](references/hardware-specifications.md) |
| 링크·별칭·섹션·각주 | [Wikilink와 백링크](references/wikilinks-backlinks.md) |
| HMY Block | 프로젝트 docs/HMY_BLOCKS.md → [선택과 검증](references/hmy-blocks.md) |
| 장애 진단 | [진단](references/troubleshooting.md) |
| 기업·역사·생태계 | [기업과 역사](references/companies-history.md) |
| 설명 방식·구조·데이터 경로 | [형식 선택](references/visual-explanations.md), [Visual Documentation](workflows/visual-documentation.md) |
| 숫자·차트·계산 | [수치 시각화](references/data-visualization.md) |
| 입력 탐색·선택형 진단 | [인터랙티브 설명](references/interactive-documentation.md) |
| 이미지·비교·권리 | [시각 자료](references/media.md) |
| 최종 검토·Review Only | [검토](references/review-checklist.md) |

반복 작업은 목적에 맞는 workflow 하나를 선택한다: [Knowledge Audit](workflows/knowledge-audit.md), [Topic Deepening](workflows/topic-deepening.md), [Knowledge Linking](workflows/knowledge-linking.md), [Technical Refresh](workflows/technical-refresh.md), [Repository-wide Improvement](workflows/repository-improvement.md). workflow는 새 공개 권한을 추가하지 않는다.

## 작성과 확인

1. 대상 전체와 관련 허브를 읽고 경로·메타데이터·참조·블록·핵심 사실·안전 조건을 보존 목록에 잡는다.
2. 기존 설명과 공백을 구분한다. 기존 링크 보존과 링크 유효성은 별도 검사다. 깨진 링크는 같은 개념의 실제 대상을 확인해 허용 범위에서 수정하거나 별도 보고한다.
3. 필요한 주장만 근거로 확인한다. 원리→현상→조건이 이어지는 설명을 쓰고, 핵심 설명을 링크나 블록으로 대체하지 않는다.
4. New Writing·Rewrite·Deep Improvement·Review Only·Refresh에서는 텍스트만으로 충분한지, 연결 관계·수치 비교·입력 변화·단계·진단 분기 중 무엇이 이해를 돕는지 선택한다. Light Edit에는 시각화 추가나 제안을 자동으로 붙이지 않는다. 기존 자산과 실제 schema·renderer·enhancer·Obsidian 지원을 확인하고 canonical Markdown으로 작성한다. 계획 문서만 있는 기능·미지원 필드·임의 JavaScript를 생성하지 않는다. 이 패키지에는 HMY parser/schema를 복제하지 않는다.
5. 기존 문서를 편집했다면 제공된 scripts/check-preservation.py에 원문과 후보 파일을 넣어 실행한다. Light Edit에는 --mode light와 --allowed-old/--allowed-new를 함께 사용해 허용된 문장·문단 구간을 지정한다. 변경본은 이 두 인자 없이는 통과할 수 없다. 실패한 후보를 완료본으로 넘기지 않는다. 파일 도구가 없다면 동일 항목을 직접 대조하고 자동 검사는 Not run으로 보고한다. 보존을 보고하기 전에 원문·후보의 Frontmatter와 참조 문자열을 실제 추출·대조한다. Wikilink가 일반 텍스트로 바뀌었거나 사라지면 복원한다. Light Edit는 허용 구간 밖 diff가 있으면 되돌린다. 결과를 검사하지 못했으면 보존 완료라고 쓰지 않는다. 본문을 직접 읽는다. 실제 프로젝트 검사와 렌더 확인을 수행한다. 평가 사본은 격리하고 명령의 입력·출력·부작용을 먼저 확인한다.

공개 본문에는 기술 사실·관계·조건을 쓴다. 조사 상태, 에이전트 지침, 내부 경로, 빌드 기록은 별도 보고나 내부 문서에 둔다. 외부 자료 절은 `## 참고 링크`다. 기존 `sources:` 키는 유지한다.

## 완료 보고

변경 문서·이유, 의미와 구조 보존, 실제 검사, 불확실성을 간결하게 보고한다. `Passed / Failed / Not run / Needs verification`를 사용한다. 자동 검사, 작성 모델 실행, 분리 검토, Quartz 렌더, Obsidian 앱 확인은 별개다.

사실·수치 생성, 안전 조건 손실, 인과 왜곡, 미확인 원인 확정, 참조 손실, 메타데이터·블록 손상, 무단 범위 확대·게시가 있으면 Critical Failure다. 문체 점수로 상쇄하지 않는다. 부분 조사를 전체 완료라고 보고하지 않는다.
