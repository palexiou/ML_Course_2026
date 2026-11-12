# Illustrated deck verification

Verified the 48-slide BioIT_AI_Eng.html on 12 November 2026 using local Google
Chrome and Playwright. See [structured results](engagement-validation.json).

- All slides checked at 1280 × 720 and 390 × 844, with no reported text overflow,
  stage overflow, panel overflow, or checked block overlap.
- All slides rendered and visually inspected; refined scientific/schema and
  token-generation slides inspected individually.
- Offline loading, notes, navigation, picker, token illustration, editing,
  autosave, HTML export/reopening, and exact final demo wording passed.
- The complete grill-me source matches the cached source file. DNA-validation
  assertions passed. The overlapping-patient assertion failed as expected;
  its disjoint comparison passed. No course notebooks were executed or edited.
- Three dedicated T3 slides, all six Main Flow skill slides, the overview,
  grill-me, and the instructor's routing table remain present.
- Both Agentomics reference files retain SHA-256
  `c144ac9384d00aaff14f8fe35efec0cf9af9b58adf0f56337b4ab51083990cb3`.

The separate T3 HTML preview tool is blocked by the host's AppArmor sandbox;
local Chrome supplied verification. The inline HTML renderer accepted the deck.
No commit, push, deployment, or demo application was prepared.
