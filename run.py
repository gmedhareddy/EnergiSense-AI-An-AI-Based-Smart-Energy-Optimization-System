from pyngrok import ngrok
import os

# Kill old processes
os.system("pkill -f streamlit")
ngrok.kill()

# Add your ngrok token here
ngrok.set_auth_token("3C7hiEubbdftTZibwu3qUhcyLor_7TMdsuYxmJJTh1r5MsgHo")

# Run streamlit
os.system("streamlit run app.py &")

# Create tunnel
public_url = ngrok.connect(8501)

print("🚀 Your App URL:", public_url)