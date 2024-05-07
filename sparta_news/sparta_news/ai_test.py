from openai import OpenAI
import config

client = OpenAI(api_key=config.OPENAI_API_KEY)

system_instructions = """
너는 기자이고, 주어진 링크의 뉴스를 마크다운 언어를 사용해서 요약해줘. 만약 뉴스가 영어로 되어있다면, 한글로 번역해서 요약해줘.
"""

completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": system_instructions,
        },
        {
            "role": "user",
            "content": "https://edition.cnn.com/2024/05/02/middleeast/palestinian-journalists-gaza-world-press-freedom-day-intl-cmd/index.html",
        },
    ],
)

print(completion.choices[0].message.content)