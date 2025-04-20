import os
import pandas as pd
import aiohttp
import asyncio
from tqdm.asyncio import tqdm_asyncio
from tqdm import tqdm

# Folder to save images
SAVE_DIR = os.path.join(os.path.dirname(__file__), '../data/baxus_images')
os.makedirs(SAVE_DIR, exist_ok=True)

# Path to the CSV file
CSV_PATH = os.path.join(os.path.dirname(__file__), '../data/baxus_data.csv')

def read_baxus_data():
    df = pd.read_csv(CSV_PATH)
    return dict(zip(df['id'], df['image_url']))

async def download(session, bottle_id, url):
    try:
        save_path = os.path.join(SAVE_DIR, f"{bottle_id}.jpg")

        # Skip if already downloaded
        if os.path.exists(save_path):
            return True

        async with session.get(url) as response:
            if response.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await response.read())
                return True
            else:
                print(f"❌ Failed: {url} (ID: {bottle_id}) - Status: {response.status}")
                return False
    except Exception as e:
        print(f"⚠️ Error downloading {url} having {bottle_id}: {e}")
        return False

async def process():
    id_url_map = read_baxus_data()
    print(f"Found {len(id_url_map)} images to download")
    
    async with aiohttp.ClientSession() as session:
        tasks = [download(session, bottle_id, url) for bottle_id, url in id_url_map.items()]
        
        # Use tqdm_asyncio.gather which handles the progress bar automatically
        results = await tqdm_asyncio.gather(*tasks, desc="Downloading images", unit="file")
        
        success_count = sum(1 for result in results if result)
        print(f"Downloaded {success_count} of {len(tasks)} images successfully!")

if __name__ == "__main__":
    asyncio.run(process())
    print("All images download process completed!")