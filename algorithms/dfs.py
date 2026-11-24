from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        # pilha: o último que entra é o primeiro que sai
        fronteira = [initial]
        # guarda a menor profundidade em que cada estado já foi expandido
        explorados = {}

        expandidos = 0
        gerados = 1
        max_fronteira = 1

        while fronteira:
            atual = fronteira.pop()

            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=expandidos,
                    nodes_generated=gerados,
                    max_frontier_size=max_fronteira,
                    depth=atual.cost,
                )

            if atual in explorados and explorados[atual] <= atual.cost:
                continue

            explorados[atual] = atual.cost
            expandidos += 1

            # não passa do limite de profundidade
            if atual.cost >= self.depth_limit:
                continue

            # invertido para o primeiro movimento ser o primeiro a sair da pilha
            for filho in reversed(atual.neighbors()):
                gerados += 1

                if filho in explorados and explorados[filho] <= filho.cost:
                    continue

                fronteira.append(filho)

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(
            solution=None,
            nodes_expanded=expandidos,
            nodes_generated=gerados,
            max_frontier_size=max_fronteira,
        )