# MiBanco Shared DevSecOps Actions

Librería centralizada de GitHub Actions reutilizables para estandarizar pipelines DevSecOps en la organización MiBanco. Optimizada para **repositorios públicos** utilizando herramientas **gratuitas** de GitHub.

## 🏗️ Arquitectura

Este repositorio contiene componentes modulares y reutilizables que implementan las mejores prácticas DevSecOps utilizando herramientas nativas de GitHub.

```
shared-devsecops-actions/
├── .github/
│   ├── workflows/
│   │   └── aks_tpl.yml              # Workflow principal reutilizable
│   └── actions/                     # Actions compuestos modulares
│       ├── build-app/               # Compilación y testing de aplicaciones
│       ├── build-docker-image/      # Construcción de imágenes Docker con semantic versioning
│       ├── container-scan/          # Escaneo de vulnerabilidades con Trivy
│       ├── sast-scanner/           # Análisis estático con GitHub CodeQL
│       ├── sca-scanner/            # Análisis de dependencias con GitHub Advisory DB
│       ├── dast-scanner/           # Análisis dinámico (OWASP ZAP)
│       ├── deploy-k8s/             # Despliegue en Kubernetes/AKS
│       └── notify-teams/           # Notificaciones Microsoft Teams
└── README.md
```

## 🚀 Uso

### Workflow Completo para Aplicaciones Maven/Spring Boot:

```yaml
name: MiBanco DevSecOps Pipeline
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
      app-name: 'mi-aplicacion'
      java-version: '17'
      maven-version: '3.9'
      
      # Configuración Docker
      registry-url: 'mibancoregistry.azurecr.io'
      dockerfile-path: './Dockerfile'
      
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

| Action | Descripción | Herramienta | Costo |
|--------|-------------|-------------|-------|
| `build-app` | Compilación Maven + Tests + JaCoCo + SonarQube | Maven, JaCoCo | ✅ Gratuito |
| `build-docker-image` | Construcción Docker con semantic versioning | Docker | ✅ Gratuito |
| `sast-scanner` | Análisis estático de código | **GitHub CodeQL** | ✅ Gratuito (repos públicos) |
| `sca-scanner` | Análisis de vulnerabilidades en dependencias | **GitHub Advisory DB** | ✅ Gratuito |
| `container-scan` | Escaneo de vulnerabilidades en contenedores | **Trivy** | ✅ Gratuito |
| `dast-scanner` | Análisis dinámico de aplicaciones web | OWASP ZAP | ✅ Gratuito |
| `deploy-k8s` | Despliegue en Azure Kubernetes Service | kubectl, helm | ✅ Gratuito |
| `notify-teams` | Notificaciones a Microsoft Teams | Webhooks | ✅ Gratuito |

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

## 🎯 Casos de Uso

### **1. Proyecto Maven Básico**
```yaml
jobs:
  pipeline:
    uses: mibanco-org/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
    with:
      app-name: 'api-productos'
      java-version: '17'
      registry-url: 'mibancoregistry.azurecr.io'
      enable-sast: true
      enable-sca: true
```

### **2. Aplicación con Despliegue Completo**
```yaml
jobs:
  pipeline:
    uses: mibanco-org/shared-devsecops-actions/.github/workflows/aks_tpl.yml@main
    with:
      app-name: 'core-banking'
      enable-deploy-staging: true
      enable-deploy-prod: true
      enable-dast: true
    secrets:
      registry-username: ${{ secrets.ACR_USERNAME }}
      registry-password: ${{ secrets.ACR_PASSWORD }}
      kube-config: ${{ secrets.KUBE_CONFIG }}
```

## � Configuración Requerida

### **Secrets del Repositorio:**
```bash
# Azure Container Registry
ACR_USERNAME=mibancoregistry
ACR_PASSWORD=<password>

# Kubernetes (opcional)
KUBE_CONFIG=<base64-encoded-kubeconfig>

# Teams (opcional)
TEAMS_WEBHOOK_URL=https://outlook.office.com/webhook/...
```

### **Variables de Entorno:**
```bash
# En el workflow o repository settings
SONAR_TOKEN=<sonarqube-token>  # Si usas SonarQube
```

## 📊 Reportes y Métricas

El pipeline genera automáticamente:

- 📈 **Cobertura de código** (JaCoCo)
- 🔍 **Reportes de seguridad** (CodeQL, Trivy)
- 📋 **Resultados de tests** (Surefire)
- 🐳 **Metadatos de imagen** Docker
- 📤 **Artefactos** (.jar, reportes)

## 🚀 Beneficios

- ✅ **100% Gratuito** para repositorios públicos
- ✅ **Herramientas nativas** de GitHub (CodeQL, Advisory DB)
- ✅ **Modular y reutilizable** 
- ✅ **Semantic versioning** automático
- ✅ **Integración completa** con GitHub Security
- ✅ **Escalable** para múltiples aplicaciones
- ✅ **Mantenimiento centralizado**

## 🔧 Mantenimiento

- **Owner**: DevSecOps Team MiBanco
- **Versioning**: Semantic Versioning (tags)
- **Updates**: Automático vía Dependabot
- **Support**: Issues en este repositorio
- **Status**: ✅ Production Ready

---

💡 **Tip**: Para repositorios públicos, todas las herramientas de seguridad son gratuitas. Para repositorios privados, considera GitHub Advanced Security.