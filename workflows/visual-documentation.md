# Intelligent Visual Documentation

New Writing·Rewrite·Deep Improvement·Review Only·Refresh에서 기술 설명을 보완할 때 사용한다. Light Edit는 요청 범위만 교정하고 시각화 추가·제안을 자동 후속 작업으로 붙이지 않는다.

1. **기술 내용 분석.** 대상 전체와 관련 문서를 읽고 독자가 이해해야 할 구조·수치·조건·분기를 정한다. 기존 설명·Frontmatter·링크·안전 조건을 보존 목록에 잡는다.
2. **형식 선택.** [선택표](../references/visual-explanations.md)로 본문·표·기존 그림·구조도·차트·탐색기·절차·진단 중 필요한 형식을 고른다. 텍스트로 충분하면 그대로 둔다.
3. **기존 자산과 구현 검색.** Vault의 _assets와 관련 문서, 현재 HMY 계약·parser·renderer·enhancer·플러그인을 확인한다. 계획만 있는 기능은 제외하고 지원이 없으면 정적 Markdown으로 설명한다.
4. **근거 확인.** 정확한 모델·규격·데이터와 재사용권을 확인한다. 계산은 입력·단위·방향·효율·가정을 대조한다. 원자료가 없으면 수치 비교를 만들지 않는다.
5. **데이터 작성.** [수치 설명](../references/data-visualization.md)과 [인터랙션 계약](../references/interactive-documentation.md)을 필요한 범위에서 읽는다. 노드·대상 ID·기본값·공식·출력·한계와 기본 상태의 핵심 설명을 준비한다.
6. **Markdown 통합.** 실제 canonical YAML 또는 지원되는 Mermaid·SVG를 사용한다. 본문과 캡션이 같은 기술 범위를 설명하게 하고 임의 JavaScript를 삽입하지 않는다. 공개 본문에 내부 조사·작업 상태를 넣지 않는다.
7. **기술·보존 검증.** 계산을 독립 대조하고 원문·후보의 메타데이터·참조·이미지·안전 조건을 비교한다. 실제 native parser·serialization·Obsidian 저장 validation을 실행한다. Review Only는 원본을 수정하지 않는다.
8. **화면·조작 확인.** 격리 Quartz build에서 본문·기본 상태·입력/분기·오류·키보드·모바일·테마·no-JS·인쇄·SPA 재방문을 필요한 범위에서 확인한다. Obsidian Reading/Live/GUI는 실제 앱에서 따로 검증한다.

보고에는 채택한 형식과 이유, 실제 지원·실행 범위, 유지한 원문, 남은 차이를 쓴다. parser 성공·공통 DOM 성공·실제 앱 성공을 같은 결과로 합치지 않는다. [독립 예시](../examples/visual-documentation.md)와 [검증 기록](../evals/visual-results.md)을 참고한다.
