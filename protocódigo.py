def calculo_resistor(cor1, cor2, cor3, cor4):
    Digitos = {
    "preto": 0,
    "marrom": 1,
    "vermelho": 2,
    "laranja": 3,
    "amarelo": 4,
    "verde": 5,
    "azul": 6,
    "violeta": 7,
    "cinza": 8,
    "branco": 9
    }

    Multiplicador = {
    "preto": 1,
    "marrom": 10,
    "vermelho": 1*10**2,
    "laranja": 1*10**3,
    "amarelo": 1*10**4,
    "verde": 1*10**5,
    "azul": 1*10**6,
    "violeta": 1*10**7,
    "dourado": 0.1,
    "prata": 0.01
    }

    Tolerancia = {
    "marrom": "±1%",
    "vermelho": "±2%",
    "verde": "±0,5%",
    "azul": "±0,25%",
    "violeta": "±0,1%",
    "cinza": "±0,05%",
    "dourado": "±5%",
    "prata": "±10%",
    "nenhuma": "±20%"
    }
    for cores, Tabela in [(cor1, Digitos), (cor2, Digitos), (cor3, Multiplicador), (cor4, Tolerancia)]:
      if cores not in Tabela:
        return None, None
      valor_base = Digitos[cor1] *10 + Digitos[cor2]
      resistencia = valor_base * Multiplicador[cor3]
      tolerancia = Tolerancia[cor4]
      return resistencia, tolerancia

def acao_calculo():
  while True:
    print("\n #CALCULAR RESISTENCIA# ")
    resistencia, tolerancia = calculo_resistor(input("Cor 1: "), input("Cor 2: "), input("Cor 3: "), input("Cor 4: "))
    if resistencia == None:
      print("Código ou cores inválidas")
      break
    else:
      print(f"Resistência: {resistencia} Ω Tolerância {tolerancia}")
itens ={}


def mostrar_opcoes():
  print("\n #MENU# ")
  print("1) Cadastrar componentes")
  print("2) Remover componentes")
  print("3) Alterar componentes")
  print("4) calcular resistor")
  print("0) Sair")
  print("###--Lista completa--###")
  for cod, dados in itens.items():
        print(f"{cod} : {dados}")

def cadastro(itens):
  while True:
    prefixo= input("Digite o prefixo do item:").upper()
    teste1 = "sim"
    teste2 = "não"
    if prefixo in itens:
        print("item ja cadastrado")
        print("cadastrar item na mesma categoria?")
        if input("sim, não?" ) == teste1:
          Sufixo= input("Digite o sulfixo do item:").upper()
          Valor= input("Digite o valor do item:")
          Modelo = input("Digite o modelo")
          Tipo= input("Digite o tipo ou unidade de medidade do item:")
          itens[prefixo][Sufixo] = {"valor": Valor, Modelo: Tipo}
          print("item cadastrado com sucesso")
          print(f"\nCategoria {prefixo} atualizada:")
          for cod, dados in itens[prefixo].items():
                    print(f"{cod} : {dados}")

        else:
          print("item não cadastrado")
    else:
       Sufixo= input("Digite o sulfixo do item:").upper()
       Valor= input("Digite o valor do item:")
       Modelo = input("Digite o modelo")
       Tipo= input("Digite o tipo ou unidade de medidade do item:")
       itens[prefixo] = {Sufixo: {"valor": Valor, Modelo: Tipo}}
       print("item cadastrado com sucesso")
       for cod, dados in itens.items():
                    print(f"{cod} : {dados}")
    return itens

def remover_item(itens):
  opcao = input("Deseja remover um item ou categoria?").lower()
  if opcao == "categoria":
    prefixo = input("Digite o prefixo do item a ser removido:\n").upper()
    if prefixo in itens:
      del itens[prefixo]
      print("item removido com sucesso")
    else:
      print("item não encontrado")
    for cod, dados in itens.items():
        print(f"{cod} : {dados}")
  else:
    print("Digite o prefixo do item a ser removido:")
    prefixo = input("Digite o prefixo do item:").upper()
    Sufixo= input("Digite o sulfixo do item:").upper()
    del itens[prefixo][Sufixo]
  for cod, dados in itens.items():
        print(f"{cod} : {dados}")

while True:
  mostrar_opcoes()
  escolha = int(input("Escolha uma das opções"))
  match escolha:
    case 1:
       cadastro(itens)
    case 2:
      remover_item(itens)
    case 3:
      print("teste")
    case 4:
      acao_calculo()
    case 0:
      print("Saindo do programa...")
      break
    case _:
      print("Opção inválida")
