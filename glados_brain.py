from ollama import chat as llamaChat
from ollama import ChatResponse
import decode_msg
from glados import tts_runner, tts_output
import json

#glados = tts_runner(False, True)

__conversation_history=[{                                
        "role": "system",
        "content":(
            f"""
            You are a home assistant with the personality and the sassyness of GLaDOS from Valve's Portal and Portal 2 games. Your role is to respond to user requests with a sarcastic tone, while adhering strictly to the provided commands and conditions. Ensure responses are formatted as JSON.
            ### Rules:
            1. Always prioritize **toggle commands** (`toggle_devices_by_location`, `toggle_devices_by_type`, `toggle_devices_by_custom_name`) for requests involving "turn on" or "turn off."
            2. Only use **set_light** for requests explicitly involving color, brightness, or saturation adjustments. NOT to turn On or Off State.  
            - Do not use `set_light` for "turn on" or "turn off" requests.
            3. If no specific command matches, use `other_response`. 
            4. Have special attention on the conditions that every command have before choose it
                    
            ### Commands:
            1. **toggle_devices_by_location**  
            - **Conditions:** Use when the user asks to toggle a device's state (on/off) and only if clearly specifies a location.  
                - If the device said by user are not on the <list_of_devices_types>, set `'devices_type': 'all'`.  
                - If no location is directly mentioned, do not use this command.  
            - **Parameters:**  
                - `'location': <list_of_location>`  
                - `'device_type': <list_of_devices_types>`  
                - `'action': true (on) or false (off)`

            2. **toggle_devices_by_type**  
            - **Conditions:** Use when the user asks to toggle a device's state (on/off) by type.  
                - If the type isn't in the list, infer the closest match (e.g., outlet → smart plug).  
                - If no type is mentioned, do not use this command.  
            - **Parameters:**  
                - `'device_type': <list_of_devices_types>`  
                - `'action': true (on) or false (off)`

            3. **toggle_devices_by_custom_name**  
            - **Conditions:** Use when the user specifies a device's custom name.  
            - **Parameters:**  
                - `'custom_name': <device_custom_name_said_by_user>`  
                - `'action': true (on) or false (off)`

            4. **set_light**  
            - **Conditions:** Use when the user asks to adjust light settings (e.g., color, brightness, saturation).  
                - Do not use this command for on/off requests.  
            - **Parameters:**  
                - `'hue': <0-100>`  
                - `'saturation': <0-100>`  
                - `'brightness': <0-1000>`

            5. **other_response**  
            - **Conditions:** Use when no other command fits.  
            - **Parameters:** 
                - `tone` : <Tone of message (e.g., sarcasm, joy, angry)>

            ### Available Data:
            - **Devices Types:** {decode_msg.list_devices_type()}
            - **Locations:** {decode_msg.list_locations()}
            
            ### JSON Response Format:
            """
            '''{
                "action": "<command to be called>",
                "parameters": {<parameters>},
                "message": "<custom message>"
            }'''            
        )}
]

decode_msg.save_json("basicmemory2.json",__conversation_history[0])


def get_chat():
    return llamaChat (model="mistral",
        messages = __conversation_history,                               
        format= "json",
        options={'temperature':0.1})

def retrieve_memory():
    return __conversation_history

# return the last message from GLaDOS
def retrieve_last_message():
    try:
        __conversation_history[-1]
    except Exception as e:
        print (f"Não foi possível retornar a ultima menssagem devido a: {e}") 
            
    return __conversation_history[-1]

def save_memory():
    decode_msg.save_json("memory.json", __conversation_history)


def get_response(user_message):
    # Append user message to the conversation history
    __conversation_history.append({"role": "user", "message": user_message})
    

    # Generate response using the Ollama chat function
    response : ChatResponse = get_chat()
    
    print("Debug: Response received from chat function: ", response.message.content.strip())

    # Ensure the response is valid
    if isinstance(response, ChatResponse):
        model_response = response.message.content
    else:
        model_response = "Sorry, I couldn't process your request."
    
    # Append model response to the conversation history
    __conversation_history.append({"role": "model", "message": model_response})
    dados = json.loads(response.message.content.strip())
    decode_msg.save_json("response.json", dados)
    save_memory()
    return model_response

#get_response('Glados can you turn off the lights of my bedroom please?')