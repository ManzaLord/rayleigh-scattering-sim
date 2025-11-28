from manim import * # utilizo biblioteca de Manim
config.disable_caching = True
config.save_last_frame = False
class Escena(Scene):
    def construct(self):

        # creo los atomos
        # orbitas como circulos 
        orbita1 = Circle(radius=2, color = WHITE)
        orbita2 = Circle(radius=4, color = WHITE)
        orbita3= Circle(radius=6, color = WHITE)

        # protones mas pequeños que el neutron como pelotitas
        proton1 = Circle(radius=0.4,fill_color=BLUE, fill_opacity=1 ).move_to(UP*0.5)
        neutron1 = Circle(radius=0.5,fill_color=GRAY, fill_opacity=1).move_to(LEFT*0.5)
        proton2 = Circle(radius=0.4, fill_color=BLUE, fill_opacity=1).move_to(RIGHT*0.5)
        neutron2 = Circle(radius=0.5, fill_color=GRAY, fill_opacity=1).move_to(DOWN*0.5)
        proton3 = Circle(radius=0.4,fill_color=BLUE, fill_opacity=1) 

        # electrones como puntos en orbitas
        electron1 = Dot(radius=0.3, color = RED).move_to(orbita1.point_from_proportion(0))
        electron2 = Dot(radius=0.3, color = RED).move_to(orbita2.point_from_proportion(0.25))
        electron3 = Dot(radius=0.3, color = RED).move_to(orbita3.point_from_proportion(0.75))

        # este updater actualiza la posicion del electron en la orbita 
        # para aparentar que orbita
        electron1.add_updater(
            lambda m, dt: m.move_to(
                orbita1.point_from_proportion((self.time *0.5 ) % 1)
            )
        )

        electron2.add_updater(
            lambda m, dt: m.move_to(
                orbita2.point_from_proportion((self.time*0.4 ) % 1)
            )
        )

        electron3.add_updater(
            lambda m, dt: m.move_to(
                orbita3.point_from_proportion((self.time*0.7) % 1)
            )
        )
        
        # agrupo los componentes del atomo en un grupo 
        atomo1 = VGroup(orbita1,orbita2,orbita3,proton1,
            proton2,proton3,neutron1,neutron2,electron1,
            electron2,electron3).move_to(LEFT*1.5).scale(0.3)
        
        # genero copias para crear el segundo atomo
        orb2_1 = orbita1.copy()
        orb2_2 = orbita2.copy()
        orb2_3 = orbita3.copy()

        e2_1 = Dot(radius=0.3, color = RED).move_to(orb2_1.point_from_proportion(0))
        e2_2 = Dot(radius=0.3, color = RED).move_to(orb2_2.point_from_proportion(0.25))
        e2_3 = Dot(radius=0.3, color = RED).move_to(orb2_3.point_from_proportion(0.75))

        # reescalo los puntos
        e2_1.scale(0.3)
        e2_2.scale(0.3)
        e2_3.scale(0.3)

        # los pongo a orbitar alrededor de las orbitas copias
        e2_1.add_updater(lambda m,dt: m.move_to(orb2_1.point_from_proportion((self.time*0.5)%1)))
        e2_2.add_updater(lambda m,dt: m.move_to(orb2_2.point_from_proportion((self.time*0.4)%1)))
        e2_3.add_updater(lambda m,dt: m.move_to(orb2_3.point_from_proportion((self.time*0.7)%1)))

        # segundo atomo
        atomo2 = VGroup(
            orb2_1, orb2_2, orb2_3,
            proton1.copy(), proton2.copy(), proton3.copy(),
            neutron1.copy(), neutron2.copy(),
            e2_1, e2_2, e2_3
        ).move_to(RIGHT*1.5)

        # animo los atomos
        self.play(Create(atomo1), run_time = 3)
        self.play(Create(atomo2),run_time = 3)

        # genero una lemniscata para englobar a los atomos
        # como una particula conjunta
        def polar(theta):
            r = 1 + np.cos(theta)**2
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            return np.array([x, y, 0])

        # Creo la lemniscata con polares
        curva = ParametricFunction(
            polar,
            t_range=np.array([0, 2*np.pi]),
            fill_color=BLUE, fill_opacity=1,).scale(2)  # ajusta el tamaño

        # animo la lemniscata
        self.play(Create(curva), run_time=4)

        # agrupo todo en una particula
        particula = VGroup(atomo1,atomo2,curva) 

        # texto
        particula_text = Text("Partícula de aire").to_edge(UP) #pone el texto arriba
        self.play(Write(particula_text))#muestra la animacion del texto
        self.wait(1) #se espera 1 s
        self.play(particula.animate.scale(0.005)) #hace la partícula mas pequeña

        # Rayo de sol
        onda = ParametricFunction(
            lambda t: np.array([t, 0.2*np.sin(4*t), 0]),
            t_range=[-1, 8],
            color=WHITE
        ).to_edge(LEFT)


        nuevo_texto = MathTex("\\text{Rayo del sol} \\hspace{1cm}", 
            "\\lambda >> \\text{partícula}") # texto

        nuevo_texto.next_to(onda, UP*1) # muevo el texto arriba de la onda

        # transforma el texto de la particula en el del rayo del sol 
        self.play(particula_text.animate.become(nuevo_texto))
        self.play(Create(onda),run_time = 3) # animo la onda
        
        self.wait(1) # esperar un tiempo

        # creo las cargas como pelotitas con texto de + y -
        positivo = Circle(radius = 0.8,fill_color=WHITE, fill_opacity=1).move_to(LEFT*1).scale(0.5)
        positivo_texto = Text("+", font_size=24, color=BLACK).move_to(positivo.get_center())  # ajusta tamaño si quieres
        
        negativo = Circle(radius = 0.8,fill_color=WHITE, fill_opacity=1).move_to(RIGHT*1).scale(0.5)
        negativo_texto = Text("-", font_size=24, color=BLACK).move_to(negativo.get_center())  # ajusta tamaño si quieres


        # hago zoom a la particula
        self.play(particula.animate.scale(100).move_to(ORIGIN), run_time=2)

        # muestro las cargas tipo dipolo 
        self.play(Create(positivo))
        self.play(Write(positivo_texto))

        self.play(Create(negativo))
        self.play(Write(negativo_texto))
        # Return to original scale
        self.remove(negativo_texto)
        self.remove(negativo)
        self.remove(positivo_texto)
        self.remove(positivo)

        # zoom out de la particula
        self.play(particula.animate.scale(0.0005).move_to(ORIGIN), run_time=2)

        # desaparece la onda
        self.play(FadeOut(onda), run_time=2)
        self.bring_to_back(particula) # pongo la particula en el fondo
    
    
        # longitudes de onda de la luz visible
        long_onda = np.array([450*1e-9,533*1e-9,575*1e-9,600*1e-9,700*1e-9])
        
        # Ángulos de dispersión
        angulos = np.arange(0,2*PI,PI/30)

        # calcula la intensidad segun la longitud de onda y el angulo dispersado
        # usa la ecuacion de rayleigh
        def calcular_intensidad(l,theta):
            return (1+np.cos(theta)**2)/(l)**4
        
        #aplica la funcion de intensidad a cada longitud de onda
        intensidades = [calcular_intensidad(i,angulos) for i in long_onda]

        # para reescalar las intensidades que estan en el orden de 1e25 aprox
        # utilizo regla de 3 para reescalar donde el valor mas grande de intensidad = 9

        I_0 = intensidades[0].max() # valor máximo posible: cos>max>pi,0 para azul

        def reescalar(I,I_0): # regla de 3 para reescalar, tomando el valor maximo como 9 
            return 9*I/I_0

        # reescalo las intensidades
        reescalados = [reescalar(i,I_0) for i in intensidades]

        # como la intensidad depende del ángulo, y la intensidad es como 
        # la magnitud del vector que me lo representa, puedo tomarlo como en 
        # coordenadas polares que convierto en cartesianas para poder visualizarlo 
        # como vector
        
        def crear_vector(r, theta, onda):
            # hace la conversion de polares a cartesianas
            x = r * np.cos(theta)
            y = r * np.sin(theta)

            # guardo los vectores de intensidad calculados
            # para la longitud de onda especifica en todas
            # direcciones usando VGroup de Manim
            vectores = VGroup()

            # Genera el vector 
            for i in range(len(x)):
                pos = np.array([x[i], y[i], 0]) # guardo las coordenadas (x,y,x)

                # genero el Mobject> Flecha
                flecha = Arrow(ORIGIN, pos,color=onda,
                    max_tip_length_to_length_ratio=0.01,buff=0 ,) 
                vectores.add(flecha) # guardo en grupo

            return vectores
        
        #creo un diccionario con el color y sus respectivas intensidades reescaladas
        dic = {BLUE:reescalados[0], GREEN:reescalados[1],
         YELLOW:reescalados[2],ORANGE: reescalados[3],
         RED:reescalados[4] }
        
        self.remove(particula_text) # elimino el texto 
        
        # guardo todas las flechas en un grupo para luego animarlas en conjunto
        dispersion = VGroup()

        # Genero las flechas por cada longitud de onda 
        for color, r in dic.items():
            dispersion.add(crear_vector(r, angulos, color))  

        
        # animo las flechas para que crezcan del centro hacia afuera
        self.play(GrowFromCenter(dispersion), run_time=6)  

        # Agrupo la partícula y las flechas
        grupo = VGroup(particula,dispersion)

        # hago pequeña las flechas
        self.play(dispersion.animate.scale(0.3))

        # muevo las flechas y las particulas a la derecha
        self.play(grupo.animate.move_to([3.5,0,0]))
        self.wait(1)

        # texto
        texto = Text("Probabilidad de Dispersión de Rayleigh").to_edge(UP) # en esquina arriba
        
        # animo el texto
        self.play(Write(texto)) 
        
        # creo la fomula de la intensidad
        formula= MathTex('I \\propto \\frac{1+\\cos(\\theta)^{2}}{\\lambda^{4}} ').move_to([-3,0,0])
        self.play(Write(formula), run_time=1) # animo la formula
        self.wait(3)
