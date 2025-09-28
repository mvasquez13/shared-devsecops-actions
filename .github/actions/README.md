# Maven DevSecOps Actions

Este conjunto de acciones proporciona una suite completa para testing, cobertura, análisis de calidad y construcción en proyectos Maven.

## 🏗️ Arquitectura Modular

Las acciones están diseñadas de forma granular para máxima reutilización:

### 🔧 Acciones de Construcción

#### 1️⃣ `build-app`
Construye aplicaciones Maven y prepara artefactos.

```yaml
- name: Build Application
  uses: ./shared-devsecops-actions/actions/build-app
  with:
    app-name: 'mi-aplicacion'
    skip-tests: 'false'
    build-profiles: 'production'
```

#### 2️⃣ `build-docker-image`
Construye y pushea imágenes Docker con versionado semántico.

```yaml
- name: Build Docker Image
  uses: ./shared-devsecops-actions/actions/build-docker-image
  with:
    app-name: 'mi-aplicacion'
    registry-url: 'myregistry.azurecr.io'
    image-name: 'mi-app'
    registry-username: ${{ secrets.REGISTRY_USERNAME }}
    registry-password: ${{ secrets.REGISTRY_PASSWORD }}
    app-version: '1.2.3'
```

**Genera tags como**: `mi-app:1.2.3-20250928`, `mi-app:latest`

### 🔒 Acciones de Seguridad

#### 3️⃣ `sast-scanner` 
Análisis estático de seguridad usando GitHub CodeQL (gratuito para repos públicos).

```yaml
- name: CodeQL SAST Analysis
  uses: ./shared-devsecops-actions/actions/sast-scanner
  with:
    language: 'java'
    build-command: 'mvn clean compile -B'
    queries: 'security-and-quality'
    upload-sarif: 'true'
```

#### 4️⃣ `container-scan`
Escanea imágenes Docker para vulnerabilidades de seguridad.

```yaml
- name: Container Security Scan
  uses: ./shared-devsecops-actions/actions/container-scan
  with:
    image: 'myregistry/myapp:latest'
    severity-threshold: 'HIGH'
    fail-on-critical: 'true'
    enable-sarif-upload: 'true'  # Para repos públicos
```

### 🧪 Acciones de Testing

#### 5️⃣ `maven-tests`
Ejecuta únicamente las pruebas Maven.

```yaml
- name: Run Tests
  uses: ./shared-devsecops-actions/actions/maven-tests
  with:
    maven-args: '-B -Dspring.profiles.active=test'
```

#### 6️⃣ `jacoco-coverage`
Genera reportes de cobertura JaCoCo.

```yaml
- name: Generate Coverage
  uses: ./shared-devsecops-actions/actions/jacoco-coverage
  with:
    coverage-threshold: '85'
    fail-on-threshold: 'false'
```

#### 7️⃣ `sonarqube-analysis`
Ejecuta análisis de SonarQube.

```yaml
- name: SonarQube Analysis
  uses: ./shared-devsecops-actions/actions/sonarqube-analysis
  with:
    sonar-token: ${{ secrets.SONAR_TOKEN }}
    sonar-project-key: 'my-project'
```

### 🚀 Suite Completa

#### 8️⃣ `maven-test-suite`

### 🧪 Acciones de Testing

#### 4️⃣ `maven-tests`
Ejecuta únicamente las pruebas Maven.

```yaml
- name: Run Tests
  uses: ./shared-devsecops-actions/actions/maven-tests
  with:
    maven-args: '-B -Dspring.profiles.active=test'
```

#### 4️⃣ `maven-tests`
Ejecuta únicamente las pruebas Maven.

```yaml
- name: Run Tests
  uses: ./shared-devsecops-actions/actions/maven-tests
  with:
    maven-args: '-B -Dspring.profiles.active=test'
```

#### 5️⃣ `jacoco-coverage`
Genera reportes de cobertura JaCoCo.

```yaml
- name: Generate Coverage
  uses: ./shared-devsecops-actions/actions/jacoco-coverage
  with:
    coverage-threshold: '85'
    fail-on-threshold: 'false'
```

#### 6️⃣ `sonarqube-analysis`
Ejecuta análisis de SonarQube.

```yaml
- name: SonarQube Analysis
  uses: ./shared-devsecops-actions/actions/sonarqube-analysis
  with:
    sonar-token: ${{ secrets.SONAR_TOKEN }}
    sonar-project-key: 'my-project'
```

### 🚀 Suite Completa

#### 7️⃣ `maven-test-suite`
Orquesta todas las acciones de testing.

```yaml
- name: Complete Test Suite
  uses: ./shared-devsecops-actions/actions/maven-test-suite
  with:
    coverage-threshold: '80'
    sonar-token: ${{ secrets.SONAR_TOKEN }}
    maven-args: '-B'
```

## 🔄 Casos de Uso

### Solo Tests (CI rápido)
```yaml
jobs:
  quick-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Run Tests
        uses: ./shared-devsecops-actions/actions/maven-tests
```

### Tests + Coverage (Pull Request)
```yaml
jobs:
  pr-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Run Tests
        uses: ./shared-devsecops-actions/actions/maven-tests
      
      - name: Generate Coverage
        uses: ./shared-devsecops-actions/actions/jacoco-coverage
        with:
          coverage-threshold: '75'
```

### Suite Completa (Main Branch)
```yaml
jobs:
  full-pipeline:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      - name: Complete Test Suite
        uses: ./shared-devsecops-actions/actions/maven-test-suite
        with:
          coverage-threshold: '80'
          sonar-token: ${{ secrets.SONAR_TOKEN }}
```

### Suite Completa con Seguridad (Recomendado para repos públicos)
```yaml
jobs:
  security-analysis:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-java@v3
        with:
          java-version: '17'
          distribution: 'temurin'
      
      # SAST Analysis con CodeQL
      - name: CodeQL SAST Analysis
        uses: ./shared-devsecops-actions/actions/sast-scanner
        with:
          language: 'java'
          queries: 'security-and-quality'
          upload-sarif: 'true'
      
      # Tests + Coverage
      - name: Complete Test Suite
        uses: ./shared-devsecops-actions/actions/maven-test-suite
        with:
          coverage-threshold: '80'
          sonar-token: ${{ secrets.SONAR_TOKEN }}
      
      # Build & Security Scan
      - name: Build Docker Image
        id: build
        uses: ./shared-devsecops-actions/actions/build-docker-image
        with:
          app-name: 'mi-app'
          registry-url: 'myregistry.azurecr.io'
          image-name: 'mi-app'
          registry-username: ${{ secrets.REGISTRY_USERNAME }}
          registry-password: ${{ secrets.REGISTRY_PASSWORD }}
      
      - name: Container Security Scan
        uses: ./shared-devsecops-actions/actions/container-scan
        with:
          image: ${{ steps.build.outputs.full-image-url }}
          enable-sarif-upload: 'true'
```

## 📊 Outputs Disponibles

Cada acción proporciona outputs específicos que pueden ser utilizados en pasos posteriores:

```yaml
- name: Run Tests
  id: tests
  uses: ./shared-devsecops-actions/actions/maven-tests

- name: Check Results
  run: |
    echo "Tests passed: ${{ steps.tests.outputs.tests-passed }}"
    echo "Tests failed: ${{ steps.tests.outputs.tests-failed }}"
    echo "Total tests: ${{ steps.tests.outputs.tests-total }}"
```

## ✅ Ventajas de esta Arquitectura

- **🔄 Reutilización**: Cada acción puede usarse independientemente
- **⚡ Performance**: Posibilidad de paralelización
- **🎯 Flexibilidad**: Diferentes workflows para diferentes necesidades
- **🛠️ Mantenimiento**: Cada componente tiene una responsabilidad única
- **🔧 Testing**: Fácil testeo individual de cada componente