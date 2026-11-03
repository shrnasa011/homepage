"""A small Manim graph animation: reveal degrees and spotlight a vertex.

Install Manim, then run:
    manim -pql examples/graph_animation.py GraphPlayground
"""
from manim import Graph, Scene, Text, Integer, BLUE, YELLOW, UP, VGroup, FadeIn


class GraphPlayground(Scene):
    def construct(self):
        vertices = ["a", "b", "c", "d", "e"]
        edges = [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e")]
        positions = {
            "a": [-2, 1, 0], "b": [0, 2, 0], "c": [-2, -1, 0],
            "d": [1, 0, 0], "e": [3, 1, 0],
        }
        graph = Graph(
            vertices,
            edges,
            layout=positions,
            labels=True,
            vertex_config={"radius": 0.18},
        )
        self.play(FadeIn(graph))
        self.wait(0.4)

        degree_labels = VGroup(*[
            Integer(len(graph.neighbors[v]), color=BLUE)
            .scale(0.5)
            .next_to(graph[v], UP, buff=0.12)
            for v in vertices
        ])
        self.play(FadeIn(degree_labels))
        self.play(graph["d"].animate.set_color(YELLOW))
        title = Text("A tiny neighborhood can tell a story", font_size=26)
        title.to_edge(UP)
        self.play(FadeIn(title))
        self.wait(1)
