
import simpy
import numpy as np  

# Configurações da simulação
LAMBDA = 2  # Taxa de chegada média dos jobs (2 jobs por segundo)
NUM_JOBS = 250000  # Total de jobs a serem processados
WARM_UP = 10000  # Número de jobs iniciais descartados para aquecer o sistema

# Duração do serviço para cada servidor em cada cenário
SERVICE_TIMES = {
    "deterministic": [0.4, 0.6, 0.95], 
    "uniform": [(0.1, 0.7), (0.1, 1.1), (0.1, 1.8)],  
    "exponential": [0.4, 0.6, 0.95],  
}



# Geração do tempo de serviço com base no tipo de servidor e cenário
"""
Gera o tempo de serviço para um servidor específico com base no tipo de distribuição.
server_type: Tipo do servidor ('deterministic', 'uniform', 'exponential')
server_id: ID do servidor (0, 1, 2 representando S1, S2, S3)
Retorna o tempo de serviço gerado.
"""
def service_time(server_type, server_id):
    if server_type == "deterministic":
        return SERVICE_TIMES["deterministic"][server_id]
    elif server_type == "uniform":
        return np.random.uniform(*SERVICE_TIMES["uniform"][server_id])
    elif server_type == "exponential":
        return np.random.exponential(SERVICE_TIMES["exponential"][server_id])


# Função que gera os jobs e os envia ao sistema
"""
Gera os jobs no sistema de acordo com uma taxa de chegada exponencial.
env: Ambiente SimPy.
system: Dicionário com os recursos (servidores).
arrival_rate: Taxa média de chegada dos jobs (lambda).
server_type: Tipo de distribuição de serviço ('deterministic', 'uniform', 'exponential').
metrics: Lista para armazenar os tempos de resposta dos jobs após o aquecimento.
"""
def job_generator(env, system, arrival_rate, server_type, metrics):
    job_id = 0  # Identificador único do job
    while job_id < NUM_JOBS:
        # Gera um intervalo de chegada baseado em uma distribuição exponencial
        # Aqui significa algo como: "Espere um tempo aleatório (exponencial) antes de criar um novo job. Enquanto isso, outros processos do sistema podem executar."
        yield env.timeout(np.random.exponential(1 / arrival_rate))
        # Cria e agenda um novo job no ambiente SimPy
        env.process(job(env, system, server_type, job_id, metrics))
        job_id += 1


# Função que representa o processamento de um job no sistema
"""
Define o fluxo de processamento de um job pelos servidores.
env: Ambiente SimPy.
system: Dicionário com os recursos (servidores).
server_type: Tipo de distribuição de serviço.
job_id: Identificador único do job.
metrics: Lista para coletar os tempos de resposta dos jobs.
"""
def job(env, system, server_type, job_id, metrics):
    arrival_time = env.now  # Tempo de chegada do job

    # Passa pelo Servidor S1, aguardando até que o recurso esteja disponível.
    with system["S1"].request() as req:
        yield req  # Aguarda o recurso ficar disponível
        yield env.timeout(service_time(server_type, 0))  # Processa no Servidor S1, simulando o tempo de serviço de acordo com o cenário

    # Decide o próximo servidor com base em uma probabilidade
    if np.random.random() < 0.5:  # 50% de chance de ir para S2
        # Processamento em S2 (com possível repetição)
        while True:
            with system["S2"].request() as req:
                yield req
                yield env.timeout(service_time(server_type, 1))
            if np.random.random() >= 0.2:  # Probabilidade de saída de S2 é 80%
                break
    else:
        # Processamento direto em S3
        with system["S3"].request() as req:
            yield req
            yield env.timeout(service_time(server_type, 2))

    # Coleta o tempo de resposta de jobs pós-aquecimento
    if job_id >= WARM_UP:
        metrics.append(env.now - arrival_time)



"""
Configura e executa uma simulação do sistema de filas.
server_type: Tipo de distribuição ('deterministic', 'uniform', 'exponential').
Retorna a média e o desvio padrão dos tempos de resposta após o aquecimento.
"""
def simulate(server_type):
    env = simpy.Environment()  # Cria o ambiente de simulação do simpy

    # Cria recursos para cada servidor (S1, S2, S3).
    # Resource é uma classe utilizada para representar recursos que podem ser compartilhados entre múltiplos processos, com capacidade limitada.
    # Portanto, funciona muito bem para representar servidores em um sistema de filas.
    # A ideia é modelar situações em que vários processos (jobs) tentam acessar um recurso compartilhado (servidor) simultaneamente.
    system = {f"S{i + 1}": simpy.Resource(env) for i in range(3)}

    metrics = []  # Lista para armazenar tempos de resposta

    # Inicia o gerador de jobs no ambiente.
    # O env.process() serve para inicializar e registrar um processo no ambiente de simulação do simpy.
    # O processo é uma função geradora que define o comportamento de um job no sistema.
    # Ao chamar env.process(minha_funcao(...)), você informa ao ambiente de simulação que deseja executar aquela função como um processo SimPy, a partir do tempo atual da simulação.
    env.process(job_generator(env, system, LAMBDA, server_type, metrics))

    env.run()  # Executa a simulação até o término dos jobs
    return np.mean(metrics), np.std(metrics)  # Retorna a média e o desvio padrão dos tempos

"""
Executa as simulações para cada cenário.
"""
def main():
    for scenario in SERVICE_TIMES.keys():  # Itera pelos cenários (deterministic, uniform, exponential)
        mean, std = simulate(scenario)  # Executa a simulação para o cenário atual
        # Exibe os resultados no console
        print(f"Situacao: {scenario}, Tempo médio: {mean:.4f}s, Desvio Padrão: {std:.4f}s")

main()
