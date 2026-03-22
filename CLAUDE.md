# CLAUDE.md — Tetris Project

## 프로젝트 개요

Python + Pygame으로 구현한 클래식 테트리스 게임.

- **언어:** Python 3
- **의존성:** `pygame >= 2.5.0`
- **실행:** `python main.py`

---

## 폴더 구조

```
tetris/                        # 프로젝트 루트
├── main.py                    # 진입점, 게임 루프
├── requirements.txt           # 의존성 (pygame>=2.5.0)
├── README.md                  # 한국어 문서
└── tetris/                    # 게임 패키지
    ├── __init__.py
    ├── game.py                # 핵심 게임 로직 + 렌더링
    └── pieces.py              # 테트로미노 정의 + Piece 클래스
```

---

## 아키텍처

레이어드 구조로, 각 파일이 단일 책임을 가진다:

```
main.py         ← UI / 이벤트 루프 레이어
tetris/game.py  ← 게임 로직 / 물리 레이어
tetris/pieces.py ← 데이터 / 도메인 레이어
```

---

## 핵심 클래스

### `Game` (`tetris/game.py`)

게임의 전체 상태를 단일 인스턴스로 관리.

**주요 상태 변수:**
- `board`: 2D 리스트 (ROWS×COLS), 고정된 블록 색상 or None
- `score`, `lines`, `level`: 게임 통계
- `current_piece`, `next_piece`: 현재/다음 Piece 객체
- `fall_interval`: 자동 낙하 속도 (ms)
- `game_over`, `paused`: 게임 상태 플래그

**주요 메서드:**

| 메서드 | 역할 |
|--------|------|
| `update(dt)` | 자동 낙하 물리 처리 (매 프레임 호출) |
| `draw(screen, fonts)` | 전체 렌더링 파이프라인 |
| `_valid(piece, dx, dy)` | 충돌 감지 |
| `_lock_piece()` | 피스를 보드에 고정, 줄 제거, 다음 피스 스폰 |
| `_clear_lines()` | 완성된 줄 제거 + 점수/레벨 업데이트 |
| `rotate()` | 회전 (Wall Kick 포함) |
| `hard_drop()` | 즉시 낙하 (+2점/셀) |
| `soft_drop()` | 수동 낙하 (+1점/셀) |
| `restart()` | `__init__()` 재호출로 상태 초기화 |

### `Piece` (`tetris/pieces.py`)

**속성:**
- `name`: 피스 종류 (`I`, `O`, `T`, `S`, `Z`, `J`, `L`)
- `color`: RGB 튜플
- `rotations`: 회전 상태 리스트
- `x`, `y`: 보드 좌표

**주요 메서드:**
- `blocks` (property): 현재 회전 상태의 상대 좌표 반환
- `get_absolute_blocks()`: 보드 절대 좌표로 변환
- `rotate()` / `rotate_back()`: 회전 전진/후퇴

---

## 게임 상수 (`tetris/game.py`)

```python
COLS = 10               # 보드 너비
ROWS = 20               # 보드 높이
CELL_SIZE = 30          # 셀 픽셀 크기
SIDEBAR_WIDTH = 150     # UI 패널 너비
SCREEN_WIDTH = 450      # 전체 윈도우 너비
SCREEN_HEIGHT = 600     # 전체 윈도우 높이

FALL_INTERVAL_INIT = 500   # 초기 낙하 속도 (ms)
FALL_INTERVAL_MIN = 100    # 최소 낙하 속도 (ms)
LEVEL_SPEED_UP = 50        # 레벨당 속도 증가량 (ms)
```

---

## 게임 메커니즘

### 점수 계산

| 줄 제거 수 | 기본 점수 | 최종 = 기본 × 레벨 |
|-----------|----------|-------------------|
| 1줄 | 100 | 100 × level |
| 2줄 | 300 | 300 × level |
| 3줄 | 500 | 500 × level |
| 4줄 (Tetris) | 800 | 800 × level |

### 레벨 / 속도 진행

```
Level = (총 제거 줄 수 // 10) + 1
낙하 속도 = max(100ms, 500ms - (level - 1) × 50ms)
```

### 회전 (Wall Kick)

1. 피스 회전
2. 위치가 유효하지 않으면 `dx = [+1, -1, +2, -2]` 순으로 보정 시도
3. 모두 실패하면 회전 취소

### Ghost Piece

현재 피스가 낙하할 위치를 미리 보여주는 반투명 외곽선 (색상: `(80, 80, 80)`).

---

## 렌더링 파이프라인

`Game.draw()` 호출 순서 (뒤→앞):

1. `_draw_board()` — 고정 블록
2. `_draw_ghost()` — 고스트 피스
3. `_draw_current()` — 현재 낙하 피스
4. `_draw_grid()` — 격자 선
5. `_draw_sidebar()` — 점수/레벨/다음 피스/조작키 UI
6. `_draw_overlay()` — GAME OVER / PAUSE 오버레이

---

## 이벤트 처리 우선순위 (`main.py`)

```
1. game_over 상태 → R 키만 수락 (재시작)
2. P 키 → 일시정지 토글
3. paused 상태 → 게임 입력 모두 무시
4. 일반 게임 입력 처리 (←→↑↓ SPACE)
```

---

## 조작 키

| 키 | 동작 |
|----|------|
| ← → | 좌우 이동 |
| ↑ | 회전 |
| ↓ | 소프트 드롭 |
| SPACE | 하드 드롭 |
| P | 일시정지/재개 |
| R | 재시작 (게임 오버 시) |

---

## 테트로미노 색상

| 피스 | 색상 | RGB |
|------|------|-----|
| I | Cyan | (0, 255, 255) |
| O | Yellow | (255, 255, 0) |
| T | Purple | (128, 0, 128) |
| S | Green | (0, 255, 0) |
| Z | Red | (255, 0, 0) |
| J | Blue | (0, 0, 255) |
| L | Orange | (255, 165, 0) |

---

## 배경 이미지

- `bg.jpg` — 프로젝트 루트에 위치한 배경 이미지 파일
- 게임 시작 시 `SCREEN_WIDTH × SCREEN_HEIGHT` 크기로 스케일해서 로드
- 매 프레임 `screen.fill(BLACK)` 대신 `screen.blit(bg_image, (0, 0))`으로 렌더링
- 이미지 로드 실패 시 기존 검정 배경으로 자동 fallback
- 다른 이미지로 교체하려면 `bg.jpg`를 원하는 이미지로 덮어쓰면 됨

---

## 개발 노트

- 테스트 파일 없음 — 검증은 `_valid()` 충돌 감지와 수동 테스트에 의존
- 전역 변수 없음 — 게임 상태는 `Game` 인스턴스 하나로 완전히 관리
- `restart()`는 새 `__init__()`를 호출하는 방식으로 구현
- 키 반복: 초기 딜레이 200ms, 반복 간격 80ms (`pygame.key.set_repeat`)
- 타겟 프레임레이트: 60 FPS
