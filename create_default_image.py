from PIL import Image, ImageDraw, ImageFont
import os

def create_default_image():
    # Créer une image de 400x300 pixels
    img = Image.new('RGB', (400, 300), color='#8B0000')
    
    # Créer un objet de dessin
    draw = ImageDraw.Draw(img)
    
    # Ajouter un gradient simple
    for i in range(300):
        color = int(139 + (160 - 139) * i / 300)  # Dégradé de #8B0000 à #A0522D
        draw.line([(0, i), (400, i)], fill=(color, max(0, 82 - i//10), max(0, 45 - i//15)))
    
    # Ajouter le texte
    try:
        # Essayer d'utiliser une police système
        font = ImageFont.truetype("arial.ttf", 48)
    except:
        font = ImageFont.load_default()
    
    # Centrer le texte
    text = "🍷"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (400 - text_width) // 2
    y = (300 - text_height) // 2
    
    draw.text((x, y), text, fill='#FFD700', font=font)
    
    # Sauvegarder l'image
    os.makedirs("data/images", exist_ok=True)
    img.save("data/images/default.jpg")
    print("Image par défaut créée avec succès !")

if __name__ == "__main__":
    create_default_image()
