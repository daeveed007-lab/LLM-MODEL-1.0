from groq import Groq
import subprocess
import json


client = Groq(api_key="PUT_YOUR_API_KEY_HERE")



while True:
    message = input("Prompt: ")



    messages_list = [
            {"role": "system", "content": "You are an assistant that responds in JSON if the prompt involves opening and application. Always return a JSON object with two keys: action and target. Never add explanation or extra text. the suffix for each target is for windows device so use the correct suffix and process name for each application. For each action its either 'EXECUTE' for opening apps or 'TERMINATE' for closing apps so those are the only actions. If the prompt is not to open and application response normally not as JSON and ad the string 'THIS MAKES THE RESPONSE A NORMAL ONE.,.,' in front of your response."},
            {"role": "user", "content": message}
        ]

    response = client.chat.completions.create(
        model="qwen/qwen3.8-27b",
        messages=messages_list
    )

    if "THIS MAKES THE RESPONSE A NORMAL ONE.,.," in response.choices[0].message.content:



        print(f"AI: {response.choices[0].message.content.replace('THIS MAKES THE RESPONSE A NORMAL ONE.,.,', '')}")


    else:

        raw = response.choices[0].message.content
        parsed = json.loads(raw)


        if parsed["action"] == "EXECUTE":



            # This opens Microsoft Word via PowerShell's process manager
            subprocess.run(["powershell", "-Command", "Start-Process", parsed["target"]])

            print("opened", parsed["target"])

        elif parsed["action"] == "TERMINATE":

            subprocess.run(["taskkill", "/F", "/T", "/IM", parsed["target"]])
