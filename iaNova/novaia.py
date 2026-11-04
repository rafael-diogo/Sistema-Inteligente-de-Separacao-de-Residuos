
from ultralytics import YOLO

# Caminho do arquivo de configuração do dataset
data_yaml = r"C:\TCC\iaNova\novaia.v5i.yolo26\data.yaml"

# Carrega o YOLO26 Nano
modelo = YOLO("yolo26n.pt")

# Treinamento
modelo.train(
    data=data_yaml,
    epochs=50,
    imgsz=640,
    batch=4,
    workers=0,
    project=r"C:\TCC\iaNova\runs",
    name="treinamento_yolo26",
    patience=10,
    plots=True
)

print("Treinamento concluído!")
print(
    r"Melhor modelo: C:\TCC\iaNova\runs\treinamento_yolo26\weights\best.pt"
)
