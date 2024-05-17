import aiohttp
from openai import OpenAI
from config import OPEN_AI_API_KEY, OPEN_AI_ASSISTANT_ID, OPEN_AI_ORGANIZATION, OPEN_AI_PROJECT


open_ai_client = OpenAI(api_key=OPEN_AI_API_KEY, organization=OPEN_AI_ORGANIZATION, project=OPEN_AI_PROJECT)


async def send_message(said: int, message: str, phone: str):
    url = "https://api.umnico.com/v1.3/messaging/post"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2NvdW50SWQiOjc2MzkzLCJjcmVhdGlvbkRhdGUiOiIyMDI0LTA1LTE2VDA3OjQ4OjQyLjg5NFoiLCJpYXQiOjE3MTU4NDU3MjJ9.PfKW6kZFFQ9wFuUjUdrL8uqn8he2ypqGZwu3b7FE8Ww"
    }
    data = {
        "message": {
            "text": message
        },
        "destination": phone,
        "saId": said
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data, headers=headers) as response:
            if response.status == 200:
               pass
            else:
                print("Ошибка при отправке сообщения:", response.status, response.text)


async def create_openai_thread(message):
    max_tokens = 500

    thread = open_ai_client.beta.threads.create(
                messages=[
                    {
                        'role': 'user',
                        'content': message
                    }
                ]
            )
    
    run = open_ai_client.beta.threads.runs.create(thread_id=thread.id, assistant_id=OPEN_AI_ASSISTANT_ID, max_completion_tokens=max_tokens)

    while run.status !='completed':
        run = open_ai_client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)


    message_response = open_ai_client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data
    latest_message = messages[0]
    latest_message_text = latest_message.content[0].text.value
    return latest_message_text, thread.id




def parse(url):
    query_params = url.query
    
    utm_term_value = query_params.get('utm_term')
    pixel_value = query_params.get('pixel')
    web_value = query_params.get('web')
    return utm_term_value, pixel_value, web_value



async def send_to_leadvertex(fio, phone, company='https://ma.nurdeo.pw/PMJbyhNS?adset_id={{adset.id}}&utm_campaign={{campaign.name}}&utm_source={{site_source_name}}&utm_placement={{placement}}&campaign_id={{campaign.id}}&utm_creative={{ad.name}}&ad_id={{ad.id}}&adset_name={{adset.name}}&web=14&pixel=адалтдиана9610&sub_id_10=2&sub_id_15=1'):
    async with aiohttp.ClientSession() as session:
        async with session.get(company, ssl=False) as response:
            utm_term, pixel_value, web_value = parse(response.url)

        url = f"https://call-center1.leadvertex.ru/api/webmaster/v2/addOrder.html?webmasterID={web_value}&token=1234"
        orderData = {
            'goods[0][goodID]': 202690,
            'goods[0][price]': 1200,
            'goods[0][quantity]': 1,
            'fio': fio,
            'phone': phone,
            'domain': 'nur.whatsapp.pw',
            'externalWebmaster': pixel_value,
            'utm_term': utm_term,
            'additional13': 'whatsapp-chat-gpt'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        async with session.post(url, data=orderData, headers=headers) as resp:
            if resp.status == 200:
                print('успешно создали заказ возвращаем')
            else:
                print('Не успешно был создан ватсап лид в лидвертексе')




async def openai_thread_send_message(message_text, thread_id):
    max_tokens = 500

    thread_message = open_ai_client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message_text
                )
    
    run = open_ai_client.beta.threads.runs.create(thread_id=thread_id, assistant_id=OPEN_AI_ASSISTANT_ID, max_completion_tokens=max_tokens)

    while run.status !='completed':
        run = open_ai_client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)


    message_response = open_ai_client.beta.threads.messages.list(thread_id=thread_id)
    messages = message_response.data
    latest_message = messages[0]
    latest_message_text = latest_message.content[0].text.value
    
    return latest_message_text


    