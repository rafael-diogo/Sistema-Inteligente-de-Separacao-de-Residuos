
from ultralytics import YOLO
from tkinter import Tk, filedialog
import cv2
import os

# Caminho do modelo treinado
CAMINHO_MODELO = r"C:\TCC\iaNova\runs\treinamento_yolo26\weights\best.pt"

# Confiança mínima de detecção (50%)
CONFIANCA = 0.50

# Carregar o modelo
print("Carregando modelo YOLO26n...")
modelo = YOLO(CAMINHO_MODELO)

# Abrir janela para selecionar imagem
janela = Tk()
janela.withdraw()

caminho_imagem = filedialog.askopenfilename(
    title="Selecione uma imagem para testar a IA",
    filetypes=[
        ("Imagens", "*.jpg *.jpeg *.png"),
        ("Todos os arquivos", "*.*")
    ]
)

janela.destroy()

if not caminho_imagem:
    print("Nenhuma imagem selecionada.")
    exit()

print(f"\nImagem: {caminho_imagem}")
print("Analisando imagem...\n")

# Executar detecção
resultados = modelo.predict(
    source=caminho_imagem,
    conf=CONFIANCA,
    imgsz=640,
    verbose=False
)

resultado = resultados[0]

# Mostrar objetos identificados
if len(resultado.boxes) == 0:
    print("Nenhum material identificado.")
    print("Classificação: NÃO IDENTIFICADO")
else:
    for caixa in resultado.boxes:
        classe_id = int(caixa.cls[0])
        confianca = float(caixa.conf[0])
        nome = modelo.names[classe_id]

        print(f"Material: {nome}")
        print(f"Confiança: {confianca * 100:.2f}%")
        print("--------------------------")

# Desenhar caixas e nomes
imagem_resultado = resultado.plot()

# Salvar imagem
pasta_saida = "resultados_teste"
os.makedirs(pasta_saida, exist_ok=True)

caminho_saida = os.path.join(
    pasta_saida,
    "resultado.jpg"
)

cv2.imwrite(caminho_saida, imagem_resultado)

print(f"\nResultado salvo em: {os.path.abspath(caminho_saida)}")

# Mostrar resultado na tela
cv2.imshow("Teste da IA - YOLO26n", imagem_resultado)

print("\nPressione qualquer tecla na imagem para fechar.")
cv2.waitKey(0)
cv2.destroyAllWindows()
