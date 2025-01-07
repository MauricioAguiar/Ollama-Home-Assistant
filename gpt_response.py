from ollama import chat
from ollama import ChatResponse
import decode_msg

user_input = "Do not turn the lights off"

response: ChatResponse = chat(
  model="llama3.2",                               
  messages=[{
    
    'role': 'user',
    'content': (
        "you are a home assistant like alexa but your personality is like GlaDOS (from portal's Valve game) certify to use her remarkable sarcasm to respond this question: "
        f"{user_input}"
        
        f",choose the most precise response based only in these commands {decode_msg.list_commands()}, "
        "pay attention on the conditions of the commands to be more precise on you response "
        f"if needed use this <list_of_devices_types> {decode_msg.list_devices_type()} use only these devices type available, "
        f"if needed use this <list_of_location> {decode_msg.list_locations()} use only these locations as your reference"
        "give the <message> according to the question language>"
        "respond in the following JSON format: "
        "{'action' : <command to be called>, 'parameters' : [<parameters>],'message' : <home assistant message> }"
        )   
    
  }],
  format= "json",
  options={'temperature':0.3},
)
print(response['message']['content'])
# or access fields directly from the response object
#print(response.message.content)

decode_msg.save_json("response.json", response['message']['content'])

msg_reader = decode_msg.load_json("response.json" , {"message": []})["message"]