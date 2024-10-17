import secrets
import json

def generate_random_hex(length=32):
    return secrets.token_hex(length // 2)


class Config:
    VISITORS_ID = generate_random_hex()
    HEADERS = {
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': f'sapphire=1; visitorId={VISITORS_ID}; TealeafAkaSid=wm5597B3Q2oWNenjsjCEogKUmflWQzHH; UserLocation=67357|11.790|76.170|KL|IN; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1OWJlOGE3ZS1jYWZkLTQ0ZmQtYjQ0Zi1lMDk2MjI1MTU2NzkiLCJpc3MiOiJNSTYiLCJleHAiOjE3MjkyMjg2MzEsImlhdCI6MTcyOTE0MjIzMSwianRpIjoiVEdULjNkYTkzYzVhMTQ3NjQ0ZmRhOGQ0MWU4MTIyZTczY2M2LWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6IjE3Y2FiMWVhZWJmZGNkYzRjMjVlZWViYzgzMzU5NjhlZjYyOWU5ZTBkZDRkN2RjMWU5Y2I1MTYzNTNlMjEzYTciLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.lvi9NR324I-XPavIxF_Q-nCE9VhGKtTOHzy7CUzu-EkXo8Oij00YocAb6fc_sa8EPfX2RyyeiHcYmCo8C5c2fpen7j5CSDzD90Rg7w6T8VD1o6EEE8d0CTqVsHxNABasvye2Bc_5gtRAHMje4c0HiWUG1QNzwmJhTluZ7A3c3hx78vfacAOZsz9r-p3ok7P_zBrCL3mopKOGCaciZiD9yWG9TeS0UQdhiymBR-CBFyaSCEhDO8j3CDq2XWZSuLNpKvhzWZNm9sGuZr9Shx05vkdmN4rL5PgpOEfIWhNd80CDWVFm6VpgoVWXdFkZXL-fZwVuLY1IcQQ-y2BHayrl3Q; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiI1OWJlOGE3ZS1jYWZkLTQ0ZmQtYjQ0Zi1lMDk2MjI1MTU2NzkiLCJpc3MiOiJNSTYiLCJleHAiOjE3MjkyMjg2MzEsImlhdCI6MTcyOTE0MjIzMSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlLCJzdCI6IktMIn19.; refreshToken=hKbp5ljaDVUrLc8CmMADh66B0hjIrvl0-SJym96dm_6J6d8mU3iRQPnKHio0TzCLyn0wKzZxdVPp9XMjdElg9g; adScriptData=KL; fiatsCookie=DSI_774|DSN_Joplin|DSZ_64801; __gads=ID=a95b0baf308b8d30:T=1729142235:RT=1729146101:S=ALNI_MZ5ysBye9ytd3TA7vZKYtUNxAeeLw; __gpi=UID=00000f46912ee7ac:T=1729142235:RT=1729146101:S=ALNI_MZpdFZE_9AkgbEAO7G-hT-T3nOEAw; __eoi=ID=140cb04e4cebbb50:T=1729142235:RT=1729146101:S=AA-AfjZZxmyl12wF6U1PvY1eyL_o; ci_pixmgr=other; ffsession={{%22sessionHash%22:%2213aa4cd8d47ef21729142230815%22%2C%22prevPageName%22:%22top%20deals:%20grocery%20deals%22%2C%22prevPageType%22:%22level%202%22%2C%22prevPageUrl%22:%22https://www.target.com/c/grocery-deals/-/N-k4uyq%22%2C%22prevSearchTerm%22:%22non-search%22%2C%22sessionHit%22:10}}; _mitata=OWIwZWJiMGJlYjZhNjAzNDk3ZTcxN2EwY2MzY2Q2YzIwN2U0ZDJhZGIwMGFlOGNlZGViOTFlYTY0YTRhYTI0YQ==_/@#/1729161127_/@#/cHhJjvRxSFQNUqxi_/@#/ZDcyNTkwZTc1N2QyODZlMDdmNTg1ZWY0MzZkZmM2NDQ0OGY3YWJlNWI1ZThlMmY2NDIwNTliYmRjZjNjZDk2Zg==_/@#/530; _mitata=M2UxZjJjODhhZDM0MWMyYTVmYTJhMzQxNDE5NDFmYzUzZDI2MWJlZGU5M2U1Y2U2NmZmZTIzNjVlZjBmMTliZQ==_/@#/1729145763_/@#/cHhJjvRxSFQNUqxi_/@#/MzFlY2Y4ZWUyY2Q3NDk3NGUyM2NmYzE5NDIwNmZhZWJlNWNhNDcxYmViMDk3NWM1ZDhkMDMyMjRkNzIzMWM0Yg==_/@#/000',
        'origin': 'https://www.target.com',
        'priority': 'u=1, i',
        'referer': 'https://www.target.com/c/grocery-deals/-/N-k4uyq',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
        }
    PROXIES = {
        'http': 'http://aimleap:VKOGGUP-VDW11QX-GJHM5VF-DLBJIMH-HJVFAIM-DVOA1GG-MMHC46T@global.rotating.proxyrack.net:9000',
        'https': 'http://aimleap:VKOGGUP-VDW11QX-GJHM5VF-DLBJIMH-HJVFAIM-DVOA1GG-MMHC46T@global.rotating.proxyrack.net:9000'
    }
    ZIPCODE = '60177'
    STORE_NAME = "Chicago Wicker Park"
    STORE_LOCATION = "1664 W Division Street, Chicago, IL 60622-3922"
    STORE_LOGO = "https://assets.targetimg1.com/webui/store-locator/targetlogo-6.jpeg"

    MAIN_CATEGORIES = [
        ("halloween", "5xt2o"),
        ("christmas", "5xt30"),
        ("grocery", "5xt1a"),
        ("clothing-shoes-accessories", "rdihz"),
        ("home", "5xtvd"),
        ("outdoor-living-garden", "5xtq9"),
        ("furniture", "5xtnr"),
        ("kitchen-dining", "hz89j"),
        ("electronics", "5xtg6"),
        ("video-games", "5xtg5"),
        ("toys", "5xtb0"),
        ("sports-outdoors", "5xt85"),
        ("movies-music-books", "5xsxe"),
        ("baby", "5xtly"),
        ("household-essentials", "5xsz1"),
        ("beauty", "55r1x"),
        ("ulta-beauty-at-target", "ueo8r"),
        ("personal-care", "5xtzq"),
        ("health", "5xu1n"),
        ("pets", "5xt44"),
        ("school-office-supplies", "5xsxr"),
        ("arts-crafts-sewing-home", "5xt4g"),
        ("party-supplies", "5xt3c"),
        ("luggage", "5tz1"),
        ("gift-ideas", "96d2i"),
        ("gift-cards", "5xsxu"),
        ("character-shop", "5oux8"),
        ("bullseye-s-playground", "tr36l"),
        ("clearance", "5q0ga")
    ]