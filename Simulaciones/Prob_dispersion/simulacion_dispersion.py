from manim import * # utilizo biblioteca de Manim

class Escena(Scene):
    def construct(self):
        # particula de aire
        particula = Circle(fill_color=BLUE, fill_opacity=1) #crea un circulo azul relleno
        self.play(Create(particula)) #muestra la animacion de la particula
        self.play(particula.animate.scale(2)) #hace la particula mas grande

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
        nuevo_texto = MathTex("\\text{Rayo de Sol} \\hspace{1cm}",
    "\\lambda \\gg \\text{partícula}") # texto
        nuevo_texto.next_to(onda, UP*1) # muevo el texto arriba de la onda

        # transforma el texto de la particula en el del rayo del sol 
        self.play(particula_text.animate.become(nuevo_texto))
        self.play(Create(onda),run_time = 3) # animo la onda
        
        self.wait(1) # esperar un tiempo

        # mueve la onda al centro de la partícula y la reduce a un tamaño 0
        self.play(onda.animate.move_to(particula.get_center()).scale(0))
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
                    max_tip_length_to_length_ratio=0.001,buff=0 ,) 
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
