# Algorithmen und Komplexitätstheorie

## 1. Definition von Algorithmen

### 1.1 Algorithmanweisungen
**Definition/Beschreibung**:  
Ein Algorithmus ist eine Anweisungsfolge, die verwendet wird, um ein bestimmtes Problem zu lösen. Er besteht aus einer Reihe von Schritten, die aufeinander folgen und das Problem in einzelne Teilprobleme zerlegen.

### 1.2 Beispiele für Algorithmen
**Beispiele**:  
Einige Beispiele für Algorithmen sind:

* Suchen nach dem kleinsten Element in einer Liste (O(n))
* Berechnung der kleinsten Differenz zwischen zwei Zahlen (O(n^2))
* Lösung des vereinfachten Rucksackproblems (exponentieller Aufwand)

## 2. Komplexitätstheorie

### 2.1 Laufzeit
**Definition/Beschreibung**:  
Die Laufzeit ist die Anzahl der Schritte, die ein Algorithmus benötigt, um ein Problem zu lösen.

### 2.2 Speicherbedarf
**Definition/Beschreibung**:  
Der Speicherbedarf ist die Anzahl der Speicherplatz, den ein Algorithmus benötigt, um ein Problem zu lösen.

## 3. Komplexitätsklassen

### 3.1 Konstante Laufzeit (O(1))
$$ O(1) = \{f(n): f(n) \leq c \text{ für alle } n > N \text{ und eine positive Konstante } c\} $$

### 3.2 Logarithmische Laufzeit (O(log n))
$$ O(\log n) = \{\log n, n^{\log k}, e^{\log k}\} $$

### 3.3 Lineare Laufzeit (O(n))
$$ O(n) = \{f(n): f(n) \leq c \cdot n \text{ für alle } n > N \text{ und eine positive Konstante } c\} $$

### 3.4 Quadratische Laufzeit (O(n^2))
$$ O(n^2) = \{f(n): f(n) \leq c \cdot n^2 \text{ für alle } n > N \text{ und eine positive Konstante } c\} $$

### 3.5 Exponentielle Laufzeit (O(2^n))
$$ O(2^n) = \{\frac{2^n}{c}, e^{n \log k}\} $$

## Begriffserklärung
* **Laufzeit**: Die Anzahl der Schritte, die ein Algorithmus benötigt, um ein Problem zu lösen.
* **Speicherbedarf**: Die Anzahl der Speicherplatz, den ein Algorithmus benötigt, um ein Problem zu lösen.

**Code**
```python
def suche_kleinstes_element(liste):
    # O(n) Laufzeit
    return min(liste)
```

Ich hoffe, diese strukturierte Erklärung hilft dir bei der Klausurvorbereitung!