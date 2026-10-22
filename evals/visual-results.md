# 시각화 집필 검증

2026-10-22. 이 기록은 [기본 평가](results.md)에 추가하는 별도 실행이다. 기본 12사례·20행동과 이전 모델 출력·실패 기록은 수정하지 않았다. 아래 결과는 독립 fixture와 실제 로컬 HMY 구현의 격리 사본에 한정한다.

## 실제 지원 확인

HMY의 로컬 구현은 작업 중 변경되었다. 원격 main이나 설계 파일만으로 기능을 확정하지 않고 실제 Core의 10개 언어, parser/serializer/renderer, 공통 enhancer와 기존 Obsidian 편집·저장 구현을 읽었다. 처음 조사할 때 구현 중이던 diagram/explorer는 구현이 연결된 뒤 실제 실행으로 확인했다. 검증한 모듈의 SHA-256은 [native 결과](visual-native.json)의 provenance에 있다. 운영 HMY push·배포는 수행하지 않았다.

| 작성 형식 | 확인 범위 |
| --- | --- |
| 일반 Markdown·기존 그림 | 기존 예시·메타데이터·참조·안전 문장 유지 |
| hmy-spec comparison / plot | 비교 항목 선택·상이 값 강조, 수치·단위·조건·0 기준축·원래 값 |
| hmy-guide / hmy-result | 기존 절차·계산 결과 해석, 절차 진행 중 안전 설명 유지 |
| hmy-diagnosis | yes/no·choices·detail/action, 실제 대상·순환 검사, 선택·이전·전체·인쇄 |
| hmy-timeline / hmy-company-event | 기존 사건 파싱·렌더·직렬화, canonical 예시의 링크 |
| hmy-media / compare | 실제 Vault 자산·alt·권리, 슬라이더 키보드·원본·no-JS |
| hmy-signal | conceptual, 채널/단계 수·상태·대체 표·공식 근거, measured 거절 |
| hmy-diagram | 고유 노드·실제 연결·계층, 선택·강조·초기화·확대·중간 노드 오해 점검 |
| hmy-explorer | DDR CAS, PCIe 1~5세대 편도 부호화 계산·기본 표·오류 입력·초기화 |

필드와 동작은 검증한 구현의 범위다. 새 설치에서 동일 기능이 있는지 다시 확인한다. 입력 범위는 실제 하드웨어 지원·전압·안정성 보장이 아니다. 범용 차트·JavaScript expression·자동 호환 판정·실측 파형은 제공 기능으로 소개하지 않는다.

## 실행 결과

| 검사 | 결과 | 관찰 범위 |
| --- | --- | --- |
| python scripts/validate.py | Passed | 명시 배포 목록, 참조·버전·원문·자산·JSON 검사 |
| python -m unittest discover -s scripts -p test_*.py | Passed | 22개, SVG 속성 및 필수 페이지 누락 탐지 포함 |
| skill-creator 형식 검사 | Passed | UTF-8 모드의 SKILL.md 구조 검사 |
| scripts/verify-hmy.mts | Passed | 17문서·50 Wikilink·14블록·10종·14 roundtrip·24 실패 입력. 실제 Core·Obsidian 함수 import |
| 모델 출력의 독립 native 재검사 | Passed | 생성된 diagnosis/explorer/plot까지 17블록의 parse/render/편집·저장/roundtrip, 수치 독립 대조 |
| 모델 출력의 독립 보존 검사 | Passed | V01 허용 한 문장 치환, V08 메타데이터·Wikilink·각주·이미지 보존 |
| 예시 SSD의 보존 검사 | Passed | 원래 Frontmatter·참조·데이터/전원 안전 조건 유지 |
| 실제 HMY Core 회귀 | Passed | 최신 격리 사본 59개, 기존 demo/legacy 포함 |
| 실제 Obsidian 함수 회귀 | Passed | 격리 사본 31개 |
| 실제 Quartz 회귀 | Passed | 격리 사본 200개 |
| Obsidian plugin:build | Passed | 격리 소스의 타입 검사와 production esbuild, 운영 runtime sync 없음 |
| site TypeScript 검사 | Passed | 격리 캐시를 제거하고 tsc --noEmit |
| Quartz 5 build | Passed | 17문서 + 블록 표본 1개, 18입력·159출력 |
| 렌더 감사 | Passed | 47 HTML, 중복 제목·raw HMY/Wikilink·관리 메타데이터 오류 0 |
| 내부 링크 감사 | Passed | 57 checked, unresolved 0 |
| 실제 Chromium | Passed | [209개 확인](visual-browser.json), pageerror 0. 360/768/1440 × light/dark의 6문서, 전체 fixture 본문·이미지 |
| 실제 조작 | Passed | CAS 변경·오류·초기화, PCIe 세대/Lane, 진단 선택/뒤로/전체/초점, 비교 선택/상이 값/인쇄, 이미지 슬라이더·권리·키보드, diagram 선택/확대/Escape·SPA Back |
| no-JS·인쇄 | Passed | 기본 계산·표, 진단 전체·이미지 원본, 선택한 경로에서 인쇄 시 전체 단계·비교 그룹 보존 |
| 실제 Obsidian 앱 UI | Not run | 이 fixture의 Reading View·Live Preview·GUI 저장·Undo. native 함수와 build를 앱 확인으로 계산하지 않음 |
| 새 Codex CLI·Claude Code 모델·자동 선택 | Not run | 이번 작성 평가는 별도 subagent 명시 호출. CLI·자동 발견 시험과 구분 |

정적 도구는 의존성 없이 실행한다. native 명령의 실제 인자는 [재현 안내](README.md)를 따른다. 브라우저 검사는 Python Playwright·Chromium이 준비된 환경에서 `python scripts/verify-quartz.py --public-dir <격리-Quartz의-public> --report <결과-JSON>`로 실행한다. 설치·게시 후 결과는 [첫 베타 Release](https://github.com/HoMongYi/hmy-wiki-writing/releases/tag/v0.1.0)에서 별도로 확인한다.

## 작성 모델

[입력 12개](visual-inputs.json), [읽은 근거](visual-sources.json), [최초 원문](visual-model-first.json), [사례별 대조](visual-assessment.json), [재실행](visual-model-retry.json)을 제공한다. 작성자에게 완성 예시·기존 모델 출력·평가 정답은 주지 않았다. 제공한 출처 메모와 격리된 실제 구현을 읽도록 했으며 생성 중 네트워크는 사용하지 않았다. 주 에이전트는 모든 반환 후보를 읽고 보존·native 검사를 독립 실행했다.

- 최초 최종 출력은 11사례 Passed, V12 Failed다. V12의 독자 본문에 “수치가 주어지지 않아 덧붙이지 않는다”는 작성 상황이 포함됐다. 기술 한계는 CPU별 조건으로 설명하고 작성 상황은 보고에 두도록 문체 참조를 보완했다. 같은 작성 세션에서 다시 처리한 V12는 Passed이며 독립 blind 재실행으로 주장하지 않는다.
- V06은 작성자가 중간 산술 기대값 오류를 보고했다. Gen1·2 ×4의 첫 기대값 1.25/2.5는 잘못됐으며 최종 1.00/2.00을 주 에이전트가 실제 공식·native 함수로 독립 확인했다. 중간 오류 요약은 재실행 JSON에 남겼다. 전체 stderr·원래 script가 보존된 실행 transcript는 아니다.
- V01은 불필요한 시각화 없이 한 문장만 교정했다. V04는 수치 없이 검토했고, V07은 제공된 구형 설치의 제한을 따라 정적 표·공식을 선택했다. V12도 새 블록을 강제하지 않았다.
- [무지침 기준선](visual-baseline.json)의 4사례는 별도 관찰이다. 조사 도중 HMY 구현이 바뀌었으므로 같은 조건의 대조군으로 점수를 비교하지 않는다. 작은 사례 집합으로 전체 정확도나 통계적 우월성을 주장하지 않는다.

## 실패 기록과 한계

최초 격리 Core 검사는 기존 _demo fixture를 복사하지 않아 57/58이었다. 빠진 fixture를 사본에 보충한 뒤 통과했다. 최초 추가 SVG mutation 검사는 새 SVG를 검사하지 않던 실제 누락을 발견했고 전체 SVG 검사로 보완한 후 20개 테스트가 통과했다.

처음 브라우저 서버는 확장자 없는 URL과 Windows 자식 프로세스 정리를 처리하지 못했다. 소유를 확인한 이번 서버만 정리하고, loopback 임의 포트와 명시 종료를 가진 검사 서버를 사용했다. 자동 폴더 페이지를 독립 문서로 잘못 검사한 대기도 별도 실패로 남겼다. 실제 페이지를 열지 못한 실행을 렌더 성공으로 집계하지 않았다.

초기 관계도는 노드 배열 때문에 선이 다른 노드를 통과해 경유지처럼 보였다. 예시의 노드 순서를 조정하고 실제 SVG 선이 무관한 노드와 겹치지 않는지 확인했다. 단순 parser 검사가 기술적 가독성을 보장하지 않는 사례다.

강화한 인쇄 검사에서 이전 HMY 사본의 선택하지 않은 진단 단계가 숨겨지는 문제가 발견됐다. 동시에 진행된 HMY의 최신 로컬 보완을 다시 복사하고 해당 소스·회귀·native·브라우저를 재검증했다. 그 뒤의 209개만 최종 결과다. 실패한 browser-first/second/final 실행과 소스 갱신 기록은 비공개 실행 폴더에 유지한다.

Chromium 레이아웃·키보드·정적 대체 성공은 모든 브라우저·OS·스크린리더·물리 터치 장치의 적합 판정이 아니다. 공식 자료의 열람·실패 범위는 visual-sources.json에 한정한다. 기본 평가에 기록한 alias의 fragment 손실 등 기존 한계도 자동으로 해소됐다고 보지 않는다.

## 최종 검사기 검토

별도 검토에서 예시·지침의 명확한 기술 오류나 추가 지원 과장은 발견되지 않았다. 검사기가 누락을 건너뛰던 세 경로는 수정했다. 필수 fixture 목록에서 생성 HTML과 contentIndex를 대조하고, 모델 출력의 nonempty cases·고유 ID·명시적 markdown을 검사하며, 모델 이미지의 자산 루트는 별도 인자로 받는다. 검증할 수 없는 자산은 Needs verification(종료 2), 누락 파일·잘못된 입력은 Failed(종료 1)로 처리한다. 모델 사례 수와 블록 수는 fixture 수와 따로 보고한다.

수정 전 누락 AMD 페이지가 206개 검사로 잘못 Passed가 되는 것과 빈 모델 입력·없는 이미지의 성공 경로를 별도 사본에서 재현했다. 수정 후 같은 누락 페이지는 브라우저 실행 전에 거절됐고, 모델 입력/자산의 실패·미검증·정상 상태를 각각 확인했다. 실제 배포 fixture가 누락됐던 것은 아니다. 두 페이지 재현 회귀와 기존 테스트를 포함한 최종 패키지 테스트는 22개다.
