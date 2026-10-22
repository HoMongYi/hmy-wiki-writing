# 원본과 메타데이터 보존

전체 원문을 읽고 Frontmatter, 파일 경로, 제목, 공개 URL, aliases, tags, 내부·외부 링크, 섹션 제목, 각주, 이미지·캡션·alt, HMY Block을 기록한다. 중요한 사실·조건·안전 문장도 대조한다. 링크 개수나 YAML 파싱 성공만으로 보존을 판정하지 않는다.

실제 규약은 docs/HMY_DOCUMENT_TYPES.md와 packages/hmy-wiki-core/src/pageTypes.ts가 소유한다. company, hardware, software, diagnosis, technology, procedure와 type 없는 일반 문서가 있다. 알 수 없는 필드·중첩 객체를 삭제하거나 새 이름으로 정규화하지 않는다.

타입 이름의 중첩 객체가 정보표의 우선 입력이며 없는 값은 최상위에서 읽는다. type이 없으면 정보표가 생기지 않는다. 스킬의 비교·역사·허브 분류를 새 type 값으로 저장하지 않는다.

visibility와 status는 다른 축이다. 공개 필터와 정책을 읽고 기존 값을 유지한다. 공개 범위 확대나 human_reviewed: true는 자동 후속 단계가 아니다. sources 키와 공개 절 제목 “참고 링크”는 별개다.

Light Edit는 가능하면 Frontmatter 원문과 구조를 유지한다. 구조 변경에서 제목·앵커를 바꿀 때는 유입 링크를 먼저 확인한다. 근거로 오류를 수정한 경우는 정보 손실과 구별해 보고한다.

별도 보고만 요청한 사실 오류는 Light Edit 본문에서 삭제하거나 교정하지 않는다. 원문을 그대로 반환하고 오류와 권장 수정은 보고에서 구분한다. 새 문서처럼 제목·섹션·Frontmatter를 붙이지 않는다.

수정 전후에서 Frontmatter 원문과 Wikilink·이미지·각주·외부 링크 문자열을 추출해 차집합을 확인한다. 사라진 참조가 있으면 복원하거나 요청된 변경 근거를 보고한다. 자체 선언만으로 “모두 보존”이라고 하지 않는다.

검사 명령: python scripts/check-preservation.py <before.md> <after.md> --mode light --allowed-old "기존 문장" --allowed-new "수정 문장". Light Edit 변경본은 허용된 구간을 두 인자로 함께 지정해야 한다. 여러 문단을 확장할 때에는 --mode deep을 사용한다. 이 검사는 문장 의미와 실제 목적지 존재를 검증하지 않지만 참조 삭제를 완료 전에 차단한다. 참조 표기 변경도 보수적으로 실패하므로 의도된 변경이면 근거와 목적지 검사를 따로 남긴다.
