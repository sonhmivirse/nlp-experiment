from transformers import pipeline, Conversation

translate_pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-vi-en")
vi_pipe = pipeline("translation", model="VietAI/envit5-translation")


conversation_pipe = pipeline("conversational", model="facebook/blenderbot-400M-distill")

def bot_answer(question):
    en_text = translate_pipe(question)
    en_text = en_text[0]['translation_text'][4:]
    conversation = Conversation(en_text)
    response = conversation_pipe(conversation)
    
    en_response = response.generated_responses[-1]
    vi_response = vi_pipe(en_response, max_length=1000)[0]['translation_text'][4:]
    
    return vi_response