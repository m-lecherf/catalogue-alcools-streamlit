import streamlit as st
import json
import os
import hashlib
from datetime import datetime
from PIL import Image
import uuid

# Configuration de l'application
st.set_page_config(
    page_title="VinPedia - Catalogue d'Alcools Faits Maison", 
    layout="wide",
    page_icon="🍷",
    initial_sidebar_state="expanded"
)

# Configuration avec chemins relatifs pour le déploiement
ADMIN_EMAIL = "admin@vinpedia.com"
ADMIN_PASSWORD = "admin123"
ALLOWED_EMAILS = ["louis@vinpedia.com", ADMIN_EMAIL]

# Chemins relatifs pour Streamlit Cloud
DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "recipes.json")
IMAGES_DIR = os.path.join(DATA_DIR, "images")

MAP_PASSWORD_EMAIL = { "louis@vinpedia.com": "user123", ADMIN_EMAIL: ADMIN_PASSWORD }

# Création des dossiers si nécessaire - avec gestion d'erreurs
def ensure_directories():
    """Créer les dossiers nécessaires avec gestion d'erreurs"""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(IMAGES_DIR, exist_ok=True)
        
        # Créer le fichier JSON s'il n'existe pas
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
                
    except Exception as e:
        st.error(f"Erreur lors de la création des dossiers: {e}")

# Appeler la fonction de création des dossiers
ensure_directories()

# CSS moderne et simple
def load_css():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&display=swap');
    
    /* Variables CSS modernes */
    :root {
        --primary: #2563eb;
        --secondary: #64748b;
        --accent: #3b82f6;
        --success: #10b981;
        --warning: #f59e0b;
        --error: #ef4444;
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-card: #ffffff;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --text-light: #94a3b8;
        --border: #e2e8f0;
        --shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        
        /* Variables artisanales */
        --primary-color: #8B7355;
        --secondary-color: #C4A484;
        --accent-color: #F4D03F;
        --olive-green: #7D8471;
        --warm-white: #FAF7F0;
        --cream: #F5F1E8;
    }
    
    /* Background principal */
    .stApp {
        background: var(--bg-secondary);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar moderne */
    .css-1d391kg {
        background: linear-gradient(145deg, var(--olive-green), var(--primary-color));
        border-right: 1px solid var(--border);
    }
    
    /* Header artisanal */
    .page-header {
        text-align: center;
        padding: 3rem 0 2rem 0;
        background: linear-gradient(135deg, var(--cream), var(--warm-white));
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
    }
    
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-family: 'Montserrat', sans-serif;
        font-size: 1.5rem;
        color: var(--text-secondary);
        font-weight: 400;
    }
    
    /* Cards recettes style artisanal */
    .recipe-card {
        background: var(--bg-card);
        border-radius: 20px;
        padding: 0;
        margin: 2rem 0;
        box-shadow: var(--shadow-lg);
        border: 2px solid var(--secondary-color);
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .recipe-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    .recipe-card-header {
        background: linear-gradient(135deg, var(--secondary-color), var(--primary-color));
        padding: 1.5rem;
        color: white;
    }
    
    .recipe-card-body {
        padding: 2rem;
    }
    
    /* Badges avec couleurs par type */
    .badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.2rem;
        font-family: 'Montserrat', sans-serif;
    }
    
    .badge-vin { background: #e0e7ff; color: #3730a3; }
    .badge-biere { background: #fed7aa; color: #c2410c; }
    .badge-liqueur { background: #fecaca; color: #dc2626; }
    .badge-rhum { background: #d4b486; color: #8b4513; }
    .badge-vodka { background: #f1f5f9; color: #475569; }
    .badge-autre { background: #f3e8ff; color: #7c3aed; }
    
    .badge-prix { background: #dcfce7; color: #166534; }
    .badge-duree { background: #fef3c7; color: #92400e; }
    
    /* Placeholder image */
    .image-placeholder {
        background: linear-gradient(135deg, var(--cream), var(--secondary-color));
        border-radius: 15px;
        padding: 3rem;
        text-align: center;
        font-size: 4rem;
        color: var(--primary-color);
        min-height: 200px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Section filtres */
    .filter-section {
        background: var(--cream);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid var(--secondary-color);
    }
    
    .filter-title {
        font-family: 'Playfair Display', serif;
        color: var(--primary-color);
        font-size: 1.8rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Statistiques */
    .stat-card {
        background: var(--bg-card);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        box-shadow: var(--shadow);
        border: 2px solid var(--secondary-color);
        margin: 1rem 0;
    }
    
    .stat-number {
        font-size: 3.5rem;
        font-weight: 700;
        color: var(--primary-color);
        margin-bottom: 0.5rem;
        font-family: 'Playfair Display', serif;
    }
    
    .stat-label {
        font-size: 1.2rem;
        color: var(--text-secondary);
        font-weight: 500;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Formulaires */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {
        border: 2px solid var(--secondary-color);
        border-radius: 10px;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.2s ease;
        background: var(--warm-white);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(139, 115, 85, 0.1);
    }
    
    /* Boutons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-family: 'Montserrat', sans-serif;
        transition: all 0.2s ease;
        box-shadow: var(--shadow);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 3rem;
        background: var(--cream);
        border-radius: 15px;
        border: 1px solid var(--secondary-color);
        color: var(--text-secondary);
    }
    
    /* Animations */
    .fade-in {
        animation: fadeIn 0.6s ease-in-out;
    }
    
    .fade-in-delay {
        animation: fadeIn 0.8s ease-in-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Login container */
    .login-container {
        background: var(--cream);
        border-radius: 20px;
        padding: 2rem;
        border: 2px solid var(--secondary-color);
        box-shadow: var(--shadow-lg);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main-title { font-size: 3rem; }
        .recipe-card { margin: 1rem 0; }
        .recipe-card-body { padding: 1rem; }
    }
    </style>
    """, unsafe_allow_html=True)

# Fonctions utilitaires avec gestion d'erreurs améliorée
def hash_password(password):
    """Hash un mot de passe"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_recipes():
    """Charge les recettes depuis le fichier JSON avec gestion d'erreurs"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        return []
    except Exception as e:
        st.error(f"Erreur lors du chargement des recettes: {e}")
        return []

def save_recipes(recipes):
    """Sauvegarde les recettes dans le fichier JSON avec gestion d'erreurs"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(recipes, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"Erreur lors de la sauvegarde: {e}")
        return False

def save_image(uploaded_file):
    """Sauvegarde une image uploadée avec gestion d'erreurs"""
    if uploaded_file is not None:
        try:
            # Créer un nom unique pour l'image
            file_extension = uploaded_file.name.split('.')[-1]
            unique_filename = f"{uuid.uuid4()}.{file_extension}"
            file_path = os.path.join(IMAGES_DIR, unique_filename)
            
            # Vérifier que le dossier existe
            os.makedirs(IMAGES_DIR, exist_ok=True)
            
            # Sauvegarder l'image
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            return unique_filename
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde de l'image: {e}")
            return "default.jpg"
    return "default.jpg"

def is_admin(email):
    """Vérifie si l'utilisateur est admin"""
    return email == ADMIN_EMAIL

def authenticate_user():
    """Gère l'authentification des utilisateurs"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.is_admin = False

    if not st.session_state.authenticated:
        # Charger le CSS
        load_css()
        
        # Header artisanal avec ambiance chaleureuse
        st.markdown("""
        <div class="page-header fade-in">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🍯🍊🌿</div>
            <h1 class="main-title">VinPedia</h1>
            <p class="subtitle">Votre collection privée d'alcools artisanaux</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Formulaire de connexion dans un container artisanal
        with st.container():
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                st.markdown("""
                <div class="login-container fade-in-delay">
                    <div style="text-align: center;">
                        <h3 style="color: var(--primary-color); font-family: 'Playfair Display', serif; margin-bottom: 1.5rem;">
                            🔐 Espace Privé
                        </h3>
                        <p style="color: var(--text-light); font-size: 1.125rem;">
                            Accédez à votre collection personnelle de recettes artisanales
                        </p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                with st.form("login_form"):
                    email = st.text_input("📧 Adresse email", placeholder="votre@email.com")
                    password = st.text_input("🔒 Mot de passe", type="password", placeholder="••••••••")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
                    with col_btn2:
                        submit = st.form_submit_button("🌟 Entrer")
                    
                    if submit:
                        # Vérification admin
                        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                            st.session_state.authenticated = True
                            st.session_state.user_email = email
                            st.session_state.is_admin = True
                            st.success("🎉 Bienvenue, Maître Distillateur!")
                            st.rerun()
                        # Vérification utilisateur normal
                        elif email in ALLOWED_EMAILS and password == MAP_PASSWORD_EMAIL.get(email):
                            st.session_state.authenticated = True
                            st.session_state.user_email = email
                            st.session_state.is_admin = False
                            st.success("🎉 Bienvenue dans votre collection!")
                            st.rerun()
                        else:
                            st.error("❌ Identifiants incorrects")
        
        # Footer de la page de connexion
        st.markdown("""
        <div class="footer fade-in">
            <p>🏠 Site privé - Usage personnel uniquement</p>
            <p style="font-size: 0.8rem; margin-top: 0.5rem; color: var(--text-light);">
                Créé avec amour pour partager nos créations artisanales
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        return False

    return True

def display_recipe_card(recipe):
    """Affiche une carte de recette style Pinterest"""
    # Définir l'icône et badge selon le type d'alcool
    icons = {
        "Vin": "🍷",
        "Bière": "🍺", 
        "Liqueur": "🥃",
        "Rhum arrangé": "🏝️",
        "Vodka aromatisée": "🧊",
        "Cidre": "🍎",
        "Autre": "🍸"
    }
    
    badge_classes = {
        "Vin": "badge-vin",
        "Bière": "badge-biere",
        "Liqueur": "badge-liqueur",
        "Rhum arrangé": "badge-rhum",
        "Vodka aromatisée": "badge-vodka",
        "Cidre": "badge-biere",
        "Autre": "badge-autre"
    }
    
    icon = icons.get(recipe['type_alcool'], "🍸")
    badge_class = badge_classes.get(recipe['type_alcool'], "badge-autre")
    
    # Card avec style Pinterest/Notion
    st.markdown(f"""
    <div class="recipe-card fade-in">
        <div class="recipe-card-header">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 2.5rem; margin-right: 1rem;">{icon}</span>
                    <div>
                        <h3 style="color: white; margin: 0; font-family: 'Playfair Display', serif; font-size: 2rem;">
                            {recipe['titre']}
                        </h3>
                        <span class="badge {badge_class}" style="margin-top: 0.5rem;">{recipe['type_alcool']}</span>
                    </div>
                </div>
                <div style="text-align: right;">
                    <span class="badge badge-prix">💰 {recipe['prix_estime']}€</span><br>
                    <span class="badge badge-duree">⏰ {recipe['duree_maceration']}j</span>
                </div>
            </div>
        </div>
        <div class="recipe-card-body">
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            image_path = os.path.join(IMAGES_DIR, recipe['image'])
            if os.path.exists(image_path):
                st.image(image_path, use_container_width=True)
            else:
                st.markdown(f"""
                <div class="image-placeholder">
                    {icon}
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="margin-bottom: 1rem;">
                <h4 style="color: var(--primary-color); font-family: 'Montserrat', sans-serif; margin-bottom: 0.5rem;">
                    📝 Description
                </h4>
                <p style="color: var(--text-secondary); line-height: 1.6; font-size: 1.1rem;">
                    {recipe['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            if 'ingredients' in recipe and recipe['ingredients']:
                st.markdown(f"""
                <div style="margin-bottom: 1rem;">
                    <h4 style="color: var(--primary-color); font-family: 'Montserrat', sans-serif; margin-bottom: 0.5rem;">
                        🧪 Ingrédients
                    </h4>
                    <p style="color: var(--text-secondary); line-height: 1.6; font-size: 1rem;">
                        {recipe['ingredients']}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            if 'methode' in recipe and recipe['methode']:
                with st.expander("📋 Méthode de préparation", expanded=False):
                    st.markdown(f"""
                    <p style="color: var(--text-secondary); line-height: 1.6; font-size: 1rem;">
                        {recipe['methode']}
                    </p>
                    """, unsafe_allow_html=True)
            
            # Informations meta avec style artisanal
            st.markdown(f"""
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--secondary-color);">
                <div style="display: flex; justify-content: space-between; font-size: 0.9rem; color: var(--text-light);">
                    <span>📅 {recipe['date_creation']}</span>
                    {"<span>👤 " + recipe['auteur'] + "</span>" if 'auteur' in recipe else ""}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div></div><br>", unsafe_allow_html=True)

def admin_page():
    """Page d'administration avec style artisanal"""
    load_css()
    
    st.markdown("""
    <div class="page-header fade-in">
        <div style="font-size: 4rem; margin-bottom: 1rem;">👑🔧✨</div>
        <h1 class="main-title">Atelier du Maître</h1>
        <p class="subtitle">Validation et curation des créations artisanales</p>
    </div>
    """, unsafe_allow_html=True)
    
    recipes = load_recipes()
    pending_recipes = [r for r in recipes if not r['valide']]
    
    if not pending_recipes:
        st.markdown("""
        <div class="recipe-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🎉</div>
            <h3 style="color: var(--primary-color); font-family: 'Playfair Display', serif;">
                Atelier à jour !
            </h3>
            <p style="color: var(--text-secondary); margin-top: 1rem;">
                Toutes les créations ont été validées avec soin
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    st.markdown(f"""
    <div class="stat-card fade-in-delay">
        <div class="stat-number">{len(pending_recipes)}</div>
        <div class="stat-label">
            {"Création en attente" if len(pending_recipes) == 1 else "Créations en attente"}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    for i, recipe in enumerate(pending_recipes):
        with st.expander(f"📋 {recipe['titre']} - {recipe['type_alcool']}", expanded=False):
            display_recipe_card(recipe)
            
            st.markdown("""
            <div style="margin-top: 2rem; padding: 1.5rem; background: var(--cream); border-radius: 15px;">
                <h4 style="color: var(--primary-color); font-family: 'Playfair Display', serif; margin-bottom: 1rem;">
                    🎯 Actions du Maître
                </h4>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button(f"✅ Valider", key=f"validate_{i}", 
                           help="Approuver cette création artisanale"):
                    # Trouver la recette dans la liste complète et la valider
                    for r in recipes:
                        if r['id'] == recipe['id']:
                            r['valide'] = True
                            r['date_validation'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                            break
                    save_recipes(recipes)
                    st.success(f"🎉 '{recipe['titre']}' ajoutée à la collection!")
                    st.balloons()
                    st.rerun()
            
            with col2:
                if st.button(f"❌ Refuser", key=f"reject_{i}", 
                           help="Retirer cette création",
                           type="secondary"):
                    # Supprimer la recette
                    recipes = [r for r in recipes if r['id'] != recipe['id']]
                    save_recipes(recipes)
                    st.success(f"🗑️ '{recipe['titre']}' retirée de l'atelier")
                    st.rerun()
            
            with col3:
                st.info("💡 Vérifiez la cohérence des ingrédients et la clarté de la méthode")
            
            st.markdown("</div>", unsafe_allow_html=True)

def gallery_page():
    """Page galerie avec style artisanal Pinterest"""
    load_css()
    
    st.markdown("""
    <div class="page-header fade-in">
        <div style="font-size: 4rem; margin-bottom: 1rem;">🍯🍊🌿</div>
        <h1 class="main-title">Collection Artisanale</h1>
        <p class="subtitle">Découvrez nos créations uniques et savoureuses</p>
    </div>
    """, unsafe_allow_html=True)
    
    recipes = load_recipes()
    validated_recipes = [r for r in recipes if r['valide']]
    
    if not validated_recipes:
        st.markdown("""
        <div class="recipe-card" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">🔍</div>
            <h3 style="color: var(--primary-color); font-family: 'Playfair Display', serif;">
                Aucune recette dans la collection
            </h3>
            <p style="color: var(--text-secondary); margin-top: 1rem;">
                Soyez le premier à partager une délicieuse création artisanale !
            </p>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Section filtres avec style naturel
    st.markdown("""
    <div class="filter-section fade-in-delay">
        <h3 class="filter-title">🎛️ Filtrer la collection</h3>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        types_alcool = list(set([r['type_alcool'] for r in validated_recipes]))
        selected_type = st.selectbox("🏷️ Type d'alcool", ["Tous les types"] + types_alcool)
    
    with col2:
        prix_max = st.slider("💰 Budget maximum", 0, 100, 100, 
                           help="Filtrer par prix maximum en euros")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Filtrage
    filtered_recipes = validated_recipes
    if selected_type != "Tous les types":
        filtered_recipes = [r for r in filtered_recipes if r['type_alcool'] == selected_type]
    filtered_recipes = [r for r in filtered_recipes if r['prix_estime'] <= prix_max]
    
    # Résultats avec compteur artisanal
    if len(filtered_recipes) > 0:
        st.markdown(f"""
        <div class="stat-card fade-in" style="margin: 2rem auto; max-width: 300px;">
            <div class="stat-number">{len(filtered_recipes)}</div>
            <div class="stat-label">
                {"Recette trouvée" if len(filtered_recipes) == 1 else "Recettes trouvées"}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Affichage des recettes en grille
        for recipe in filtered_recipes:
            display_recipe_card(recipe)
    else:
        st.markdown("""
        <div class="recipe-card" style="text-align: center; padding: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🤷‍♂️</div>
            <h3 style="color: var(--primary-color);">Aucun résultat</h3>
            <p style="color: var(--text-secondary);">Essayez de modifier vos filtres</p>
        </div>
        """, unsafe_allow_html=True)

def submit_recipe_page():
    """Page de soumission avec design artisanal"""
    load_css()
    
    st.markdown("""
    <div class="page-header fade-in">
        <div style="font-size: 4rem; margin-bottom: 1rem;">✨🍯📝</div>
        <h1 class="main-title">Partager une Création</h1>
        <p class="subtitle">Ajoutez votre recette artisanale à la collection</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("recipe_form"):
        st.markdown("""
        <div class="recipe-card fade-in-delay">
            <div class="recipe-card-header">
                <h3 style="color: white; text-align: center; font-family: 'Playfair Display', serif;">
                    🌟 Nouvelle Recette Artisanale
                </h3>
                <p style="text-align: center; color: rgba(255,255,255,0.8); margin-top: 0.5rem;">
                    Partagez votre savoir-faire avec la communauté
                </p>
            </div>
            <div class="recipe-card-body">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <h4 style="color: var(--primary-color); font-family: 'Montserrat', sans-serif; margin-bottom: 1rem;">
                📋 Informations Essentielles
            </h4>
            """, unsafe_allow_html=True)
            
            titre = st.text_input("🏷️ Nom de votre création *", 
                                placeholder="Ex: Limoncello de grand-mère")
            
            type_alcool = st.selectbox("🍸 Type d'alcool artisanal *", 
                                     ["Vin", "Bière", "Liqueur", "Rhum arrangé", "Vodka aromatisée", "Cidre", "Autre"],
                                     help="Choisissez la catégorie qui correspond le mieux")
            
            col_prix, col_duree = st.columns(2)
            with col_prix:
                prix_estime = st.number_input("💰 Coût estimé (€) *", 
                                            min_value=0.0, max_value=1000.0, 
                                            value=15.0, step=0.5,
                                            help="Coût approximatif des ingrédients")
            with col_duree:
                duree_maceration = st.number_input("⏰ Temps de macération (jours) *", 
                                                 min_value=1, max_value=365, 
                                                 value=30,
                                                 help="Durée nécessaire pour la préparation")
        
        with col2:
            st.markdown("""
            <h4 style="color: var(--primary-color); font-family: 'Montserrat', sans-serif; margin-bottom: 1rem;">
                📸 Présentation Visuelle
            </h4>
            """, unsafe_allow_html=True)
            
            image = st.file_uploader("📷 Photo de votre création", 
                                   type=['jpg', 'jpeg', 'png'],
                                   help="Formats acceptés: JPG, JPEG, PNG (max 5MB)")
            
            description = st.text_area("📝 Description de votre recette *", 
                                     height=120, 
                                     placeholder="Décrivez le goût, l'arôme, l'occasion parfaite pour la déguster...")
        
        st.markdown("""
        <h4 style="color: var(--primary-color); font-family: 'Montserrat', sans-serif; margin: 2rem 0 1rem 0;">
            🧪 Détails de Préparation
        </h4>
        """, unsafe_allow_html=True)
        
        ingredients = st.text_area("🧪 Liste des ingrédients", 
                                 height=100, 
                                 placeholder="Ex: 1L d'alcool blanc à 40°, 6 citrons bio, 400g de sucre de canne...")
        
        methode = st.text_area("📋 Méthode de préparation", 
                             height=150, 
                             placeholder="Décrivez étape par étape votre méthode artisanale...")
        
        st.markdown("</div></div>", unsafe_allow_html=True)
        
        # Bouton de soumission artisanal
        st.markdown("<br>", unsafe_allow_html=True)
        col_submit1, col_submit2, col_submit3 = st.columns([1, 1, 1])
        with col_submit2:
            submit_button = st.form_submit_button("🌟 Partager ma création")
        
        if submit_button:
            if not titre or not description:
                st.error("❌ Veuillez remplir tous les champs obligatoires (*)")
            else:
                # Sauvegarder l'image
                image_filename = "default.jpg"
                if image is not None:
                    image_filename = save_image(image)
                    if image_filename:
                        st.success("📷 Photo sauvegardée avec succès!")
                
                # Créer la nouvelle recette
                new_recipe = {
                    "id": str(uuid.uuid4()),
                    "titre": titre,
                    "type_alcool": type_alcool,
                    "prix_estime": prix_estime,
                    "duree_maceration": duree_maceration,
                    "image": image_filename,
                    "description": description,
                    "ingredients": ingredients,
                    "methode": methode,
                    "valide": False,
                    "date_creation": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "auteur": st.session_state.user_email
                }
                
                # Sauvegarder
                recipes = load_recipes()
                recipes.append(new_recipe)
                save_recipes(recipes)
                
                st.success("🎉 Votre création a été soumise avec succès!")
                st.balloons()
                
                # Afficher un résumé artisanal
                st.markdown(f"""
                <div class="recipe-card" style="margin-top: 2rem;">
                    <div class="recipe-card-header">
                        <h3 style="color: white; font-family: 'Playfair Display', serif;">
                            📋 Résumé de votre soumission
                        </h3>
                    </div>
                    <div class="recipe-card-body">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <p><strong>Création:</strong> {titre}</p>
                                <p><strong>Type:</strong> {type_alcool}</p>
                                <p><strong>Budget:</strong> {prix_estime}€</p>
                            </div>
                            <div style="font-size: 3rem;">✨</div>
                        </div>
                        <div style="margin-top: 1rem; padding: 1rem; background: var(--cream); border-radius: 10px;">
                            <p style="margin: 0; color: var(--text-secondary); font-size: 1rem;">
                                🔄 Votre recette sera visible après validation par notre Maître Distillateur
                            </p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def main():
    """Fonction principale avec interface artisanale complète"""
    # Vérifier l'authentification
    if not authenticate_user():
        return
    
    # Charger CSS pour les pages authentifiées
    load_css()
    
    # Sidebar avec style artisanal chaleureux
    st.sidebar.markdown("""
    <div style="padding: 1rem; text-align: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">🍯</div>
        <h2 style="color: #FFFFFF; font-family: 'Playfair Display', serif; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.7);">
            VinPedia
        </h2>
        <p style="color: #F0F0F0; font-size: 1rem; margin: 0.5rem 0; text-shadow: 1px 1px 2px rgba(0,0,0,0.6);">
            Collection Artisanale
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Profil utilisateur dans la sidebar
    user_icon = "👑" if st.session_state.is_admin else "👤"
    user_title = "Maître Distillateur" if st.session_state.is_admin else "Collectionneur"
    
    st.sidebar.markdown(f"""
    <div class="stat-card" style="background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.3); backdrop-filter: blur(10px);">
        <div style="text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{user_icon}</div>
            <div style="color: #FFFFFF; font-weight: 600; font-size: 1rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.8);">
                {st.session_state.user_email}
            </div>
            <div style="color: #E0E0E0; font-size: 1rem; margin-top: 0.3rem; text-shadow: 1px 1px 2px rgba(0,0,0,0.7);">
                {user_title}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Menu de navigation artisanal
    st.sidebar.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h4 style="color: var(--warm-white); font-family: 'Montserrat', sans-serif; margin-bottom: 1rem;">
            🧭 Navigation
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.is_admin:
        pages = ["🍯 Collection", "✨ Nouvelle Création", "👑 Atelier du Maître"]
    else:
        pages = ["🍯 Collection", "✨ Nouvelle Création"]
    
    page = st.sidebar.selectbox("Choisir une page", pages, label_visibility="collapsed")
    
    # Statistiques artisanales dans la sidebar
    recipes = load_recipes()
    validated_count = len([r for r in recipes if r['valide']])
    pending_count = len([r for r in recipes if not r['valide']])
    
    st.sidebar.markdown("""
    <div style="margin: 2rem 0 1rem 0;">
        <h4 style="color: var(--warm-white); font-family: 'Montserrat', sans-serif; margin-bottom: 1rem;">
            📊 Collection
        </h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Carte statistiques validées
    st.sidebar.markdown(f"""
    <div class="stat-card" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.3);">
        <div class="stat-number" style="color: var(--warm-white);">{validated_count}</div>
        <div class="stat-label" style="color: rgba(255,255,255,0.8);">
            {"Création validée" if validated_count <= 1 else "Créations validées"}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carte statistiques en attente (admin seulement)
    if st.session_state.is_admin:
        st.sidebar.markdown(f"""
        <div class="stat-card" style="background: rgba(255,255,255,0.1); border-color: rgba(255,255,255,0.3);">
            <div class="stat-number" style="color: var(--warm-white);">{pending_count}</div>
            <div class="stat-label" style="color: rgba(255,255,255,0.8);">
                {"En attente" if pending_count <= 1 else "En attente"}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Bouton de déconnexion artisanal
    st.sidebar.markdown("<br>", unsafe_allow_html=True)
    if st.sidebar.button("🚪 Quitter l'atelier", help="Se déconnecter de VinPedia"):
        st.session_state.authenticated = False
        st.session_state.user_email = None
        st.session_state.is_admin = False
        st.rerun()
    
    # Affichage des pages selon le choix
    if page == "🍯 Collection":
        gallery_page()
    elif page == "✨ Nouvelle Création":
        submit_recipe_page()
    elif page == "👑 Atelier du Maître" and st.session_state.is_admin:
        admin_page()
    
    # Footer artisanal
    st.markdown("""
    <div class="footer fade-in">
        <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🏠✨🍯</div>
        <p>Site privé - Usage personnel uniquement</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; color: var(--text-light);">
            Créé avec amour pour partager nos créations artisanales
        </p>
        <div style="margin-top: 1rem; font-size: 1rem; color: var(--primary-color);">
            VinPedia - Développé avec ❤️ et Streamlit
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()