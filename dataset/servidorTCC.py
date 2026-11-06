
from ultralytics import YOLO
import os
from flask import Flask, request
import socket
import threading

app = Flask(__name__)

# Pasta onde as imagens serão salvas
PASTA_FOTOS = r"C:\TCC\Fotos"
os.makedirs(PASTA_FOTOS, exist_ok=True)

# Caminho do modelo YOLO treinado
CAMINHO_MODELO = (
    r"C:\TCC\runs\detect\runs\TCC\YOLO26n_TCC-2\weights/best.pt"
)

# Carrega o modelo uma única vez, ao iniciar o servidor
model = YOLO(CAMINHO_MODELO)


def descobrir_servidor():
    porta_descoberta = 4210

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp:
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp.bind(("0.0.0.0", porta_descoberta))

        print(f"Descoberta UDP ativa na porta {porta_descoberta}")

        while True:
            mensagem, endereco = udp.recvfrom(1024)

            print("Mensagem recebida:", mensagem)
            print("Endereço da ESP32:", endereco)

            if mensagem.decode(errors="ignore").strip() == "FIND_FLASK":
                teste = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                try:
                    # Descobre o IP usado para alcançar a ESP32
                    teste.connect(endereco)
                    ip_servidor = teste.getsockname()[0]
                except OSError as erro:
                    print("Erro ao descobrir IP:", erro)
                    continue
                finally:
                    teste.close()

                resposta = f"{ip_servidor}:5000"

                try:
                    udp.sendto(resposta.encode(), endereco)
                    print("Resposta enviada:", resposta)
                except OSError as erro:
                    print("Erro ao enviar resposta:", erro)


@app.route("/upload", methods=["POST"])
def upload():
    foto = request.get_data()

    if not foto:
        return "Nenhuma imagem recebida", 400

    caminho = os.path.join(PASTA_FOTOS, "Lixo_detectar.jpg")

    try:
        with open(caminho, "wb") as arquivo:
            arquivo.write(foto)

        print(f"Imagem salva: {caminho} ({len(foto)} bytes)")
        return "ok", 200

    except OSError as erro:
        print("Erro ao salvar imagem:", erro)
        return "Erro ao salvar imagem", 500




@app.route("/imagem", methods=["GET"])
def imagem():
    caminho = os.path.join(PASTA_FOTOS, "Lixo_detectar.jpg")

    if not os.path.exists(caminho):
        return "4", 200

    try:
        # Executa a classificação com YOLO
        resultados = model(caminho, show=False, conf=0.01)
        resultado = resultados[0]

        # Mapeamento das classes
        classes_numeros = {
            "paper": 1,
            "plastic": 2,
            "metal": 3
        }

        # Guarda a detecção com maior confiança
        maior_confianca = 0
        melhor_classe = None

        for box in resultado.boxes:
            classe = int(box.cls[0])
            nome = model.names[classe].lower()
            confianca = float(box.conf[0])

            print(f"Material: {nome} | Confiança: {confianca * 100:.2f}%")

            if confianca > maior_confianca:
                maior_confianca = confianca
                melhor_classe = nome

        # Nenhuma detecção encontrada
        if melhor_classe is None:
            print("Resultado: 4 - Não reciclável / Não identificado")
            return "4", 200

        # Verifica se a confiança é menor que 40%
        if maior_confianca < 0.10:
            print("Confiança abaixo de 10%")
            print("Resultado: 4 - Não reciclável / Não identificado")
            return "4", 200

        # Converte a classe para número
        numero = classes_numeros.get(melhor_classe, 4)

        print(f"Melhor detecção: {melhor_classe}")
        print(f"Maior confiança: {maior_confianca * 100:.2f}%")
        print(f"Resultado enviado: {numero}")

        return str(numero), 200

    except Exception as erro:
        print("Erro durante a classificação:", erro)
        return "Erro na classificação", 500



@app.route("/info", methods=["GET"])
def info():
    return {"servidor": "Flask", "porta": 5000}, 200


if __name__ == "__main__":
    threading.Thread(
        target=descobrir_servidor,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
