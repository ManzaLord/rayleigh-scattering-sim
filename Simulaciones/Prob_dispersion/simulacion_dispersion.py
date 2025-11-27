from manim import *

class Escena(Scene):
    def construct(self):
    
        particula = Circle(fill_color=BLUE, fill_opacity=1)
        self.play(Create(particula))
        self.play(particula.animate.scale(2))
        
        particula_text = Text("Partícula de aire").to_edge(UP)
        self.play(Write(particula_text))
        self.wait(1)
        self.play(particula.animate.scale(0.1))
        luz_incidente = Arrow(ORIGIN, RIGHT*4, color=WHITE).to_edge(LEFT)
        self.play(Create(luz_incidente))
        self.play(particula_text.animate.become(Text("Rayo del sol").next_to(luz_incidente,UP)))
        self.wait(1)
        onda = ParametricFunction(
            lambda t: np.array([t, 0.05*np.sin(16*t), 0]),
            t_range=[-1, 3],
            color=WHITE
        ).to_edge(LEFT)

        self.remove(luz_incidente)
        self.play(Create(onda)) 
        self.play(onda.animate.move_to(particula.get_center()).scale(0))
       
        self.play(particula_text.animate.become(Text("Dispersion de Rayleigh").to_edge(UP)))
        self.wait(1)

        long_onda = np.array([450*1e-9,533*1e-9,575*1e-9,600*1e-9,700*1e-9])
        angulos = np.arange(0,2*PI,PI/10)

        def calcular_intensidad(l,theta):
            return (1+np.cos(theta)**2)/(l)**4
        
        intensidades = [calcular_intensidad(i,angulos) for i in long_onda]

        I_0 = 2.44*1e25 #valor máximo posible: cos>max>pi,0 para azul

        def reescalar(I,I_0):
            return 4*I/I_0

        reescalados = [reescalar(i,I_0) for i in intensidades]

        def crear_vector(r,theta,onda):

            x = r*np.cos(theta)
            y = r*np.sin(theta)

            vectores = VGroup()

            for i in range(len(x)):
                pos = np.array([x[i], y[i], 0])
                vectores.add(Arrow(ORIGIN, pos, color=onda, buff=0))
            
            return vectores
        
        dic = {BLUE:reescalados[0], GREEN:reescalados[1],
         YELLOW:reescalados[2],ORANGE: reescalados[3],
         RED:reescalados[4] }

        dispersion = VGroup()

        for color, r in dic.items():
            dispersion.add(crear_vector(r, angulos, color))
        
        self.bring_to_front(particula_text)
        self.play(GrowFromCenter(dispersion), run_time=5)
        self.bring_to_front(particula_text)
        #self.play(ApplyWave(dispersion),run_time=5)


#self.play(particula_text.animate.move_to([-5,2,0]).scale(0.5))
#agrupo_coordenadas y vectores
#reescalo grupo y lo muevo a la derecha
