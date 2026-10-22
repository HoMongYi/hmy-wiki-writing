# 평가와 재현

입력은 [inputs.json](inputs.json), 근거는 [sources.json](sources.json), 행동 대응은 [coverage.json](coverage.json), 관찰 결과는 [results.md](results.md)에 둔다. 예시 정답을 생성 모델의 프롬프트에 넣지 않는다.

## 층별 검사

1. 패키지: `python scripts/validate.py`. 명시적 배포 목록, 상대 링크·앵커, 버전, 제거 대상, 원문 보존을 검사한다.
2. 검사기: `python -m unittest discover -s scripts -p "test_*.py"`. 누락 파일·링크·Frontmatter·이미지·각주·미닫힌 fence를 실제 변형해서 탐지 여부를 확인한다.
3. native 통합: `node <tsx-CLI> scripts/verify-hmy.mts --hmy-root <HMY-root>`. 실제 HMY core, Obsidian 편집·저장 검증, Vault resolver를 import한다. 예시용 대체 parser는 없다.
4. 모델: 새 세션에 스킬, 해당 입력, 원문과 근거만 제공한다. 결과·coverage·작성된 예시는 제공하지 않는다. 출력과 읽은 자료 목록을 원문 그대로 비공개 실행 폴더에 보존한다.
5. 분리 검토: 작성 세션과 다른 검토자가 원문·주장·근거·출력을 대조한다. 자동 검사의 성공을 기술적 정확성으로 계산하지 않는다.
6. 앱: 격리된 HMY 소스 사본과 fixture Vault로 실제 Quartz를 빌드한다. 생성 HTML, 링크·이미지·각주·백링크와 블록을 브라우저에서 확인한다. Obsidian 앱 Reading View·Live Preview·GUI 확인은 따로 기록한다.
7. 설치: 격리 프로젝트에서 skills CLI로 설치한 뒤 새 Codex 실행으로 명시적 호출과 작성·편집·검토를 확인한다. 설치 성공만으로 모델 실행 성공을 주장하지 않는다.

## 격리 빌드

HMY의 site/, packages/hmy-wiki-core/, obsidian-plugin/ 소스와 필요한 의존성을 비공개 임시 폴더에 복사한다. 자격증명·운영 Vault·.git·기존 public 출력은 복사하지 않는다. node_modules는 링크보다 독립 사본을 우선한다. 예시 Vault를 사본의 vault/로 사용한다.

사본 site/에서 `npm run build`, `node scripts/audit-render.mjs public`, `node scripts/audit-internal-links.mjs public`를 실행한다. build의 prebuild는 캐시와 플러그인 인덱스를 바꿀 수 있으므로 원본에서 실행하지 않는다. 홈에 하드코딩된 운영 링크가 있으면 fixture 본문 링크 오류와 따로 기록한다. 앱 확인 없이 배포 준비 완료라고 보고하지 않는다.

## Critical Failure

사실·수치 생성, 안전 조건 누락, 인과 왜곡, 미확인 원인 확정, 링크·이미지 손실, Frontmatter·HMY schema 손상, 무단 공개 범위 변경·배포는 하나라도 발생하면 해당 사례 Failed다. 문체 점수와 평균으로 상쇄하지 않는다.

요청 범위 밖의 문장 삭제·구조 변경도 편집 계약 실패로 기록한다. 실패 원본을 성공 출력으로 덮어쓰지 않는다. 지침 수정 후 새 실행은 별도 행으로 기록하며 이전 실패를 지우지 않는다.

`Passed / Failed / Not run / Needs verification`를 사용한다. 작은 사례 집합으로 전체 정확도나 통계적 우월성을 주장하지 않는다. 스킬 미적용과 적용을 비교할 때 입력·근거·도구·모델 조건이 다르면 직접 점수 비교를 하지 않는다.

## 편집 보존 게이트

python scripts/check-preservation.py <원문> <후보> --mode light 또는 --mode deep으로 메타데이터와 참조를 대조한다. Light Edit에서 내용이 바뀌었다면 --allowed-old/--allowed-new가 모두 필요하며 지정한 한 구간 밖의 변경까지 검출한다. 실제 모델의 H02 링크 누락을 이 검사로 거절했다. 모델의 “보존했다”는 보고는 검사 결과가 아니다.

## 시각화 집필 평가

[별도 입력 12개](visual-inputs.json), [읽은 근거](visual-sources.json), [native 결과·소스 지문](visual-native.json), [실행 결과](visual-results.md)를 제공한다. 기본 평가 파일은 그대로 유지한다. 기준선은 [무지침 출력](visual-baseline.json), 새 지침의 원문은 [최초 출력](visual-model-first.json)과 [별도 재실행](visual-model-retry.json)이다. 기준선 조사 중 HMY 구현이 바뀌었으므로 직접 점수 비교에 사용하지 않는다.

전체 예시의 블록·자산·분기·계산을 검증하려면 `node <HMY의 tsx CLI> scripts/verify-hmy.mts --hmy-root <실제 프로젝트 또는 격리 사본>`을 실행한다. `--outputs <모델 JSON>`을 추가하면 출력의 HMY Block을 별도로 검사한다. 모델 cases는 비어 있지 않아야 하며 고유 id(이전 형식의 mode도 허용)와 명시적인 markdown이 필요하다. Review Only는 빈 markdown과 실제 report를 함께 제공한다. 모델 이미지 파일을 검사할 때는 --outputs-assets-root <자산-루트>를 지정한다. 루트가 없거나 원격 이미지의 존재를 확인하지 못하면 Needs verification(종료 2), 구조·누락 오류는 Failed(종료 1), 확인된 성공은 종료 0이다. 실제 검사한 모델 사례·블록 수는 fixture 결과와 구분한다. 모델 후보의 메타데이터·참조와 의미는 실제 보존 게이트와 본문 대조로 다시 확인한다.

격리 Quartz에는 examples/fixtures/vault/를 입력으로 복사한다. examples/hmy-blocks.md의 블록 표본을 별도 문서로 검사할 때에는 설명 파일의 상대 링크를 복사한 Vault 경로에 맞춘다. 운영 Vault·자격증명·기존 산출물은 복사하지 않는다. Python Playwright와 Chromium이 준비된 경우 다음 명령으로 실제 화면·조작을 확인한다.

```bash
python scripts/verify-quartz.py --public-dir <격리-Quartz의-public> --report <결과-JSON>
```

이 검사는 fixture의 실제 제목·블록·동작을 대상으로 한다. 새 브라우저 세션과 loopback 서버를 사용하고 종료 시 정리한다. 선택적 `--screenshots <폴더>`로 캡처한다. 실제 Obsidian 앱 Reading/Live/GUI는 이 Chromium 검사와 별개이며 미실행이면 Not run이다.
