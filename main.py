import time
from services.instagram_service import InstagramService

def main():
    start_time = time.time()
    service = InstagramService()
    
    try:
        service.login()
        user_id = '1234302260'
        followers = service.get_followers(user_id)
        if followers is not None:
            print(f"Total de seguidores: {len(followers)}")
            # print("Seguidores:")
            # print(followers)
        
        following = service.get_following(user_id)
        if following is not None:
            print(f"Total de quem você segue: {len(following)}")
            # print("Quem você segue:")
            # print(following)
        
        service.screenshot()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
    finally:
        service.close()
    
    end_time = time.time()
    execution_time = end_time - start_time
    print("___________________")
    print(f"Tempo de execução: {execution_time:.2f} segundos")

if __name__ == "__main__":
    main()
