"""The rule grammar and the genetic-programming search of evo-1 (research/evo-1.md, "The
grammar" and "The search"). Pure numpy, no data access: a rule is evaluated on arrays of inputs
of shape (decisions, assets), so the same code runs on real panels and on synthetic worlds.

A rule is `(mode, tree)`, `mode` "slot" or "full". Trees are nested tuples:

- weight nodes: `("if", cond, weight, weight)`, `("const", v)`, `("volcap", t)`
- condition nodes: `("gtc", inp, c)` (input > c), `("ltc", inp, c)`, `("gt", inp, inp)`,
  `("coin",)`, `("and", cond, cond)`, `("or", cond, cond)`, `("not", cond)`
- an input is `(name, lookback)`, e.g. `("mom", 365)`.

Every tuple above is one node (inputs and constants are not nodes): `tsmom12` is 4 nodes.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from functools import partial
from typing import Any

import numpy as np

Node = tuple[Any, ...]
Rule = tuple[str, Node]
# (name, lookback) -> (T, A) floats, NaN where undefined; "coin" -> (A,) booleans;
# "vol30" -> (T, A) annualised 30-day volatility
Feats = dict[Any, np.ndarray]

LOOKBACKS = (7, 14, 30, 61, 91, 182, 290, 365)
FAMILY = {
    "mom": "M",
    "gap": "M",
    "dd": "M",
    "univ": "M",
    "lvol": "V",
    "rank": "U",
    "breadth": "U",
    "vrank": "U",
    "vbreadth": "U",
}
INPUTS = tuple((name, h) for name in FAMILY for h in LOOKBACKS)
GRID = {
    "M": (-2.0, -1.0, -0.5, 0.0, 0.5, 1.0, 2.0),
    "V": tuple(math.log(v) for v in (0.10, 0.15, 0.20, 0.30, 0.45, 0.60, 0.90)),
    "U": (0.2, 0.35, 0.5, 0.65, 0.8),
}
CONSTS = (0.0, 0.25, 0.5, 0.75, 1.0)
VOLCAPS = (0.10, 0.20, 0.40)
MAX_NODES, MAX_DEPTH = 20, 6
NODE_PENALTY = 0.01

_CHILDREN = {"if": (1, 2, 3), "and": (1, 2), "or": (1, 2), "not": (1,)}
_WEIGHT_OPS = ("if", "const", "volcap")

TSMOM12: Rule = ("slot", ("if", ("gtc", ("mom", 365), 0.0), ("const", 1.0), ("const", 0.0)))


# --- structure ---


def kind(node: Node) -> str:
    return "W" if node[0] in _WEIGHT_OPS else "C"


def size(node: Node) -> int:
    return 1 + sum(size(node[i]) for i in _CHILDREN.get(node[0], ()))


def depth(node: Node) -> int:
    return 1 + max((depth(node[i]) for i in _CHILDREN.get(node[0], ())), default=0)


def within_limits(node: Node) -> bool:
    return size(node) <= MAX_NODES and depth(node) <= MAX_DEPTH


def paths(node: Node, prefix: tuple[int, ...] = ()) -> list[tuple[tuple[int, ...], str]]:
    out = [(prefix, kind(node))]
    for i in _CHILDREN.get(node[0], ()):
        out += paths(node[i], (*prefix, i))
    return out


def get(node: Node, path: tuple[int, ...]) -> Node:
    for i in path:
        node = node[i]
    return node


def put(node: Node, path: tuple[int, ...], new: Node) -> Node:
    if not path:
        return new
    i = path[0]
    return (*node[:i], put(node[i], path[1:], new), *node[i + 1 :])


def valid(node: Node, want: str = "W") -> bool:
    """True if the tree is a sentence of the card's grammar."""
    op = node[0]
    if kind(node) != want:
        return False
    if op == "if":
        return valid(node[1], "C") and valid(node[2], "W") and valid(node[3], "W")
    if op == "const":
        return node[1] in CONSTS
    if op == "volcap":
        return node[1] in VOLCAPS
    if op in ("gtc", "ltc"):
        return node[1] in INPUTS and node[2] in GRID[FAMILY[node[1][0]]]
    if op == "gt":
        a, b = node[1], node[2]
        return a in INPUTS and b in INPUTS and a != b and FAMILY[a[0]] == FAMILY[b[0]]
    if op == "coin":
        return len(node) == 1
    if op in ("and", "or"):
        return valid(node[1], "C") and valid(node[2], "C")
    if op == "not":
        return valid(node[1], "C")
    return False


def show(node: Node) -> str:
    op = node[0]
    if op == "if":
        return f"if({show(node[1])}, {show(node[2])}, {show(node[3])})"
    if op == "const":
        return f"{node[1]:g}"
    if op == "volcap":
        return f"volcap({node[1]:g})"
    if op in ("gtc", "ltc"):
        return f"{node[1][0]}({node[1][1]}) {'>' if op == 'gtc' else '<'} {node[2]:.4g}"
    if op == "gt":
        return f"{node[1][0]}({node[1][1]}) > {node[2][0]}({node[2][1]})"
    if op == "coin":
        return "coin"
    if op == "not":
        return f"not({show(node[1])})"
    return f"{op}({show(node[1])}, {show(node[2])})"


def show_rule(rule: Rule) -> str:
    return f"{rule[0]}: {show(rule[1])}"


# --- evaluation ---


def evaluate(node: Node, feats: Feats) -> np.ndarray:
    """The tree's value per decision and asset: floats in [0, 1] for a weight node, booleans for
    a condition. A comparison with an undefined (NaN) input is false."""
    op = node[0]
    with np.errstate(invalid="ignore", divide="ignore"):
        if op == "if":
            return np.where(
                evaluate(node[1], feats), evaluate(node[2], feats), evaluate(node[3], feats)
            )
        if op == "const":
            return np.full(feats["vol30"].shape, node[1])
        if op == "volcap":
            v = feats["vol30"]
            return np.where(v > 0, np.minimum(1.0, node[1] / v), 0.0)  # undefined vol: hold none
        if op == "gtc":
            return np.asarray(feats[node[1]] > node[2])
        if op == "ltc":
            return np.asarray(feats[node[1]] < node[2])
        if op == "gt":
            return np.asarray(feats[node[1]] > feats[node[2]])
        if op == "coin":
            return np.broadcast_to(feats["coin"], feats["vol30"].shape)
        if op == "and":
            return evaluate(node[1], feats) & evaluate(node[2], feats)
        if op == "or":
            return evaluate(node[1], feats) | evaluate(node[2], feats)
        if op == "not":
            return ~evaluate(node[1], feats)
    raise ValueError(f"unknown node {op!r}")


def weights(rule: Rule, feats: Feats, eligible: np.ndarray) -> np.ndarray:
    """Target weights (T, A), long only, summing to at most 1. `slot`: the number is the share
    of the asset's equal slot (1 / eligible assets); `full`: rescaled to sum to 1 when any is
    held."""
    mode, tree = rule
    raw = np.where(eligible, evaluate(tree, feats), 0.0)
    if mode == "slot":
        n = eligible.sum(axis=1, keepdims=True)
        return np.asarray(raw / np.maximum(n, 1))
    tot = raw.sum(axis=1, keepdims=True)
    out = np.zeros_like(raw)
    np.divide(raw, tot, out=out, where=tot > 0)
    return out


# --- random rules and the genetic operators ---


def _pick(rng: np.random.Generator, seq: tuple[Any, ...]) -> Any:
    return seq[int(rng.integers(len(seq)))]


def _leaf(rng: np.random.Generator) -> Node:
    if rng.random() < 0.7:
        return ("const", _pick(rng, CONSTS))
    return ("volcap", _pick(rng, VOLCAPS))


def _comparison(rng: np.random.Generator) -> Node:
    u = rng.random()
    if u < 0.1:
        return ("coin",)
    a = _pick(rng, INPUTS)
    if u < 0.3:
        same = tuple(b for b in INPUTS if FAMILY[b[0]] == FAMILY[a[0]] and b != a)
        return ("gt", a, _pick(rng, same))
    return ("gtc" if rng.random() < 0.5 else "ltc", a, _pick(rng, GRID[FAMILY[a[0]]]))


def random_tree(rng: np.random.Generator, want: str, max_depth: int, full: bool) -> Node:
    """A random subtree of the wanted kind, at most `max_depth` deep; `full` grows every branch
    to that depth, otherwise branches stop early at random."""
    stop = max_depth <= 1 or (not full and rng.random() < 0.4)
    if want == "W":
        if stop:
            return _leaf(rng)
        return (
            "if",
            random_tree(rng, "C", max_depth - 1, full),
            random_tree(rng, "W", max_depth - 1, full),
            random_tree(rng, "W", max_depth - 1, full),
        )
    if stop:
        return _comparison(rng)
    op = _pick(rng, ("and", "or", "not"))
    if op == "not":
        return ("not", random_tree(rng, "C", max_depth - 1, full))
    return (
        op,
        random_tree(rng, "C", max_depth - 1, full),
        random_tree(rng, "C", max_depth - 1, full),
    )


def random_rule(rng: np.random.Generator, max_depth: int, full: bool) -> Rule:
    """An initial rule: an `if` at the root, so the rule has at least one condition. A draw over
    the size limits is drawn again. A full tree of depth 4 never fits in 20 nodes (it has at
    least 26), so after 20 failed full draws the rule is grown freely until one reaches exactly
    `max_depth` (card note of 2026-11-18)."""
    mode = "slot" if rng.random() < 0.5 else "full"
    tries = 0
    while True:
        as_full = full and tries < 20
        tree: Node = (
            "if",
            random_tree(rng, "C", max_depth - 1, as_full),
            random_tree(rng, "W", max_depth - 1, as_full),
            random_tree(rng, "W", max_depth - 1, as_full),
        )
        tries += 1
        if within_limits(tree) and (as_full or not full or depth(tree) == max_depth):
            return (mode, tree)


def _checked(parent: Rule, tree: Node) -> Rule:
    """A child over the limits is replaced by its parent."""
    return (parent[0], tree) if within_limits(tree) else parent


def crossover(a: Rule, b: Rule, rng: np.random.Generator) -> Rule:
    """A random subtree of `a` is replaced by a random subtree of `b` of the same kind."""
    pa, k = _pick(rng, tuple(paths(a[1])))
    donors = tuple(p for p, kb in paths(b[1]) if kb == k)
    if not donors:
        return a
    return _checked(a, put(a[1], pa, get(b[1], _pick(rng, donors))))


def subtree_mutation(a: Rule, rng: np.random.Generator) -> Rule:
    pa, k = _pick(rng, tuple(paths(a[1])))
    return _checked(a, put(a[1], pa, random_tree(rng, k, int(rng.integers(1, 4)), False)))


def point_mutation(a: Rule, rng: np.random.Generator) -> Rule:
    """One lookback, constant, comparison direction, leaf or the slot/full switch changes."""
    ops = ("gtc", "ltc", "gt", "const", "volcap")
    spots = [p for p, _ in paths(a[1]) if get(a[1], p)[0] in ops]
    j = int(rng.integers(len(spots) + 1))
    if j == len(spots):
        return ("full" if a[0] == "slot" else "slot", a[1])
    node = get(a[1], spots[j])
    op = node[0]
    new: Node
    if op in ("const", "volcap"):
        new = _leaf(rng)
        while new == node:
            new = _leaf(rng)
    elif op == "gt":
        side = 1 + int(rng.integers(2))
        other = node[3 - side]
        hs = tuple(h for h in LOOKBACKS if (node[side][0], h) not in (node[side], other))
        new = put(node, (side,), (node[side][0], _pick(rng, hs)))
    else:
        what = int(rng.integers(3))
        if what == 0:
            hs = tuple(h for h in LOOKBACKS if h != node[1][1])
            new = (op, (node[1][0], _pick(rng, hs)), node[2])
        elif what == 1:
            cs = tuple(c for c in GRID[FAMILY[node[1][0]]] if c != node[2])
            new = (op, node[1], _pick(rng, cs))
        else:
            new = ("ltc" if op == "gtc" else "gtc", node[1], node[2])
    return (a[0], put(a[1], spots[j], new))


# --- the search ---


def order(scored: dict[Rule, float]) -> list[Rule]:
    """Best first; ties: fewer nodes, then alphabetical."""
    return sorted(scored, key=lambda r: (-scored[r], size(r[1]), show_rule(r)))


def _tournament(pop: list[Rule], fit: np.ndarray, k: int, rng: np.random.Generator) -> Rule:
    draw = rng.integers(len(pop), size=k)
    return pop[int(draw[np.argmax(fit[draw])])]


def evolve(
    fitness: Callable[[Rule], float],
    seed: int,
    population: int = 500,
    generations: int = 30,
    tournament: int = 4,
    elite: int = 5,
) -> dict[Rule, float]:
    """One GP run. `fitness` returns the penalised fitness of a rule (-inf if invalid). Returns
    every different formula scored with its fitness: the search's universe for this run."""
    rng = np.random.default_rng(seed)
    scored: dict[Rule, float] = {}

    def score(rule: Rule) -> float:
        if rule not in scored:
            scored[rule] = fitness(rule)
        return scored[rule]

    pop = [random_rule(rng, 2 + i % 3, full=i % 2 == 1) for i in range(population)]
    for _ in range(generations):
        fit = np.array([score(r) for r in pop])
        ranked = sorted(range(population), key=lambda i: (-fit[i], size(pop[i][1]), i))

        nxt = [pop[i] for i in ranked[:elite]]
        while len(nxt) < population:
            pick = partial(_tournament, pop, fit, tournament, rng)
            u = rng.random()
            if u < 0.60:
                nxt.append(crossover(pick(), pick(), rng))
            elif u < 0.75:
                nxt.append(subtree_mutation(pick(), rng))
            elif u < 0.95:
                nxt.append(point_mutation(pick(), rng))
            else:
                nxt.append(pick())
        pop = nxt
    for r in pop:
        score(r)
    return scored
