
from ultralytics import YOLO
import torch

# =====================================
# 1. CONFIGURAÇÕES
# =====================================

# Caminho do arquivo data.yaml do Roboflow
DATASET = r"C:\Users\rafae\Downloads\novaia.v7-modificada-2.yolo26\data.yaml"

# Nome do modelo inicial
MODELO = "yolo26n.pt"

# =====================================
# 2. VERIFICAR DISPOSITIVO
# =====================================

if torch.cuda.is_available():
    dispositivo = 0
    print("Treinamento utilizando GPU")
else:
    dispositivo = "cpu"
    print("Treinamento utilizando CPU")

# =====================================
# 3. CARREGAR MODELO
# =====================================

model = YOLO(MODELO)

# =====================================
# 4. TREINAMENTO
# =====================================

resultados = model.train(

    data=DATASET,

    # Épocas
    epochs=100,

    # Resolução das imagens
    imgsz=640,

    # Imagens processadas por lote
    batch=8,

    # Parada antecipada
    patience=15,

    # Dispositivo
    device=dispositivo,

    # Transformações adicionais
    degrees=10,
    fliplr=0.5,
    flipud=0.0,
    mosaic=0.0,

    # Organização dos resultados
    project="runs/TCC",
    name="YOLO26n_TCC",

    # Salvar os melhores pesos
    save=True,

    # Mostrar resultados
    plots=True,

    # Semente para reprodução
    seed=42
)

print("\nTreinamento finalizado!")

print("Melhor modelo salvo em:")
print("runs/TCC/YOLO26n_TCC/weights/best.pt")
