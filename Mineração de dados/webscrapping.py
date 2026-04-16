import sqlite3
import telnetlib
import time
import re
from datetime import datetime

# 1. Base de Conhecimento
mitigadores = {
    "264409": "Huge Networks",
    "52863": "UPX",
    "263004": "Sage Networks",
    "263444": "OpenX",
    "52925": "BR.Digital"
}

# 2. Inicializar Banco de Dados (Adicionada coluna as_path_len)
def inicializar_banco():
    conn = sqlite3.connect('monitoramento_bgp.db', timeout=30)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coletas_bgp (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            prefixo TEXT NOT NULL,
            status_mitigacao TEXT NOT NULL,
            asn_mitigador TEXT,
            as_path TEXT,
            as_path_len INTEGER,
            communities TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 3. Função de Coleta e Mineração
def coletar_via_telnet(prefixo):
    host = "lg.sp.ix.br"
    port = 23
    
    try:
        print(f"[{datetime.now()}] Minerando: {prefixo}")
        tn = telnetlib.Telnet(host, port, timeout=20)
        time.sleep(2)
        
        comando = f"show ip bgp {prefixo}\n"
        tn.write(comando.encode('ascii'))
        
        time.sleep(6) 
        full_output = tn.read_very_eager().decode('ascii', errors='ignore')
        tn.close()

        # --- LÓGICA DE LIMPEZA ---
        if "show ip bgp" in full_output:
            resultado_limpo = full_output.split(comando.strip())[-1].strip()
        else:
            resultado_limpo = full_output.strip()

        if "not in table" in resultado_limpo.lower() or not resultado_limpo:
            print(f"-> Prefixo {prefixo} sem rota no momento.")
            return

        # --- MINERANDO DADOS (ATRIBUTOS) ---
        status_mitigacao = "Normal"
        asn_detetado = "Nenhum"
        for asn, nome in mitigadores.items():
            if asn in resultado_limpo:
                status_mitigacao = "100% Mitigada"
                asn_detetado = f"{asn} ({nome})"
                break
        
        # 1. Extração do AS Path Length
        # Procuramos a linha que contém apenas números (o rastro do AS Path)
        as_path_match = re.search(r'^\s*([\d\s]+)$', resultado_limpo, re.MULTILINE)
        if as_path_match:
            lista_asns = as_path_match.group(1).strip().split()
            qtd_saltos = len(lista_asns)
        else:
            qtd_saltos = 0

        # 2. Extração de Communities
        comm_encontradas = re.findall(r'\d+:\d+', resultado_limpo)
        communities_str = ", ".join(list(set(comm_encontradas))) if comm_encontradas else "N/A"

        # --- PERSISTÊNCIA NO SQLITE (Com timeout de segurança) ---
        conn = sqlite3.connect('monitoramento_bgp.db', timeout=30)
        cursor = conn.cursor()
        agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
            INSERT INTO coletas_bgp (timestamp, prefixo, status_mitigacao, asn_mitigador, as_path, as_path_len, communities)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (agora, prefixo, status_mitigacao, asn_detetado, resultado_limpo, qtd_saltos, communities_str))
        conn.commit()
        conn.close()
        
        print(f"-> SUCESSO: Gravado {prefixo} (Saltos: {qtd_saltos})")

    except Exception as e:
        print(f"-> ERRO na conexão: {e}")

# 4. Configuração da Amostragem
alvos = [
    "104.234.147.0/24", "104.234.148.0/24", "104.234.150.0/24", "45.163.76.0/24",
    "45.233.176.0/24", "45.233.177.0/24", "145.233.178.0/24", "177.101.157.0/24",
    "143.0.166.0/24", "45.184.198.0/24", "187.33.138.0/24", "45.233.179.0/24",
    "128.201.36.0/24", "108.165.230.0/24", "131.0.11.0/24", "128.201.38.0/24"
]

# 5. Loop Principal
inicializar_banco()
print(f"=== SISTEMA DE MINERAÇÃO BGP ATUALIZADO ===")
print(f"Monitorando {len(alvos)} prefixos com contagem de saltos.\n")

while True:
    for p in alvos:
        coletar_via_telnet(p)
        time.sleep(1)
    
    print(f"\n[{datetime.now()}] Ciclo completo. Próxima coleta em 30 min...")
    time.sleep(1800)