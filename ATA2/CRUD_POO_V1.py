import json
import os

class Equipamento:
    def __init__(self, identificador, nome, tipo, responsavel, setor):
        self.identificador = identificador
        self.nome = nome
        self.tipo = tipo
        self.responsavel = responsavel
        self.setor = setor
        self.vulnerabilidades = []

    def adicionar_vulnerabilidade(self, descricao, severidade, status):
        vulnerabilidade = {
            "descricao": descricao,
            "severidade": severidade,
            "status": status
        }
        self.vulnerabilidades.append(vulnerabilidade)

    def listar_dados(self):
        print(f"Dados do ativo {self.identificador}:")
        print(f"Nome: {self.nome}")
        print(f"Tipo: {self.tipo}")
        print(f"Responsável: {self.responsavel}")
        print(f"Setor: {self.setor}")
        print("Vulnerabilidades:")
        if self.vulnerabilidades:
            for v in self.vulnerabilidades:
                print(f" - Descrição: {v['descricao']} | Severidade: {v['severidade']} | Status: {v['status']}")
        else:
            print("   Nenhuma vulnerabilidade cadastrada.")

    # Converte o objeto em um dicionário estruturado para o JSON
    def para_dicionario(self):
        return {
            "identificador": self.identificador,
            "nome": self.nome,
            "tipo": self.tipo,
            "responsavel": self.responsavel,
            "setor": self.setor,
            "vulnerabilidades": self.vulnerabilidades
        }

    # Reconstrói o objeto a partir de um dicionário vindo do JSON
    @classmethod
    def de_dicionario(cls, dados):
        equipamento = cls(
            identificador=dados["identificador"],
            nome=dados["nome"],
            tipo=dados["tipo"],
            responsavel=dados["responsavel"],
            setor=dados["setor"]
        )
        equipamento.vulnerabilidades = dados.get("vulnerabilidades", [])
        return equipamento


class GerenciadorAtivos:
    def __init__(self, caminho_arquivo="ativos.json"):
        self.ativos = {}
        self.caminho_arquivo = caminho_arquivo
        # Carrega automaticamente os dados existentes ao iniciar o sistema
        self.carregar_de_json()

    def salvar_em_json(self):
        # Converte o dicionário de objetos em um array (lista) de objetos JSON
        lista_ativos = [equipamento.para_dicionario() for equipamento in self.ativos.values()]
        
        try:
            with open(self.caminho_arquivo, "w", encoding="utf-8") as arquivo:
                json.dump(lista_ativos, arquivo, indent=4, ensure_ascii=False)
            print("")
        except Exception as e:
            print(f"Erro ao salvar arquivo JSON: {e}")

    def carregar_de_json(self):
        if not os.path.exists(self.caminho_arquivo):
            return  # Se o arquivo não existir, inicia com o dicionário vazio

        try:
            with open(self.caminho_arquivo, "r", encoding="utf-8") as arquivo:
                lista_ativos = json.load(arquivo)
                
                # Reconstrói o mapeamento self.ativos a partir da lista estruturada
                self.ativos = {}
                for dados in lista_ativos:
                    equipamento = Equipamento.de_dicionario(dados)
                    self.ativos[equipamento.identificador] = equipamento
        except Exception as e:
            print(f"Erro ao carregar arquivo JSON: {e}")

    def criar_ativo(self):
        identificador = input("Crie o ID único do dispositivo: ")
        if identificador in self.ativos:
            print("ID já existe!")
            return
        
        nome = input("Digite o nome do dispositivo: ")
        tipo = input("Digite o tipo (Notebook/ Smart TV/ Smartphone/ PC Gamer/ Video Game/ Impressora): ")
        responsavel = input("Digite o responsável: ")
        setor = input("Digite o setor/local: ")

        novo_equipamento = Equipamento(identificador, nome, tipo, responsavel, setor)
        self.ativos[identificador] = novo_equipamento
        print("Ativo cadastrado com sucesso!")
        self.salvar_em_json()  # Salva após alterações

    def consultar_ativo(self):
        identificador = input("Digite o ID do ativo para consulta: ")
        if identificador in self.ativos:
            self.ativos[identificador].listar_dados()
        else:
            print("Ativo não encontrado.")

    def listar_ativos(self):
        if self.ativos:
            print("Lista de ativos cadastrados:")
            for id_ativo, equipamento in self.ativos.items():
                print(f"ID: {id_ativo} | Nome: {equipamento.nome} | Tipo: {equipamento.tipo} | Responsável: {equipamento.responsavel} | Setor: {equipamento.setor}")
        else:
            print("Nenhum ativo cadastrado ainda!")

    def atualizar_ativo(self):
        identificador = input("Digite o ID do ativo para atualizar: ")
        if identificador in self.ativos:
            equipamento = self.ativos[identificador]
            campo = input("Digite o campo a atualizar (nome, tipo, responsavel, setor): ").lower()
            
            if hasattr(equipamento, campo) and campo not in ["vulnerabilidades", "identificador"]:
                novo_valor = input("Digite o novo valor: ")
                setattr(equipamento, campo, novo_valor)
                print("Ativo atualizado com sucesso!")
                self.salvar_em_json()  # Salva após alterações
            else:
                print("Campo inválido.")
        else:
            print("Ativo não encontrado.")

    def deletar_ativo(self):
        identificador = input("Digite o ID do ativo para remover: ")
        if identificador in self.ativos:
            del self.ativos[identificador]
            print("Ativo removido com sucesso!")
            self.salvar_em_json()  # Salva após alterações
        else:
            print("Ativo não encontrado.")

    def cadastrar_vulnerabilidade(self):
        identificador = input("Digite o ID do ativo para adicionar vulnerabilidade: ")
        if identificador in self.ativos:
            descricao = input("Digite a descrição da vulnerabilidade: ")
            severidade = input("Digite a severidade (Baixa/Média/Alta/Crítica): ")
            status = input("Digite o status (Aberta/Em tratamento/Corrigida/Aceita como risco): ")

            self.ativos[identificador].adicionar_vulnerabilidade(descricao, severidade, status)
            print("Vulnerabilidade cadastrada com sucesso!")
            self.salvar_em_json()  # Salva após alterações
        else:
            print("Ativo não encontrado.")

    def atualizar_vulnerabilidade(self):
        identificador = input("Digite o ID do ativo: ")
        if identificador in self.ativos:
            equipamento = self.ativos[identificador]
            if not equipamento.vulnerabilidades:
                print("Este ativo não possui vulnerabilidades cadastradas.")
                return

            print("Vulnerabilidades cadastradas:")
            for i, v in enumerate(equipamento.vulnerabilidades, start=1):
                print(f"{i}. Descrição: {v['descricao']} | Severidade: {v['severidade']} | Status: {v['status']}")

            try:
                escolha = int(input("Digite o número da vulnerabilidade que deseja atualizar: "))
                if 1 <= escolha <= len(equipamento.vulnerabilidades):
                    campo = input("Digite o campo a atualizar (descricao, severidade, status): ").lower()
                    if campo in ["descricao", "severidade", "status"]:
                        novo_valor = input(f"Digite o novo valor para {campo}: ")
                        equipamento.vulnerabilidades[escolha - 1][campo] = novo_valor
                        print("Vulnerabilidade atualizada com sucesso!")
                        self.salvar_em_json()  # Salva após alterações
                    else:
                        print("Campo inválido.")
                else:
                    print("Número inválido.")
            except ValueError:
                print("Entrada inválida. Digite um número.")
        else:
            print("Ativo não encontrado.")


def menu():
    gerenciador = GerenciadorAtivos()
    while True:
        print("\n--- MENU ---\n")
        print("1. Criar ativo")
        print("2. Consultar ativo")
        print("3. Listar ativos")
        print("4. Atualizar ativo")
        print("5. Deletar ativo")
        print("6. Cadastrar vulnerabilidade")
        print("7. Atualizar vulnerabilidade")
        print("8. Sair\n")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            gerenciador.criar_ativo()
        elif opcao == "2":
            gerenciador.consultar_ativo()
        elif opcao == "3":
            gerenciador.listar_ativos()
        elif opcao == "4":
            gerenciador.atualizar_ativo()
        elif opcao == "5":
            gerenciador.deletar_ativo()
        elif opcao == "6":
            gerenciador.cadastrar_vulnerabilidade()
        elif opcao == "7":
            gerenciador.atualizar_vulnerabilidade()
        elif opcao == "8":
            print("Encerrando programa...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    menu()