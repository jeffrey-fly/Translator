from google import genai

def main():
    client = genai.Client()

    response = client.models.generate_content(
        model="gemini-2.5-flash", contents="Explain how AI works in a few words"
    )
    print(response.text)

if __name__ == '__main__':
    print("hello world")
    main()