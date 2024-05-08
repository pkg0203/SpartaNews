from openai import OpenAI
from django.conf import settings


def news_link_ai(url):
    client = OpenAI(api_key=settings.OPENAI_API_KEY)

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
                "content": url,
            },
        ],
    )

    return completion.choices[0].message.content
