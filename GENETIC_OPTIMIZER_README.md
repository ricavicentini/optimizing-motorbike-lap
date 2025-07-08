# 🧬 Genetic Algorithm Lap Optimizer

Sistema modular para otimização de tempo de volta usando Algoritmos Genéticos configuráveis.

## 🚀 Quick Start

### 1. Configurar Environment
```bash
# Ativar environment conda
conda activate ag_motorbike

# Atualizar dependências (se necessário)
conda env update -f environment.yml
```

### 2. Uso Básico - Função Direta
```python
from genetic_optimizer import FindBestLap
from track_loader import load_waypoints, build_spline

# Carregar pista
x, y = load_waypoints("tracks/waypoints_S.csv")
x_s, y_s = build_spline(x, y, num_points=500)

# Otimizar (usa config/genetic_algorithm.yaml)
results = FindBestLap(x_s, y_s)

# Ver Top 5 resultados
print(f"Melhor tempo: {results[0].lap_time:.3f}s")
for i, result in enumerate(results):
    print(f"#{i+1}: {result.lap_time:.3f}s (Gen {result.generation})")
```

### 3. Executar Exemplos
```bash
# Exemplo completo
python example_usage.py

# Script com mais opções
python scripts/optimize_lap.py --track tracks/waypoints_S.csv
```

## ⚙️ Configuração

Edite `config/genetic_algorithm.yaml` para personalizar:

```yaml
# Parâmetros principais
population:
  size: 100              # Tamanho da população
  hall_of_fame_size: 5   # Top N para retornar

evolution:
  generations: 100       # Número de gerações
  crossover_probability: 0.7   # Taxa de crossover
  mutation_probability: 0.2    # Taxa de mutação

# Logging
logging:
  show_progress: true    # Mostrar progresso
  show_statistics: true  # Mostrar estatísticas por geração
```

## 📊 Resultados

Cada resultado contém:
```python
@dataclass
class LapResult:
    individual: List[float]  # Genes do indivíduo
    lap_time: float         # Tempo de volta (segundos)
    generation: int         # Geração onde foi encontrado
    rank: int              # Posição no hall da fama (1-5)
```

## 🎯 Exemplos de Uso

### Configuração Personalizada
```python
from genetic_optimizer import GeneticOptimizer

# Criar otimizador com config personalizada
optimizer = GeneticOptimizer("minha_config.yaml")
results = optimizer.FindBestLap(x_s, y_s)
```

### Otimização Rápida (Teste)
```yaml
# config/fast_test.yaml
population:
  size: 20
evolution:
  generations: 10
```

```python
results = FindBestLap(x_s, y_s, config_path="config/fast_test.yaml")
```

### Otimização Intensiva
```yaml
# config/intensive.yaml  
population:
  size: 200
evolution:
  generations: 500
```

## 📁 Estrutura de Arquivos

```
├── config/
│   └── genetic_algorithm.yaml    # Configuração padrão
├── src/
│   └── genetic_optimizer.py      # Módulo principal
├── scripts/
│   └── optimize_lap.py          # Script completo
├── example_usage.py             # Exemplo simples
└── environment.yml              # Dependências conda
```

## 🔧 Comparação de Performance

O algoritmo genético tipicamente melhora o tempo de volta base:

- **Baseline**: ~20.43s (sem otimização)
- **GA Otimizado**: ~20.05s (melhoria de ~0.38s)
- **Melhoria**: ~1.9%

## ✅ Vantagens do Sistema

- ✅ **Configuração Externa**: Mude parâmetros sem editar código
- ✅ **Resultado Estruturado**: Top 5 automaticamente ordenados  
- ✅ **Logging Profissional**: Progress e estatísticas configuráveis
- ✅ **Flexível**: Use função direta ou classe completa
- ✅ **Conda Integration**: Funciona perfeitamente com environment.yml

## 🐛 Troubleshooting

### PyYAML não encontrado
```bash
conda env update -f environment.yml
# ou
conda install pyyaml
```

### Config file não encontrado
O módulo procura automaticamente em:
- Caminho especificado
- `config/genetic_algorithm.yaml`
- `../config/genetic_algorithm.yaml`

### Performance lenta
Ajuste na configuração:
```yaml
population:
  size: 50        # Reduzir população
evolution:
  generations: 30 # Menos gerações
``` 