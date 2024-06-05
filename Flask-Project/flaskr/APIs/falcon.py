from gpt4all import GPT4All

# Correctly initialize the GPT4All object with a properly formatted path
llm = GPT4All("gpt4all-falcon-newbpe-q4_0.gguf")

# Use the correct method for generating responses
query = "explain photosynthesis but structure the answer as follows, i need 3 Pages in the same format: (TITLE | first talkingpoint | second talkingpoint | third talkingpoint | text) so pls use the | as separatores. the 3 pages are separated by a || . pls respond with just this format and its contents, nothing else! not even newlines"
query = "give me 3 very short bullet points to put in a powerpoint about: photosynthesis. Answer just with them nothing else, and separate them with ;"
with llm.chat_session():
    response = llm.generate(query,max_tokens=100,)
# print(response)
with open("output.txt", "w") as file:
    file.write(response)
