import os
import requests
from datetime import datetime
from supabase import create_client, Client
from typing import Dict, List
import time
from dotenv import load_dotenv
MAX_GAMES = 2

load_dotenv('.env')
# Configurações
RAWG_API_KEY = os.getenv("RAWG_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL") 
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Inicialização do cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_games_from_api(page: int = 1, page_size: int = 20) -> Dict:
    """Obtém jogos da API RAWG"""
    url = f"https://api.rawg.io/api/games"
    params = {
        "key": RAWG_API_KEY,
        "page": page,
        "page_size": page_size
    }
    response = requests.get(url, params=params)
    return response.json()

def get_game_details(game_id: int) -> Dict:
    """Obtém detalhes específicos de um jogo, incluindo developers e publishers"""
    url = f"https://api.rawg.io/api/games/{game_id}"
    params = {
        "key": RAWG_API_KEY
    }
    response = requests.get(url, params=params)
    return response.json()

def insert_genre(genre: Dict) -> int:
    """Insere um gênero e retorna seu ID"""
    try:
        result = supabase.table('genre').select("genre_id").eq('slug', genre['slug']).execute()
        if result.data:
            return result.data[0]['genre_id']
        
        data = {
            'name': genre['name'],
            'slug': genre['slug']
        }
        result = supabase.table('genre').insert(data).execute()
        return result.data[0]['genre_id']
    except Exception as e:
        print(f"Erro ao inserir gênero: {e}")
        return None

def insert_platform(platform: Dict) -> int:
    """Insere uma plataforma e retorna seu ID"""
    try:
        result = supabase.table('platform').select("platform_id").eq('slug', platform['platform']['slug']).execute()
        if result.data:
            return result.data[0]['platform_id']
        
        data = {
            'name': platform['platform']['name'],
            'slug': platform['platform']['slug']
        }
        result = supabase.table('platform').insert(data).execute()
        return result.data[0]['platform_id']
    except Exception as e:
        print(f"Erro ao inserir plataforma: {e}")
        return None

def insert_developer(developer: Dict) -> int:
    """Insere um desenvolvedor e retorna seu ID"""
    try:
        result = supabase.table('developer').select("developer_id").eq('slug', developer['slug']).execute()
        if result.data:
            return result.data[0]['developer_id']
        
        data = {
            'name': developer['name'],
            'slug': developer['slug']
        }
        result = supabase.table('developer').insert(data).execute()
        return result.data[0]['developer_id']
    except Exception as e:
        print(f"Erro ao inserir desenvolvedor: {e}")
        return None

def insert_publisher(publisher: Dict) -> int:
    """Insere uma publicadora e retorna seu ID"""
    try:
        result = supabase.table('publisher').select("publisher_id").eq('slug', publisher['slug']).execute()
        if result.data:
            return result.data[0]['publisher_id']
        
        data = {
            'name': publisher['name'],
            'slug': publisher['slug']
        }
        result = supabase.table('publisher').insert(data).execute()
        return result.data[0]['publisher_id']
    except Exception as e:
        print(f"Erro ao inserir publicadora: {e}")
        return None

def insert_game(game: Dict) -> int:
    """Insere um jogo e seus relacionamentos"""
    try:
        # Inserir jogo
        game_data = {
            'name': game['name'],
            'release_date': game.get('released'),
            'rating': game.get('rating'),
            'description': game.get('description', ''),
            'background_image': game.get('background_image'),
            'website': game.get('website')
        }
        
        result = supabase.table('game').insert(game_data).execute()
        game_id = result.data[0]['game_id']

        # Obter detalhes adicionais do jogo
        game_details = get_game_details(game['id'])

        # Inserir relacionamentos com gêneros
        for genre in game.get('genres', []):
            genre_id = insert_genre(genre)
            if genre_id:
                supabase.table('game_genre').insert({
                    'game_id': game_id,
                    'genre_id': genre_id
                }).execute()

        # Inserir relacionamentos com plataformas
        for platform in game.get('platforms', []):
            platform_id = insert_platform(platform)
            if platform_id:
                supabase.table('game_platform').insert({
                    'game_id': game_id,
                    'platform_id': platform_id
                }).execute()

        # Inserir relacionamentos com desenvolvedores
        for developer in game_details.get('developers', []):
            developer_id = insert_developer(developer)
            if developer_id:
                supabase.table('game_developer').insert({
                    'game_id': game_id,
                    'developer_id': developer_id
                }).execute()

        # Inserir relacionamentos com publicadoras
        for publisher in game_details.get('publishers', []):
            publisher_id = insert_publisher(publisher)
            if publisher_id:
                supabase.table('game_publisher').insert({
                    'game_id': game_id,
                    'publisher_id': publisher_id
                }).execute()


        return game_id
    except Exception as e:
        print(f"Erro ao inserir jogo: {e}")
        return None

def main():
    """Função principal para executar o ETL"""
    page = 1
    total_games = 0
    max_games = MAX_GAMES  # Limite de jogos a serem coletados

    while total_games < max_games:
        print(f"Coletando página {page}...")
        games_data = get_games_from_api(page)
        
        if not games_data.get('results'):
            break

        for game in games_data['results']:
            if total_games >= max_games:
                break
                
            game_id = insert_game(game)
            if game_id:
                total_games += 1
                print(f"Jogo inserido com sucesso: {game['name']}")
            
            # Respeitar rate limits
            time.sleep(1)  
        
        page += 1

    print(f"povoamento concluído. Total de jogos inseridos: {total_games}")

if __name__ == "__main__":
    main()