from fastapi import FastAPI
from pydantic import BaseModel
from skills.echo_skill import echo
from nuri_sdk.kernel import NuriKernel

app = FastAPI(title="Nuri Core API")

@app.get("/health")
def health():
    return {"status": "ok"}

class EchoRequest(BaseModel):
    text: str

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/echo")
def echo_endpoint(req: EchoRequest):
    return {"reply": echo(req.text)}

# Kernel initialisieren
kernel = NuriKernel()

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    reply = kernel.ask(req.text)
    return ChatResponse(reply=reply)