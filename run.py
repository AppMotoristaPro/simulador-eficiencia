from app import create_app

app = create_app()

if __name__ == '__main__':
    # Roda na porta 5000 e fica acessível na rede local
    app.run(host='0.0.0.0', port=5000, debug=True)

