from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):

    def search(self, initial: State) -> SearchResult:
        if initial.is_goal:
            return SearchResult(solution=initial, nodes_generated=1, max_frontier_size=1, depth=0)

        # fila: o primeiro que entra é o primeiro que sai
        fronteira = deque([initial])
        na_fronteira = {initial}
        explorados = set()

        expandidos = 0
        gerados = 1
        max_fronteira = 1

        while fronteira:
            atual = fronteira.popleft()
            na_fronteira.remove(atual)
            explorados.add(atual)
            expandidos += 1

            for filho in atual.neighbors():
                gerados += 1

                if filho in explorados or filho in na_fronteira:
                    continue

                if filho.is_goal:
                    return SearchResult(
                        solution=filho,
                        nodes_expanded=expandidos,
                        nodes_generated=gerados,
                        max_frontier_size=max_fronteira,
                        depth=filho.cost,
                    )

                fronteira.append(filho)
                na_fronteira.add(filho)

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(
            solution=None,
            nodes_expanded=expandidos,
            nodes_generated=gerados,
            max_frontier_size=max_fronteira,
        )