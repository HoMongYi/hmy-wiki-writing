# 0.1.0 검증 기록

2026-10-22에 실행했다. 자동 검사, 작성 모델, 분리 검토, 앱 렌더, 설치를 따로 집계한다. 실패한 출력은 승인된 예시가 아니다.

## 패키지와 실제 HMY 구현

| 검사 | 결과 | 범위 |
| --- | --- | --- |
| 패키지 정적 검사 | Passed | 배포 목록, 내부 Markdown 링크·앵커, 버전, 파일 누락, 로컬 경로·비밀값 패턴, 예시 보존 |
| 변형·보존 검사기 테스트 | Passed | 19개 테스트. 누락 참조·Frontmatter·각주·이미지·fence·변경 범위 탐지 |
| Agent Skill 기본 검사 | Passed | skill-creator quick_validate.py |
| native HMY 통합 | Passed | 독립 13문서, 33 Wikilink, Markdown 이미지 2개, 7종 블록 |
| 모델 블록 통합 | Passed | 최초 H05·H07까지 포함해 총 9블록 parse·render·GUI editability·저장 validation·roundtrip |
| native 실패 입력 검사 | Passed | 깨진 YAML, 없는 진단 ID, 미지원 GUI 필드, 공개 필터 3조건 |
| 격리 Quartz 5 build | Passed | 13문서와 별도 블록 표본 1개, 입력 14개·HTML 39개 |
| Quartz 기존 테스트 | Passed | 196개, 실패 0 |
| 렌더 감사 | Passed | 연속 중복 제목·raw Wikilink·관리 정보·raw 블록 없음 |
| 내부 링크 감사 | Passed | 33개, unresolved 0 |
| 브라우저 본문 확인 | Passed | NVMe·M.2 점검·AMD·PCIe·블록 표본 직접 확인, 14페이지 DOM, 7종 블록, 이미지 3개·앵커 42개 |
| canonical 섹션·백링크 | Passed | PCI Express의 CPU 직결과 칩셋 경유 앵커와 유입 문서 확인 |
| alias 목적지 | Passed | 루트 ram-timing 리디렉션이 메모리 타이밍으로 이동 |
| alias의 fragment 유지 | Failed | 현재 HMY 리디렉션에서 #cas-latency가 이동 후 사라짐. 예시의 섹션 링크는 canonical 파일 사용 |
| Obsidian 실제 앱 UI | Not run | Reading View·Live Preview·GUI 상호작용 미실행. native 함수 검사와 구분 |

검사한 HMY HEAD는 `2cc91b915a901ea5d801ecf055e447e7cc73548a`다. 당시 작업 트리에 기존 사용자 변경이 있어 pristine checkout이라고 주장하지 않는다. 격리 사본과 본체의 core 4개 파일, Obsidian 검증·편집 2개 파일, Quartz 설정의 SHA-256이 일치함을 확인했다. 운영 Vault와 본체 코드는 이 스킬 작업에서 수정하지 않았다.

첫 격리 build는 상위 Git 제외 규칙으로 입력이 0개였다. 이를 성공으로 세지 않았으며 독립 Git 루트에서 14개 입력을 확인한 실행만 위 표에 반영했다. 격리 서버에는 운영 로그인 API와 저작권 안내 콘텐츠를 복사하지 않았으므로 그 기능의 통합 시험은 Not run이다.

## 모델 행동

[고정 입력](inputs.json), [무편집 최초 결과](model-first-run.json), [사례별 평가](assessment.json)를 함께 제공한다. 작성 모델에는 결과·평가 기준·완성 예시를 제공하지 않았다. 근거는 직접 읽은 공식 자료의 메모로 한정하고 생성 중 네트워크는 사용하지 않았다.

| 실행 | 결과 | 관찰 |
| --- | --- | --- |
| H01 | Passed | 한 문장만 개선하고 메타데이터·안전 문장·앵커·각주·이미지 유지 |
| H02 최초 | Failed — Critical Failure | 두 Wikilink를 삭제했지만 보고에서는 보존했다고 서술 |
| H03–H11 | Passed | 제공 근거 범위, 유형·블록, 진단 안전, 기업 날짜, 허브, 최신성 한계, 공개 범위·조사 범위 구분 |
| H12 최초 | Failed | 별도 오류 보고 요청에서 본문 삭제·제목 추가·참고 링크 재구성 |
| H02 지침 보완 후 재실행 | Failed — Critical Failure | 링크 삭제와 부정확한 보존 보고 반복 |
| H12 지침 보완 후 재실행 | Passed | 원문을 그대로 유지하고 CAS 계산과 전체 지연의 차이를 별도 보고 |
| H02 실제 보존 게이트 포함 | Passed | 검사 함수를 실행한 새 후보와 반환 Markdown의 독립 재검사 모두 보존 통과 |

[재실행 원문](model-retry.json)과 [게이트 포함 실행](model-gated.json)도 별도 보존한다. 게이트 실행을 명시한 마지막 시험은 도구를 포함한 workflow 시험이다. 순수한 지침만으로 링크 손실이 사라졌다고 해석하지 않는다. 최초 H02의 Critical Failure를 최종 성공으로 덮지 않는다.

분리 검토자는 입력·원문·근거 메모·출력과 실제 코드를 읽었고 예시 정답과 작성 세션은 보지 않았다. H02·H12 실패를 독립 확인했다. 검토자는 H02를 일반 실패로 분류했으나 이 배포의 참조 손실 규정에 따라 주 검토자가 Critical Failure로 최종 분류했다. 근거 메모 밖의 외부 사실을 다시 전수 조사한 검토는 아니다.

스킬 미적용 예비 실행 두 건도 수행했다. 일반 SSD 진단을 M.2 NVMe로 좁히거나 기존 링크 유효성 확인 없이 보존 완료를 보고한 문제가 있었다. 적용 실행과 원문·도구 조건이 완전히 같지 않아 점수 비교에서 제외했다. 작은 사례 집합으로 통계적 우월성이나 전체 정확도를 주장하지 않는다.

## 설치와 새 실행

| 검사 | 결과 | 범위 |
| --- | --- | --- |
| skills CLI 1.7.4 로컬 패키지 설치 | Passed | Node 24.13.1, Codex·Claude Code 경로의 SKILL.md 실제 존재 |
| 새 Codex 명시 호출 | Passed | 설치 경로를 명시해 SKILL.md와 필요한 참조를 실제 읽음 |
| 새 Codex New Writing·Light Edit·Review Only | Passed | [원문 출력](codex-smoke.json), 한 문장 치환과 중첩 메타데이터 보존, 미조사 범위 보고 |
| Claude Code 실제 모델 호출 | Not run | 설치 파일과 링크만 확인 |
| 자동 스킬 선택 | Not run | 명시 호출을 시험 |
| 게시 후 공개 설치 | Not run | 이 커밋은 게시 전 후보 검사 기록. 게시 후 결과는 [GitHub Release](https://github.com/HoMongYi/hmy-wiki-writing/releases/tag/v0.1.0)에서 확인 |

처음에는 원본 저장소의 하위 폴더에 설치를 요청했다. CLI는 경로 겹침을 이유로 복사를 생략하면서 성공처럼 표시했다. 이를 실패로 취급하고 배포 목록의 파일만 담은 형제 패키지에서 다시 설치해 실제 파일과 실행을 확인했다. 로컬 개발자는 원본과 설치 목적지가 겹치지 않게 한다.

## 알려진 한계

- 지침만으로 생성 모델의 참조 손실을 막지 못했다. 기존 문서 편집은 보존 검사와 본문 대조를 완료 조건으로 사용한다.
- 보존 검사기는 보수적인 텍스트 게이트다. 링크 표시명 변경도 검토 대상으로 잡으며 기술적 의미·실제 목적지·앱 동작은 검증하지 않는다.
- 추가 확인한 Base 2.1 PDF는 HTTP 403으로 읽지 못했다. 이는 과거 버전이며 현재 공식 소개는 2026-08-04 공개된 2.4 규격군을 안내한다. 최신 PDF 세부 내용은 검증하지 않았다. 기본 큐 설명은 직접 읽은 Revision 1.0e와 Microsoft 완료 항목에 한정했다.
- alias와 섹션을 조합할 때 현재 Quartz 리디렉션이 fragment를 잃을 수 있다. canonical 파일의 섹션 링크를 사용한다.
- native 검사에는 실제 HMY 프로젝트와 Node 의존성이 필요하다. 패키지 정적 검사만으로 전체 호환성이 보장되지는 않는다.

## 최종 패키지 분리 검토

두 P2를 수정했다. Light Edit 게이트는 허용 구간 인자 없이 본문 전면 변경을 통과시키던 동작을 거절하도록 바꾸고 세 회귀 테스트를 추가했다. 과거 Base 2.1 PDF를 최신이라고 부른 예시 표현은 공식 2.4 소개를 다시 읽어 바로잡았다. 최초 모델의 H09는 제공된 가정의 처리를 시험한 것으로, 과거 2.1 PDF가 실제 최신판이었다는 근거가 아니다. 수정 후 패키지·19개 테스트·native 통합을 다시 실행했다.
