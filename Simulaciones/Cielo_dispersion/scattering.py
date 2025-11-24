from manim import *
import numpy as np

class Cuadro(Scene):
    def construct(self):
        cr = Circle(radius=3, color=BLUE)
        sq = Square(side_length=5, stroke_color=GREEN, fill_color=GREEN_B, fill_opacity=0.8)

        self.play(Create(sq), run_time= 5)
        self.wait()

class Test(Scene):
    def construct(self):
        
        name = Tex("Manza").to_edge(UL, buff=0.5)
        sq = Square(side_length=0.5, fill_color=BLUE, fill_opacity=0.9).shift(LEFT *3)
        tri = Triangle().scale(0.6).to_edge(DR)

        self.play(Write(name))
        self.play(DrawBorderThenFill(sq), run_time= 5)
        self.play(Create(tri))
        self.wait()

        self.play(name.animate.to_edge(UR), run_time= 2)
        self.play(sq.animate.scale(2), tri.animate.to_edge(DL), run_time=6)
        self.wait()

class Sky(Scene):
    
    def construct(self):
        earth = Circle(radius=0.5, color="#26AD44", fill_color="#156025", fill_opacity=1)
        atmosphere = Circle(radius=2,  color="#194BB8", fill_color="#378BD0", fill_opacity=0.3)
        
        self.play(Create(atmosphere),Create(earth), run_time=3)
        self.wait()

        planet = Group(atmosphere,earth)
        self.play(planet.animate.to_edge(DL), run_time= 3)

        target = Dot(point=ORIGIN)
        target.move_to(DOWN * 1.5 * earth.radius)
        sun = Circle(radius=0.3, color="#E38E2D", fill_color="#DDE32D", fill_opacity=1)
        light = always_redraw(lambda: Line(sun.get_center(), target.get_center(), color=WHITE))
        
        self.play(Create(target), Create(light), Create(sun))
        self.play(target.animate.move_to(earth.get_center() + UP * earth.radius),run_time=2)
        self.play(sun.animate.move_to(earth.get_center() + UP * 8 * earth.radius),run_time=2)
        self.wait()

