from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client=OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
#client

res = client.responses.create(
    model = 'gpt-4o-mini',
    input = [
        {"role" : "system", "content":"너는 금융 전문가야"},
        {"role" : "user", "content":"주식 시장 뉴스 작성"}
    ],
    temperature=0
)

print(res.output_text)