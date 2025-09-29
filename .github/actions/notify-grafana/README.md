# Notify Grafana Cloud Action

Esta acción envía métricas y eventos del pipeline DevSecOps a **Grafana Cloud** con integración modular para Loki, Prometheus y Annotations.

## 🎯 Características

- **📝 Loki Integration**: Envía eventos y logs del pipeline
- **📊 Prometheus Integration**: Envía métricas numéricas para dashboards y alertas
- **📋 Annotations Integration**: Marca eventos en líneas de tiempo
- **🔧 Modular**: Habilita/deshabilita integraciones independientemente
- **🚀 Fast**: Integración nativa con API de Grafana Cloud

## 🔧 Inputs

### Requeridos
- `grafana-url`: URL de la instancia Grafana Cloud (para annotations)
- `grafana-api-key`: API key o service account token
- `app-name`: Nombre de la aplicación
- `app-version`: Versión de la aplicación
- `environment`: Ambiente de deployment (dev, staging, prod)
- `build-status`: Estado del build (success, failure)

### Opcionales - URLs Específicas
- `loki-url`: URL del endpoint Loki (auto-detectada si no se proporciona)
- `prometheus-url`: URL del endpoint Prometheus (auto-detectada si no se proporciona)

### URLs por Región

| Región | Loki | Prometheus |
|--------|------|------------|
| **US Central** | `https://logs-prod-us-central1.grafana.net` | `https://prometheus-prod-us-central1.grafana.net` |
| **US East** | `https://logs-prod4.grafana.net` | `https://prometheus-prod-01-us-east-0.grafana.net` |
| **EU West** | `https://logs-prod-eu-west-0.grafana.net` | `https://prometheus-prod-01-eu-west-0.grafana.net` |

### Opcionales - Feature Flags
- `enable-loki`: Habilitar Loki (default: `true`)
- `enable-prometheus`: Habilitar Prometheus (default: `true`)
- `enable-annotations`: Habilitar Annotations (default: `true`)

### Opcionales - Métricas
- `vulnerabilities-critical`: Número de vulnerabilidades críticas (default: `0`)
- `vulnerabilities-high`: Número de vulnerabilidades altas (default: `0`)
- `vulnerabilities-medium`: Número de vulnerabilidades medias (default: `0`)
- `vulnerabilities-low`: Número de vulnerabilidades bajas (default: `0`)
- `code-coverage`: Porcentaje de cobertura de código (default: `0`)
- `execution-time`: Tiempo de ejecución en segundos (default: `0`)

## 📤 Outputs

- `status`: Estado general de la integración (`success`, `partial`, `failed`)
- `loki-status`: Estado de Loki (`success`, `failed`, `disabled`)
- `prometheus-status`: Estado de Prometheus (`success`, `failed`, `disabled`)
- `annotations-status`: Estado de Annotations (`success`, `failed`, `disabled`)
- `metrics-count`: Número de métricas enviadas

## 📋 Uso Básico

### Auto-detección de URLs (Recomendado)
```yaml
- name: Send to Grafana Cloud
  uses: ./shared-devsecops-actions/.github/actions/notify-grafana
  with:
    grafana-url: 'https://myorg.grafana.net'
    grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
    app-name: 'mi-aplicacion'
    app-version: '1.0.0'
    environment: 'production'
    build-status: 'success'
    vulnerabilities-critical: 0
    vulnerabilities-high: 2
    vulnerabilities-medium: 5
    vulnerabilities-low: 10
    code-coverage: 85
    execution-time: 120
```

### URLs Específicas por Región
```yaml
- name: Send to Grafana Cloud (US Central)
  uses: ./shared-devsecops-actions/.github/actions/notify-grafana
  with:
    grafana-url: 'https://myorg.grafana.net'
    loki-url: 'https://logs-prod-us-central1.grafana.net'
    prometheus-url: 'https://prometheus-prod-us-central1.grafana.net'
    grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
    app-name: 'mi-aplicacion'
    app-version: '1.0.0'
    environment: 'production'
    build-status: 'success'
```

### URLs Específicas para EU West
```yaml
- name: Send to Grafana Cloud (EU West)
  uses: ./shared-devsecops-actions/.github/actions/notify-grafana
  with:
    grafana-url: 'https://myorg.grafana.net'
    loki-url: 'https://logs-prod-eu-west-0.grafana.net'
    prometheus-url: 'https://prometheus-prod-01-eu-west-0.grafana.net'
    grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
    app-name: 'mi-aplicacion'
    app-version: '1.0.0'
    environment: 'production'
    build-status: 'success'
```

## 🔧 Uso Modular

### Solo Loki (Logs)
```yaml
- name: Send Logs to Loki
  uses: ./shared-devsecops-actions/.github/actions/notify-grafana
  with:
    grafana-url: 'https://myorg.grafana.net'
    grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
    app-name: 'mi-aplicacion'
    app-version: '1.0.0'
    environment: 'production'
    build-status: 'success'
    enable-prometheus: false
    enable-annotations: false
```

### Solo Prometheus (Métricas)
```yaml
- name: Send Metrics to Prometheus
  uses: ./shared-devsecops-actions/.github/actions/notify-grafana
  with:
    grafana-url: 'https://myorg.grafana.net'
    grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
    app-name: 'mi-aplicacion'
    app-version: '1.0.0'
    environment: 'production'
    build-status: 'success'
    vulnerabilities-critical: 0
    code-coverage: 85
    enable-loki: false
    enable-annotations: false
```

### Solo Annotations (Timeline)
```yaml
- name: Send Timeline Event
  uses: ./shared-devsecops-actions/.github/actions/notify-grafana
  with:
    grafana-url: 'https://myorg.grafana.net'
    grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
    app-name: 'mi-aplicacion'
    app-version: '1.0.0'
    environment: 'production'
    build-status: 'success'
    enable-loki: false
    enable-prometheus: false
```

## 🎯 Diferencias entre Componentes

| Componente | Propósito | Tipo de Datos | Uso |
|------------|-----------|---------------|-----|
| **📝 Loki** | Logs y eventos | Texto estructurado | Debugging, auditoría, contexto |
| **📊 Prometheus** | Métricas | Datos numéricos | Dashboards, alertas, tendencias |
| **📋 Annotations** | Timeline | Eventos puntuales | Marcas en gráficos, correlación |

## 🔒 Configuración de Secrets

Añade a tus secrets de repositorio:

```
GRAFANA_API_KEY=glsa_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🚀 Pipeline Completo

```yaml
name: DevSecOps Pipeline

on:
  push:
    branches: [main]

jobs:
  devsecops:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run Tests & Security Scan
        id: scan
        # ... tu pipeline de pruebas y seguridad
      
      - name: Send to Grafana Cloud
        uses: ./shared-devsecops-actions/.github/actions/notify-grafana
        with:
          grafana-url: 'https://myorg.grafana.net'
          grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
          app-name: ${{ github.event.repository.name }}
          app-version: ${{ github.sha }}
          environment: 'production'
          build-status: ${{ job.status }}
          vulnerabilities-critical: ${{ steps.scan.outputs.critical }}
          vulnerabilities-high: ${{ steps.scan.outputs.high }}
          vulnerabilities-medium: ${{ steps.scan.outputs.medium }}
          vulnerabilities-low: ${{ steps.scan.outputs.low }}
          code-coverage: ${{ steps.scan.outputs.coverage }}
          execution-time: ${{ steps.scan.outputs.time }}
```

## 📊 Métricas Enviadas

### Prometheus Metrics
- `devsecops_build_status{app, version, environment}`: Estado del build (1=success, 0=failure)
- `devsecops_vulnerabilities_total{app, severity, environment}`: Total de vulnerabilidades por severidad
- `devsecops_code_coverage_percent{app, environment}`: Porcentaje de cobertura
- `devsecops_execution_time_seconds{app, environment}`: Tiempo de ejecución

### Loki Logs
- Pipeline status y contexto
- Resultados de seguridad detallados
- Métricas de calidad

### Annotations
- Eventos de deployment
- Estados de pipeline
- Correlación temporal