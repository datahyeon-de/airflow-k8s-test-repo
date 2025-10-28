# Airflow Kubernetes Test Repository

이 레포지토리는 Airflow의 Git-Sync 기능을 테스트하기 위한 예제 DAG 파일들을 포함합니다.

## 폴더 구조

```
airflow-k8s-test-repo/
├── dags/              # DAG 파일들 (Git에 저장)
├── plugins/           # 커스텀 플러그인 (Git에 저장)
├── logs/              # 실행 로그 (.gitignore됨)
├── config/            # 설정 파일들
└── README.md          # 이 파일
```

## 중요: 로그는 Git에 저장되지 않습니다

### 로그 저장 방식

**Git 레포에는 코드만 저장:**
- ✅ DAG 파일들 (dags/)
- ✅ 커스텀 플러그인 (plugins/)
- ✅ 설정 파일 (config/)
- ❌ 실행 로그 (logs/) - `.gitignore` 처리됨

**로그는 Kubernetes PVC에 저장:**
- 위치: `/Users/limseonghyeon/DATA/end2end-airflow/logs/`
- 크기: 20Gi
- 보존 기간: 설정에 따라 자동 삭제

### 로그 동작 원리

```
1. DAG 실행 시작
   ↓
2. Worker Pod에서 태스크 실행
   ↓
3. 로그는 PVC(영구 저장소)에 직접 기록
   └── /DATA/end2end-airflow/logs/dag_id/task_id/attempt/
   ↓
4. Worker Pod 종료 (백그라운드 실행시)
   ↓
5. 로그는 PVC에 그대로 유지됨 ✅
```

### 로그 구조 예시

```
/DATA/end2end-airflow/logs/
├── dag_id=example_bash_dag/
│   ├── run_id=scheduled__2025-01-15T00:00:00+00:00/
│   │   ├── task_id=print_date/
│   │   │   ├── attempt=1.log
│   │   │   └── ...
│   │   └── task_id=print_env/
│   │       └── attempt=1.log
│   └── ...
```

### PVC vs EmptyDir

**현재 설정 (persistence.enabled: true):**
```yaml
logs:
  persistence:
    enabled: true           # ✅ PVC 사용 (영구 저장)
    existingClaim: end2end-airflow-logs
    size: 20Gi
```

**만약 persistence.enabled: false라면:**
```yaml
logs:
  persistence:
    enabled: false          # ❌ EmptyDir 사용
    # 파드가 삭제되면 로그도 삭제됨!
```

### 로그 조회 방법

1. **웹 UI에서 조회:**
   - Airflow UI → DAG → Task → Log

2. **직접 PVC에서 조회:**
   ```bash
   # macOS/Docker Desktop
   ls -la /Users/limseonghyeon/DATA/end2end-airflow/logs/
   ```

3. **Kubernetes에서 조회:**
   ```bash
   kubectl exec -it <pod-name> -n end2end-airflow -- cat /opt/airflow/logs/...
   ```

## Git-Sync 설정

이 레포를 Airflow에서 사용하려면 `values.yaml`에서 다음을 설정:

```yaml
dags:
  persistence:
    enabled: false  # Git-Sync 사용 시
  gitSync:
    enabled: true
    repo: https://github.com/YOUR_USERNAME/airflow-k8s-test-repo.git
    ref: main
    subPath: "dags"
    period: 300s
```

## 테스트 시나리오

1. 이 레포를 GitHub에 push
2. Git-Sync 설정 적용
3. Airflow 파드들이 DAG 자동으로 가져옴
4. DAG 실행 → 로그는 PVC에 저장
5. 웹 UI에서 로그 확인

