# MiBanco Shared DevSecOps Actions

Librería centralizada de GitHub Actions reutilizables para estandarizar pipelines DevSecOps en la organización MiBanco. Implementa un enfoque **template-based** para manifiestos de Kubernetes, integración completa con **Grafana Cloud** para métricas DevSecOps, y optimización para repositorios públicos utilizando herramientas **gratuitas** de GitHub.

## 🏗️ Arquitectura DevSecOps

Este repositorio contiene componentes modulares y reutilizables que implementan las mejores prácticas DevSecOps con integración completa de métricas y deployment.

```
shared-devsecops-actions/
├── .github/
│   ├── workflows/
│   │   └── aks_tpl.yml                     # Pipeline principal DevSecOps
│   └── actions/                            # Actions compuestos modulares
│       ├── build-app/                      # Compilación Maven/Spring Boot
│       │   ├── action.yml
│       │   └── README.md
│       ├── build-docker-image/             # Construcción Docker + Semantic Versioning
│       │   ├── action.yml
│       │   └── README.md
│       ├── container-scan/                 # Trivy container scanning
│       │   ├── action.yml
│       │   └── README.md
│       ├── sast-scanner/                   # GitHub CodeQL SAST
│       │   ├── action.yml
│       │   └── README.md
│       ├── sca-scanner/                    # GitHub Advisory DB SCA
│       │   ├── action.yml
│       │   └── README.md
│       ├── dast-scanner/                   # OWASP ZAP DAST
│       │   ├── action.yml
│       │   └── README.md
│       ├── deploy-k8s/                     # 🆕 Template-based K8s Deployment
│       │   ├── action.yml                  # Action principal usando templates
│       │   ├── generate-manifest.sh        # Script generador de manifests
│       │   ├── maven-manifest.yml          # Template parametrizado para Spring Boot
│       │   ├── manifest-vars.env           # Variables de ejemplo
│       │   ├── README-template.md          # Documentación del template
│       │   ├── README-action-usage.md      # Documentación del action
│       │   └── mibanco-production.yml      # Ejemplo generado
│       └── notify-grafana/                 # 🆕 Integración Grafana Cloud
│           ├── action.yml                  # Action para envío de métricas
│           ├── send_data.py                # Script Python con prometheus-remote-writer
│           ├── grafana-dashboard.json      # Dashboard DevSecOps completo
│           ├── import-dashboard.sh         # Script para importar dashboard
│           └── README.md                   # Documentación Grafana
├── docs/                                   # 🆕 Documentación técnica
│   ├── architecture.md                     # Arquitectura del sistema
│   ├── deployment-guide.md                 # Guía de deployment
│   └── troubleshooting.md                  # Resolución de problemas
└── README.md                               # Esta documentación
```

## 🆕 **Nuevas Características Implementadas**

### **📊 Integración Grafana Cloud**
- ✅ **Dashboard DevSecOps** completo con métricas en tiempo real
- ✅ **Script Python** para envío directo a Prometheus
- ✅ **Métricas de vulnerabilidades** por severidad (CRITICAL, HIGH, MEDIUM, LOW)
- ✅ **Métricas de build** (duración, estado, cobertura)
- ✅ **Visualización temporal** de tendencias de seguridad
- ✅ **Alertas configurables** para umbrales críticos

### **🎯 Template-Based Kubernetes Deployment**
- ✅ **Template parametrizado** para aplicaciones Spring Boot
- ✅ **Script generador** de manifests con variables dinámicas
- ✅ **Soporte multi-entorno** (dev, staging, prod)
- ✅ **Security best practices** incluidas por defecto
- ✅ **Recursos K8s completos**: Deployment, Service, Ingress, HPA, NetworkPolicy
- ✅ **Validación automática** de manifests antes del deployment

### **🔧 Mejoras en Container Scanning**
- ✅ **Reporte completo** de vulnerabilidades incluye severidad LOW
- ✅ **Integración mejorada** con métricas de Grafana
- ✅ **JSON parsing** optimizado para Trivy
- ✅ **Debugging** enhanzado para troubleshooting

## 🚀 Uso Avanzado

### **Pipeline DevSecOps Completo con Grafana Integration:**

```yaml
name: MiBanco DevSecOps Pipeline with Metrics
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  devsecops-pipeline:
    uses: mibanco-org/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
    with:
      # Configuración de aplicación
      app-name: 'mibanco-core-api'
      java-version: '17'
      maven-version: '3.9'
      
      # Configuración Docker
      registry-url: 'mibancoregistry.azurecr.io'
      dockerfile-path: './Dockerfile'
      
      # 🆕 Configuración de métricas Grafana
      enable-grafana-metrics: true
      grafana-endpoint: 'https://prometheus-prod-24-prod-eu-west-2.grafana.net/api/prom/push'
      
      # Configuración de seguridad (GitHub gratuito)
      enable-sast: true           # CodeQL gratuito para repos públicos
      enable-sca: true            # GitHub Advisory DB gratuito
      enable-container-scan: true # Trivy gratuito
      enable-dast: true           # OWASP ZAP
      
      # 🆕 Configuración de despliegue con templates
      enable-deploy-staging: true
      enable-deploy-prod: true
      k8s-template-mode: true     # Usa templates parametrizados
      staging-namespace: 'mibanco-staging'
      prod-namespace: 'mibanco-production'
      
    secrets:
      # Credenciales de registry
      registry-username: ${{ secrets.ACR_USERNAME }}
      registry-password: ${{ secrets.ACR_PASSWORD }}
      
      # 🆕 Credenciales Grafana Cloud
      grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
      
      # Credenciales Kubernetes
      azure-credentials: ${{ secrets.AZURE_CREDENTIALS }}
      
      # Notificaciones (opcional)
      teams-webhook: ${{ secrets.TEAMS_WEBHOOK_URL }}
```

### **🎯 Deployment con Templates Personalizados:**

```yaml
# Deployment específico con template customizado
- name: Deploy to Production with Custom Template
  uses: ./shared-devsecops-actions/.github/actions/deploy-k8s
  with:
    registry: 'mibancoregistry.azurecr.io'
    image-name: 'mibanco-core-api'
    image-tag: 'v2.1.0'
    app-name: 'mibanco-core-api'
    namespace: 'production'
    environment: 'prod'
    replicas: '5'
    ingress-host: 'api.mibanco.com'
    manifests-path: './k8s-manifests'
    azure-credentials: ${{ secrets.AZURE_CREDENTIALS }}
    cluster-name: 'aks-production'
    resource-group: 'rg-mibanco-prod'
    registry-username: ${{ secrets.ACR_USERNAME }}
    registry-password: ${{ secrets.ACR_PASSWORD }}
```

### **📊 Grafana Dashboard Setup:**

```bash
# Importar dashboard DevSecOps a Grafana
cd shared-devsecops-actions/.github/actions/notify-grafana
./import-dashboard.sh \
  --grafana-url "https://mibanco.grafana.net" \
  --api-key "$GRAFANA_API_KEY" \
  --dashboard-file "grafana-dashboard.json"
```
      
      # Configuración de seguridad (GitHub gratuito)
      enable-sast: true           # CodeQL gratuito para repos públicos
      enable-sca: true            # GitHub Advisory DB gratuito
      enable-container-scan: true # Trivy gratuito
      enable-dast: false          # Solo si es necesario
      
      # Configuración de despliegue
      enable-deploy-staging: false  # Habilitar cuando tengas AKS configurado
      enable-deploy-prod: false     # Habilitar cuando tengas AKS configurado
      
    secrets:
      # Credenciales de registry (Azure Container Registry)
      registry-username: ${{ secrets.ACR_USERNAME }}
      registry-password: ${{ secrets.ACR_PASSWORD }}
      
      # Credenciales de Kubernetes (cuando esté listo)
      # kube-config: ${{ secrets.KUBE_CONFIG }}
      
      # Notificaciones Teams (opcional)
      # teams-webhook: ${{ secrets.TEAMS_WEBHOOK_URL }}
```

## 📋 Actions Modulares Disponibles

| Action | Descripción | Herramientas | Estado | Costo |
|--------|-------------|--------------|--------|-------|
| `build-app` | Compilación Maven + Tests + JaCoCo + SpotBugs | Maven, JaCoCo, SpotBugs | ✅ Estable | ✅ Gratuito |
| `build-docker-image` | Construcción Docker con semantic versioning | Docker, GitVersion | ✅ Estable | ✅ Gratuito |
| `sast-scanner` | Análisis estático de código | **GitHub CodeQL** | ✅ Estable | ✅ Gratuito (repos públicos) |
| `sca-scanner` | Análisis de vulnerabilidades en dependencias | **GitHub Advisory DB** | ✅ Estable | ✅ Gratuito |
| `container-scan` | Escaneo de vulnerabilidades en contenedores | **Trivy** | 🆕 Mejorado | ✅ Gratuito |
| `dast-scanner` | Análisis dinámico de aplicaciones web | OWASP ZAP | ✅ Estable | ✅ Gratuito |
| `deploy-k8s` | Despliegue template-based en AKS | kubectl, templates | 🆕 Template-based | ✅ Gratuito |
| `notify-grafana` | Envío de métricas DevSecOps a Grafana Cloud | Python, Prometheus | 🆕 Nuevo | ✅ Gratuito |

### **🆕 Detalles de Actions Actualizados**

#### **deploy-k8s (Template-Based)**
- **Template**: `maven-manifest.yml` parametrizado
- **Script**: `generate-manifest.sh` con CLI completa
- **Recursos**: Namespace, Deployment, Service, Ingress, HPA, NetworkPolicy
- **Entornos**: dev, staging, prod con configuraciones específicas
- **Validación**: Pre-deployment manifest validation
- **Security**: Security contexts, resource limits, network policies

#### **notify-grafana (Metrics Integration)**
- **Script**: `send_data.py` con prometheus-remote-writer
- **Dashboard**: Dashboard DevSecOps pre-configurado
- **Métricas**: Vulnerabilidades, builds, coverage, deployment status
- **Alerting**: Configuración de alertas por severidad
- **Visualización**: Time series, pie charts, gauges, tables

#### **container-scan (Enhanced)**
- **Scanner**: Trivy con output JSON completo
- **Severidades**: CRITICAL, HIGH, MEDIUM, LOW (todas incluidas)
- **Outputs**: Counts por severidad para integración con metrics
- **Debugging**: Logs detallados para troubleshooting

## � Seguridad Nativa de GitHub

### **GitHub CodeQL (SAST)**
- ✅ **Gratuito** para repositorios públicos
- ✅ Análisis estático para Java, JavaScript, Python, C#, etc.
- ✅ Integración nativa con GitHub Security
- ✅ SARIF reports automáticos

### **GitHub Advisory Database (SCA)**
- ✅ **Gratuito** para repositorios públicos
- ✅ Base de datos de vulnerabilidades actualizada
- ✅ Integración con Dependabot
- ✅ Alertas automáticas de seguridad

### **Dependabot (Recomendado)**
Para monitoreo continuo, habilita Dependabot agregando `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "maven"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    reviewers:
      - "security-team"
    labels:
      - "dependencies"
      - "security"
```

## 🎯 Casos de Uso Avanzados

### **1. Aplicación Maven con Métricas Completas**
```yaml
jobs:
  pipeline:
    uses: mibanco-org/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
    with:
      app-name: 'api-productos'
      java-version: '17'
      registry-url: 'mibancoregistry.azurecr.io'
      
      # Seguridad completa
      enable-sast: true
      enable-sca: true
      enable-container-scan: true
      enable-dast: true
      
      # 🆕 Métricas DevSecOps
      enable-grafana-metrics: true
      grafana-endpoint: 'https://prometheus-prod-24-prod-eu-west-2.grafana.net/api/prom/push'
      
    secrets:
      grafana-api-key: ${{ secrets.GRAFANA_API_KEY }}
      registry-username: ${{ secrets.ACR_USERNAME }}
      registry-password: ${{ secrets.ACR_PASSWORD }}
```

### **2. Deployment Multi-Entorno con Templates**
```yaml
jobs:
  deploy-staging:
    uses: mibanco-org/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
    with:
      app-name: 'core-banking'
      environment: 'staging'
      k8s-template-mode: true
      staging-replicas: '3'
      staging-ingress-host: 'staging-api.mibanco.com'
      
  deploy-production:
    needs: deploy-staging
    uses: mibanco-org/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
    with:
      app-name: 'core-banking'
      environment: 'prod'
      k8s-template-mode: true
      prod-replicas: '5'
      prod-ingress-host: 'api.mibanco.com'
    secrets:
      azure-credentials: ${{ secrets.AZURE_CREDENTIALS_PROD }}
```

### **3. Pipeline de Desarrollo con Templates Locales**
```yaml
# Generar manifests localmente para testing
- name: Generate K8s Manifests
  run: |
    cd shared-devsecops-actions/.github/actions/deploy-k8s
    ./generate-manifest.sh \
      --app-name my-app \
      --namespace development \
      --environment dev \
      --registry myregistry.azurecr.io \
      --tag dev-latest \
      --replicas 1 \
      --ingress-host dev-app.local \
      --output-file dev-manifest.yml
    
    # Validar sin aplicar
    kubectl apply --dry-run=client -f dev-manifest.yml
```

## 📊 Dashboard DevSecOps en Grafana

### **Métricas Incluidas:**
- 🏗️ **Build Metrics**: Duración, estado, frecuencia
- 🔒 **Security Metrics**: Vulnerabilidades por severidad y tipo
- 📊 **Coverage Metrics**: Cobertura de código y tests
- 🚀 **Deployment Metrics**: Frecuencia, éxito/fallo, tiempo de deployment
- 📈 **Trend Analysis**: Evolución temporal de métricas

### **Paneles del Dashboard:**
1. **Overview** - Resumen ejecutivo de métricas DevSecOps
2. **Security Status** - Estado de seguridad por aplicación
3. **Build Health** - Salud del pipeline de builds
4. **Deployment Tracking** - Seguimiento de deployments
5. **Vulnerability Trends** - Tendencias de vulnerabilidades
6. **Performance Metrics** - Métricas de rendimiento del pipeline

### **Configuración de Alertas:**
```yaml
# Ejemplo de configuración de alerta
- alert: CriticalVulnerabilities
  expr: devsecops_vulnerabilities{severity="CRITICAL"} > 0
  for: 0m
  labels:
    severity: critical
  annotations:
    summary: "Vulnerabilidades críticas detectadas"
    description: "{{ $value }} vulnerabilidades críticas encontradas en {{ $labels.app }}"
```

## ⚙️ Configuración Requerida

### **Secrets del Repositorio (GitHub):**
```bash
# Azure Container Registry
ACR_USERNAME=mibancoregistry
ACR_PASSWORD=<acr-access-token>

# Azure Kubernetes Service
AZURE_CREDENTIALS='{
  "clientId": "<client-id>",
  "clientSecret": "<client-secret>",
  "subscriptionId": "<subscription-id>",
  "tenantId": "<tenant-id>"
}'

# 🆕 Grafana Cloud Integration
GRAFANA_API_KEY=<grafana-cloud-api-key>

# Kubernetes (alternativo a Azure Credentials)
KUBE_CONFIG=<base64-encoded-kubeconfig>

# Notificaciones (opcional)
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
```

### **Variables de Entorno del Pipeline:**
```yaml
env:
  # 🆕 Grafana Configuration
  GRAFANA_ENDPOINT: 'https://prometheus-prod-24-prod-eu-west-2.grafana.net/api/prom/push'
  GRAFANA_USERNAME: 'your-grafana-username'
  
  # SonarQube (opcional)
  SONAR_TOKEN: '<sonarqube-token>'
  SONAR_HOST_URL: 'https://sonarqube.mibanco.com'
  
  # Application Configuration
  MAVEN_OPTS: '-Xmx2048m'
  JAVA_TOOL_OPTIONS: '-XX:+UseContainerSupport'
```

### **🆕 Configuración de Templates K8s:**
```bash
# Variables para generación de manifests
cd shared-devsecops-actions/.github/actions/deploy-k8s

# Copiar y personalizar variables
cp manifest-vars.env mibanco-vars.env

# Editar con configuración específica
cat > mibanco-vars.env << EOF
APP_NAME=mibanco-core-api
NAMESPACE=production
IMAGE_REGISTRY=mibancoregistry.azurecr.io
IMAGE_TAG=v1.0.0
REPLICAS=5
ENVIRONMENT=prod
INGRESS_HOST=api.mibanco.com
EOF
```

### **🆕 Setup Grafana Dashboard:**
```bash
# Importar dashboard automáticamente
cd shared-devsecops-actions/.github/actions/notify-grafana

# Método 1: Script automático
./import-dashboard.sh \
  --grafana-url "https://mibanco.grafana.net" \
  --api-key "$GRAFANA_API_KEY" \
  --dashboard-file "grafana-dashboard.json"

# Método 2: Manual import
# 1. Abrir Grafana UI
# 2. Ir a Dashboards > Import
# 3. Subir grafana-dashboard.json
# 4. Configurar data source: Prometheus
```

## 📊 Reportes y Métricas Avanzadas

### **🆕 Métricas DevSecOps en Tiempo Real:**
- 📈 **Build Metrics**: Duración, estado, frecuencia por aplicación
- 🔒 **Security Metrics**: Vulnerabilidades CRITICAL/HIGH/MEDIUM/LOW
- � **Coverage Metrics**: Cobertura de código, líneas cubiertas
- 🚀 **Deployment Metrics**: Frecuencia, éxito/fallo, MTTR
- � **Trend Analysis**: Evolución temporal de todas las métricas
- ⚠️ **Alert Management**: Alertas configurables por umbrales

### **Reportes Automáticos Generados:**
- 📈 **JaCoCo Coverage Report** (HTML + XML + CSV)
- 🔍 **Trivy Security Report** (JSON + SARIF)
- � **SpotBugs Analysis Report** (XML + HTML)
- �📋 **Surefire Test Results** (XML + TXT)
- 🐳 **Docker Image Metadata** (labels, tags, size)
- 📤 **GitHub Step Summary** con métricas visuales

### **🆕 Dashboard DevSecOps Features:**
- **Real-time metrics** con actualización automática
- **Multi-application view** para organizaciones
- **Drill-down capabilities** desde overview hasta detalles
- **Time range selection** (1h, 24h, 7d, 30d)
- **Filtering by**: application, environment, severity
- **Export capabilities** para reportes ejecutivos

### **Artifacts Disponibles:**
```yaml
# Descarga automática de artifacts
- build-artifacts/
  ├── target/
  │   ├── *.jar                    # Aplicación compilada
  │   ├── jacoco.exec             # Coverage data
  │   └── site/jacoco/            # Coverage HTML report
  ├── security-reports/
  │   ├── trivy-report.json       # Container vulnerabilities
  │   ├── sarif-results/          # SAST/SCA SARIF files
  │   └── spotbugs.xml           # Code quality issues
  └── k8s-manifests/
      └── deployment.yml          # 🆕 Generated K8s manifest
```

## 🚀 Beneficios del Sistema DevSecOps

### **💰 Económicos:**
- ✅ **100% Gratuito** para repositorios públicos
- ✅ **Herramientas nativas** de GitHub (CodeQL, Advisory DB)
- ✅ **Sin costos adicionales** de herramientas third-party
- ✅ **ROI inmediato** con reducción de vulnerabilidades

### **🔧 Técnicos:**
- ✅ **Template-based deployment** para consistencia
- ✅ **Modular y reutilizable** entre aplicaciones
- ✅ **Semantic versioning** automático
- ✅ **Integración completa** con GitHub Security
- ✅ **Escalable** para múltiples equipos
- ✅ **Mantenimiento centralizado**

### **📊 Observabilidad:**
- ✅ **Métricas en tiempo real** con Grafana Cloud
- ✅ **Dashboard DevSecOps** pre-configurado
- ✅ **Alerting inteligente** por severidad
- ✅ **Trazabilidad completa** del pipeline
- ✅ **Trend analysis** para mejora continua

### **🔒 Seguridad:**
- ✅ **Shift-left security** integrado
- ✅ **Multi-layer scanning** (SAST, SCA, Container, DAST)
- ✅ **Security by design** en templates K8s
- ✅ **Compliance reporting** automático
- ✅ **Vulnerability management** centralizado

## �️ Mantenimiento y Governance

### **Ownership y Responsabilidades:**
- **Owner**: DevSecOps Team MiBanco
- **Maintainers**: Platform Engineering Team
- **Contributors**: Development Teams
- **Security Review**: InfoSec Team

### **Versionado y Releases:**
- **Versioning**: Semantic Versioning (v1.0.0, v1.1.0, v2.0.0)
- **Release Cycle**: Mensual para features, inmediato para security fixes
- **Branch Strategy**: 
  - `main` - Production stable
  - `develop` - Integration branch
  - `feature/*` - Feature development
  - `hotfix/*` - Emergency fixes

### **Quality Gates:**
```yaml
# Criterios de calidad requeridos
quality_gates:
  security:
    critical_vulnerabilities: 0      # Cero vulnerabilidades críticas
    high_vulnerabilities: <= 5       # Máximo 5 vulnerabilidades altas
    sast_issues: <= 10               # Máximo 10 issues SAST
  
  testing:
    code_coverage: >= 80%            # Mínimo 80% cobertura
    test_success_rate: 100%          # Todos los tests deben pasar
    build_time: <= 10min             # Build máximo 10 minutos
  
  deployment:
    manifest_validation: required    # Validación de manifests obligatoria
    security_context: required      # Security contexts en K8s
    resource_limits: required       # Resource limits definidos
```

### **🔄 Updates y Maintenance:**
- **Dependabot**: Automático para dependencies
- **Security Updates**: Inmediatos para CVEs críticos
- **Feature Updates**: Review mensual
- **Documentation**: Actualización continua
- **Monitoring**: 24/7 con alerting

### **📞 Support y Troubleshooting:**
- **Issues**: GitHub Issues para bugs y feature requests
- **Documentation**: README técnicos por action
- **Slack**: #devsecops-support para ayuda inmediata
- **Office Hours**: Miércoles 10-12h para consultas
- **Status Page**: https://status.mibanco.com/devsecops

### **🎯 Roadmap:**
#### **Q4 2025:**
- ✅ Template-based deployment (Completado)
- ✅ Grafana integration (Completado)
- 🔄 Multi-cloud support (En progreso)
- 📋 Helm integration (Planificado)

#### **Q1 2026:**
- 📋 ArgoCD integration
- 📋 Advanced RBAC templates
- 📋 Cost optimization metrics
- 📋 Performance benchmarking

---

## 💡 Quick Start Guide

### **1. Setup básico (5 minutos):**
```bash
# 1. Fork este repositorio
# 2. Configurar secrets básicos
# 3. Crear primer pipeline
```

### **2. Configuración avanzada (30 minutos):**
```bash
# 1. Setup Grafana Cloud
# 2. Configurar Azure credentials
# 3. Personalizar templates K8s
# 4. Importar dashboard DevSecOps
```

### **3. Producción (1 hora):**
```bash
# 1. Multi-environment setup
# 2. Alerting configuration
# 3. Team onboarding
# 4. Monitoring setup
```

**📧 Contacto**: devsecops-team@mibanco.com  
**🌐 Status**: https://status.mibanco.com/devsecops  
**📚 Docs**: https://docs.mibanco.com/devsecops

---

💡 **Tip**: Este README se actualiza automáticamente. Para contribuir, crea un PR con los cambios propuestos.