# pontia-mlops-tutorial-Jose-antonio-gonzalez-alcantara

## Descripción General
Este es un proyecto MLOps completo que entrena un modelo RandomForest para predicción de ingresos en datos tabulares del dataset Adult. El proyecto implementa un pipeline CI/CD automatizado con GitHub Actions, integración con MLflow para gestión de experimentos, y despliegue en Azure Container Instances.

## Integrantes del Equipo
- **José Antonio González Alcántara** - Desarrollador Principal

## Estructura del Proyecto

```
├── src/                          # Código fuente del proyecto
│   ├── main.py                  # Script principal de entrenamiento
│   ├── data_loader.py           # Carga y preprocesamiento de datos
│   ├── model.py                 # Definición y entrenamiento del modelo
│   ├── evaluate.py              # Evaluación y métricas del modelo
│   └── run_id.txt               # ID del último run de MLflow
│
├── unit_tests/                   # Tests unitarios
│   ├── test_data_loader.py      # Tests para carga de datos
│   ├── test_model.py            # Tests para el modelo
│   └── test_evaluate.py         # Tests para evaluación
│
├── model_tests/                  # Tests de integración del modelo
│   └── test_model.py            # Tests de predicción y carga
│
├── deployment/                   # Configuración de despliegue
│   ├── Dockerfile               # Imagen Docker para la API
│   └── app/
│       └── main.py              # API FastAPI para predicciones
│
├── scripts/                       # Scripts auxiliares
│   ├── register_model.py        # Registro de modelo en MLflow
│   └── query_model.py           # Script para consultar la API
│
├── .github/workflows/            # Pipelines de CI/CD
│   ├── build.yml                # Pipeline de construcción y entrenamiento
│   ├── integration.yml          # Pipeline de integración y tests
│   └── deploy.yml               # Pipeline de despliegue
│
├── data/
│   └── raw/                     # Datos crudos (descargados automáticamente)
│
├── models/                       # Modelos entrenados y artifacts
│
├── requirements.txt              # Dependencias del proyecto
├── pytest.ini                   # Configuración de pytest
├── .gitignore                   # Archivos ignorados en git
└── README.md                    # Este archivo
```

## Funcionalidad de Cada Componente

### [src/data_loader.py](src/data_loader.py)
Módulo responsable de:
- Cargar datos de entrenamiento y prueba desde archivos CSV
- Manejar valores faltantes
- Codificar variables categóricas con LabelEncoder
- Escalar características numéricas con StandardScaler
- Retorna datos preprocesados listos para el modelo

### [src/model.py](src/model.py)
Módulo que:
- Define y entrena el modelo RandomForestClassifier
- Registra parámetros e información del entrenamiento
- Retorna el modelo entrenado

### [src/evaluate.py](src/evaluate.py)
Módulo de evaluación que:
- Calcula la precisión (accuracy) del modelo
- Genera reporte de clasificación detallado
- Registra métricas en logs

### [src/main.py](src/main.py)
Script principal que:
- Orquesta todo el pipeline de ML
- Carga e integra con MLflow para tracking
- Maneja logging a archivo y consola
- Guarda artefactos (modelo, scaler, encoders)
- Registra el run_id para posterior referencia

### [unit_tests/test_model.py](unit_tests/test_model.py)
Tests unitarios que validan:
- Que el modelo entrenado es una instancia de RandomForestClassifier
- Que el modelo posee el método predict
- Que los logs contienen mensajes esperados

### [unit_tests/test_evaluate.py](unit_tests/test_evaluate.py)
Tests que verifican:
- Evaluación correcta del modelo
- Generación de reportes de clasificación
- Registro adecuado de métricas en logs

### [unit_tests/test_data_loader.py](unit_tests/test_data_loader.py)
Tests que validan:
- Carga correcta de datos en DataFrames
- Formas correctas de datasets
- Preprocesamiento adecuado (escalado, codificación)

### [model_tests/test_model.py](model_tests/test_model.py)
Tests de integración que verifican:
- Existencia y cargabilidad del modelo
- Forma correcta de predicciones
- Valores válidos de predicción (0 o 1)
- Accuracy mínima requerida (80%)

### [scripts/register_model.py](scripts/register_model.py)
Script que:
- Recupera el run_id del entrenamiento
- Registra el modelo en MLflow Registry
- Transiciona el modelo a etapa "Staging"
- Establece alias "champion"

### [scripts/query_model.py](scripts/query_model.py)
Script de prueba que:
- Envía requests POST a la API de predicción
- Proporciona ejemplo de payload esperado
- Retorna predicción del modelo desplegado

### [deployment/Dockerfile](deployment/Dockerfile)
Define imagen Docker que:
- Usa Python 3.10
- Instala dependencias del proyecto
- Expone puerto 8080
- Ejecuta aplicación FastAPI

### [deployment/app/main.py](deployment/app/main.py)
API FastAPI que:
- Carga el modelo desde MLflow en startup
- Proporciona endpoint `/health` para verificación
- Proporciona endpoint `/predict` para hacer predicciones
- Aplica preprocesamiento (encoding, scaling)
- Retorna predicciones en formato JSON
- Expone métricas en endpoint `/metrics`

### [.github/workflows/build.yml](.github/workflows/build.yml)
Pipeline de construcción que:
- Descarga dataset Adult automáticamente
- Entrena el modelo
- Ejecuta tests de integración
- Registra el modelo en MLflow
- Se ejecuta en cada push a main

### [.github/workflows/integration.yml](.github/workflows/integration.yml)
Pipeline de integración que:
- Ejecuta tests unitarios con cobertura
- Genera reportes HTML de cobertura
- Comenta resultados en Pull Requests
- Se ejecuta en cada PR

### [.github/workflows/deploy.yml](.github/workflows/deploy.yml)
Pipeline de despliegue que:
- Construye imagen Docker
- Pushea a Azure Container Registry
- Despliega en Azure Container Instances
- Verifica salud de la API
- Se ejecuta manualmente (workflow_dispatch)

## Instalación y Uso

### Requisitos
- Python 3.10+
- pip o conda

### Setup Local

```bash
# Crear entorno virtual
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar datos
mkdir -p data/raw
curl -o data/raw/adult.data https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data
curl -o data/raw/adult.test https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.test

# Entrenar modelo
python src/main.py

# Ejecutar tests
pytest unit_tests/ --cov=src
pytest model_tests/
```

## Pipeline CI/CD

El proyecto utiliza **GitHub Actions** para automatización:

1. **Build Pipeline** (build.yml):
   - Descarga datos
   - Entrena modelo
   - Ejecuta tests de integración
   - Registra modelo en MLflow

2. **Integration Pipeline** (integration.yml):
   - Ejecuta tests unitarios
   - Genera reportes de cobertura
   - Comenta en PRs

3. **Deploy Pipeline** (deploy.yml):
   - Construye imagen Docker
   - Pushea a ACR (Azure Container Registry)
   - Despliega en Azure Container Instances
   - Verifica disponibilidad

## Variables de Entorno Requeridas

```
MLFLOW_URL              # URL del servidor MLflow
EXPERIMENT_NAME         # Nombre del experimento en MLflow
MODEL_NAME              # Nombre del modelo en MLflow Registry
AZURE_STORAGE_CONNECTION_STRING  # Conexión a Azure Storage
AZURE_CREDENTIALS       # Credenciales de Azure
ACR_NAME                # Nombre del Azure Container Registry
```

## Métricas Clave

- **Test Accuracy**: Precisión del modelo en datos de prueba
- **Train Time**: Tiempo de entrenamiento
- **Prediction Latency**: Tiempo de respuesta de la API
- **Total Predictions**: Cantidad de predicciones realizadas

## Tecnologías Utilizadas

- **ML Framework**: scikit-learn
- **Tracking**: MLflow
- **API**: FastAPI
- **Container**: Docker
- **Cloud**: Microsoft Azure
- **CI/CD**: GitHub Actions
- **Testing**: pytest

## Licencia

Este proyecto es parte del programa Master IA DevOps Cloud - Introducción a DevOps.
