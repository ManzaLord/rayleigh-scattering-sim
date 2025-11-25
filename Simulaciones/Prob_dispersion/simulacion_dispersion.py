from manim import *

class Escena(Scene):
    def construct(self):
    
        particula = Circle(fill_color=BLUE, fill_opacity=1)
        self.play(Create(particula))
        self.play(particula.animate.scale(2))
        
        particula_text = Text("Partícula del aire").to_edge(UP)
        self.play(Write(particula_text))
        self.wait(1)
        self.play(particula.animate.scale(0.1))
        luz_incidente = Arrow(ORIGIN, RIGHT*4, color=WHITE).to_edge(LEFT)
        self.play(Create(luz_incidente))
        luz_text = Text("Luz del sol").next_to(luz_incidente,UP)
        self.play(Transform(particula_text,luz_text))
        self.wait(1)
        onda = ParametricFunction(
            lambda t: np.array([t, 0.05*np.sin(16*t), 0]),
            t_range=[-1, 3],
            color=WHITE
        ).to_edge(LEFT)
        self.remove(luz_incidente)
        self.play(Create(onda)) 
        self.play(onda.animate.move_to(particula.get_center()).scale(0))
        dispersion_text = Text("Dispersion de Rayleigh")
        self.play(FadeOut(onda))

        def intensidad(l):
            return (1 + np.cos(np.deg2rad(45))**2) / l**4
        
        coord_polares = Axes()
        

        
