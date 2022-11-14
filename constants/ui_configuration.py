import pygame


class UIConfiguration:

    def __init__(self, pygame) -> None:
        super().__init__()
        self.__pygame = pygame
        self.__pygame.display.set_caption("PYTRIS™")

        self.block_size = 17  # Height, width of single block

        self.screen = pygame.display.set_mode((300, 374))
        self.leaders = None
        self.lines = None

        # Fonts
        self.font_path = "../assets/fonts/OpenSans-Light.ttf"
        self.font_path_b = "../assets/fonts/OpenSans-Bold.ttf"
        self.font_path_i = "../assets/fonts/Inconsolata/Inconsolata.otf"

        self.h1 = self.__pygame.font.Font(self.font_path, 50)
        self.h2 = self.__pygame.font.Font(self.font_path, 30)
        self.h4 = self.__pygame.font.Font(self.font_path, 20)
        self.h5 = self.__pygame.font.Font(self.font_path, 13)
        self.h6 = self.__pygame.font.Font(self.font_path, 10)

        self.h1_b = self.__pygame.font.Font(self.font_path_b, 50)
        self.h2_b = self.__pygame.font.Font(self.font_path_b, 30)

        self.h2_i = self.__pygame.font.Font(self.font_path_i, 30)
        self.h5_i = self.__pygame.font.Font(self.font_path_i, 13)

        # Sounds
        self.click_sound = self.__pygame.mixer.Sound("assets/sounds/SFX_ButtonUp.wav")
        self.move_sound = self.__pygame.mixer.Sound("assets/sounds/SFX_PieceMoveLR.wav")
        self.drop_sound = self.__pygame.mixer.Sound("assets/sounds/SFX_PieceHardDrop.wav")
        self.single_sound = self.__pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearSingle.wav")
        self.double_sound = self.__pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearDouble.wav")
        self.triple_sound = self.__pygame.mixer.Sound("assets/sounds/SFX_SpecialLineClearTriple.wav")
        self.tetris_sound = self.__pygame.mixer.Sound("assets/sounds/SFX_SpecialTetris.wav")

        # Background colors
        self.black = (10, 10, 10)  # rgb(10, 10, 10)
        self.white = (255, 255, 255)  # rgb(255, 255, 255)
        self.grey_1 = (26, 26, 26)  # rgb(26, 26, 26)
        self.grey_2 = (35, 35, 35)  # rgb(35, 35, 35)
        self.grey_3 = (55, 55, 55)  # rgb(55, 55, 55)

        # Tetrimino colors
        self.cyan = (69, 206, 204)  # rgb(69, 206, 204) # I
        self.blue = (64, 111, 249)  # rgb(64, 111, 249) # J
        self.orange = (253, 189, 53)  # rgb(253, 189, 53) # L
        self.yellow = (246, 227, 90)  # rgb(246, 227, 90) # O
        self.green = (98, 190, 68)  # rgb(98, 190, 68) # S
        self.pink = (242, 64, 235)  # rgb(242, 64, 235) # T
        self.red = (225, 13, 27)  # rgb(225, 13, 27) # Z

        self.t_color = [self.grey_2, self.cyan, self.blue, self.orange, self.yellow, self.green, self.pink, self.red,
                        self.grey_3]




