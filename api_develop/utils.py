from transformers import pipeline, Conversation, AutoTokenizer, AutoModelForSeq2SeqLM
from googletrans import Translator

translate_pipe = pipeline("translation", model="Helsinki-NLP/opus-mt-vi-en")
vi_pipe = pipeline("translation", model="VietAI/envit5-translation")


conversation_pipe = pipeline("conversational", model="facebook/blenderbot-400M-distill")




def initBlenderModel():
    model_name = "/media/ivirse/Data1/Project_ISOFH/chatbotdocs/models/blenderbot"
    blenderBotTokenize = AutoTokenizer.from_pretrained(model_name)
    blenderBotModel = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    blenderBotModel.resize_token_embeddings(len(blenderBotTokenize))
    special_token_dict = blenderBotTokenize.special_tokens_map
    blenderBotTokenize.add_special_tokens(special_token_dict)
    
    return blenderBotTokenize, blenderBotModel

blenderBotTokenize, blenderBotModel = initBlenderModel()

def vi_to_en(text):
  translator = Translator()
  translation = translator.translate(text, src='vi', dest='en')
  return translation.text

def en_to_vi(text):
  translator = Translator()
  translation = translator.translate(text, src='en', dest='vi')
  return translation.text

def bot_answer(question):
    en_text = translate_pipe(question)
    en_text = en_text[0]['translation_text'][4:]
    conversation = Conversation(en_text)
    response = conversation_pipe(conversation)
    
    en_response = response.generated_responses[-1]
    vi_response = vi_pipe(en_response, max_length=1000)[0]['translation_text'][4:]
    
    return vi_response

def blender_bot_answer(question):
    device = "cpu"
    en_text = vi_to_en(question)
    tokenized_input = blenderBotTokenize(en_text, return_tensors='pt')
    
    inputs = tokenized_input['input_ids'].to(device)
    tokenized_input = tokenized_input.to(device)
    
    outputs = blenderBotModel.generate(**tokenized_input)
    
    response = en_to_vi(blenderBotTokenize.batch_decode(outputs)[0])
    
    return response