# SDS Tools - Simple Data Structures

[![PyPI version](https://img.shields.io/pypi/v/pysds-tools.svg)](https://pypi.org/project/pysds-tools/)
[![Documentation](https://readthedocs.org/projects/pysds-tools/badge/?version=latest)](https://pysds-tools.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-informational)](http://mypy-lang.org/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-informational)](https://flake8.pycqa.org/)
[![Static Badge](https://img.shields.io/badge/security-bandit-informational)](https://github.com/PyCQA/bandit)

Une bibliothèque Python complète et pédagogique de structures de données fondamentales
— des listes chaînées aux modèles graphiques probabilistes — implémentées avec des
principes de programmation orientée objet et une documentation exhaustive de style
académique.

> **Note sur le nom du package** : la distribution PyPI/pip s'appelle
> **`pysds-tools`** (`sds-tools` entre en collision avec un package existant, sans
> rapport, une fois le nom normalisé par PyPI). Le module importable n'est pas
> affecté — il reste `sds` (`import sds.linear`, `import sds.probabilistic`, ...).

## Objectifs

- **Pédagogique** : Code clair et bien documenté pour l'apprentissage — pas
  seulement du code qui fonctionne, mais du code qui explique le *pourquoi*
- **Complet** : Couverture exhaustive des structures de données classiques et avancées
- **Typé** : Support complet de MyPy en mode strict, compatible pyright/basedpyright
- **Testé** : Objectif de couverture 80–90 %+ par module, vérifié via pytest-cov
- **Performant** : `__slots__` sur chaque classe de nœud et de structure

## Installation

```bash
pip install pysds-tools
```

## Démarrage rapide

```python
from sds.linear import Stack
from sds.graph import DirectedGraph, GraphNode, DirectedEdge
from sds.probabilistic import BayesianNetwork, Factor, RandomVariable

# Structures linéaires
stack = Stack()
stack.push(1)
stack.push(2)
stack.pop()  # 2

# Graphes
task_graph = DirectedGraph()
design, backend = GraphNode("Design"), GraphNode("Backend")
task_graph.add_node(design)
task_graph.add_node(backend)
task_graph.add_edge(DirectedEdge(design, backend))
task_graph.is_acyclic()  # True

# Modèles graphiques probabilistes
rain = RandomVariable("Rain", ("true", "false"))
bn = BayesianNetwork()
bn.add_variable(rain)
bn.set_cpt(rain, Factor((rain,), {("true",): 0.2, ("false",): 0.8}))
```

## Architecture

Le projet est organisé en modules thématiques, un par famille de structures :

```plaintext
src/sds/
├── core/           # Fondations : AbstractNode, AbstractContainer, exceptions
├── linear/         # Structures linéaires (liste chaînée, pile, file)
├── tree/           # Structures arborescentes (binaire, AVL, heaps, B-tree, trie, segment tree)
├── graph/          # Structures de graphes (dirigés, pondérés, représentations d'adjacence)
├── advanced/       # Structures avancées déterministes (disjoint set, Bloom filter, ...)
├── probabilistic/  # Modèles graphiques probabilistes (réseaux bayésiens, MRF, HMM)
├── algorithms/      # (prévu) tri, algorithmes de graphes, parcours d'arbres, inférence
└── utils/          # (prévu) visualiseur, exceptions étendues
```

## Structures disponibles

### `sds.core` — Fondations

Abstractions de base partagées par tous les autres modules : `AbstractNode`,
`AbstractContainer`, et la hiérarchie d'exceptions commune. Ne contient aucune
structure de données concrète par conception — tous les autres modules
importent depuis `core`, jamais l'inverse.

### `sds.linear` — Structures linéaires

- **`LinkedList`** : liste doublement chaînée — O(1) ajout en tête/queue
- **`Stack`** : LIFO — `push()`, `pop()`, `peek()`, tout en O(1)
- **`Queue`** : FIFO — `enqueue()`, `dequeue()`, tout en O(1)

### `sds.tree` — Structures arborescentes

- **`BinaryTree`**, **`AVLTree`** (auto-équilibré, O(log n) garanti),
  **`GeneralTree`** (n-aire)
- **`MinHeap`**, **`MaxHeap`**
- **`BTree`**, **`Trie`** (recherche par préfixe), **`SegmentTree`** (requêtes sur intervalle)

### `sds.graph` — Structures de graphes

- **`Graph`**, **`DirectedGraph`**, **`UndirectedGraph`** (wrapper strict —
  rejette explicitement les arêtes dirigées plutôt que de les convertir silencieusement)
- **`WeightedGraph`**, **`WeightedDirectedGraph`**
- **`AdjacencyListGraph`** (creux, espace O(V+E)), **`AdjacencyMatrixGraph`**
  (dense, recherche d'arête O(1))

### `sds.advanced` — Structures avancées

Structures déterministes qui ne rentrent pas naturellement dans linear/tree/graph :

- **`DisjointSet`** (Union-Find, path compression + union-by-rank — O(α(n)) amorti)
- **`BloomFilter`** (appartenance probabiliste), **`SkipList`** (structure triée probabiliste)
- **`HashTableChaining`**, **`HashTableOpenAddressing`**
- **`LRUCache`**, **`FenwickTree`** (arbre indexé binaire), **`CountMinSketch`**
  (estimation de fréquence sur flux)

### `sds.probabilistic` — Modèles graphiques probabilistes

Structures encodant des distributions de probabilité sur des variables aléatoires
discrètes. Aucune logique d'inférence (requêtes marginales, explication la plus
probable) n'est implémentée ici — c'est prévu pour `sds.algorithms`.

- **`RandomVariable`**, **`Factor`** : briques de base partagées (une variable
  discrète et une table de potentiel/CPT sur une portée de variables)
- **`BayesianNetwork`** : modèle graphique dirigé acyclique avec CPT
  localement normalisées, compose `sds.graph.DirectedGraph` pour la topologie
- **`MarkovRandomField`** : modèle graphique non dirigé (cycles autorisés)
  avec potentiels non normalisés, compose `sds.graph.Graph`
- **`HiddenMarkovModel`** : modèle séquentiel sur une paire fixe
  états/observations, avec composantes initiale/transition/émission

## Documentation

Référence API complète et guide utilisateur, avec fondements mathématiques,
diagrammes Mermaid, tables de complexité et exemples concrets pour chaque module :

**https://pysds-tools.readthedocs.io**

## Tests

```bash
# Exécuter tous les tests
pytest

# Avec couverture
pytest --cov=sds --cov-report=html

# Tests d'un module spécifique
pytest tests/06_Probabilistic/

# Mode verbeux
pytest -v
```

Organisation de la suite de tests (miroir de l'arborescence source, un dossier par module) :

```plaintext
tests/
├── 01_Core/
├── 02_Linear/
├── 03_Tree/
├── 04_Graph/
├── 05_Advanced/
└── 06_Probabilistic/
```

## Analyse statique

Le projet est entièrement typé et vérifié avec mypy, flake8 et bandit :

```bash
mypy src/sds/
flake8 src/sds/
bandit -r src/sds/
```

Ou, via `tox` :

```bash
tox -e mypy,flake8,bandit
```

## Contribuer

Les contributions sont les bienvenues !

1. **Forkez** le projet
2. Créez une **branche** pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Committez** vos changements en suivant [Conventional Commits](https://www.conventionalcommits.org/)
4. **Poussez** la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une **Pull Request**

L'ensemble des conventions du projet (labels, templates d'issues, format de
commit, versioning, releases) est documenté dans
[`CONVENTIONS.md`](https://github.com/skyfrigate/.github/blob/main/CONVENTIONS.md)
dans le dépôt partagé `.github`.

### Standards de qualité

- ✅ Typage vérifié avec mypy (mode strict)
- ✅ Style conforme à flake8
- ✅ Sécurité vérifiée avec bandit
- ✅ Tests avec pytest (objectif de couverture 80–90 %+)
- ✅ Docstrings au format NumPy
- ✅ `__slots__` sur toutes les classes de nœuds et de structures

## Feuille de route

### `v0.1.0`–`v0.5.0` — Fondations à Structures avancées ✅ *Terminé*

- `sds.core`, `sds.linear`, `sds.tree`, `sds.graph`, `sds.advanced` —
  entièrement implémentés, testés et documentés

### `v0.6.0` — Structures probabilistes ✅ *Terminé (cette release)*

- `sds.probabilistic` : `BayesianNetwork`, `MarkovRandomField`, `HiddenMarkovModel`

### `v0.7.0` — Algorithmes *Prévu*

- Tri (QuickSort, MergeSort), algorithmes de graphes (DFS, BFS, Dijkstra,
  Kruskal), parcours d'arbres — et inférence probabiliste (Variable
  Elimination, Belief Propagation, Forward, Viterbi)

### `v0.8.0` — Utilitaires *Prévu*

- Visualiseur partagé, hiérarchie d'exceptions étendue

### `v0.9.0`–`v1.0.0` — Consolidation qualité & Release stable *Prévu*

- Passe complète couverture/mypy, polissage documentaire, première API stable

### `v1.1.0`–`v1.2.0` — Traduction française *Prévu*

- Documentation bilingue via un projet ReadTheDocs dédié

## Licence

Ce projet est sous licence Apache License 2.0 — voir le fichier
[LICENSE](LICENSE.md) pour les détails. La documentation est sous licence
séparée CC BY-NC 4.0 — voir [`docs/source/license.rst`](docs/source/license.rst).

## Remerciements

- Inspiré par les cours classiques de structures de données et d'algorithmes
- Conçu pour l'apprentissage
- Merci à la communauté Python pour ses outils exceptionnels
  ([pytest](https://docs.pytest.org/en/stable/),
  [mypy](https://mypy-lang.org/), [flake8](https://flake8.pycqa.org/en/latest/),
  [bandit](https://bandit.readthedocs.io/en/latest/), [Sphinx](https://www.sphinx-doc.org/),
  [Furo](https://pradyunsg.me/furo/))

## Ressources

- [Documentation Python](https://docs.python.org/3/)
- [Type Hints — PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [Guide docstring NumPy](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Modèles graphiques probabilistes — notes Stanford CS228](https://ermongroup.github.io/cs228-notes/)
  (référence en accès libre pour `sds.probabilistic`)

---

**Miroir GitLab** : https://gitlab.com/open-works/sds
