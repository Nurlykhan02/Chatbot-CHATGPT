from fastapi import APIRouter, Request, Depends, HTTPException
from utils.utils import send_message, create_openai_thread, send_to_leadvertex, openai_thread_send_message
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import CustomersTable




class ChatController:
    def __init__(self):
        self.chat = APIRouter()

        self.chat.add_api_route('/webhook_connect', self.webhook_connect, methods=['POST'])
        
    async def webhook_connect(self, request: Request, db: Session = Depends(get_db)):
        try:
            data = await request.json()
            is_new_lead = data.get('isNewLead', False)  
            is_new_customer = data.get('isNewCustomer', False)
            message_type = data.get('type', '')  

            if is_new_lead and is_new_customer and message_type == 'message.incoming':
                message_outer = data.get('message', {})
                message_inner = message_outer.get('message', {})
                message_text = message_inner.get('text','')
                
                sa = message_outer.get('sa',{})
                said = sa.get('id','')

                sender = message_outer.get('sender',{})

                client_name = sender.get('login','')
                client_phone = sender.get('socialId','')
                print(client_name, client_phone)
                latest_message, thread_id = await create_openai_thread(message_text)
                print(latest_message,thread_id)
                await send_message(said=said, message=latest_message, phone=client_phone)
                await send_to_leadvertex(client_name, client_phone)
                print(said, client_phone, thread_id)
                print(type(said), type(client_phone), type(thread_id))
                user_info = CustomersTable(
                    saID=said, 
                    phone=client_phone, 
                    openai_thread=thread_id)
                    
                db.add(user_info)
                db.commit()

            elif message_type == 'message.incoming':
                message_outer = data.get('message', {})
                message_inner = message_outer.get('message', {})
                message_text = message_inner.get('text','')
                print('проходим')
                sa = message_outer.get('sa',{})
                said = sa.get('id','')

                sender = message_outer.get('sender',{})

                client_phone = sender.get('socialId','')
                print(client_phone)
                thread_id = db.query(CustomersTable.openai_thread).filter(CustomersTable.phone == client_phone).scalar()
                print(thread_id)
                if thread_id:
                    latest_message = await openai_thread_send_message(message_text=message_text, thread_id=thread_id)
                    await send_message(said=said, message=latest_message, phone=client_phone)

        except Exception as e:
            
            print(f"Internal Server Error: {e}")
            return ('Success', 200) 
