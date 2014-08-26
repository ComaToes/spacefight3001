import os, sys, pygame, resource

background = None
planets = {}
sounds = {}
music = {}
sprites = {}

def init():
    
    backgroundPath = os.path.join( "resource", "images", "starfield.png" )
    
    resource.background = pygame.image.load( packagedPath( backgroundPath ) ).convert()
    
    baseSpritePath = os.path.join( "resource", "sprites" )
    
    planetFilenames = [ "600blue", "600yellow", "bunny", "spacehattanday", "spacehattannight" ]
    
    for planetFilename in planetFilenames:
        img = pygame.image.load( packagedPath( os.path.join( baseSpritePath, planetFilename + ".png" ) ) ).convert_alpha()
        resource.planets[planetFilename] = img
    
    baseSoundPath = os.path.join( "resource", "sounds" )
    
    soundFilenames = [ "bazooka_fire", "explosion", "human_pain", "sound_psh" ]
    
    for soundFilename in soundFilenames:
        sound = pygame.mixer.Sound( packagedPath( os.path.join( baseSoundPath, soundFilename+".ogg" ) ) )
        resource.sounds[soundFilename] = sound
    
    baseMusicPath = os.path.join( "resource", "music" )
    
    musicFilenames = [ "title_music", "theme" ]
    
    for musicFilename in musicFilenames:
        resource.music[musicFilename] = packagedPath( os.path.join( baseMusicPath, musicFilename+".ogg" ) )

def packagedPath(path):
    if hasattr(sys,"_MEIPASS"):
        return os.path.join( sys._MEIPASS, path )
    return path

def sprite(name):
    if not name in resource.sprites:
        path = packagedPath( os.path.join( "resource", "sprites" , name+".png" ) )
        sprite = pygame.image.load( path ).convert_alpha()
        resource.sprites[name] = sprite
        
    return resource.sprites[name]    

