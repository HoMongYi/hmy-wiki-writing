# HMY Wiki Writing

Obsidian과 Quartz 5를 함께 사용하는 [HMY Wiki](https://wiki.homongyi.org/)의 PC 하드웨어 문서를 작성하고 개선하는 Agent Skill이다. 기술 원리, 규격과 호환성, 장애 진단, 기업과 역사를 설명하고 기존 문서를 Wikilink로 연결한다.

정확한 기존 문장과 Markdown 원본을 보존한다. 문장 교정은 필요한 부분만 바꾸고, 전면 고도화는 부족한 작동 원리와 조건을 근거로 보완한다. 현재 배포 버전은 초기 베타 **0.1.0**이다. 본문·표·구조도·수치 비교·입력 탐색·진단 분기 중 기술 내용을 이해하는 데 필요한 형식을 선택한다.

## 설치

Node.js 22.20 이상과 Git이 있는 환경에서 실행한다. 기본 명령은 설치 대상을 선택하는 대화형 방식이다.

```bash
npx skills add HoMongYi/hmy-wiki-writing
```

| 환경 | 프로젝트 설치 | 명시적 호출 |
| --- | --- | --- |
| Codex | `.agents/skills/hmy-wiki-writing/` | `$hmy-wiki-writing` |
| Claude Code | `.claude/skills/hmy-wiki-writing/` | `/hmy-wiki-writing` |

CLI는 공유 스킬 폴더와 에이전트별 링크를 만들 수 있다. 특정 에이전트만 설치하려면 다음과 같이 실행한다.

```bash
npx skills add HoMongYi/hmy-wiki-writing --agent codex --skill hmy-wiki-writing -y
npx skills add HoMongYi/hmy-wiki-writing --agent claude-code --skill hmy-wiki-writing -y
```

사용자 전체 설치는 `--global`을 추가한다. Codex 공식 사용자 경로는 `~/.agents/skills/`다. 같은 이름의 예전 복사본이 다른 검색 경로에 있으면 실제 로드 경로를 확인한다. 설치 후 새 대화에서 스킬을 호출하고 HMY 프로젝트 또는 원문을 지정한다. HMY 본체, Quartz, Obsidian 플러그인은 별도로 준비해야 한다.

설치와 실제 모델 동작의 확인 범위는 [검증 기록](evals/results.md)에 구분해 둔다.

## 적용 전후

### 문장 교정

> **전:** 연결 방식의 확인을 위해서는 메인보드 매뉴얼에서 해당 슬롯의 사양을 조회하는 것이 필요하다.
>
> **후:** 연결 방식을 확인하려면 메인보드 매뉴얼에서 해당 슬롯의 사양을 살펴본다.

[Light Edit 전체 비교](examples/light-edit.md)는 여러 문단 중 한 문장만 바꾼다. Frontmatter의 중첩 사용자 필드, 섹션, 링크, 각주와 이미지는 그대로다.

### 기술문서 고도화

[NVMe 원문](examples/fixtures/before/NVMe.md)의 정확한 정의와 M.2 구분을 유지하면서 [개선본](examples/fixtures/vault/01_하드웨어/NVMe.md)에 호스트·컨트롤러, 제출 큐·완료 큐, PCIe 전송 경로와 호환 조건을 추가했다. 실제 설명을 늘렸으며 실측하지 않은 성능 수치는 넣지 않았다. [변경 이유와 보존 항목](examples/deep-improvement.md)을 함께 볼 수 있다.

이 비교는 공식 자료를 확인해 독립 집필한 예시다. 무편집 모델 출력과는 구분하며, 모델 실행 결과는 평가 기록에 남긴다.

## 요청 예시

**새로운 기술문서**

> $hmy-wiki-writing PCIe 레인과 슬롯의 관계를 HMY Wiki 문서로 작성해줘. 기존 관련 문서를 먼저 찾고, CPU 직결과 칩셋 경유의 차이부터 확장카드와 SSD에 미치는 영향까지 설명해줘.

**기존 문서 고도화**

> $hmy-wiki-writing NVMe 문서를 전체적으로 개선해줘. 정확한 내용과 Wikilink를 유지하고 부족한 작동 원리와 호환성 설명을 보완해줘. HMY Block은 설명에 도움이 되는 곳에만 사용해줘.

**기업과 역사**

> $hmy-wiki-writing x86과 관련된 기업 및 기술 역사를 정리해줘. 기존 문서와 연결하고 라이선스·기업 관계·기술 발전 과정을 공식 자료로 검증해줘.

**HMY Block**

> $hmy-wiki-writing 이 진단 문서에서 HMY Block을 활용하면 좋은 부분을 개선해줘. 실제 schema를 읽고 Obsidian과 Quartz에서 표시되는 범위까지 확인해줘.

**위키 전체 품질 검토**

> $hmy-wiki-writing 공개 하드웨어 문서를 전수 조사해줘. 가독성, 기술 설명, 중복, Wikilink, Frontmatter, 블록과 참고 자료를 평가하고 개선 우선순위를 정리해줘. 이번에는 원본을 수정하지 마.

**기술 정보 최신화**

> $hmy-wiki-writing GPU 보조전원 커넥터 문서를 최신 공식 규격으로 점검해줘. 기존 설명과 현재 규격의 차이를 확인하고 안전 및 호환성 조건을 반영해줘.

Claude Code에서는 위 요청의 호출 부분을 `/hmy-wiki-writing`으로 바꾼다.

## 작성 방식

| 모드 | 쓰임 |
| --- | --- |
| New Writing | 기존 파일·제목·별칭을 검색한 뒤 새 글 작성 |
| Light Edit | 요청한 문장·문단만 교정 |
| Rewrite | 유효한 사실을 보존하며 구조 재편 |
| Deep Improvement | 근거 조사와 원리·관계·실사용 설명 확장 |
| Review Only | 파일을 바꾸지 않고 근거와 개선안 보고 |
| Refresh | 바뀐 기술 주장과 적용 시점 갱신 |

개념, 부품, 규격, 제품, 비교, 진단, 절차, 기업, 역사, 생태계, 허브의 정보 구조를 구분한다. 실제 Frontmatter type은 HMY 프로젝트가 정한 여섯 종류를 사용한다. 일반 설명은 본문에 쓰고, 순서·분기·사양·사건·결과·미디어·관계·계산 탐색이 필요한 경우에만 실제 프로젝트가 지원하는 HMY Block을 선택한다.

[지식 감사](workflows/knowledge-audit.md), [주제 고도화](workflows/topic-deepening.md), [지식 연결](workflows/knowledge-linking.md), [최신화](workflows/technical-refresh.md), [시각 자료](workflows/visual-documentation.md), [전체 개선](workflows/repository-improvement.md) workflow를 제공한다.

## 시각적 설명과 입력 탐색

기존 글·관련 자산을 먼저 검색한다. Light Edit는 요청한 문장·문단만 고치며 시각화를 자동으로 추가하지 않는다. [Visual Documentation](workflows/visual-documentation.md)은 구조·데이터·입력 변화·실제 진단 분기에 맞는 형식을 선택하고 본문과 수치·자산을 함께 검증한다.

| 실제 HMY 문법 | 작성 용도 |
| --- | --- |
| hmy-spec | 구조화된 항목, comparison, 근거 데이터의 plot |
| hmy-guide / hmy-result | 실제 절차와 결과 해석 |
| hmy-diagnosis | yes/no 또는 choices, detail/action을 사용한 점검 경로 |
| hmy-timeline / hmy-company-event | 검증된 날짜와 기업 사건 |
| hmy-media | 이미지·설명·권리, compare를 이용한 두 이미지 비교 |
| hmy-signal | 시간·전압 실측이 아닌 개념적 신호 순서 |
| hmy-diagram | 구성 요소와 연결 관계·계층 탐색 |
| hmy-explorer | DDR CAS와 PCIe 1~5세대의 이론 계산 탐색 |

[메인보드 데이터 경로](examples/fixtures/vault/01_하드웨어/메인보드%20데이터%20경로.md), [PCIe 대역폭](examples/fixtures/vault/01_하드웨어/PCIe%20대역폭%20비교.md), [DDR CAS](examples/fixtures/vault/01_하드웨어/DDR%20CAS%20지연시간.md), [CPU 캐시](examples/fixtures/vault/01_하드웨어/CPU%20캐시%20계층.md), [SSD 진단](examples/fixtures/vault/01_하드웨어/SSD%20인식%20불량.md)의 [선택 이유](examples/visual-documentation.md)를 제공한다. 단순한 설명은 일반 문단·Markdown 표·Mermaid·기존 SVG로 충분할 수 있다.

예를 들어 기본 전송률과 CL을 명시한 CAS 설명은 다음 실제 YAML로 작성한다. 본문에는 계산식 `CL × 2000 ÷ MT/s`와 기본값의 결과 10 ns, 전체 접근 지연·실측과의 차이도 남긴다.

```hmy-explorer
kind: ddr-cas
title: 전송률과 CL의 관계
description: 이론 CAS 구간만 계산하며 전체 메모리 접근 지연이나 제품 실측이 아니다.
baseline: {dataRate: 6000, cl: 30}
source: https://www.kingston.com/en/blog/gaming/cas-latency-cl-ram-timing-explained
```

이 문법에는 해당 기능을 갖춘 HMY 공통 Core·Quartz renderer/enhancer·기존 Obsidian 플러그인이 필요하다. 스킬 설치가 엔진을 갱신하지는 않는다. 로컬 최신 구현, 원격 main, 운영 사이트의 지원은 다를 수 있으므로 실제 대상의 schema·저장·렌더·조작을 확인한다. 지원이 없으면 정적 공식·표·도식으로 설명한다.

범용 차트·임의 JavaScript·새 계산 expression·실측 파형·자동 부품 호환 판정을 생성하지 않는다. 입력 가능 범위는 하드웨어 지원·안정성 보장이 아니다. 수치 원자료가 없으면 벤치마크 그래프를 만들지 않는다.

## 지원 범위와 제한

- canonical 원본은 HMY 프로젝트의 `vault/`다. 기본 집필 범위는 `vault/index.md`와 `vault/01_하드웨어/**`이며 내부 관리 문서는 제외한다.
- Frontmatter·URL·별칭·링크·이미지·각주를 보존하고, 안전 조건과 기술적 의미를 별도로 대조한다.
- HMY schema와 parser를 복제하지 않는다. 실제 프로젝트 문서·공유 코어·Obsidian 저장 검증·Quartz 결과를 확인한다.
- 파일 접근, 공식 자료 검색, 빌드, 브라우저 확인은 사용하는 에이전트의 도구와 권한이 필요하다. 스킬 자체는 실행 엔진이 아니다.
- parser 통과와 기술 정확성, GUI 저장, 실제 앱 표시는 서로 다른 검증이다. 최신 자료를 열지 못하면 확인 범위를 제한해서 보고한다.
- 스킬 호출은 운영 게시나 공개 범위 확대 승인이 아니다. 문서 감사에서 일부 표본만 읽었다면 전체 완료로 보고하지 않는다.
- 최신 HMY의 진단 enhancer는 관찰별 단계 선택을 제공한다. 클릭 결과가 실제 장치 시험이나 원인 자동 확정을 대신하지 않는다.

## 파일 구성

| 경로 | 내용 |
| --- | --- |
| [SKILL.md](SKILL.md) | 진입점, 편집 모드, 범위와 완료 조건 |
| [references](references/document-types.md) | 유형·문체·근거·보존·링크·블록 등 16개 참조 |
| [workflows](workflows/repository-improvement.md) | 6개 반복 작업 흐름 |
| [examples](examples/fixtures/README.md) | 기술 예시, 편집 전후, 독립 Vault |
| [evals](evals/README.md) | 입력, 20개 행동 기준, 공식 근거, 평가 결과 |
| [scripts](scripts/package-files.json) | 배포 목록, 정적 검사, native HMY 통합 검사 |
| [agents/openai.yaml](agents/openai.yaml) | Codex 표시·호출 설정 |

## 검사

Python 3.10 이상에서 의존성 없이 패키지를 검사한다.

```bash
python scripts/validate.py
python scripts/check-preservation.py <before.md> <after.md> --mode light --allowed-old "기존 문장" --allowed-new "수정 문장"
python -m unittest discover -s scripts -p "test_*.py"
```

HMY 프로젝트와 설치된 Node 의존성이 있으면 공통 코어와 저장 검증을 직접 호출한다.

```bash
node <HMY의-tsx-CLI-경로> scripts/verify-hmy.mts --hmy-root <HMY-프로젝트-루트>
```

전체 Quartz 빌드는 원본과 분리한 사본에서 수행한다. Python Playwright와 Chromium이 준비된 경우 독립 예시의 실제 페이지·조작을 검사한다.

```bash
python scripts/verify-quartz.py --public-dir <격리-Quartz의-public> --report <결과-JSON>
```

[시각화 검증](evals/visual-results.md)은 패키지·native·모델·브라우저를 구분한다. 관찰한 범위는 22개 패키지 테스트, 실제 HMY Core 59개·플러그인 31개·사이트 200개, Chromium 209개 확인이다. 실제 Obsidian Reading View·Live Preview·GUI, Claude Code 모델 호출, 자동 스킬 선택은 이번 실행에서 Not run이다. [재현 절차와 한계](evals/README.md)를 확인한다.

## 라이선스와 참고 자료

스킬 지침, 코드, 독립 집필 예시와 자체 SVG는 [MIT License](LICENSE)로 제공한다. 연결한 외부 자료의 권리는 각 권리자에게 있다. HMY Wiki 운영 문서 전체의 라이선스를 이 패키지가 재정의하지 않는다.

- [Agent Skills 규격](https://agentskills.io/specification)
- [Codex 스킬](https://developers.openai.com/codex/skills/)
- [Claude Code 스킬](https://code.claude.com/docs/en/skills)
- [skills CLI](https://github.com/vercel-labs/skills)
- [공식 근거와 열람 범위](evals/sources.json)
