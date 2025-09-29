# Ejemplo de uso del workflow DevSecOps

Este es un ejemplo de cómo usar el workflow DevSecOps con integración a Grafana Cloud desde tu repositorio de aplicación.

## 📁 Estructura del repositorio de aplicación

```
mi-aplicacion/
├── .github/
│   └── workflows/
│       └── ci-cd.yml
├── src/
├── pom.xml
└── Dockerfile
```

## 🚀 Workflow de ejemplo (`mi-aplicacion/.github/workflows/ci-cd.yml`)

```yaml
name: 'DevSecOps Pipeline'

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  devsecops:
    name: 'DevSecOps Pipeline'
    uses: mvasquez13/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
    with:
      # Aplicación
      app-name: 'mi-aplicacion'
      java-version: '17'
      maven-version: '3.9'
      
      # Quality Gates
      coverage-threshold: 80
      fail-on-critical-vulnerabilities: true
      
      # Kubernetes
      k8s-namespace: 'mi-aplicacion'
      
      # Grafana Cloud Integration
      grafana-url: 'https://mibanco.grafana.net'
      enable-grafana-metrics: true
      
    secrets:
      registry-username: ${{ secrets.DOCKER_USERNAME }}
      registry-password: ${{ secrets.DOCKER_PASSWORD }}
      grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
```

## 🔧 Configuración de Secrets

En tu repositorio de aplicación, añade estos secrets:

### GitHub Secrets (`Settings > Secrets and variables > Actions`)

```bash
DOCKER_USERNAME=tu-usuario-docker
DOCKER_PASSWORD=tu-password-docker
GRAFANA_API_KEY=glsa_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Variables de Repositorio (Opcional)

```bash
GRAFANA_URL=https://mibanco.grafana.net
```

## 📊 Datos que se envían automáticamente a Grafana

### 🎯 Datos Dinámicos Capturados

| Métrica | Fuente | Descripción |
|---------|--------|-------------|
| **app-name** | `inputs.app-name` | Nombre de la aplicación |
| **app-version** | `build.outputs.semantic-version` | Versión semántica generada |
| **environment** | Detección automática de branch | `main`→production, `develop`→staging, otros→development |
| **build-status** | Resultado de todos los jobs | `success`, `failure`, `partial` |
| **vulnerabilities-critical** | SAST + SCA | Suma de vulnerabilidades críticas |
| **vulnerabilities-high** | SAST + SCA | Suma de vulnerabilidades altas |
| **vulnerabilities-medium** | SAST + SCA | Suma de vulnerabilidades medias |
| **vulnerabilities-low** | SAST + SCA | Suma de vulnerabilidades bajas |
| **code-coverage** | Tests de Maven | Porcentaje de cobertura |
| **execution-time** | Build job | Tiempo total en segundos |

### 🔄 Flujo de Datos

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Build     │───▶│    SAST     │───▶│     SCA     │───▶│   Notify    │
│   + Tests   │    │  Analysis   │    │  Analysis   │    │  Grafana    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
 • app-version        • sast-critical    • sca-critical     • Calcula totales
 • code-coverage      • sast-high        • sca-high         • Determina status
 • execution-time     • sast-medium      • sca-medium       • Envía a Grafana
 • build-status       • sast-low         • sca-low
```

## 🎯 Configuración Avanzada

### Solo métricas específicas
```yaml
- name: Send only Security Metrics
  uses: mvasquez13/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
  with:
    app-name: 'mi-aplicacion'
    grafana-url: 'https://mibanco.grafana.net'
    enable-grafana-metrics: true
  secrets:
    grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
```

### Por ambiente
```yaml
# Producción: Todas las integraciones
- name: Production Pipeline
  if: github.ref == 'refs/heads/main'
  uses: mvasquez13/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
  with:
    grafana-url: 'https://mibanco.grafana.net'
    enable-grafana-metrics: true
    fail-on-critical-vulnerabilities: true

# Desarrollo: Solo métricas básicas  
- name: Development Pipeline
  if: github.ref != 'refs/heads/main'
  uses: mvasquez13/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
  with:
    grafana-url: 'https://mibanco-dev.grafana.net'
    enable-grafana-metrics: true
    fail-on-critical-vulnerabilities: false
```

## 📈 Dashboards en Grafana

Con estos datos automáticos podrás crear dashboards que muestren:

- **📊 Métricas de Build**: Tiempo de ejecución, tasa de éxito
- **🔍 Seguridad**: Trend de vulnerabilidades por aplicación
- **📋 Calidad**: Cobertura de código por proyecto
- **🌍 Por Ambiente**: Métricas separadas por environment
- **⏰ Timeline**: Eventos de deployment y fallos

## 🚀 Resultado

Cada ejecución del pipeline enviará automáticamente:

1. **📝 Loki**: Logs estructurados del pipeline
2. **📊 Prometheus**: 6 métricas numéricas para dashboards
3. **📋 Annotations**: Eventos de timeline para correlación

¡Todo configurado automáticamente sin intervención manual! 🎉