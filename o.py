import time
import random
import os
import sys

# CONFIGURAÇÕES, CORES, ORGNZAÇÃO DE TEXTO

class Cores:
    VERMELHO = '\033[91m'
    VERDE = '\033[92m'
    AMARELO = '\033[93m'
    AZUL = '\033[94m'
    MAGENTA = '\033[95m'
    CIANO = '\033[96m'
    BRANCO = '\033[97m'
    NEGRITO = '\033[1m'
    SUBLINHADO = '\033[4m'
    FIM = '\033[0m'
    LIMPAR_TELA = '\033[H\033[2J'

def limpar_tela():
    sys.stdout.write(Cores.LIMPAR_TELA)
    sys.stdout.flush()

def centralizar(texto, largura=60):
    return texto.center(largura)

def falas(texto, velocidade=0.02, cor=Cores.BRANCO):
    sys.stdout.write(cor)
    for letra in texto:
        sys.stdout.write(letra)
        sys.stdout.flush()
        time.sleep(velocidade)
    sys.stdout.write(Cores.FIM + "\n")

def bip():
    sys.stdout.write('\a')
    sys.stdout.flush()

def linha_divisora(cor=Cores.AZUL):
    print(cor + "=" * 60 + Cores.FIM)

def pressionar_enter():
    input(Cores.AMARELO + centralizar("[ Pressione ENTER para continuar ]") + Cores.FIM)

# CONFIGURAÇÕES

CLASSES = {
    "1": {
        "nome": "Guerreiro",
        "desc": "Mestre da espada, equilibra força e defesa.",
        "vida": 150,
        "ataque": 18,
        "defesa": 14,
        "recurso_nome": "Raiva",
        "recurso_max": 100,
        "habilidade_nome": "Corte Titânico",
        "habilidade_custo": 50,
        "cor": Cores.VERMELHO
    },
    "2": {
        "nome": "Mago",
        "desc": "Manipulador das artes arcanas, frágil mas devastador.",
        "vida": 90,
        "ataque": 30,
        "defesa": 6,
        "recurso_nome": "Mana",
        "recurso_max": 120,
        "habilidade_nome": "Explosão Arcana",
        "habilidade_custo": 40,
        "cor": Cores.AZUL
    },
    "3": {
        "nome": "Arqueiro",
        "desc": "Atirador veloz, especialista em acertos críticos.",
        "vida": 115,
        "ataque": 24,
        "defesa": 9,
        "recurso_nome": "Foco",
        "recurso_max": 100,
        "habilidade_nome": "Chuva de Flechas",
        "habilidade_custo": 45,
        "cor": Cores.VERDE
    }
}

INIMIGOS_DATA = [
    {"nome": "Lobo Corrompido", "vida": 60, "ataque": 14, "ouro": 35, "tipo": "veloz", "cor": Cores.BRANCO},
    {"nome": "Cavaleiro esqueleto", "vida": 85, "ataque": 17, "ouro": 50, "tipo": "defensivo", "cor": Cores.BRANCO},
    {"nome": "Bruxa Trix", "vida": 95, "ataque": 21, "ouro": 75, "tipo": "mágico", "cor": Cores.MAGENTA}
]

AREAS_DATA = [
    {"nome": "Floresta Sombria", "desc": "Árvores retorcidas bloqueiam a luz. Um uivo ecoa."},
    {"nome": "Catacumbas Perdidas", "desc": "Ar frio e cheiro de decomposição. O silêncio é interrompido por passos metálicos."},
    {"nome": "Pântano do Eclipse", "desc": "Águas paradas e névoa venenosa. O risco de uma bruxa paira no ar."}
]

# CLASSES DE PERSONAGEM

class Personagem:
    def __init__(self, nome, classe_id):
        c = CLASSES[classe_id]
        self.nome = nome
        self.classe = c["nome"]
        self.cor = c["cor"]
        
        self.vida_max = c["vida"]
        self.vida = c["vida"]
        
        self.ataque = c["ataque"]
        self.defesa = c["defesa"]
        
        self.recurso_nome = c["recurso_nome"]
        self.recurso_max = c["recurso_max"]
        self.recurso = 0 if self.classe == "Guerreiro" else c["recurso_max"]
        
        self.habilidade_nome = c["habilidade_nome"]
        self.habilidade_custo = c["habilidade_custo"]
        
        self.pocoes = 3
        self.fragmentos = 0
        self.ouro = 25

    def exibir_status(self):
        limpar_tela()
        linha_divisora(self.cor)
        print(centralizar(Cores.NEGRITO + f"{self.nome.upper()} - O {self.classe.upper()}" + Cores.FIM))
        linha_divisora(self.cor)
        
        vida_bar = f"{Cores.VERDE}Vida: {self.vida}/{self.vida_max}"
        recurso_bar = f"{self.cor}{self.recurso_nome}: {self.recurso}/{self.recurso_max}"
        print(f"{vida_bar:<30} {recurso_bar}")
        
        print(f"Atk: {self.ataque:<28} Def: {self.defesa}")
        print(centralizar(f"{Cores.AMARELO}Poções: {self.pocoes} | Ouro: {self.ouro} | Fragmentos: {self.fragmentos}/3{Cores.FIM}"))
        linha_divisora(self.cor)

    def atacar(self):
        dano = random.randint(self.ataque - 3, self.ataque + 5)
        if self.classe == "Guerreiro":
            self.recurso = min(self.recurso_max, self.recurso + 12)
        return dano

    def defender(self):
        self.recurso = min(self.recurso_max, self.recurso + 25)
        falas(f"Você assume postura de guarda! A concentração gerou {self.recurso_nome}.", cor=Cores.CIANO)

    def usar_pocao(self):
        if self.pocoes > 0:
            cura = random.randint(40, 60)
            self.vida = min(self.vida_max, self.vida + cura)
            self.pocoes -= 1
            falas(f"Você bebeu uma poção e restaurou {cura} de vida!", cor=Cores.VERDE)
            bip()
            return True
        else:
            falas("Suas poções acabaram!", cor=Cores.VERMELHO)
            return False

    def habilidade(self, inimigo_nome):
        if self.recurso < self.habilidade_custo:
            falas(f"Recurso insuficiente para usar {self.habilidade_nome}!", cor=Cores.VERMELHO)
            return 0
        
        self.recurso -= self.habilidade_custo
        dano = 0
        
        if self.classe == "Guerreiro":
            falas(f"Você canaliza sua fúria no {Cores.NEGRITO}{self.habilidade_nome}{Cores.FIM}{self.cor}!", cor=self.cor)
            dano = random.randint(45, 65)
        elif self.classe == "Mago":
            dano = random.randint(50, 75)
            if random.random() < 0.35:
                dano *= 2
                falas(f"{Cores.NEGRITO}CRÍTICO ARCANO! O feitiço duplicou de tamanho!{Cores.FIM}", cor=Cores.AMARELO)
            falas(f"Você lança uma colossal {Cores.NEGRITO}{self.habilidade_nome}{Cores.FIM}{self.cor}!", cor=self.cor)
        elif self.classe == "Arqueiro":
            falas(f"Você dispara uma saraivada com a {Cores.NEGRITO}{self.habilidade_nome}{Cores.FIM}{self.cor}!", cor=self.cor)
            dano = random.randint(30, 45)
            if random.random() < 0.60:
                extra = random.randint(15, 25)
                dano += extra
                falas(f"Flechas adicionais perfuram o {inimigo_nome}!", cor=Cores.VERDE)
        
        bip()
        return dano

class Inimigo:
    def __init__(self, data):
        self.nome = data["nome"]
        self.vida = data["vida"]
        self.ataque = data["ataque"]
        self.ouro_recompensa = data["ouro"]
        self.tipo = data["tipo"]
        self.cor = data["cor"]
        self.defendendo = False

    def agir(self, jogador):
        self.defendendo = False
        acao_rng = random.random()
        
        # Ataque do mostro
        if self.tipo == "veloz" and acao_rng < 0.40:
            falas(f"O {self.nome} avança com um Ataque Furtivo Duplo!", cor=Cores.VERMELHO)
            dano1 = random.randint(self.ataque - 4, self.ataque)
            dano2 = random.randint(self.ataque - 4, self.ataque)
            return dano1 + dano2, "ataque"
            
        elif self.tipo == "defensivo" and acao_rng < 0.35:
            falas(f"O {self.nome} levanta o escudo de ferro pesadamente!", cor=Cores.CIANO)
            self.defendendo = True
            return 0, "defesa"
            
        elif self.tipo == "mágico" and acao_rng < 0.45:
            falas(f"A {self.nome} conjura uma Maldição de Drenagem!", cor=Cores.MAGENTA)
            jogador.recurso = max(0, jogador.recurso - 20)
            dano = random.randint(self.ataque - 2, self.ataque + 2)
            falas(f"Seu recurso {jogador.recurso_nome} foi sugado!", cor=Cores.VERMELHO)
            return dano, "ataque"
            
        # Ataque padrão
        dano_normal = random.randint(self.ataque - 2, self.ataque + 4)
        falas(f"O {self.nome} lança um ataque direto!", cor=self.cor)
        return dano_normal, "ataque"

# EVENTOS ALEATÓRIOS

def evento_exploracao(jogador):
    limpar_tela()
    linha_divisora(Cores.AMARELO)
    print(centralizar(Cores.NEGRITO + "EVENTO DE ESTRADA" + Cores.FIM))
    linha_divisora(Cores.AMARELO)
    
    evento = random.choice(["altar", "Camponês_caido", "bau"])
    
    if evento == "altar":
        falas("Você encontra um Altar Antigo da Luz esquecido no caminho.")
        print(" 1 - Orar no altar (Ganha +10 de recurso máximo)")
        print(" 2 - Purificar feridas (Cura 40 de vida)")
        escolha = input("\nEscolha: ")
        if escolha == "1":
            jogador.recurso_max += 10
            falas("Uma aura brilha ao seu redor. Seu limite místico aumentou!", cor=Cores.VERDE)
        else:
            jogador.vida = min(jogador.vida_max, jogador.vida + 40)
            falas("Suas feridas se fecham parcialmente.", cor=Cores.VERDE)
            
    elif evento == "Camponês_caido":
        falas("No caminho um Camponês quebrado implora por ajuda na beira da estrada.")
        print(" 1 - Doar 15 moedas de ouro (Ele te recompensa com 2 Poções)")
        print(" 2 - Ignorar e continuar marchando")
        escolha = input("\nEscolha: ")
        if escolha == "1" and jogador.ouro >= 15:
            jogador.ouro -= 15
            jogador.pocoes += 2
            falas("O homem chora de gratidão e te entrega as melhores poções do estoque!", cor=Cores.VERDE)
        else:
            falas("Você passa reto. O mundo já não anda fácil para ninguém.", cor=Cores.BRANCO)
            
    elif evento == "bau":
        falas("Um baú de ferro trancado está parcialmente enterrado.")
        print(" 1 - Forçar a fechadura usando força/magia")
        print(" 2 - Deixar para trás para evitar armadilhas")
        escolha = input("\nEscolha: ")
        if escolha == "1":
            if random.random() < 0.65:
                ganho = random.randint(30, 60)
                jogador.ouro += ganho
                falas(f"Sucesso! Você encontrou uma bolsa contendo {ganho} Moedas de Ouro!", cor=Cores.AMARELO)
            else:
                jogador.vida -= 15
                falas("Uma armadilha de dardos dispara! Você perdeu 15 de vida.", cor=Cores.VERMELHO)
        else:
            falas("Você decide não arriscar sua jornada por ganância.", Cores.BRANCO)
            
    pressionar_enter()

# FERINHA DO SEU ZÉ

def acampamento(jogador):
    while True:
        jogador.exibir_status()
        print(centralizar(Cores.NEGRITO + "FERINHA DO SEU ZÉ" + Cores.FIM))
        linha_divisora(Cores.AMARELO)
        print(" 1 - Comprar Poção de Vida (25 Ouro)")
        print(" 2 - Amolar Lâminas/Focar Cajado (+3 Ataque) (45 Ouro)")
        print(" 3 - Reforçar Malha da Armadura (+2 Defesa) (45 Ouro)")
        print(" 4 - Descanso Completo (Recupera 35 de Vida) (Gratis)")
        print(" 5 - Levantar acampamento e avançar (vc só avança)")
        linha_divisora(Cores.AMARELO)
        
        escolha = input("Ação desejada: ")
        
        if escolha == "1":
            if jogador.ouro >= 25:
                jogador.ouro -= 25
                jogador.pocoes += 1
                falas("Poção adicionada au inventário.", cor=Cores.VERDE)
            else:
                falas("Ouro insuficiente para negociar.", cor=Cores.VERMELHO)
        elif escolha == "2":
            if jogador.ouro >= 45:
                jogador.ouro -= 45
                jogador.ataque += 3
                falas("Armamento aprimorado! Seus golpes causarão mais dano.", cor=Cores.VERDE)
            else:
                falas("Ouro insuficiente.", cor=Cores.VERMELHO)
        elif escolha == "3":
            if jogador.ouro >= 45:
                jogador.ouro -= 45
                jogador.defesa += 2
                falas("Defesa fortificada com sucesso.", cor=Cores.VERDE)
            else:
                falas("Ouro insuficiente.", cor=Cores.VERMELHO)
        elif escolha == "4":
            jogador.vida = min(jogador.vida_max, jogador.vida + 35)
            falas("Você medita sob as brasas. Sente-se revigorado.", cor=Cores.VERDE)
        elif escolha == "5":
            break
        pressionar_enter()

# SISTEMA DE COMBATE

def interface_combate(jogador, inimigo, mensagem=""):
    jogador.exibir_status()
    linha_divisora(inimigo.cor)
    status_inimigo = f"{inimigo.nome.upper()} [DEFENDENDO]" if inimigo.defendendo else inimigo.nome.upper()
    print(centralizar(f"{Cores.NEGRITO}ALVO SELECIONADO: {status_inimigo}{Cores.FIM}"))
    linha_divisora(inimigo.cor)
    print(f"Vida Total do Inimigo: {inimigo.vida}")
    if mensagem:
        print(f"\n> {mensagem}")
    linha_divisora(Cores.BRANCO)
    print(" 1 - Investida Física (Ataque Normal)")
    print(f" 2 - {jogador.cor}{jogador.habilidade_nome} ({jogador.habilidade_custo} {jogador.recurso_nome}){Cores.FIM}")
    print(f" 3 - {Cores.CIANO}Postura de Bloqueio (Reduz dano e acumula {jogador.recurso_nome}){Cores.FIM}")
    print(f" 4 - {Cores.VERDE}Consumir Poção{Cores.FIM}")
    linha_divisora(Cores.BRANCO)

def combate(jogador, inimigo):
    falas(f"O perigo espreita! Um {inimigo.nome} bloqueia o caminho.", cor=inimigo.cor)
    time.sleep(1)
    mensagem_turno = ""
    
    while jogador.vida > 0 and inimigo.vida > 0:
        interface_combate(jogador, inimigo, mensagem_turno)
        mensagem_turno = ""
        
        escolha = input("\nComando: ")
        turno_valido = False
        defendendo = False
        
        if escolha == "1":
            dano = jogador.atacar()
            if inimigo.defendendo:
                dano = max(1, dano - inimigo.ataque // 2)
                mensagem_turno = f"O inimigo usou a guarda! Seu dano foi reduzido para {dano}."
            else:
                mensagem_turno = f"Você desferiu {dano} de dano."
            inimigo.vida -= dano
            turno_valido = True
        elif escolha == "2":
            dano = jogador.habilidade(inimigo.nome)
            if dano > 0:
                if inimigo.defendendo:
                    dano = max(1, dano - inimigo.ataque)
                    falas("A postura inimiga absorveu parte do impacto devastador.", cor=Cores.VERMELHO)
                inimigo.vida -= dano
                mensagem_turno = f"A habilidade causou {dano} de dano massivo."
                turno_valido = True
            else:
                pressionar_enter()
                continue
        elif escolha == "3":
            jogador.defender()
            defendendo = True
            turno_valido = True
        elif escolha == "4":
            if jogador.usar_pocao():
                turno_valido = True
            else:
                pressionar_enter()
                continue
        else:
            mensagem_turno = "Hesitação em batalha custa caro! O inimigo avança."
            turno_valido = True
            
        # Turnos dos inimigos
        if turno_valido and inimigo.vida > 0:
            interface_combate(jogador, inimigo, mensagem_turno)
            print("\a")
            
            dano_inimigo, tipo_acao = inimigo.agir(jogador)
            
            if tipo_acao == "ataque":
                dano_final = max(1, dano_inimigo - (jogador.defesa // 2))
                if defendendo:
                    dano_final = max(1, dano_final // 2)
                    mensagem_turno = "Bloqueio Perfeito! Dano mitigado drasticamente."
                jogador.vida -= dano_final
                
                if jogador.classe == "Guerreiro":
                    jogador.recurso = min(jogador.recurso_max, jogador.recurso + (dano_final // 2))
                    
                falas(f"Você sofreu {dano_final} de dano do contra-ataque.", cor=Cores.VERMELHO)
            else:
                mensagem_turno = f"O {inimigo.nome} está preparando uma estratégia defensiva."
            time.sleep(1.5)

    if jogador.vida > 0:
        falas(f"\nAlvo neutralizado! {inimigo.nome} foi desintegrado.", cor=Cores.VERDE)
        jogador.ouro += inimigo.ouro_recompensa
        falas(f"Espólios de guerra recolhidos: +{inimigo.ouro_recompensa} Ouro.", cor=Cores.AMARELO)
        return True
    else:
        falas(f"\nSua jornada termina aqui. O {inimigo.nome} triunfou.", cor=Cores.VERMELHO)
        return False

# BATALHA FINAL

class Zarek(Inimigo):
    def __init__(self):
        super().__init__({"nome": "Zarek", "vida": 260, "ataque": 30, "ouro": 0, "tipo": "boss", "cor": Cores.MAGENTA})
        self.escudo = True

    def exibir_status_boss(self):
        linha_divisora(self.cor)
        status_escudo = "BARREIRA INTACTA" if self.escudo else "BARREIRA QUEBRADA"
        print(centralizar(f"CONFRONTO FINAL: {self.nome.upper()}"))
        print(centralizar(f"Integração Vital: {self.vida} | Escudo de Sombras: {status_escudo}"))
        linha_divisora(self.cor)

    def acao_turno(self):
        magia = random.choice(["fogo", "raio", "dreno", "escudo"])
        if magia == "fogo":
            return 24, "conjura Chamas Orbitais Obliterantes!"
        elif magia == "raio":
            return 32, "invoca um Relâmpago de Ruína Arcana!"
        elif magia == "dreno":
            self.vida += 15
            return 16, "rompe sua estamina drenando sua vida (+15 Cura do Boss)!"
        elif magia == "escudo" and not self.escudo:
            self.escudo = True
            return 0, "ergue novamente os nexos do Escudo de Sombras!"
        else:
            return random.randint(self.ataque - 2, self.ataque + 5), "avança com golpes corporais imbuídos em ódio puro!"

def batalha_final(jogador):
    limpar_tela()
    Zarek = Zarek()
    falas("Zarek desce do trono flutuante: 'Seu sacrifício será o alicerce do meu novo império...'", cor=Zarek.cor)
    pressionar_enter()
    
    mensagem_turno = ""
    
    while jogador.vida > 0 and Zarek.vida > 0:
        jogador.exibir_status()
        Zarek.exibir_status_boss()
        
        if mensagem_turno:
            print(f"\n> {mensagem_turno}")
            linha_divisora(Cores.BRANCO)
            
        print(" 1 - Investida Física (Ataque Normal)")
        print(f" 2 - {jogador.cor}{jogador.habilidade_nome}{Cores.FIM}")
        print(f" 3 - {Cores.CIANO}Postura de Bloqueio{Cores.FIM}")
        print(f" 4 - {Cores.AMARELO}Ativar os Fragmentos Solares{Cores.FIM}")
        print(f" 5 - {Cores.VERDE}Consumir Poção{Cores.FIM}")
        linha_divisora(Cores.BRANCO)
        
        escolha = input("\nAção contra o Lorde: ")
        turno_valido = False
        defendendo = False
        mensagem_turno = ""
        
        if escolha == "1":
            dano = jogador.atacar()
            if Zarek.escudo:
                dano = max(1, dano // 4)
                falas("Sua investida bate de frente contra a barreira impenetrável!", cor=Cores.VERMELHO)
            Zarek.vida -= dano
            mensagem_turno = f"Dano aplicado: {dano}."
            turno_valido = True
        elif escolha == "2":
            dano = jogador.habilidade("Zarek")
            if dano > 0:
                if Zarek.escudo:
                    dano = max(1, dano // 3)
                    falas("A pressão mágica do escudo reduziu o impacto do seu golpe.", cor=Cores.VERMELHO)
                Zarek.vida -= dano
                mensagem_turno = f"Dano do poder elemental: {dano}."
                turno_valido = True
            else:
                pressionar_enter()
                continue
        elif escolha == "3":
            jogador.defender()
            defendendo = True
            turno_valido = True
        elif escolha == "4":
            if jogador.fragmentos >= 3 and Zarek.escudo:
                Zarek.escudo = False
                falas("A ENERGIA CONCENTRADA DOS TRÊS FRAGMENTOS ESTOURA O ESCUDO SOMBRIO!", cor=Cores.AMARELO)
                turno_valido = True
            else:
                falas("O artefato não responde (ou o escudo já sucumbiu).", cor=Cores.VERMELHO)
                pressionar_enter()
                continue
        elif escolha == "5":
            if jogador.usar_pocao():
                turno_valido = True
            else:
                pressionar_enter()
                continue
        else:
            mensagem_turno = "Você errou o tempo do movimento. Zarek ataca!"
            turno_valido = True
            
        # Turno Boss
        if turno_valido and Zarek.vida > 0:
            dano, efeito = Zarek.acao_turno()
            dano_final = max(1, dano - (jogador.defesa // 2))
            if defendendo:
                dano_final = max(1, dano_final // 2)
            
            jogador.vida -= dano_final
            falas(f"\nZarek {efeito}", cor=Zarek.cor)
            if dano_final > 0:
                falas(f"O ataque te causou {dano_final} de dano fatal!", cor=Cores.VERMELHO)
            time.sleep(1.5)

    return jogador.vida > 0

# FLUXO DO JOGO

def iniciar_jogo():
    limpar_tela()
    linha_divisora(Cores.AMARELO)
    print(centralizar(Cores.NEGRITO + "O ÚLTIMO ECLIPSE" + Cores.FIM))
    linha_divisora(Cores.AMARELO)
    
    falas("qual seu nome héroi?:")
    nome = input("> ")
    if not nome: nome = "Guerreiro da Luz"
    
    print("\nQual sua classe?:")
    for id, c in CLASSES.items():
        print(f" {id} - {c['cor']}{c['nome']}{Cores.FIM}: {c['desc']}")
        
    classe_id = input("\n> ")
    while classe_id not in CLASSES:
        classe_id = input("> ")
        
    jogador = Personagem(nome, classe_id)
    
    # Ciclo 
    for i in range(len(AREAS_DATA)):
        # Loja 
        if i > 0:
            acampamento(jogador)
        
        # Mecânica de Evento antes do perigo (Ajuda)
        evento_exploracao(jogador)
            
        area = AREAS_DATA[i]
        inimigo = Inimigo(INIMIGOS_DATA[i])
        
        limpar_tela()
        falas(f"Sondando a região da {area['nome']}...", cor=Cores.BRANCO)
        falas(area['desc'], cor=Cores.BRANCO)
        pressionar_enter()
        
        venceu = combate(jogador, inimigo)
        
        if venceu:
            jogador.fragmentos += 1
            falas(f"Estilhaço recuperado! Você possui {jogador.fragmentos}/3 Fragmentos do Sol.", cor=Cores.AMARELO)
            pressionar_enter()
        else:
            falas("A escuridão sepultou fantastiki por completo...", cor=Cores.VERMELHO)
            return

    # Preparação o final
    falas("O topo da Torre Obsidiana está à vista. vc vai na ferinha do zé", cor=Cores.AMARELO)
    pressionar_enter()
    acampamento(jogador)

    # Confronto e Finais
    venceu_final = batalha_final(jogador)
    limpar_tela()
    linha_divisora(Cores.AMARELO if venceu_final else Cores.VERMELHO)
    
    if venceu_final:
        print(centralizar("FINAL BOM: A LUZ RESTAURADA"))
        falas(f"O Lorde das Sombras desmoronou em cinzas. O amanhecer retorna a fantastiki pelas mãos de {jogador.nome}!", cor=Cores.AMARELO)
    else:
        print(centralizar("FINAL RUIM: O ECLIPSE INFINITO"))
        falas("Vc morreu e o universo conhecerá apenas o vazio gelado da noite sem estrelas.", cor=Cores.VERMELHO)
    linha_divisora(Cores.AMARELO if venceu_final else Cores.VERMELHO)

if __name__ == "__main__":
    iniciar_jogo()