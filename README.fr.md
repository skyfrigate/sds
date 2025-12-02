# SDS - Simple Data Structures

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Type Checked](https://img.shields.io/badge/type%20checked-mypy-informational)](http://mypy-lang.org/)
[![Code Style](https://img.shields.io/badge/code%20style-flake8-informational)](https://flake8.pycqa.org/)
[![Static Badge](https://img.shields.io/badge/security-bandit-informational)](https://github.com/PyCQA/bandit)


Une bibliothèque Python complète et pédagogique de structures de données fondamentales, implémentées avec des principes de programmation orientée objet et une documentation exhaustive.

## 🎯 Objectifs

- **Pédagogique** : Code clair et bien documenté pour l'apprentissage
- **Complet** : Couverture exhaustive des structures de données classiques
- **Typé** : Support complet de MyPy avec type hints stricts
- **Testé** : Couverture de tests complète avec pytest
- **Performant** : Utilisation de `__slots__` pour l'optimisation mémoire

## 📦 Installation

```bash
# Installation depuis le dépôt
pip install git+https://github.com/votre-username/sds.git

# Installation en mode développement
git clone https://github.com/votre-username/sds.git
cd sds
pip install -e .
```

## 🏗️ Architecture

Le projet est organisé en modules thématiques :

```
sds/
├── core/           # Composants fondamentaux (Node abstraite, interfaces, exceptions)
├── linear/         # Structures linéaires (listes, piles, files)
├── trees/          # Structures arborescentes (arbres binaires, BST, AVL, heaps)
└── graphs/         # Structures de graphes (graphes, arêtes, algorithmes)
```

## 📚 Structures disponibles

### 🔗 Nœuds (Nodes) - `sds.core.node`

Tous les types de nœuds héritent d'une classe abstraite `Node` commune utilisant un système unifié de références (`_refs`).

#### Nœuds linéaires - `sds.linear.node`
- **`SimpleNode`** : Nœud pour listes chaînées simples (référence `next`)
- **`DoublyNode`** : Nœud pour listes doublement chaînées (références `next` et `prev`)

#### Nœuds arborescents - `sds.trees.node`
- **`BinaryNode`** : Nœud pour arbres binaires (références `left` et `right`)
- **`TreeNode`** : Nœud pour arbres généraux (liste de `children`)

#### Nœuds de graphes - `sds.graphs.node`
- **`GraphNode`** : Nœud pour graphes (identifiant unique, pas de références internes)

```python
from sds.linear.node import SimpleNode, DoublyNode
from sds.tree.node import BinaryNode, TreeNode
from sds.graph.node import GraphNode

# Liste chaînée simple
node1 = SimpleNode(1)
node2 = SimpleNode(2)
node1.next = node2

# Arbre binaire
root = BinaryNode(10)
root.left = BinaryNode(5)
root.right = BinaryNode(15)

# Graphe
node_a = GraphNode("A", "node_a")
node_b = GraphNode("B", "node_b")
```

### 📋 Structures linéaires - `sds.linear`

#### Listes chaînées - `sds.linear.list`
- **`LinkedList`** : Liste chaînée simple
  - Complexité : O(1) prepend, O(n) append, O(n) accès par index
  - Utilise `SimpleNode`
- **`DoublyLinkedList`** : Liste doublement chaînée
  - Complexité : O(1) prepend/append, O(n/2) accès par index optimisé
  - Utilise `DoublyNode`
  - Support de `__reversed__()` pour itération inverse
- **`CircularLinkedList`** : Liste chaînée circulaire
  - Méthode `rotate()` pour rotation en O(1)
  - Dernier nœud pointe vers le premier

```python
from sds.linear.list import LinkedList, DoublyLinkedList, CircularLinkedList

# Liste simple
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.prepend(0)
print(list(ll))  # [0, 1, 2]

# Liste doublement chaînée
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
print(list(reversed(dll)))  # [2, 1]

# Liste circulaire
cll = CircularLinkedList()
cll.append(1)
cll.append(2)
cll.append(3)
cll.rotate(1)
print(list(cll))  # [2, 3, 1]
```

#### Pile - `sds.linear.stack`
- **`Stack`** : Pile LIFO (Last In First Out)
  - Opérations : `push()`, `pop()`, `peek()`
  - Toutes les opérations en O(1)
  - Utilise `LinkedList` en interne

```python
from sds.linear.stack import Stack

stack = Stack()
stack.push(1)
stack.push(2)
stack.push(3)
print(stack.pop())  # 3
print(stack.peek()) # 2
```

#### Files - `sds.linear.queue`
- **`Queue`** : File FIFO (First In First Out)
  - Opérations : `enqueue()`, `dequeue()`, `front()`, `rear()`
  - Utilise `LinkedList` en interne
- **`Deque`** : File à double entrée
  - Opérations : `add_front()`, `add_rear()`, `remove_front()`, `remove_rear()`
  - Toutes les opérations en O(1)
  - Utilise `DoublyLinkedList` en interne
- **`PriorityQueue`** : File avec priorité
  - Élément avec priorité minimale défilé en premier
  - `enqueue()` en O(n), `dequeue()` en O(1)

```python
from sds.linear.queue import Queue, Deque, PriorityQueue

# File FIFO
queue = Queue()
queue.enqueue(1)
queue.enqueue(2)
print(queue.dequeue())  # 1

# Deque
deque = Deque()
deque.add_front(1)
deque.add_rear(2)
print(list(deque))  # [1, 2]

# File de priorité
pq = PriorityQueue()
pq.enqueue(5)
pq.enqueue(1)
pq.enqueue(3)
print(pq.dequeue())  # 1 (priorité minimale)
```

### 🌳 Structures arborescentes - `sds.trees`

#### Arbres de base
- **`BinaryTree`** : Arbre binaire simple *(à venir)*
  - Parcours : inorder, preorder, postorder, level-order
  - Opérations : hauteur, nombre de nœuds, recherche
- **`BinarySearchTree` (BST)** : Arbre binaire de recherche *(à venir)*
  - Propriété : left < parent < right
  - Recherche, insertion, suppression
  - O(log n) en moyenne, O(n) pire cas
- **`GeneralTree`** : Arbre général (n-aire) *(à venir)*
  - Nombre variable d'enfants par nœud
  - Parcours DFS/BFS

#### Arbres équilibrés
- **`AVLTree`** : Arbre AVL auto-équilibré *(à venir)*
  - Garantie O (log n) pour toutes les opérations
  - Rotations automatiques après insertion/suppression
- **`RedBlackTree`** : Arbre Rouge-Noir *(à venir)*
  - Auto-équilibré avec propriétés de couleur
  - Moins de rotations que pour un AVLTree

#### Tas (Heaps)
- **`MinHeap`** : Tas minimum *(à venir)*
  - Parent ≤ enfants
  - Extract-min en O(log n)
- **`MaxHeap`** : Tas maximum *(à venir)*
  - Parent ≥ enfants
  - Extract-max en O(log n)

#### Arbres spécialisés
- **`Trie`** : Arbre préfixe pour chaînes *(à venir)*
  - Auto-complétion, recherche de préfixe
- **`SegmentTree`** : Arbre de segments *(à venir)*
  - Requêtes de plage efficaces
- **`BTree`** : Arbre B pour bases de données *(à venir)*

### 🕸️ Structures de graphes - `sds.graphs`

#### Nœuds et arêtes
- **`GraphNode`** : Nœud de graphe avec identifiant unique
- **`Edge`** : Arête entre deux nœuds *(à venir)*
- **`DirectedEdge`** : Arc orienté *(à venir)*
- **`WeightedEdge`** : Arête pondérée *(à venir)*

#### Graphes
- **`Graph`** : Graphe de base *(à venir)*
- **`DirectedGraph`** : Graphe orienté *(à venir)*
- **`UndirectedGraph`** : Graphe non orienté *(à venir)*
- **`WeightedGraph`** : Graphe pondéré *(à venir)*

```python
from sds.graph.node import GraphNode

# Création de nœuds
node_a = GraphNode("A", "node_a")
node_b = GraphNode("B", "node_b")

# Les connexions seront gérées par Edge et Graph
```

## 🧪 Tests

Le projet utilise pytest avec une couverture de tests complète :

```bash
# Exécuter tous les tests
pytest

# Exécuter avec couverture
pytest --cov=sds --cov-report=html

# Exécuter les tests d'un module spécifique
pytest tests/02_linear/

# Exécuter en verbose
pytest -v
```

Structure des tests :
```
tests/
├── 01_core/        # Tests pour core (Node abstraite, interfaces, exceptions)
├── 02_linear/      # Tests pour structures linéaires
├── 03_trees/       # Tests pour structures arborescentes
└── 04_graphs/      # Tests pour structures de graphes
```

## 🔍 Analyse statique

Le projet est entièrement typé et vérifié avec MyPy et Flake8 :

```bash
# Vérification des types avec MyPy (mode strict)
mypy --strict sds/

# Vérification du style avec Flake8
flake8 sds/ --max-line-length=88

# Vérification combinée
mypy --strict sds/ && flake8 sds/ --max-line-length=88
```

## 📖 Documentation

La documentation utilise le format NumPy pour les docstrings et peut être générée avec Sphinx :

```bash
# Installer les dépendances de documentation
pip install sphinx numpydoc sphinx-rtd-theme

# Générer la documentation
cd docs
sphinx-build -b html . _build
```

## 🤝 Contribution

Les contributions sont les bienvenues ! Veuillez suivre ces guidelines :

1. **Fork** le projet
2. Créer une **branche** pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. **Commiter** vos changements (`git commit -m 'Add some AmazingFeature'`)
4. **Pousser** vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir un **Pull Request**

### Standards de qualité

- ✅ Code typé avec MyPy (strict mode)
- ✅ Style conforme à Flake8 (PEP 8)
- ✅ Tests avec pytest (couverture > 90%)
- ✅ Docstrings au format NumPy
- ✅ Utilisation de `__slots__` pour optimisation mémoire

## 📋 Roadmap

### ✅ Phase 1 : Fondations (Complétée)
- [x] Architecture modulaire
- [x] Nœuds abstraits avec système `_refs` unifié
- [x] Nœuds pour listes (SimpleNode, DoublyNode)
- [x] Nœuds pour arbres (BinaryNode, TreeNode)
- [x] Nœuds pour graphes (GraphNode)
- [x] Structures linéaires complètes
- [x] Tests exhaustifs pour linear

### 🚧 Phase 2 : Arbres (En cours)
- [ ] Interfaces abstraites (AbstractTree, AbstractBinaryTree)
- [ ] BinaryTree et BinarySearchTree
- [ ] MinHeap et MaxHeap
- [ ] AVLTree
- [ ] RedBlackTree
- [ ] Trie
- [ ] Tests exhaustifs pour trees

### 📅 Phase 3 : Graphes (Planifiée)
- [ ] Edge, DirectedEdge, WeightedEdge
- [ ] Graph, DirectedGraph, UndirectedGraph
- [ ] Algorithmes : DFS, BFS, Dijkstra, Kruskal
- [ ] Tests exhaustifs pour graphs

### 🔮 Phase 4 : Structures avancées (Planifiée)
- [ ] Union-Find (Disjoint Set)
- [ ] Bloom Filter
- [ ] Skip List
- [ ] Segment Tree
- [ ] B-Tree

## 📄 Licence

Ce projet est sous licence Apache 2.0 - voir le fichier [LICENSE](LICENSE.md) pour plus de détails.

## 👥 Auteurs

- **Votre Nom** - *Travail initial* - [votre-github](https://github.com/votre-username)

## 🙏 Remerciements

- Inspiré par les cours de structures de données classiques
- Conçu pour l'apprentissage et l'enseignement
- Merci à la communauté Python pour les outils exceptionnels (pytest, mypy, flake8)

## 📚 Ressources

- [Documentation Python](https://docs.python.org/3/)
- [Type Hints PEP 484](https://www.python.org/dev/peps/pep-0484/)
- [NumPy Docstring Guide](https://numpydoc.readthedocs.io/en/latest/format.html)
- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms-third-edition)

---

**Note** : Ce projet est en développement actif. Les fonctionnalités marquées *(à venir)* sont planifiées, mais pas encore implémentées.