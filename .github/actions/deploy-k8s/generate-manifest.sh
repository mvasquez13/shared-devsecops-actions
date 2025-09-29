#!/bin/bash

# Script para generar manifiestos de Kubernetes desde template
# Uso: ./generate-manifest.sh [opciones]

set -e

# Valores por defecto
APP_NAME="mibanco-app"
NAMESPACE="mibanco"
IMAGE_REGISTRY="myregistry.azurecr.io"
IMAGE_TAG="latest"
REPLICAS="2"
ENVIRONMENT="prod"
INGRESS_HOST="mibanco-app.local"
TEMPLATE_FILE="maven-manifest.yml"
OUTPUT_FILE=""

# Función de ayuda
show_help() {
    cat << EOF
Generador de Manifiestos de Kubernetes

Uso: $0 [opciones]

Opciones:
    -n, --app-name NAME          Nombre de la aplicación (default: mibanco-app)
    -s, --namespace NAMESPACE    Namespace de Kubernetes (default: mibanco)
    -r, --registry REGISTRY      Registry de imágenes (default: myregistry.azurecr.io)
    -t, --tag TAG               Tag de la imagen (default: latest)
    -c, --replicas COUNT        Número de réplicas (default: 2)
    -e, --environment ENV       Entorno (dev/staging/prod) (default: prod)
    -i, --ingress-host HOST     Host para ingress (default: mibanco-app.local)
    -f, --template-file FILE    Archivo template (default: maven-manifest.yml)
    -o, --output-file FILE      Archivo de salida (default: stdout)
    -h, --help                  Mostrar esta ayuda

Ejemplos:
    # Generar para desarrollo
    $0 -n my-app -s development -e dev -t v1.0.0 -o deployment.yml

    # Generar para producción
    $0 -n mibanco-app -s production -e prod -c 5 -i app.mibanco.com

    # Usar variables de entorno
    export APP_NAME=my-app
    export NAMESPACE=staging
    $0 -o staging-deployment.yml

Variables de entorno soportadas:
    APP_NAME, NAMESPACE, IMAGE_REGISTRY, IMAGE_TAG, REPLICAS, ENVIRONMENT, INGRESS_HOST
EOF
}

# Procesar argumentos de línea de comandos
while [[ $# -gt 0 ]]; do
    case $1 in
        -n|--app-name)
            APP_NAME="$2"
            shift 2
            ;;
        -s|--namespace)
            NAMESPACE="$2"
            shift 2
            ;;
        -r|--registry)
            IMAGE_REGISTRY="$2"
            shift 2
            ;;
        -t|--tag)
            IMAGE_TAG="$2"
            shift 2
            ;;
        -c|--replicas)
            REPLICAS="$2"
            shift 2
            ;;
        -e|--environment)
            ENVIRONMENT="$2"
            shift 2
            ;;
        -i|--ingress-host)
            INGRESS_HOST="$2"
            shift 2
            ;;
        -f|--template-file)
            TEMPLATE_FILE="$2"
            shift 2
            ;;
        -o|--output-file)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Verificar que el archivo template existe
if [[ ! -f "$TEMPLATE_FILE" ]]; then
    echo "Error: El archivo template '$TEMPLATE_FILE' no existe"
    exit 1
fi

# Mostrar configuración
echo "🔧 Configuración del manifiesto:"
echo "  - Aplicación: $APP_NAME"
echo "  - Namespace: $NAMESPACE"
echo "  - Registry: $IMAGE_REGISTRY"
echo "  - Tag: $IMAGE_TAG"
echo "  - Réplicas: $REPLICAS"
echo "  - Entorno: $ENVIRONMENT"
echo "  - Ingress Host: $INGRESS_HOST"
echo "  - Template: $TEMPLATE_FILE"
echo "  - Salida: ${OUTPUT_FILE:-stdout}"
echo ""

# Generar el manifiesto reemplazando las variables
echo "📝 Generando manifiesto..."

# Función para procesar el template
process_template() {
    sed -e "s|{{APP_NAME}}|$APP_NAME|g" \
        -e "s|{{NAMESPACE}}|$NAMESPACE|g" \
        -e "s|{{IMAGE_REGISTRY}}|$IMAGE_REGISTRY|g" \
        -e "s|{{IMAGE_TAG}}|$IMAGE_TAG|g" \
        -e "s|{{REPLICAS}}|$REPLICAS|g" \
        -e "s|{{ENVIRONMENT}}|$ENVIRONMENT|g" \
        -e "s|{{INGRESS_HOST}}|$INGRESS_HOST|g" \
        "$TEMPLATE_FILE"
}

# Generar y escribir el resultado
if [[ -n "$OUTPUT_FILE" ]]; then
    process_template > "$OUTPUT_FILE"
    echo "✅ Manifiesto generado: $OUTPUT_FILE"
    
    # Mostrar resumen del archivo generado
    echo ""
    echo "📊 Resumen del archivo generado:"
    echo "  - Líneas: $(wc -l < "$OUTPUT_FILE")"
    echo "  - Recursos:"
    grep -E "^kind:" "$OUTPUT_FILE" | sed 's/kind: /    - /' | sort | uniq -c
    
    echo ""
    echo "🚀 Para desplegar:"
    echo "  kubectl apply -f $OUTPUT_FILE"
    echo ""
    echo "🔍 Para verificar:"
    echo "  kubectl get all -n $NAMESPACE"
else
    process_template
fi

echo "✨ Generación completada!"