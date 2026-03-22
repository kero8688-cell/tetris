# Tetris (Python + pygame)

Python과 pygame으로 만든 클래식 테트리스 게임입니다.

## 폴더 구조

```
tryProject/
├── main.py            # 진입점 (게임 루프)
├── requirements.txt   # 의존 패키지
├── .gitignore
└── tetris/
    ├── __init__.py
    ├── pieces.py      # 테트리미노 모양 / 색상 / 회전 정의
    └── game.py        # 보드 로직, 충돌, 라인 클리어, 렌더링
```

## 설치 및 실행

```bash
# 1. 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate   # macOS/Linux
# venv\Scripts\activate    # Windows

# 2. 의존 패키지 설치
pip install -r requirements.txt

# 3. 게임 실행
python main.py
```

## 조작법

| 키 | 동작 |
|---|---|
| ← → | 좌우 이동 |
| ↑ | 회전 |
| ↓ | 소프트 드롭 |
| Space | 하드 드롭 |
| P | 일시정지 / 재개 |
| R | 게임 오버 후 재시작 |

## 점수 체계

| 클리어 라인 수 | 점수 |
|---|---|
| 1줄 | 100 × 레벨 |
| 2줄 | 300 × 레벨 |
| 3줄 | 500 × 레벨 |
| 4줄 (테트리스) | 800 × 레벨 |

- 소프트 드롭: 1칸당 +1점
- 하드 드롭: 1칸당 +2점
- 10줄 클리어마다 레벨 1 상승, 낙하 속도 증가
