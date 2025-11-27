from manim import *
import numpy as np


class Sky(Scene):
    
    def construct(self):
        #Crea las figuras de la tierra y la atmosfera
        earth = Circle(radius=0.5, color="#26AD44", fill_color="#156025", fill_opacity=1)
        atmosphere = Circle(radius=2,  color="#194BB8", fill_color="#378BD0", fill_opacity=0.3)
        textY = Text("&")
        textEarth = Text("Tierra",color=GREEN).move_to(UP*1)
        textAtm = Text("Atmosfera",color=BLUE).move_to(DOWN*1)
        textGroup = VGroup(textEarth,textY,textAtm).to_edge(RIGHT)
        
        #Muestra la tierra y la atmosfera en el escenario
        self.play(Create(atmosphere),Create(earth),FadeIn(textGroup), run_time=3)
        self.wait(2)

        #Agrupa la tierra y la atmosfera y la mueve a un lado del escenario
        planet = Group(atmosphere,earth)
        self.play(planet.animate.to_edge(DL),FadeOut(textGroup), run_time= 2)

        #Crea el sol, el blanco y el rayo de luz que viaja de uno a otro
        target = Dot(point=ORIGIN)
        target.move_to(DOWN * 1.5 * earth.radius)
        sun = Circle(radius=0.3, color="#E38E2D", fill_color="#DDE32D", fill_opacity=1)
        light = always_redraw(lambda: Line(target.get_center(), sun.get_center(), color=WHITE))
        textSun = Text("Sol", color=YELLOW).move_to(UP*1)
        textY2 = Text("&")
        textTarget = Text("Receptor").move_to(DOWN*1)
        textGroup2 = VGroup(textSun,textY2,textTarget).to_edge(RIGHT)
        
        #MUesta el sol, el blanco y el rayo de luz en el escenario
        self.play(Create(target), Create(light), Create(sun),FadeIn(textGroup2),run_time=2)
        self.wait()

        #Mueve el blanco, y el sol a sus posiciones iniciales
        self.play(FadeOut(textGroup2),target.animate.move_to(earth.get_center() + UP * earth.radius), sun.animate.move_to(earth.get_center() + UP * 8 * earth.radius),run_time=2)
        self.wait()

        #Genera un marco de cordenadas en la ubicacion del blanco
        xAxis = Arrow(target.get_center(), target.get_center() + RIGHT * 8 * earth.radius, color = "#27BEF5",buff= 0)
        yAxis = Arrow(target.get_center(), target.get_center() + UP * 8 * earth.radius, color = "#27BEF5",buff=0)

        #Coloca el marco de coordenadas detras del resto de figuras
        xAxis.set_z_index(-1)
        yAxis.set_z_index(-1)

        #Crea un plano para mostrar los resultados
        plane = NumberPlane(x_range=[400,700,50], x_length=6, y_range=[0,100,20], y_length=4, background_line_style={"stroke_opacity": 1}).to_edge(RIGHT).add_coordinates()

        #Nombres en los ejes
        xLabel = MathTex(r"\lambda (nm)").scale(0.4).move_to(RIGHT*6.7+DOWN*1)
        yLabel = MathTex(r"I/I_0 (\%)").to_edge(UP).scale(0.4)
        labels = Group(xLabel,yLabel)

        #Muestra el marco de coordenadas y el plano en el escenario
        self.play(Create(xAxis), Create(yAxis), Rotate(sun, -PI/4, about_point=target.get_center()), DrawBorderThenFill(plane), run_time=3)
        self.wait()

        #Genera el angulo entre la tangente de la tierra y el sol
        angle = always_redraw(lambda: Angle(xAxis, light, radius=1, color=WHITE))
        symbol = always_redraw(lambda: MathTex(r"\alpha").next_to(angle).scale(0.9))
        alpha = always_redraw(lambda: MathTex(r"\alpha = " + f"{self.getAngle(light,xAxis)*180/PI:.2f}^\circ").to_edge(DOWN).scale(1))

        #Calcula la intensidad en funcion de la longitud de onda y el angulo
        graf = always_redraw(lambda: plane.plot(lambda x: self.getIntensity(x,self.getAngle(light,xAxis)), x_range=[400,700], color=WHITE))

        #Genera los colores para seguir de forma mas sencilla el sistema
        rainbow = ["#4b369d", "#487de7", "#79c314", "#faeb36", "#ffa500", "#e81416"]
        colors = always_redraw(lambda:plane.get_riemann_rectangles(graf, x_range=[400,700], dx=5,color=rainbow))

        #Junta las partes del grafico para moverlo en conjunto
        graphicGroup = Group(plane,colors)

        #Muestra el angulo en pantalla
        self.play(Create(angle), Create(symbol), Create(alpha), Create(colors),run_time=4)
        self.play(graphicGroup.animate.to_edge(UP),FadeIn(labels),run_time= 3)
        self.play(Rotate(sun, -2*PI/9, about_point=target.get_center()), run_time=3)
        self.wait()
        
        #Gira el sol para mostrar la dependencia de la intensidad de este
        self.play(Rotate(sun, 17*PI/36, about_point=target.get_center()), run_time=6)
        self.wait()
        self.play(Rotate(sun, -17*PI/36, about_point=target.get_center()), run_time=6)
        self.wait()


    #Funcion que obtiene el angulo en grados entre 2 lineas
    def getAngle(self,l1,l2):
        #Convierte las lineas en vectores
        v1 = l1.get_unit_vector()
        v2 = l2.get_unit_vector()

        #Realiza el producto punto
        dot = np.dot(v1, v2)
        
        #Devuelve el angulo
        return np.arccos(dot)


    def getIntensity(self,wavelength, angle):
        #Ajusta la longitud de onda a su valor en nanometros
        wl = wavelength * 1e-9

        #Calcula la intensidad maxima
        intensityMax = 2 / (np.power(400 * 1e-9,4))

        #Calcula la intensidad para el caso especifico
        intensity = (1 + np.power(np.cos(angle),2)) / np.power(wl,4)

        #Retorna un porcentaje de  I / Imax
        return 100 * (1 - (intensity/ intensityMax))