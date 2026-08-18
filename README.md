# 2단 CMOS Op-amp의 이상적 근사 유효 한계 규명

전기회로 과목에서 배우는 op-amp의 **이상적 근사**(`A_cl = 1 + Rf/R1`)가 실제로 어느 주파수까지 유효한지를 ngspice 시뮬레이션으로 정량적으로 규명한 학부생 개인 프로젝트입니다.

**[EN]** Investigated where the ideal op-amp approximation breaks down 
in a two-stage CMOS op-amp using ngspice. A_cl × f_break converges to 
theory at high gain but deviates up to ~65% at low gain; a VCVS control 
group (0.97%) confirms the cause is the circuit's non-dominant pole.

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

## 실행 방법

> 환경: WSL Ubuntu + ngspice. 회로 파일명은 `op_amp_lab.cir`(실제 회로), `vcvs.cl.cir`(대조군) 기준입니다.

**1. Open-loop 특성 측정 (A₀, GBW, PM)**
```bash
ngspice -b op_amp_lab.cir     # 실제 2단 CMOS op-amp
ngspice -b vcvs.cl.cir        # VCVS 대조군
```

**2. Cc 스윕 — PM 45°를 만족하는 최소 Cc(5pF) 결정**
```bash
for cc in 1p 2p 5p 10p 20p 50p; do
  echo "--- Cc = $cc ---"
  sed "s/^Cc d2 v0 5p/Cc d2 v0 $cc/" op_amp_lab.cir > tmp.cir
  ngspice -b tmp.cir 2>&1 | grep -E "a0_db|gbw_hz|pm_raw"
done
```

**3. 메인 sweep — 실제 회로 (A_cl 2~50, `results.txt` 생성)**
```bash
echo "# acl fbreak lowf group - lab" > results.txt
for cfg in "2 100k" "3 200k" "4 300k" "5 400k" "7 600k" "10 900k" "15 1400k" "20 1900k" "30 2900k" "50 4900k"; do
  set -- $cfg; acl=$1; rf=$2
  sed -e "s|^Rf v0 vin_l .*|Rf v0 vin_l $rf|" \
      -e "s|abs(acl_lin - [0-9]*) */ *[0-9]*|abs(acl_lin - $acl)/$acl|" \
      op_amp_lab.cir > tmp.cir
  out=$(ngspice -b tmp.cir 2>&1)
  fb=$(echo "$out" | grep '^f_break' | grep -oE '[0-9.]+e[+-][0-9]+')
  lowf=$(echo "$out" | grep 'acl_lowf' | grep -oE '[0-9.]+e[+-][0-9]+')
  echo "$acl $fb $lowf real" | tee -a results.txt
done
```

**4. 메인 sweep — VCVS 대조군 (`results.txt`에 append)**
```bash
echo "" >> results.txt
echo "#acl fbreak lowf group - vcvs" >> results.txt
for cfg in "2 100k" "3 200k" "4 300k" "5 400k" "7 600k" "10 900k" "15 1400k" "20 1900k" "30 2900k" "50 4900k"; do
  set -- $cfg; acl=$1; rf=$2
  sed -e "s|^Rf v0 vin_l .*|Rf v0 vin_l $rf|" \
      -e "s|abs(a - [0-9]*) */ *[0-9]*|abs(a - $acl)/$acl|" \
      vcvs.cl.cir > tmp.cir
  out=$(ngspice -b tmp.cir 2>&1)
  fb=$(echo "$out" | grep '^f_break' | grep -oE '[0-9.]+e[+-][0-9]+')
  lowf=$(echo "$out" | grep 'acl_lowf' | grep -oE '[0-9.]+e[+-][0-9]+')
  echo "$acl $fb $lowf vcvs" | tee -a results.txt
done
```

**5. Bode 곡선 데이터 생성 (그래프용, `data/cl_acl{N}.txt`)**
```bash
for cfg in "2 100k" "3 200k" "4 300k" "5 400k" "7 600k" "10 900k" "15 1400k" "20 1900k" "30 2900k" "50 4900k"; do
  set -- $cfg; acl=$1; rf=$2
  sed -e "s|^Rf v0 vin_l .*|Rf v0 vin_l $rf|" \
      -e "s|abs(acl_lin - [0-9]*) */ *[0-9]*|abs(acl_lin - $acl)/$acl|" \
      -e "s|wrdata [^ ]*|wrdata data/cl_acl${acl}.txt|" \
      op_amp_lab.cir > tmp.cir
  ngspice -b tmp.cir 2>&1 | grep -E "acl_lowf|f_break"
done
```

**6. Loading check (R1·Rf 10배, `loading_check.txt` 생성)**
```bash
for cfg in "2 1meg 1meg" "10 1meg 9meg" "50 1meg 49meg"; do
  set -- $cfg; acl=$1; r1=$2; rf=$3
  sed -e "s|^R1 vin_l 0 .*|R1 vin_l 0 $r1|" \
      -e "s|^Rf v0 vin_l .*|Rf v0 vin_l $rf|" \
      -e "s|abs(acl_lin - [0-9]*) */ *[0-9]*|abs(acl_lin - $acl)/$acl|" \
      op_amp_lab.cir > tmp.cir
  out=$(ngspice -b tmp.cir 2>&1)
  fb=$(echo "$out" | grep '^f_break' | grep -oE '[0-9.]+e[+-][0-9]+')
  lowf=$(echo "$out" | grep 'acl_lowf' | grep -oE '[0-9.]+e[+-][0-9]+')
  echo "$acl $fb $lowf load10x" | tee -a loading_check.txt
done
```

**7. 그래프 생성**
```bash
python fig1.py
python fig2.py
```

## 검증

측정 신뢰성을 위해 세 가지 검증을 수행했습니다.

1. **대조군 (VCVS)** — 2차 극점 없는 단일 극점 모델로 측정 파이프라인 무결성 확인
2. **Loading check** — R1·Rf를 비율 유지한 채 10배로 키워도 f_break가 1% 내외로 유지됨을 확인 (저항 절대값에 둔감)
3. **저주파 이득 검증** — 각 설정의 1kHz 이득이 이론값(`20·log A_cl`)과 일치함을 확인 (Rf 치환 무결성)

## 논문

전체 분석 과정과 이론 유도는 별도 논문 파일을 참고하세요.
