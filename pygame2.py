import pygame
import random
from pygame import *

# Paramètres de l'écran
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600

# Initialisation de Pygame et création de l'écran
pygame.init()
ecran = pygame.display.set_mode([LARGEUR_ECRAN, HAUTEUR_ECRAN])
pygame.display.set_caption("The shoot'em up 1.0")

# Charger l'image de fond pour l'écran d'accueil après l'initialisation de l'écran
background = pygame.image.load("ressources/backgroundjeu.png").convert()

class Vaisseau(pygame.sprite.Sprite):
    def __init__(self):
        super(Vaisseau, self).__init__()
        self.surf = pygame.image.load("ressources/vaisseau.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys, le_missile, tous_sprites):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            if len(le_missile.sprites()) < 20:
                missile = Missile(self.rect.center)
                le_missile.add(missile)
                tous_sprites.add(missile)
        # Limites de l'écran
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > LARGEUR_ECRAN:
            self.rect.right = LARGEUR_ECRAN
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= HAUTEUR_ECRAN:
            self.rect.bottom = HAUTEUR_ECRAN


class Missile(pygame.sprite.Sprite):
    def __init__(self, center_missile):
        super(Missile, self).__init__()
        self.surf = pygame.image.load("ressources/missile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=center_missile)
        son_missile.play()

    def update(self):
        self.rect.move_ip(15, 0)
        if self.rect.left > LARGEUR_ECRAN:
            self.kill()

class Enemmi(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemmi, self).__init__()
        self.surf = pygame.image.load("ressources/ennemi.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(LARGEUR_ECRAN + 50, random.randint(0, HAUTEUR_ECRAN))
        )
        self.speed = random.randint(5, 20)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center_vaisseau):
        super(Explosion, self).__init__()
        self._compteur = 10
        self.surf = pygame.image.load("ressources/explosion.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=center_vaisseau)
        son_explosion.play()

    def update(self):
        self._compteur -= 1
        if self._compteur == 0:
            self.kill()

class Etoile(pygame.sprite.Sprite):
    def __init__(self):
        super(Etoile, self).__init__()
        self.surf = pygame.image.load("ressources/etoile.png").convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(LARGEUR_ECRAN + 20, random.randint(0, HAUTEUR_ECRAN))
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()

class Score(pygame.sprite.Sprite):
    def __init__(self):
        super(Score, self).__init__()
        self._scoreCourant = 0
        self._setText()

    def _setText(self):
        self.surf = police_score.render('Score : ' + str(self._scoreCourant), False, (255, 255, 255))
        self.rect = self.surf.get_rect(center=(LARGEUR_ECRAN / 2, 15))

    def update(self):
        self._setText()

    def incremente(self, valeur):
        self._scoreCourant += valeur


# Variables pour gérer les sons, polices, etc.
pygame.mixer.init()
son_missile = pygame.mixer.Sound("ressources/laser.ogg")
son_explosion = pygame.mixer.Sound("ressources/explosion.ogg")

pygame.font.init()
police_score = pygame.font.SysFont('Comic Sans MS', 30)
police_bouton = pygame.font.SysFont('Comic Sans MS', 50)

clock = pygame.time.Clock()

pygame.init()
pygame.display.set_caption("The shoot'em up 1.0")


ecran = pygame.display.set_mode([LARGEUR_ECRAN, HAUTEUR_ECRAN])

# Variables pour gérer les écrans
ecran_accueil = True

score_final = None
# Fonction pour afficher le bouton "Jouer"
def afficher_bouton_jouer(score_final=None):
    texte_jouer = police_bouton.render("JOUER", True, (255, 255, 255))
    rect_jouer = texte_jouer.get_rect(center=(LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2))
    ecran.blit(texte_jouer, rect_jouer)

    # Affiche le score final si disponible
    if score_final is not None:
        texte_score_final = police_score.render(f"Score final : {score_final}", True, (255, 255, 255))
        rect_score_final = texte_score_final.get_rect(center=(LARGEUR_ECRAN // 2, HAUTEUR_ECRAN // 2 + 60))
        ecran.blit(texte_score_final, rect_score_final)

    return rect_jouer


# Boucle de l'écran d'accueil
# Fonction pour l'écran d'accueil
def ecran_accueil(score_final=None):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if rect_jouer.collidepoint(event.pos):
                    return True

        ecran.blit(background, (0, 0))
        rect_jouer = afficher_bouton_jouer(score_final)
        pygame.display.flip()
        clock.tick(30)



# Boucle principale du jeu
# Fonction pour lancer la partie
def ecran_de_jeu():
    # Initialisation des groupes de sprites
    tous_sprites = pygame.sprite.Group()
    le_missile = pygame.sprite.Group()
    les_ennemies = pygame.sprite.Group()
    les_explosions = pygame.sprite.Group()
    les_etoiles = pygame.sprite.Group()
    vaisseau = Vaisseau()

    tous_sprites.add(vaisseau)
    score = Score()
    tous_sprites.add(score)

    AJOUTE_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(AJOUTE_ENEMY, 500)
    AJOUTE_ETOILE = pygame.USEREVENT + 2
    pygame.time.set_timer(AJOUTE_ETOILE, 100)

    # Boucle principale du jeu
    continuer = True
    score_final = None
    while continuer:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == AJOUTE_ENEMY:
                nouvel_enemmi = Enemmi()
                les_ennemies.add(nouvel_enemmi)
                tous_sprites.add(nouvel_enemmi)
            elif event.type == AJOUTE_ETOILE:
                nouvel_etoile = Etoile()
                les_etoiles.add(nouvel_etoile)
                tous_sprites.add(nouvel_etoile)

        ecran.fill((0, 0, 0))

        if pygame.sprite.spritecollideany(vaisseau, les_ennemies):
            vaisseau.kill()
            explosion = Explosion(vaisseau.rect.center)
            les_explosions.add(explosion)
            tous_sprites.add(explosion)
            score_final = score._scoreCourant
            continuer = False

        for missile in le_missile:
            liste_ennemis_touches = pygame.sprite.spritecollide(missile, les_ennemies, True)
            if len(liste_ennemis_touches) > 0:
                missile.kill()
                score.incremente(len(liste_ennemis_touches))
            for ennemi in liste_ennemis_touches:
                explosion = Explosion(ennemi.rect.center)
                les_explosions.add(explosion)
                tous_sprites.add(explosion)

        touche_appuyee = pygame.key.get_pressed()
        vaisseau.update(touche_appuyee, le_missile, tous_sprites)
        le_missile.update()
        les_ennemies.update()
        les_explosions.update()
        les_etoiles.update()
        score.update()

        for mon_sprite in tous_sprites:
            ecran.blit(mon_sprite.surf, mon_sprite.rect)
        ecran.blit(vaisseau.surf, vaisseau.rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.time.delay(3000)  # Pause avant de retourner à l'accueil
    return score_final

# Boucle principale de l'application
continuer_application = True
while continuer_application:
    score_final = ecran_de_jeu() if ecran_accueil(score_final) else None
    if score_final is None:
        continuer_application = False

pygame.quit()
