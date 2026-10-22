# 실제 프로젝트와 연결

스킬은 집필 지침과 평가 도구다. HMY 본체의 parser·renderer·플러그인·공개 정책을 설치하거나 덮어쓰지 않는다. 루트는 사용자 환경에서 찾고 하드코딩하지 않는다.

| 경로 | 역할 |
| --- | --- |
| vault/ | 유일한 canonical Markdown·자산, Obsidian 루트 |
| site/ | Quartz 5 설정·렌더·빌드 |
| packages/hmy-wiki-core/ | 공통 타입·parser·renderer |
| obsidian-plugin/ | 기존 HMY Wiki Tools 소스 |
| vault/.obsidian/plugins/hmy-wiki-tools/ | 플러그인 런타임 산출물 |
| docs/, .agents/, HANDOFF.md | 내부 지침·작업 기록 |

## 현황 확인

루트 AGENTS.md와 docs/HMY_WIKI_AUTHORING.md, docs/HMY_CONTENT_POLICY.md를 읽는다. 메타데이터는 docs/HMY_DOCUMENT_TYPES.md, 블록은 docs/HMY_BLOCKS.md와 실제 구현을 확인한다.

기본 집필 공개 범위는 vault/index.md와 vault/01_하드웨어/**다. **/_관리/**와 내부 지침은 제외한다. 다른 Vault 폴더가 있어도 범위를 넓히지 않는다.

site/quartz.config.yaml의 ignorePatterns와 plugins/filters/hmy-status.ts를 함께 확인한다. 현재 설정은 폴더 제외 방식이므로 미래의 새 최상위 폴더까지 자동으로 차단하는 allowlist로 간주하지 않는다. 기존 저작권 안내 같은 별도 공개 페이지는 현황으로 기록하고 하드웨어 집필 대상으로 자동 포함하지 않는다.

title은 표시 제목이고 파일 경로는 slug의 기반이다. 현재 Wikilink·각주·Mermaid·백링크가 지원되지만 shortest 링크 전략, 별칭 리디렉션, 공개 필터가 함께 작동한다. Obsidian 탐색 성공을 Quartz 결과와 혼동하지 않는다.

## 검사 실행

package.json과 실제 검사 파일의 인자를 읽는다. 현재 site에는 npm run build, npm test, scripts/audit-render.mjs, scripts/audit-internal-links.mjs, scripts/check-links.mjs가 있다. build는 ../vault를 입력으로 쓰며 prebuild에서 플러그인을 준비하므로 읽기 전용 명령이 아니다. 원본 보존 평가는 독립 복사본에서 입력·출력·캐시를 격리한다.

플러그인 변경 없는 집필에서 plugin:build를 항상 실행할 필요는 없다. 공통 parser, Obsidian 저장 검증 함수, 실제 앱 Reading View·Live Preview·GUI는 다른 검사다. 앱을 열지 못하면 Not run이다.

패키지 통합 검사: `node <HMY의 tsx CLI 경로> scripts/verify-hmy.mts --hmy-root <프로젝트 루트>`. 의존성이 없으면 미실행을 기록하고 대체 schema를 만들어 통과시키지 않는다.

## 시각화 지원 확인

블록 문서의 확장 부록과 docs/architecture/visual-blocks.md, Core의 HMY_BLOCK_LANGUAGES·visual/intelligent 모델 및 renderer/enhancer, 기존 Obsidian editing/validation/등록을 함께 읽는다. 로컬 작업 중인 설계나 테스트만으로 기능을 확정하지 않는다. 모델·정적 출력·조작·저장·실제 앱을 각각 확인한다. 이 스킬의 [검증 스냅샷](../evals/visual-results.md)은 당시 구현의 범위이며 운영 배포 여부나 다른 설치 버전을 보장하지 않는다.
