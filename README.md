# 2단 CMOS Op-amp의 이상적 근사 유효 한계 규명

전기회로 과목에서 배우는 op-amp의 **이상적 근사**(`A_cl = 1 + Rf/R1`)가 실제로 어느 주파수까지 유효한지를 ngspice 시뮬레이션으로 정량적으로 규명한 학부 프로젝트입니다.

## 개요

교과서는 op-amp의 이상적 조건만 제시할 뿐, 그 근사가 성립하는 범위는 다루지 않습니다. 본 연구는 2단 Miller-compensated CMOS op-amp를 transistor-level로 구현하고, 여러 closed-loop gain에서 이상적 근사가 5% 이상 벗어나는 주파수(`f_break`)를 측정하여 근사의 유효 한계를 정량화합니다.

핵심 지표는 `A_cl × f_break`이며, 단일 극점 이론에 따르면 이 곱은 gain과 무관하게 `0.329 × GBW`로 일정해야 합니다.

## 주요 결과

- **고이득 구간**: `A_cl × f_break`가 이론값에 수렴 (A_cl=50에서 오차 0.1% 미만)
- **저이득 구간**: 이론값에서 이탈, A_cl=2에서 최대 약 65% 차이 (본 실험 조건 기준)
- **대조군(VCVS)**: 2차 극점이 없는 단일 극점 모델은 0.97%만 변동 → 저이득 이탈이 측정 방식이 아닌 **2차 극점(회로 특성)**에서 비롯됨을 확인

측정된 회로 특성: A₀ ≈ 93.4 dB, GBW ≈ 4.81 MHz, PM ≈ 53.4°, Cc = 5 pF

## 파일 구조

```
.
├── netlists/
│   ├── op_amp_lab.cir      # 실제 2단 CMOS op-amp (main)
│   ├── op_amp_std.cir      # 표준 파라미터 회로
│   └── vcvs_cl.cir         # 대조군 (VCVS 단일 극점 모델)
├── scripts/
│   ├── fig1.py             # 결과 그래프 1: A_cl × f_break vs 이론값
│   └── fig2.py             # 결과 그래프 2: Bode plot + f_break 마커
├── data/
│   ├── cl_acl{2..50}.txt   # 각 A_cl의 closed-loop AC 응답
│   ├── openloop.txt        # open-loop 응답 (A₀, GBW, PM 측정용)
│   ├── results.txt         # real·vcvs f_break 및 저주파 이득 취합
│   └── loading_check.txt   # loading check 검증 데이터
└── figures/                # 생성된 그래프
```

## 환경

- **OS**: WSL Ubuntu
- **시뮬레이터**: [ngspice](http://ngspice.sourceforge.net/) (Level-1 MOSFET 모델)
- **분석**: Python (NumPy, matplotlib)

## 실행 방법

<!-- TODO: 실제로 돌린 sweep 스크립트/명령으로 교체 -->
```bash
# 1. A_cl sweep — 각 설정의 f_break 측정 및 results.txt 생성
#    (실제 사용한 bash 루프 / 명령을 여기에 입력)

# 2. 그래프 생성
python scripts/fig1.py
python scripts/fig2.py
```

## 검증

측정 신뢰성을 위해 세 가지 검증을 수행했습니다.

1. **대조군 (VCVS)** — 2차 극점 없는 단일 극점 모델로 측정 파이프라인 무결성 확인
2. **Loading check** — R1·Rf를 비율 유지한 채 10배로 키워도 f_break가 1% 내외로 유지됨을 확인 (저항 절대값에 둔감)
3. **저주파 이득 검증** — 각 설정의 1kHz 이득이 이론값(`20·log A_cl`)과 일치함을 확인 (Rf 치환 무결성)

## 논문

전체 분석 과정과 이론 유도는 별도 논문 파일을 참고하세요.
