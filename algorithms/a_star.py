import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        # distância de Manhattan: soma de quantas linhas e colunas cada peça está longe do lugar certo
        distancia = 0

        for indice, peca in enumerate(state.tiles):
            if peca == 0:
                continue

            linha_atual, coluna_atual = divmod(indice, 3)
            linha_certa, coluna_certa = divmod(GOAL_STATE.index(peca), 3)
            distancia += abs(linha_atual - linha_certa) + abs(coluna_atual - coluna_certa)

        return distancia

    def search(self, initial: State) -> SearchResult:
        # fila de prioridade ordenada por f = g + h
        contador = 0
        fronteira = [(self.heuristic(initial), contador, initial)]
        melhor_custo = {initial: 0}
        explorados = set()

        expandidos = 0
        gerados = 1
        max_fronteira = 1

        while fronteira:
            _, _, atual = heapq.heappop(fronteira)

            if atual in explorados:
                continue

            if atual.is_goal:
                return SearchResult(
                    solution=atual,
                    nodes_expanded=expandidos,
                    nodes_generated=gerados,
                    max_frontier_size=max_fronteira,
                    depth=atual.cost,
                )

            explorados.add(atual)
            expandidos += 1

            for filho in atual.neighbors():
                gerados += 1

                if filho in explorados:
                    continue

                # só entra na fronteira se for um caminho novo ou mais barato
                if filho not in melhor_custo or filho.cost < melhor_custo[filho]:
                    melhor_custo[filho] = filho.cost
                    contador += 1
                    f = filho.cost + self.heuristic(filho)
                    heapq.heappush(fronteira, (f, contador, filho))

            max_fronteira = max(max_fronteira, len(fronteira))

        return SearchResult(
            solution=None,
            nodes_expanded=expandidos,
            nodes_generated=gerados,
            max_frontier_size=max_fronteira,
        )